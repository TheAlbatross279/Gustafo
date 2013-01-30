package main

import (
	"bitbucket.org/zombiezen/stackexchange"
	"flag"
	"fmt"
	"log"
)

var (
	Site = stackexchange.StackOverflow
	Client StackExchangeClient
)

func main() {
	flag.StringVar(&Site, "site", Site, "the site name to scrape from")
	flag.Parse()

	{
		rlc := NewRateLimitClient(stackexchange.DefaultClient)
		defer rlc.Close()
		Client = rlc
	}

	for {
		var questions []stackexchange.Question
		_, err := Client.Do("/questions", &questions, stackexchange.Params{
			Site: Site,
			Sort: stackexchange.SortActivity,
			Order: "desc",
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
}
