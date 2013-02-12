import csv

def insertPhrases (phrases_csv):
    with open(phrases_csv[:-3]+'sql','w') as output:
        output.write('INSERT INTO DATA_PHRASES (orig_utterance, sani_utterance) VALUES')
        with open(phrases_csv, 'Urb') as f:
            phrasereader = csv.reader(f, delimiter=',')
            for (row) in enumerate(phrasereader):
                output.write('\n('+str(row[1])[1:-1]+'), ')
                output.write('--'+str(row[0]+1))
 
def insertPairs (pairs_csv):
    with open(pairs_csv[:-3]+'sql','w') as output:
        output.write('INSERT INTO DATA_CONVO_PAIRS (utterance_id, response_id) VALUES')
        with open(pairs_csv, 'Urb') as f:
            phrasereader = csv.reader(f, delimiter=',')
            for (row) in enumerate(phrasereader):
                output.write('\n('+str(row[1])[1:-1]+'), ')
        

if __name__ == "__main__":
    import sys
    insertPhrases(sys.argv[1])
    insertPairs(sys.argv[2])
