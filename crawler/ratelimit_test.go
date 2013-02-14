package main

import (
	"bitbucket.org/zombiezen/stackexchange"
	"sync"
	"testing"
	"time"
)

func TestRateLimitClientBasic(t *testing.T) {
	base := time.Date(2009, 11, 10, 23, 0, 0, 0, time.UTC)
	timer := &mockTimer{t: base}
	mtc := &mockTimeClient{timer: timer}

	// init
	rlc := &RateLimitClient{
		client: mtc,
		c:      make(chan *apiRequest),
		timer:  timer,
	}
	go rlc.run()

	// run tests
	if _, err := rlc.Do("/questions", nil, nil); err != nil {
		t.Errorf("#1 error: %v", err)
	}
	if !timer.t.Equal(base) {
		t.Error("#1 slept")
	}
	if _, err := rlc.Do("/questions", nil, nil); err != nil {
		t.Errorf("#2 error: %v", err)
	}
	if !timer.t.Equal(base.Add(time.Second / 30)) {
		t.Error("#2 did not wait")
	}

	// TODO: test particular paths, test backoff, test daily
}

func TestRateLimitClientAddDaily(t *testing.T) {
	base := time.Date(2009, 11, 10, 23, 0, 0, 0, time.UTC)
	ticker := make(chan time.Time)
	timer := &mockTimer{t: base, tick: ticker}
	mtc := &mockTimeClient{timer: timer}

	// init
	rlc := &RateLimitClient{
		client: mtc,
		c:      make(chan *apiRequest),
		timer:  timer,
		qr:     make(chan int),
	}
	go rlc.run()

	// run tests
	if qr, expect := <-rlc.qr, 10000; qr != expect {
		t.Errorf("quota remaining = %d; want %d", qr, expect)
	}
	if _, err := rlc.Do("/questions", nil, nil); err != nil {
		t.Errorf("#1 error: %v", err)
	}
	if !timer.t.Equal(base) {
		t.Error("#1 slept")
	}
	if qr, expect := <-rlc.qr, 9999; qr != expect {
		t.Errorf("quota remaining = %d; want %d", qr, expect)
	}
	ticker <- base.Add(24 * time.Hour)
	if qr, expect := <-rlc.qr, 19999; qr != expect {
		t.Errorf("quota remaining = %d; want %d", qr, expect)
	}
}

type mockTimeClient struct {
	times []time.Time
	timer *mockTimer
}

func (mtc *mockTimeClient) Do(path string, v interface{}, params *stackexchange.Params) (*stackexchange.Wrapper, error) {
	mtc.times = append(mtc.times, mtc.timer.t)
	return nil, nil
}

type mockTimer struct {
	t    time.Time
	tick chan time.Time
	sync.RWMutex
}

func (mt *mockTimer) Now() time.Time {
	mt.RLock()
	defer mt.RUnlock()
	return mt.t
}

func (mt *mockTimer) Sleep(d time.Duration) {
	mt.Lock()
	defer mt.Unlock()
	mt.t = mt.t.Add(d)
}

func (mt *mockTimer) NewTicker(d time.Duration) ticker {
	return mockTicker(mt.tick)
}

type mockTicker chan time.Time

func (mt mockTicker) Chan() <-chan time.Time {
	return mt
}

func (mt mockTicker) Stop() {
}
