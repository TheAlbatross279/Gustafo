import csv

def insertPhrases (phrases_csv):
    with open(phrases_csv[:-3] + 'sql','w') as output:
        with open(phrases_csv, 'Urb') as f:
            phrasereader = csv.reader(f, delimiter=',')
            for row in phrasereader:
                output.write('INSERT INTO DATA_PHRASES (orig_utterance, sani_utterance) VALUES (' + str(row)[1:-1] + ');\n')
 
def insertPairs (pairs_csv):
    with open(pairs_csv[:-3]+'sql','w') as output:
        with open(pairs_csv, 'Urb') as f:
            phrasereader = csv.reader(f, delimiter=',')
            for row in phrasereader:
                output.write('INSERT INTO DATA_CONVO_PAIRS (utterance_id, response_id) VALUES (' + str(row)[1:-1] + ');\n')

def insertUsage(usage_csv):
    with open(usage_csv[:-3]+'sql','w') as output:
        with open(usage_csv, 'Urb') as f:
            phrasereader = csv.reader(f, delimiter=',')
            for row in phrasereader:
                output.write('INSERT INTO DATA_PHRASE_STATS (id, user_use, gust_use) VALUES ('  + str(row)[1:-1] + ');\n')
    


if __name__ == "__main__":
    insertPhrases('insert_seeds.csv')
    insertPairs('insert_pairings.csv')
    insertUsage('insert_usage.csv')
