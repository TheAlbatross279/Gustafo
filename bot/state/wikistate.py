"""
Wiki parser
@version lab 3
"""
import nltk
import os
import calendar
from nltk import pos_tag, word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk.tree import Tree
from state import State
from HTMLParser import HTMLParser
from datetime import datetime
import urllib
import string

class WikiState(State):

   #finds birthday keywords and removes them, setting isbirthday to true
   @staticmethod
   def clear_birthday_words(input_text):
      birthday_keywords = ['born', 'birthdate', 'birthday', 'birth', 'date']
      info_keywords = ['information', 'subject']
      candidates = []
      isBirthday = False
      for (w, pos) in input_text:
         if w not in birthday_keywords:
            if w not in info_keywords:
               candidates.append((w, pos))
         elif not isBirthday:
            isBirthday = True

      if(isBirthday):
         remove = [('\xe2', 'NNP'), ('\x80', 'NNP'), ('\x99', 'NNP')]
         for item in remove:
            if item in candidates:
               candidates.remove(item)

      return (candidates, isBirthday)
   
   @staticmethod
   def parser_results(candidates):
      name = None

      #tagged_words = pos_tag(input_text)
      grammar = "NP: {((?:(?:<DT>)?(?:<NN[P]?[S]?>|<CD>|<JJ>)+)(?:(?:<DT>|<IN>)*(?:<NN[P]?[S]?>|<CD>|<CC>|<POS>|<JJ>)+)*)}"
      cp = RegexpParser(grammar)
      result = cp.parse(candidates)

      foundNP = False
      for e in result:
         if isinstance(e, Tree):
            if e.node == 'NP':
               if e[0][1] == "DT" and e[0][0][0] not in string.uppercase:
                  e = e[1:]
               name = [w[0] for w in e]
               foundNP = True
     
      return (name, foundNP)

   @staticmethod
   def recognize(cmd):
      #remove birthday keywords
      (candidates, isBirthday) = WikiState.clear_birthday_words(cmd)
      (name, foundNP) = WikiState.parser_results(candidates)
      
      #if can't find noun phrase, try all results again
      if not foundNP:
         (name, foundNP) = WikiState.parser_results(cmd)

      if name == None:
         return (0, {})
      
      return (0.9, {'name': name, 'isBirthday': isBirthday})

   @staticmethod      
   def respond(context):
      #prefix = "\"http://en.wikipedia.org/w/api.php?format=dump&action=query&prop=revisions&rvprop=content&titles="
      prefix = "\"http://en.wikipedia.org/wiki/"

      page = urllib.quote('_'.join(context["name"]))

      print page
#      page = re.sub("[ ]", "_", page)

      link = prefix + page + "\""
      print link

      os.system("wget -O wiki.tmp " + link)

      wiki_file = open('wiki.tmp')
      input_text = wiki_file.read()
#      print input_text

      wiki_file.close()
      #print input_text

      if not context['isBirthday']:
         #clean_wiki = re.compile("^\|[^\n]*|^:[^\n]*|^;[^\n]*|^\*[^\n]*|<ref[^>]*>[^<]*</ref>|</?ref[^/>]*/?>|\[\[File:[^\]]*\]]|\[\[[^\|\]]*\||\[\[|\]\]|<[^/>]*/>|<!--[^-]*-->|{{[^}\n]*}};?|}}|{{[^\n]*|'''|&nbsp;|</?nowiki>", re.M)
         #input_text = re.sub(clean_wiki, "", input_text)
         #input_text = re.sub(r'(?:.|\n)*\["\*"\]=>\n\W*string\(\d+\)\W*"', "", input_text, 1)
         #print input_text[:5000]
         #input_text = input_text.split('\n')
         #input_text = [line for line in input_text if len(line) > 250]
         input_text = re.findall(r"<p>(.*?)<\/p>", input_text)
         if len(input_text) == 0:
            return "I don't know anything about " + " ".join(context['name'])

         count = 0
         input_text_temp = nltk.util.clean_html(input_text[count])
         print count, input_text_temp[0]
         while('^' in input_text_temp):
            count = count + 1
            input_text_temp = nltk.util.clean_html(input_text[count])
 
         input_text = nltk.util.clean_html(input_text[count])
 
         input_text = re.sub(r'\[(?:\s*\d+\s*|\s*[cC]itation [nN]eeded\s*)\]', "", input_text)
         input_text = re.sub(r' +', " ", input_text)
         input_text = re.sub(r' (-|,|\.|\)|:|;)', r"\g<1>", input_text)
         input_text = re.sub(r'(-|\() ', r"\g<1>", input_text)
         input_text = re.sub(r'&nbsp;', " ", input_text)
         input_text = re.sub(r'&\S+;', "", input_text)

         pst = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(input_text)
         
         length = len(context['_nick']) 
         final_string = ""
         for sent in pst:
            length += len(sent) + 1
            if length < 425:
               final_string += sent + " "

         os.system("rm wiki.tmp") 
         
         dis_string = re.split('\W+', final_string)
         if(dis_string[len(dis_string)-2] == 'to' and dis_string[len(dis_string)-3] == 'refer' and dis_string[len(dis_string)-4] == 'may'):
            final_string = "Disambiguation page found for " + " ".join(context['name'])

         return final_string
      else: #is birthday
         dob = re.findall(r'<span class="bday">([\d-]+)</span>', input_text)
         os.system("rm wiki.tmp") 
         if len(dob) < 1:
            return "I'm not sure when " + " ".join(context['name']) + " was born..."
         else:
            date = datetime.strptime(dob[0], "%Y-%m-%d")
            dob = calendar.month_name[date.month] + " " + str(date.day) + ", " + str(date.year)

            return " ".join(context['name']) + " was born on " + dob

#State.register(WikiState, True)
