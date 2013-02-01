package main

import (
	"time"
)

// Interfaces for mocking time

type timer interface {
	Now() time.Time
	Sleep(d time.Duration)
	NewTicker(d time.Duration) ticker
}

type ticker interface {
	Chan() <-chan time.Time
	Stop()
}

type realTime struct{}

func (realTime) Now() time.Time {
	return time.Now()
}

func (realTime) Sleep(d time.Duration) {
	time.Sleep(d)
}

func (realTime) NewTicker(d time.Duration) ticker {
	return (*realTicker)(time.NewTicker(d))
}

type realTicker time.Ticker

func (rt *realTicker) Chan() <-chan time.Time {
	return (*time.Ticker)(rt).C
}

func (rt *realTicker) Stop() {
	(*time.Ticker)(rt).Stop()
}
