package main

import (
	"time"
)

type Question struct {
	ID               int       `bson:"_id"`
	AcceptedAnswerID int       `bson:"accepted_answer_id,omitempty"`
	AnswerCount      int       `bson:"answer_count"`
	ClosedDate       time.Time `bson:"closed_date,omitempty"`
	ClosedReason     string    `bson:"closed_reason,omitempty"`
	Created          time.Time `bson:"creation_date"`
	IsAnswered       bool      `bson:"is_answered"`
	Link             string    `bson:"link"`
	Score            int       `bson:"score"`
	Title            string    `bson:"title"`
}

type Answer struct {
	ID         int       `bson:"_id"`
	Body       string    `bson:"body"`
	Created    time.Time `bson:"creation_date"`
	IsAccepted bool      `bson:"is_accepted"`
	Link       string    `bson:"link"`
	QuestionID int       `bson:"question_id"`
	Score      int       `bson:"score"`
	Title      string    `bson:"title"`
}
