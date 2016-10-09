import traceback
import sys
import re
import glob
import json
import urllib
import urllib2
from time import gmtime, strftime

INPUT_DIR = '../data/text/'
OUTPUT_DIR = '../data/json/'

API_KEY= ''
annotatorUrl = 'http://data.bioontology.org/annotator' 

ontology_list = 'ICD9CM,LOINC'
tui_list = 'T017,T029,T023,T030'

def get_json(text):
    params = {
        'text':text, 
        'longest_only':'true',
        'whole_word_only':'true',
        'stop_words':'',
        'ontologies':ontology_list,   
        'ontologiesToKeepInResult':'',   
        'isVirtualOntologyId':'true', 
        'semantic_types':tui_list,
        'apikey':API_KEY
    }
    headers = {'Authorization': 'apikey token=' + API_KEY}
    data = urllib.urlencode(params)
    request = urllib2.Request(annotatorUrl, data, headers)
    response = urllib2.urlopen(request)
    data_json = json.loads(response.read().decode('utf-8'))
    # print 'http status: '+ str(response.getcode())
    return data_json

def main():
    for filename in glob.glob(INPUT_DIR+'*.txt'):
        # for each file load file 
        text = ''
        lines = open(filename,"r").read().splitlines()
        for l in lines:
            text = text + l.rstrip()
        # remove special characters
        text = re.sub('[^A-Za-z0-9]+', ' ', text)
        try:
            # get json
            data = get_json(text)
            # save to json file
            filename_nodir = filename.split('/')[-1].split('.')[0]
            json_fn = '' + filename_nodir + '.json'
            with open(OUTPUT_DIR+json_fn, 'w') as outfile:
                json.dump(data, outfile)
            print strftime("%Y-%m-%d %H:%M:%S") + ' SUCCESS ' + filename_nodir
        except:
            print strftime("%Y-%m-%d %H:%M:%S") + ' FAIL ' + filename_nodir
            raise

if __name__ == "__main__":
    main()
