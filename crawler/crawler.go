package main

import (
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"
	"os/signal"
	"time"

	"bitbucket.org/zombiezen/stackexchange"
	"labix.org/v2/mgo"
	"labix.org/v2/mgo/bson"
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

// Filters
const (
	AllQuestionsFilter    = "!)QZFB_UZYOb1Jf*eWmfaRigq"
	QuestionAnswersFilter = "!4.nQbWlQBREYlr6GF"
)

// Flags
var (
	Site       = stackexchange.StackOverflow
	OAuthToken = ""
	Tag        = ""
	PerCall    = 50
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
	flag.IntVar(&PerCall, "percall", PerCall, "# of questions to grab per heartbeat")
	heartRate := flag.Duration("heartbeat", time.Minute, "time between scrapes for questions")
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

	heartbeat := time.Tick(*heartRate)
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)
	for {
		select {
		case <-interrupt:
			return
		default:
			// keep calm and carry on
		}

		log.Println("heartbeat")
		if err := fetchBatch(); err != nil {
			log.Println("batch failed:", err)
		}

		select {
		case <-heartbeat:
			// still beating!
		case <-interrupt:
			return
		}
	}
}

func fetchBatch() error {
	const (
		questionIDKey = "question_id"
		answerIDKey   = "answer_id"
	)

	questions, err := fetchQuestions(50, Tag)
	if err != nil {
		return err
	}
	questionIDs := make([]int, 0, len(questions))
	for _, q := range questions {
		if id, ok := getID(q, questionIDKey); ok {
			questionIDs = append(questionIDs, id)
			if _, err := Mongo.C(QuestionCollection).UpsertId(id, q); err != nil {
				log.Printf("question (id=%d) upsert failed: %v", id, err)
			}
		} else {
			log.Println("question has no ID")
		}
	}

	answers, err := fetchQuestionAnswers(questionIDs)
	if err != nil {
		return err
	}
	for _, a := range answers {
		if id, ok := getID(a, answerIDKey); ok {
			if _, err := Mongo.C(AnswerCollection).UpsertId(id, a); err != nil {
				log.Printf("answer (id=%d) upsert failed: %v", id, err)
			}
		} else {
			log.Println("answer has no ID")
		}
	}

	_, _ = questions, answers
	return nil
}

func fetchQuestions(n int, tag string) ([]bson.M, error) {
	var questions []bson.M
	_, err := Client.Do(stackexchange.PathAllQuestions, &questions, &stackexchange.Params{
		Site:     Site,
		Tagged:   tag,
		PageSize: n,
		Filter:   AllQuestionsFilter,
	})
	return questions, err
}

func fetchQuestionAnswers(ids []int) ([]bson.M, error) {
	var answers []bson.M
	_, err := Client.Do(stackexchange.PathQuestionAnswers, &answers, &stackexchange.Params{
		Site:   Site,
		Args:   []string{stackexchange.JoinIDs(ids)},
		Filter: QuestionAnswersFilter,
	})
	return answers, err
}

func getID(m bson.M, key string) (id int, ok bool) {
	if fid, ok := m[key].(float64); ok {
		return int(fid), true
	}
	return 0, false
}
