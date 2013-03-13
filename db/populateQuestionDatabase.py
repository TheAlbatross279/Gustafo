import pymongo
from pymongo import MongoClient
import psycopg2
import datetime
from HTMLParser import HTMLParser

#Set up the postgres database connection
pconn = psycopg2.connect(database='mydb', user='postgres', password = 'password')
pgCur = pconn.cursor()

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

def saveUser(uname, uRep):
   #Query the DB to see if the user already exists
   pgCur.execute("SELECT * FROM so_user WHERE so_user = %s", [uname])
   result = pgCur.fetchone()

   #If the user does not exist, save it
   if(result == None):
      pgCur.execute("INSERT INTO so_user (so_user, reputation) VALUES (%s, %s)", (uname, uRep))


#Saves all comments for the specified answer
def saveAnswerComments(comments, aid):
   for comment in comments:
      
      curU = comment['owner']
      uname = curU['display_name']
      try:
         uRep = curU['reputation']
      except:
         uRep = 0

      saveUser(uname, uRep)

      cId = comment['comment_id']
      cBody = formatString(comment['body'])
      rating = comment['score']
      date = formatDate(comment['creation_date'])

      pgCur.execute("INSERT INTO acomment (acid, aid, so_user, text, rating, time) VALUES (%s, %s, %s, %s, %s, %s)", (cId, aid, uname, cBody, rating, date))



#Saves all comments for the specified question
def saveQuestionComments(comments, qid):
   for comment in comments:
      
      curU = comment['owner']
      uname = curU['display_name']
      try:
         uRep = curU['reputation']
      except:
         uRep = 0

      saveUser(uname, uRep)

      cId = comment['comment_id']
      cBody = formatString(comment['body'])
      rating = comment['score']
      date = formatDate(comment['creation_date'])

      pgCur.execute("INSERT INTO qcomment (qcid, qid, so_user, text, rating, time) VALUES (%s, %s, %s, %s, %s, %s)", (cId, qid, uname, cBody, rating, date))

#Saves all tags associated with the quesiton in the database
def saveTags(tags, qid):
   for tag in tags:

      #See if the tag exists
      pgCur.execute("SELECT * FROM tag WHERE tag = %s", [tag])
      result = pgCur.fetchone()

      if(result == None):
         pgCur.execute("INSERT INTO tag (tag) VALUES (%s)", [tag])

      #Add the relationship
      pgCur.execute("INSERT INTO tag_question (tag, qid) VALUES (%s, %s)", (tag, qid))



#Setting up the mongo connection
connection = MongoClient()
db = connection['gustafocrawler']
#Getting the 'tables' from the db
questions = db.questions
answers = db.answers

#Get all questions from the mongo db
allQuestions = questions.find({"is_answered":True})
#qNum = allQuestions.count()
i = 0

for curQ in allQuestions:

   #curQ = allQuestions.next()
   i = i + 1
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
   try:
      uRep = curU['reputation']
   except:
      uRep = 0

   #Make sure the user exists
   saveUser(uname, uRep)

   #Pull all attributes off the question
   title = formatString(curQ['title'])
   creator = curQ['owner']['display_name']
   editor = curQ['owner']['display_name']
   body = formatString(curQ['body']) 
   rating = curQ['up_vote_count']
   viewCount = curQ['view_count']
   favorited = curQ['favorite_count'] 
   created = formatDate(curQ['creation_date'])
   edited = formatDate(curQ['last_activity_date'])

   #Save the question in the postgresDB
   pgCur.execute("INSERT INTO question (qid, creator, editor, title, text, rating, num_views, favorited, created, edited) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (qid, creator, editor, title, body, rating, viewCount, favorited, created, edited))

   #Iterate over all question comments and persist them
   try:
      comments = curQ['comments']
      saveQuestionComments(comments, qid)
   except:
      pass

   tags = curQ['tags']
   saveTags(tags, qid)

   #Find all the answers associated with this question
   allAnswers = answers.find({"question_id":qid})
   aNum = allAnswers.count()

   for n in range(aNum):

      curA = allAnswers.next()

      #Get the user and put the user in the database
      curU = curA['owner']
      uname = curU['display_name']
      try:
         uRep = curU['reputation']
      except:
         uRep = 0

      #Pull all of the attributes off the answer
      aid = curA['answer_id'] 
      user = curA['owner']['display_name']
      body = formatString(curA['body'])
      rating = curA['up_vote_count']
      isAccepted = curA['is_accepted']
      time = formatDate(curA['creation_date'])

      saveUser(uname, uRep)

      #Save the answer in the postgresDB
      pgCur.execute("INSERT INTO answer (aid, qid, so_user, text, rating, is_accepted, time) VALUES (%s, %s, %s, %s, %s, %s, %s)", (aid, qid, user, body, rating, isAccepted, time))

      try:
         comments = curA['comments']
         saveAnswerComments(comments, aid)
      except:
         pass
      

   print str(i) + " Questions saved"

   #Commit each question
   pconn.commit()
