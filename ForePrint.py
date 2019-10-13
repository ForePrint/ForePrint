import MySQLdb
import pandas
from database import Database
from fingerprint import *
import logging
import hashlib
from tqdm import *
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
from ast import literal_eval
import csv
import time
import concurrent.futures
import multiprocessing
from functools import partial
from itertools import repeat
from pathlib import Path
from rules import Rules
from queue import Queue
import threading
import pickle
from utils import calculate_rule_hash

logging.basicConfig(filename='ForePrint.log',level=logging.INFO)
"""
Storing log file into ForePrint.log
"""

rule_pipe = Queue()

def front_end(rule_operations, options, known_user_portions):
    """
    Front-End Operations.
    """
    try:
        unmatched_list = []
        matched_list = []
        df_whole = rule_operations.df_whole
        df_rule = rule_operations.df_rule
        rule_list = df_rule['browserid'].tolist()
        whole_list = df_whole['browserid'].tolist()
        e = threading.Event()
        a = threading.Thread(target=back_end, args=(aqueue, e, rule_operations))
        a.setDaemon(True)
        a.start()
        for idx in tqdm(df_whole.index):
            idx_browserid = df_whole.at[idx, 'browserid']
            idx_fp = df_whole.loc[[idx]]
            if idx_browserid in rule_list:
                '''
                For all the logged-in users, generate the rules. 
                '''
                indexes_to_keep = set(range(rule_operations.df_predicts.shape[0])) - set([idx])
                rule_operations.df_predicts = rule_operations.df_predicts.take(list(indexes_to_keep))
                rule = rule_operations.update_rules(idx_fp)
                if not rule:
                    continue
                if not rule_operations.judge_rule(rule):
                    continue
                aqueue.put(rule)
                e.set()
                temp_hash = calculate_rule_hash(rule)
                rule_operations.insert_rule(temp_hash)
            elif rule_operations.have_match(idx_fp, idx, options):
                '''
                If the fingerprint has match in the predictions, then record the data.
                '''
                rule_operations.insert_prediction_without_rule(rule_operations.calculate_hash(idx_fp), idx_browserid, idx)
                matched_list.append(idx)
                rule_operations.update_result()
                rule_operations.insert_fingerprint(idx)
            else:
                '''
                Update the result, mainly for negtive false.
                '''
                rule_operations.insert_prediction_without_rule(rule_operations.calculate_hash(idx_fp), idx_browserid, idx)
                rule_operations.insert_fingerprint(idx)
                # if idx_browserid in whole_list[:idx]:
                #     unmatched_list.append(idx)

        # with open('match_list.txt', 'wb') as f:
        #     pickle.dump(rule_operations.match_list, f)
        # with open('unmatch_list.txt', 'wb') as f:
        #     pickle.dump(unmatched_list, f)
         """
         Get the Result for the system.
         """
         rule_operations.get_result()
    except Exception as e:
        logging.exception(str(e))

def back_end(queue, e, rule_operations):
    while True:
        e.wait()
        while not queue.empty():
            rule = queue.get()
            rule_operations.update_dataset(rule)

def main(argv):
    """
    The first element is the options number.
    The Second element is the known users portions.
    This main function is responsible for the system.
    """
    options = argv[0]
    known_user_portions = argv[1]
    rule_operations = Rules()
    front_end(rule_operations, options, knonw_user_portions)

if __name__ == "__main__":
    main()

