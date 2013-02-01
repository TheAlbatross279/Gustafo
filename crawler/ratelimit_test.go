package main

import (
	"bitbucket.org/zombiezen/stackexchange"
	"testing"
	"time"
)

func TestRateLimitClient(t *testing.T) {
	base := time.Date(2009, 11, 10, 23, 0, 0, 0, time.UTC)
	timer := &mockTimer{base}
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

type mockTimeClient struct {
	times []time.Time
	timer *mockTimer
}

func (mtc *mockTimeClient) Do(path string, v interface{}, params *stackexchange.Params) (*stackexchange.Wrapper, error) {
	mtc.times = append(mtc.times, mtc.timer.t)
	return nil, nil
}

type mockTimer struct {
	t time.Time
}

func (mt *mockTimer) Now() time.Time {
	return mt.t
}

func (mt *mockTimer) Sleep(d time.Duration) {
	mt.t = mt.t.Add(d)
}

func (mt *mockTimer) NewTicker(d time.Duration) ticker {
	return new(mockTicker)
}

type mockTicker struct{}

func (mt *mockTicker) Chan() <-chan time.Time {
	// TODO
	return make(chan time.Time)
}

func (mt *mockTicker) Stop() {
}
