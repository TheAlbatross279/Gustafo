package main

import (
	"bitbucket.org/zombiezen/stackexchange"
	"log"
	"sync"
	"time"
)

const (
	apiPerSecond = 30
	apiPerDay    = 10000

	dayDuration = 24 * time.Hour

	secondsPerApi = time.Second / apiPerSecond
)

type StackExchangeClient interface {
	Do(path string, v interface{}, params *stackexchange.Params) (*stackexchange.Wrapper, error)
}

// RateLimitClient rate-limits requests sent to an underlying StackExchangeClient.
// A RateLimitClient is safe to use from multiple goroutines.
type RateLimitClient struct {
	client StackExchangeClient
	c      chan *apiRequest
	locker keyLocker
	timer  timer
	qr     chan int // quota remaining channel (for testing)
}

func NewRateLimitClient(client StackExchangeClient) *RateLimitClient {
	rlc := &RateLimitClient{
		client: client,
		c:      make(chan *apiRequest),
		timer:  realTime{},
	}
	go rlc.run()
	return rlc
}

func (rlc *RateLimitClient) run() {
	day := rlc.timer.NewTicker(dayDuration)
	defer day.Stop()

	quotaRemaining := apiPerDay
	var lastRequest time.Time
	for {
		for quotaRemaining > 0 {
			select {
			case req, ok := <-rlc.c:
				if !ok {
					return
				}
				now := rlc.timer.Now()
				if elapsed := now.Sub(lastRequest); elapsed < secondsPerApi {
					rlc.timer.Sleep(secondsPerApi - elapsed)
					now = rlc.timer.Now()
				}
				lastRequest = now
				quotaRemaining--
				go rlc.handle(req)
			case rlc.qr <- quotaRemaining:
				// send quota remaining (if under test)
			case <-day.Chan():
				quotaRemaining = apiPerDay
			}
		}

		<-day.Chan()
		quotaRemaining = apiPerDay
	}
}

func (rlc *RateLimitClient) handle(req *apiRequest) {
	// Ensure sequential access to this path
	lock := rlc.locker.Get(req.path)
	lock.Lock()
	defer lock.Unlock()

	// Send request
	wrapper, err := rlc.client.Do(req.path, req.v, req.params)

	// Log API call
	if wrapper != nil {
		if werr := &wrapper.Error; werr.ID != 0 {
			log.Printf("API %v (quota=%d/%d backoff=%d) error: %v", req.path, wrapper.QuotaRemaining, wrapper.QuotaMax, wrapper.Backoff, werr)
		} else {
			log.Printf("API %v (quota=%d/%d backoff=%d) OK", req.path, wrapper.QuotaRemaining, wrapper.QuotaMax, wrapper.Backoff)
		}
	} else {
		log.Printf("API %v FAIL: %v", req.path, err)
	}

	// Send back response
	req.c <- &apiResponse{wrap: wrapper, err: err}

	// Wait for backoff before releasing lock
	if wrapper != nil && wrapper.Backoff > 0 {
		dur := time.Duration(wrapper.Backoff) * time.Second
		rlc.timer.Sleep(dur)
	}
}

func (rlc *RateLimitClient) Do(path string, v interface{}, params *stackexchange.Params) (*stackexchange.Wrapper, error) {
	c := make(chan *apiResponse)
	rlc.c <- &apiRequest{
		path:   path,
		v:      v,
		params: params,
		c:      c,
	}
	resp := <-c
	return resp.wrap, resp.err
}

func (rlc *RateLimitClient) Close() error {
	close(rlc.c)
	return nil
}

type apiRequest struct {
	path   string
	v      interface{}
	params *stackexchange.Params
	c      chan *apiResponse
}

type apiResponse struct {
	wrap *stackexchange.Wrapper
	err  error
}

// keyLocker is a key-value lock store.  The zero value is an empty mapping.
type keyLocker struct {
	mutex sync.Mutex
	m     map[string]*sync.Mutex
}

// Get returns the lock for the key, creating a lock if necessary.
func (kl *keyLocker) Get(key string) sync.Locker {
	kl.mutex.Lock()
	defer kl.mutex.Unlock()

	if kl.m == nil {
		kl.m = make(map[string]*sync.Mutex)
	}
	lock := kl.m[key]
	if lock == nil {
		lock = new(sync.Mutex)
		kl.m[key] = lock
	}
	return lock
}
