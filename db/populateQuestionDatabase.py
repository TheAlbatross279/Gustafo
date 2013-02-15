import pymongo
from pymongo import MongoClient
import psycopg2
import datetime
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
   def __init__(self):
      self.reset()
      self.fed = []
   def handle_data(self, d):
      self.fed.append(d)
   def get_data(self):
      return ''.join(self.fed)

def strip_tags(htmlText):
   s = MLStripper()
   s.feed(htmlText)
   return s.get_data()

def formatString(text):
   return strip_tags(text)

def formatDate(dateNum):
   return datetime.datetime.fromtimestamp(dateNum)

#Setting up the postgres connection
pconn = psycopg2.connect(database='mydb', user='postgres', password = 'password')
pgCur = pconn.cursor()

#Setting up the mongo connection
connection = MongoClient()
db = connection['gustafocrawler']
#Getting the 'tables' from the db
questions = db.questions
answers = db.answers

#Get all questions from the mongo db
allQuestions = questions.find({"is_answered":True})
qNum = allQuestions.count()

for i in range(qNum):

   curQ = allQuestions.next()

   #Retrieve the question id
   qid = curQ['question_id']

   #See if this question is already in the postgres db
   pgCur.execute("SELECT * FROM question WHERE qid = %s", [qid])
   result = pgCur.fetchone()

   #If the question already exists in the DB, continue
   if(result != None):
      continue

   #Get the user and put the user in the database
   curU = curQ['owner']
   uname = curU['display_name']
   uRep = 0#curU['reputation']

   #Query the DB to see if the user already exists
   pgCur.execute("SELECT * FROM so_user WHERE so_user = %s", [uname])
   result = pgCur.fetchone()

   #If the user does not exist, save it
   if(result == None):
      pgCur.execute("INSERT INTO so_user (so_user, reputation) VALUES (%s, %s)", (uname, uRep))

   #Pull all attributes off the question
   title = formatString(curQ['title'])
   creator = curQ['owner']['display_name']
   editor = curQ['owner']['display_name']
   body = formatString(curQ['body']) 
   rating = curQ['up_vote_count']
   favorited = curQ['favorite_count'] 
   created = formatDate(curQ['creation_date'])
   edited = formatDate(curQ['last_activity_date'])

   #Save the question in the postgresDB
   pgCur.execute("INSERT INTO question (qid, creator, editor, title, text, rating, favorited, created, edited) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (qid, creator, editor, title, body, rating, favorited, created, edited))


   #Find all the answers associated with this question
   allAnswers = answers.find({"question_id":qid})
   aNum = allAnswers.count()

   for n in range(aNum):

      curA = allAnswers.next()

      #Get the user and put the user in the database
      curU = curA['owner']
      uname = curU['display_name']
      uRep = 0#curU['reputation']

      #Pull all of the attributes off the answer
      aid = curA['answer_id'] 
      user = curA['owner']['display_name']
      body = formatString(curA['body'])
      rating = curA['up_vote_count']
      time = formatDate(curA['creation_date'])

      #Query the DB to see if the user already exists
      pgCur.execute("SELECT * FROM so_user WHERE so_user = %s", [uname])
      result = pgCur.fetchone()

      #If the user does not exist, save it
      if(result == None):
         pgCur.execute("INSERT INTO so_user (so_user, reputation) VALUES (%s, %s)", (uname, uRep))

      #Save the answer in the postgresDB
      pgCur.execute("INSERT INTO answer (aid, qid, so_user, text, rating, time) VALUES (%s, %s, %s, %s, %s, %s)", (aid, qid, user, body, rating, time))


   print str(i) + " Questions saved"

#Commit to make sure everything is in the DB
pconn.commit()
