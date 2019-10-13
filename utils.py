import pandas
from database import Database
from fingerprint import *
import logging
import hashlib
from tqdm import *
import numpy as np
import json
from ast import literal_eval
import csv
import time
from functools import partial
from itertools import repeat
from pathlib import Path
import pickle

def calculate_rule_hash(rule):
    """
    calculate the hash value for a rule.
    """
    hash_string = ''
    for value in rule.values():
        hash_string = hash_string + str(value[0]) + str(value[1])
    hashvalue = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    return hash_value

def generate_changes_database(db, feature_list = feature_list):
    """
    this function will generate the changes database
    the database should be generated before the call of this function
    we will keep users who visit more than 3 times
    """
    browserid = 'browserid'

    feature_list = db.get_column_names('pandas_features')
    df = db.load_data(feature_list = ["*"],
            table_name = "pandas_features")
    df = filter_less_than_n(df, 3)

    # add label changes to database
    if 'label' not in feature_list:
        feature_list.append('label')

    maps = {}
    for feature in feature_list:
        maps[feature] = {'browserid':[], "clientid":[], "IP":[], "from":[], "to":[], "fromtime":[], "totime":[], "browser":[], "os":[]}

    grouped = df.groupby(browserid)
    pre_fingerprint = ""
    pre_row = []
    for cur_key, cur_group in tqdm(grouped):
        if cur_group['browserfingerprint'].nunique() == 1:
            continue
        pre_fingerprint = ""
        for idx, row in cur_group.iterrows():
            if pre_fingerprint == "":
                pre_fingerprint = row['browserfingerprint']
                pre_row = row
                continue
            for feature in feature_list:
                if feature not in row:
                    continue
                if pre_row[feature] != row[feature]:
                    maps[feature]['browserid'].append(row[browserid])
                    maps[feature]['clientid'].append(row['clientid'])
                    maps[feature]['IP'].append(row['IP'])
                    maps[feature]["from"].append(pre_row[feature])
                    maps[feature]['to'].append(row[feature])
                    maps[feature]['fromtime'].append(pre_row['time'])
                    maps[feature]['totime'].append(row['time'])
                    maps[feature]['browser'].append(row['browser'])
                    maps[feature]['os'].append(get_os_from_agent(row['agent']))
            pre_row = row
            # why previously we dont have this update
            pre_fingerprint = row['browserfingerprint']
    db = Database('filteredchanges{}'.format(browserid))
    for feature in feature_list:
        print (feature)
        try:
            df = pd.DataFrame.from_dict(maps[feature])
            db.export_sql(df, '{}changes'.format(feature))
            print ('success')
        except:
            print (len(maps[feature]['from']), len(maps[feature]['to']), len(maps[feature]['fromtime']), len(maps[feature]['totime']))
    return maps

def get_change_strs(str1, str2, sep = '_'):
    """
    the two strs put in this function is separated by _
    if it's separated by ' ', trans them before this function
    or use the sep param
    return the diff of str1 to str2 and str2 to str1
    """
    str1 = str(str1)
    str2 = str(str2)
    if str1 == None:
        str1 = ""
    if str2 == None:
        str2 = ""
    words_1 = set(str1.split(sep))
    words_2 = set(str2.split(sep))
    return words_1 - words_2, words_2 - words_1

