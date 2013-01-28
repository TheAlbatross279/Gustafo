package main

import (
	"bitbucket.org/zombiezen/stackexchange"
)

type StackExchangeClient interface {
	Do(path string, v interface{}, params stackexchange.Params) (*stackexchange.Wrapper, error)
}

// RateLimitClient rate-limits requests sent to an underlying StackExchangeClient.
type RateLimitClient struct {
	client StackExchangeClient
	c      chan struct{}
}

func NewRateLimitClient(client StackExchangeClient) *RateLimitClient {
	rlc := &RateLimitClient{
		client: client,
		c:      make(chan struct{}),
	}
	go rlc.run()
	return rlc
}

func (rlc *RateLimitClient) run() {
	// TODO
}

func (rlc *RateLimitClient) Do(path string, v interface{}, params stackexchange.Params) (*stackexchange.Wrapper, error) {
	// TODO
	return nil, nil
}

func (rlc *RateLimitClient) Close() error {
	close(rlc.c)
	return nil
}
