package main

import (
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"
	"time"

	"bitbucket.org/zombiezen/stackexchange"
	"labix.org/v2/mgo"
)

// OAuth parameters
const (
	appClientID    = "1144"
	appKey         = "VbR*HN60lyuKdIHm3M)3)Q(("
	oauthDialogURL = "https://stackexchange.com/oauth/dialog"
	redirectURL    = "https://stackexchange.com/oauth/login_success"
)

// Collection names
const (
	QuestionCollection = "questions"
	AnswerCollection   = "answers"
)

// Flags
var (
	Site       = stackexchange.StackOverflow
	OAuthToken = ""
	Tag        = ""
)

// Connections
var (
	Client StackExchangeClient
	Mongo  *mgo.Database
)

func main() {
	flag.StringVar(&Site, "site", Site, "the site name to scrape from")
	flag.StringVar(&OAuthToken, "oauth", OAuthToken, "OAuth 2.0 token")
	flag.StringVar(&Tag, "tag", Tag, "tag to scrape on")
	mongoURL := flag.String("mongo", "localhost/gustafocrawler", "the URL for the MongoDB database")
	flag.Parse()

	if OAuthToken == "" {
		fmt.Fprintln(os.Stderr, "No OAuth 2.0 token given. Please visit:")
		fmt.Fprintln(os.Stderr)
		fmt.Fprintln(os.Stderr, "  "+oauthDialogURL+"?"+url.Values{
			"client_id":    {appClientID},
			"scope":        {"no_expiry"},
			"redirect_uri": {redirectURL},
		}.Encode())
		fmt.Fprintln(os.Stderr)
		fmt.Fprintln(os.Stderr, "And grab the token from the URL when you are finished.")
		os.Exit(1)
	}

	{
		sess, err := mgo.Dial(*mongoURL)
		if err != nil {
			log.Fatalln("mongo connect failed:", err)
		}
		Mongo = sess.DB("")
	}

	{
		rlc := NewRateLimitClient(&stackexchange.Client{
			AccessToken: OAuthToken,
			Key:         appKey,
		})
		defer rlc.Close()
		Client = rlc
	}

	err := fetchBatch()
	if err != nil {
		log.Print(err)
	}
}

func fetchBatch() error {
	questions, err := fetchQuestions(1, Tag)
	if err != nil {
		return err
	}
	for i := range questions {
		q := &questions[i]
		_, err := Mongo.C(QuestionCollection).UpsertId(q.ID, Question{
			ID:               q.ID,
			AcceptedAnswerID: q.AcceptedAnswerID,
			AnswerCount:      q.AnswerCount,
			ClosedDate:       time.Time(q.ClosedDate),
			ClosedReason:     q.ClosedReason,
			Created:          time.Time(q.Created),
			IsAnswered:       q.IsAnswered,
			Link:             q.Link,
			Score:            q.Score,
			Title:            q.Title,
		})
		if err != nil {
			log.Printf("question (id=%d) upsert failed: %v", q.ID, err)
		}
	}

	questionIDs := make([]int, len(questions))
	for i := range questions {
		questionIDs[i] = questions[i].ID
	}
	answers, err := fetchQuestionAnswers(questionIDs)
	log.Println(len(answers), "answers")
	if err != nil {
		return err
	}
	for i := range answers {
		a := &answers[i]
		_, err := Mongo.C(AnswerCollection).UpsertId(a.ID, Answer{
			ID:         a.ID,
			Body:       a.Body,
			Created:    time.Time(a.Created),
			IsAccepted: a.IsAccepted,
			Link:       a.Link,
			QuestionID: a.QuestionID,
			Score:      a.Score,
			Title:      a.Title,
		})
		if err != nil {
			log.Printf("answer (id=%d) upsert failed: %v", a.ID, err)
		}
	}

	_, _ = questions, answers
	return nil
}

func fetchQuestions(n int, tag string) ([]stackexchange.Question, error) {
	var questions []stackexchange.Question
	_, err := Client.Do(stackexchange.PathAllQuestions, &questions, &stackexchange.Params{
		Site:     Site,
		Tagged:   tag,
		PageSize: n,
	})
	return questions, err
}

func fetchQuestionAnswers(ids []int) ([]stackexchange.Answer, error) {
	var answers []stackexchange.Answer
	_, err := Client.Do(stackexchange.PathQuestionAnswers, &answers, &stackexchange.Params{
		Site: Site,
		Args: []string{stackexchange.JoinIDs(ids)},
	})
	return answers, err
}
