package main

import (
	"bitbucket.org/zombiezen/stackexchange"
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"
)

var (
	Site = stackexchange.StackOverflow
	Client *stackexchange.Client
)

func main() {
	flag.StringVar(&Site, "site", Site, "the site name to scrape from")
	flag.Parse()

	transport := NewThrottledRoundTripper(http.DefaultTransport)
	defer transport.Close()
	Client = &stackexchange.Client{
		Client: &http.Client{
			Transport: transport,
		},
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

// ThrottledRoundTripper rate-limits requests sent to an underlying http.RoundTripper.
type ThrottledRoundTripper struct {
	http.RoundTripper
	c    chan roundTripRequest
	quit chan struct{}
}

func NewThrottledRoundTripper(rt http.RoundTripper) *ThrottledRoundTripper {
	t := &ThrottledRoundTripper{
		RoundTripper: rt,
		c:            make(chan roundTripRequest),
		quit:         make(chan struct{}),
	}
	go t.run()
	return t
}

type roundTripRequest struct {
	r *http.Request
	c chan roundTripResponse
}

type roundTripResponse struct {
	resp *http.Response
	err  error
}

func (rt *ThrottledRoundTripper) run() {
	const (
		perDay    = 10000
		perSecond = 30

		tickDuration = time.Second / perSecond
	)

	remaining := perDay
	day := time.Tick(24 * time.Hour)
	ticker := time.NewTicker(tickDuration)
	tickChan := ticker.C
	for {
		select {
		case <-tickChan:
			req := <-rt.c
			resp, err := rt.RoundTripper.RoundTrip(req.r)
			req.c <- roundTripResponse{resp, err}

			remaining--
			if remaining <= 0 {
				ticker.Stop()
				ticker = nil
				tickChan = nil
			}
		case <-day:
			remaining += perDay
			if ticker == nil {
				ticker = time.NewTicker(tickDuration)
				tickChan = ticker.C
			}
		case <-rt.quit:
			return
		}
	}
}

func (rt *ThrottledRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	c := make(chan roundTripResponse)
	rt.c <- roundTripRequest{req, c}
	resp := <-c
	return resp.resp, resp.err
}

func (rt *ThrottledRoundTripper) Close() error {
	close(rt.c)
	return nil
}
