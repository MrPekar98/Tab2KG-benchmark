import sys
from pathlib import Path
import time
import csv
import re
import threading
import queue
import ast
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor
from config import Config

if len(sys.argv) < 5:
    print('Provide arguments API key, KG name (wikidata or dbpedia), input directory, and output path')
    exit(1)

# MODEL CONFIGURATION
GEMINI_API_KEY = sys.argv[1]
KG = sys.argv[2]
INPUT = sys.argv[3]
OUTPUT = sys.argv[4]
MODEL_NAME = "gemini-2.5-pro"
LOOKUP_URL = sys.argv[5]

if KG != 'wikidata' and KG != 'dbpedia':
    print('KG \'' + KG + '\' not recognized')
    exit(1)

genai.configure(api_key = GEMINI_API_KEY)

generation_config = {
  "temperature": 0.25,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name=MODEL_NAME,
  generation_config=generation_config,
)

# INITIALIZATION
entity_dict = {}
event = threading.Event()
task_queue = queue.Queue()
task_lock = threading.Lock()

config = Config[KG]

# IMPLEMENTATION
def write_csv(wfilename, wrow, wcol, wurl):
    output_filename = OUTPUT + "/cea-" + MODEL_NAME + ".csv"

    with open(output_filename, mode='a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([wfilename, wrow, wcol, wurl])

def extract_csv(filename: str) -> list:
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        return list(csv_reader)

url_pattern = re.compile(r'http[s]?://[^\s",]+')

def extract_url(text):
    matches = url_pattern.findall(text)

    if matches:
        KG_url = " ".join(matches)
        return KG_url
    else:
        KG_url = " "
        return KG_url

'''
Clean the data using a prompt by the LLM.
It corrects words that are not written properly and output it in the same format it has been input.
'''
def clean_data(raw_csv_data):
    clean_data_msg = f"""
        Analyse the whole CSV file, perform data cleaning to remove noise and correct any misspelled words.
        Provide the response as the same format with no other text.
        CSV file: {raw_csv_data}"""

    try:
        csv_data_response = model.generate_content(clean_data_msg).text.strip()
        csv_data = ast.literal_eval(csv_data_response)

        return csv_data

    except Exception as e:
        print(e)

'''
Up to 5 entities are retrieved from the Lookup API
'''
def get_entities(cell_data):
    limit = 5
    KG_api = config["KG_api"]

    KG_results = []
    entities = KG_api.getKGEntities(cell_data, limit)

    for ent in entities:
        KG_results.append(ent)

    return KG_results

'''
Annotation process of each cell data with an entity
'''
def process_cell(filename, row_index, col_index, cell_data, csv_data, entity_dict):
    KG_source = config["KG_source"]
    KG_link_template = config["KG_link_template"]

    ## Entities are retrieved or added into the dictionary cache
    with task_lock:
        if cell_data in entity_dict:
            KG_results = entity_dict[cell_data]
        else:
            KG_results = get_entities(cell_data)
            entity_dict[cell_data] = KG_results

    candidates = ''

    for entity in KG_results:
        candidates += entity + '#'

    with task_lock:
        write_csv(filename, row_index, col_index, candidates)

def is_numeric(value):
    numeric_pattern = re.compile(r'^-?\d+(\.\d+)?$')
    numeric_thousands_pattern = re.compile(r'^-?\d{1,3}(,\d{3})*(\.\d+)?$')
    return bool(numeric_pattern.match(value)) or bool(numeric_thousands_pattern.match(value))

def is_date(value):
    date_pattern = re.compile(r'^(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}|\d{2}/\d{2}/\d{2})$')       
    return bool(date_pattern.match(value))

'''
Clear the entity cache dictionary after 15 seconds
'''
def clear_entity_cache(entity_dict):
    if event.is_set():
        return
    with task_lock:
        entity_dict.clear()
    threading.Timer(15, clear_entity_cache, args=[entity_dict]).start()

'''
Loop through the file to process all the data cells
'''
def annotate_csv_cell(filepath):
    filepath = Path(filepath)
    filename = filepath.name.removesuffix('.csv')

    clear_entity_cache(entity_dict)
    raw_csv_data = extract_csv(filepath)
    csv_data = clean_data(raw_csv_data)

    for row_index, row in enumerate(csv_data[1:], start = 1):
        for col_index, cell_data in enumerate(row):
            if not (is_numeric(cell_data) or is_date(cell_data) or cell_data.strip() == '' or cell_data is None):
                process_cell(filename, row_index, col_index, cell_data, csv_data, entity_dict)

'''
Loop through  the folder to process all csv files.
Threading was implemented with the help of Generative AI (ChatGPT).
'''
def annotate_csv_files(input_folderpath):
    folderpath = Path(input_folderpath)

    with ThreadPoolExecutor(max_workers=1) as executor:
        for csv_file in folderpath.rglob('*.csv'):
            task_queue.put(csv_file)

        while not task_queue.empty():
            filepath = task_queue.get()
            executor.submit(annotate_csv_cell, filepath)
            task_queue.task_done()

if __name__ == '__main__':
    start_time = time.time()
    event.clear()
    input_folderpath = INPUT

    annotate_csv_files(input_folderpath)

    task_queue.join()
    event.set()     # stop threading timer

    print('\n\nTime taken:', time.time() - start_time, 's\n\n')
