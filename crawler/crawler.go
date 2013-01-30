package main

import (
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"

	"bitbucket.org/zombiezen/stackexchange"
)

// OAuth constants
const (
	appClientID    = "1144"
	appKey         = "VbR*HN60lyuKdIHm3M)3)Q(("
	oauthDialogURL = "https://stackexchange.com/oauth/dialog"
	redirectURL    = "https://stackexchange.com/oauth/login_success"
)

var (
	Site       = stackexchange.StackOverflow
	OAuthToken = ""

	Client StackExchangeClient
)

func main() {
	flag.StringVar(&Site, "site", Site, "the site name to scrape from")
	flag.StringVar(&OAuthToken, "oauth", OAuthToken, "OAuth 2.0 token")
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
		rlc := NewRateLimitClient(&stackexchange.Client{
			AccessToken: OAuthToken,
			Key:         appKey,
		})
		defer rlc.Close()
		Client = rlc
	}

	var questions []stackexchange.Question
	_, err := Client.Do("/questions", &questions, stackexchange.Params{
		Site:     Site,
		Sort:     stackexchange.SortActivity,
		Order:    "desc",
		PageSize: 10,
	})
	if err != nil {
		log.Print(err)
		return
	}
	fmt.Println("10 Most Recent:")
	for i := range questions {
		q := &questions[i]
		fmt.Printf("%d. %s (score=%d) %s\n", i+1, q.Title, q.Score, q.Link)
	}
	fmt.Println()
}
