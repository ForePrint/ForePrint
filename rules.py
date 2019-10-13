import MySQLdb
import pandas
from database import Database
from fingerprint import *
import logging
import hashlib
from tqdm import *
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import json
from ast import literal_eval
import csv
import time
import concurrent.futures
import multiprocessing
from functools import partial
from itertools import repeat
from pathlib import Path
import threading
from utils import calculate_rule_hash

class Rules():
    """
    Rules class contains all the operations related to rules.
    """

    def __init__(self):
        '''
        Initialize some values for analysis.
        '''

        self.rules = []
        self.fingerprints = self.df_whole[0:1]

        self.__rules = []
        self.__rule_store = {}
        self.__known = {}
        self.__prediction = {}
        self.__result = {}
        self.__featureDiff = []
        self.__predicts = 0
        self.__predicts_before = 0
        self.__predicts_after = 0

        self.__match = 0
        self.__unmatch = 0
        self.__total = 0
        self.__fail = 0   

        MAX_NUMBER = 99999

        #self.__per = 0

        self.match_list = []
        #self.time1 = 0
        #self.time2 = 0
        #self.time3 = 0

        self.__rule_store['SelfPrediction'] = MAX_NUMBER
        self.db = Database('ForePrint')
        self.df_whole = self.db.load_data(table_name='ForePrint')
        # self.df_rule = self.db.load_data(table_name='rule_table')
        # self.df_predicts = db.load_data(table_name='predicted_table')
        # self.df_predicts = self.df_whole[0:100000]

        self._value_lock = threading.Lock()

    def have_match(self, df, index, options):
        """
        Find if there is a prediction for the fingerprint. 
        Also calculate the probablity based on the rules.
        """
        idx_browserid = df.iloc[0]['browserid']
        feature_hash = ''
        for feature in fingerprint_change_feature_list:
            feature_hash = feature_hash + str(df.iloc[0][feature])
        hashvalue = hashlib.md5(feature_hash.encode('utf-8')).hexdigest()
        if hashvalue in self.__prediction.keys():
            temp_list = get_options_list(options, self.__prediction[hashvalue])
            if idx_browserid in temp_list:
                self.__match = self.__match + 1
                self.match_list.append(df.iloc[0]['counter'])
                #self.__per = self.__per + len(self.__prediction[hashvalue])
            else:
                #self.__per = self.__per + len(self.__prediction[hashvalue])
                self.__unmatch = self.__unmatch + 1
            #"""
            #Calculate the total number.
            #"""
            #match = 0
            #for i in self.__prediction[hashvalue]:
            #    if self.same_attribute(index, i[1]):
            #        match = 1
            #        break
 #               self.__per = self.__per + len(self.__prediction[hashvalue])
            #if match == 1:
            #    self.__match = self.__match + 1
            #    self.match_list.append(df.iloc[0]['counter'])
            #else:
            #    self.__unmatch = self.__unmatch + 1
            return True
        else:
            return False

    def get_options(self, options, option_list):
        """
        Get the first N options from the option_list
        """
        if len(option_list) < options:
            return [i[0] for i in option_list]
        else:
            temp_list = []
            for i in option_list:
                temp_list.append([i[0], self.__rule_store[i[1]]])
            sorted(temp_list, key = lambda x: x[1], reverse=True)
            result_list = []
            for i in temp_list[0:options]:
                result_list.append(i[0])
            return result_list


    def same_jsFonts_attribute(self, unknown_idx, known_idx):
        """
        Find jsFonts information between two fingerprint.
        """
        unknown_fp = self.df_whole.loc[unknown_idx]
        known_fp = self.df_whole.loc[known_idx]
        unknown_jsFonts = set(unknown_fp['jsFonts'].split('~'))
        known_jsFonts = set(known_fp['jsFonts'].split('~'))
        if unknown_jsFonts <= unknown_jsFonts or unknown_jsFonts >= known_jsFonts:
            return True
        else:
            return False;

    def add_predicts(self, index):
        # self.df_predicts = self.df_predicts.append(df.iloc[0])
        # self.__predicts_after = index
        self.__predicts = index


    def update_fail(self, idx):
        df_predicts = self.df_whole[:idx]
        browserid = df_predicts['browserid'].tolist()
        if self.df_whole.at[idx, 'browserid'] not in browserid:
            self.__fail = self.__fail + 1

    def make_prediction(self, df):
        self.df_predicts = self.df_predicts.append(df.iloc[0])
        feature_hash = ''
        for feature in fingerprint_change_feature_list:
            feature_hash = feature_hash + df.iloc[0][feature]
        hashvalue = hashlib.md5(feature_hash.encode('utf-8')).hexdigest()
        if hashvalue not in self.__prediction:
            self.__prediction[hashvalue] = [df.iloc[0]['browserid']]
        for rule in self.__rules:
            if rule == {}:
                continue
            flag = 1
            for key in rule.keys():
                if df.iloc[0][key] != rule[key][0]:
                    flag = 0
                    break
                elif df.iloc[0][key] == rule[key][0]:
                    df.iloc[0][key] = rule[key][1]
            if flag == 1:
                self.insert_prediction(self.calculate_hash(df), df.iloc[0]['browserid'])
            for key in rule.keys():
                df.iloc[0][key] = rule[key][0]

    def calculate_hash(self, df):
        """
        Calculate the hash value for the dataframe object.
        """
        feature_hash = ''
        for feature in fingerprint_change_feature_list:
            feature_hash = feature_hash + str(df.iloc[0][feature])
        hashvalue = hashlib.md5(feature_hash.encode('utf-8')).hexdigest()
        return hashvalue

    def insert_rule(self, rule_hash):
        """
        Insert the rule hash data into the rule hash database.
        """
        if rule_hash in self.__rule_store.keys():
            self.__rule_store[rule_hash] += 1
        else:
            self.__rule_store[rule_hash] = 1

    def update_rules(self, df):
        """
        Generate a rule based by finding the most recent fingerprint.
        """
        rule_dict = {}
        temp_string = ''
        idx_browserid = df.iloc[0]['browserid']
        if idx_browserid in self.__known.keys():
            index = self.__known[idx_browserid]
            df_before = self.df_whole.loc[[index]]
            df_after = df
            for feature in fingerprint_change_feature_list:
                temp_string = temp_string + ' feature: ' + str(feature)
                if df_after.iloc[0][feature] != df_before.iloc[0][feature]:
                    rule_dict[feature] = [df_before.iloc[0][feature], df_after.iloc[0][feature]]
            handle_fonts_plugins(rule_dict)
        self.__known[idx_browserid] = df.index[0]
        #print(self.__featureDiff)
        return rule_dict
    
    def handle_fonts_plugins(self, rule_dict):
        """
        Handle set type features. 
        In this case, handle fonts and plugins.
        """
        if 'jsFonts' not in rule_dict.keys() and 'Plugins' not in rule_dict.keys():
            return rule_dict
        else:
            if 'jsFonts' in rule_dict.keys():
                fonts_before = rule_dict['jsFonts'][0]
                fonts_after = rule_dict['jsFonts'][1]
                fonts_before_list = list(fonts_before.split(' '))
                fonts_after_list = list(fonts_after.split(' '))
                fonts_before_list,fonts_after_list = [i for i in fonts_before_list if i not in fonts_after_list],[j for j in fonts_after_list if j not in fonts_before_list]
                fonts_before_string = ' '.join(fonts_before_list)
                fonts_after_string = ' '.join(fonts_after_list)
                rule_dict['jsFonts'][0] = fonts_before_string
                rule_dict['jsFonts'][1] = fonts_after_string
            if 'Plugins' in rule_dict.keys():
                plugins_before = rule_dict['Plugins'][0]
                plugin_after = rule_dict['Plugins'][1]
                plugins_before_list = list(plugins_before.split('~'))
                plugins_after_list = list(plugins_after.split('~'))
                plugins_before_list,plugins_after_list = [i for i in plugins_before_list if i not in plugins_after_list],[j for j in plugins_after_list if j not in plugins_before_list]
                plugins_before_string = '~'.join(plugins_before_list)
                plugins_after_string = '~'.join(plugins_after_list)
                rule_dict['Plugins'][0] = plugins_before_string
                rule_dict['Plugins'][1] = plugins_after_string
            return rule_dict


    def update_result(self):
        """
        For calculating the Negative False.
        """
        self.__total = self.__total + 1

    def insert_prediction_with_rule(self, hashvalue, browserid, rule_dict):
        """
        Insert the predictions with rules to calculate the probablity.
        """
        temp_hash = calculate_rule_hash(rule_dict)
        if hashvalue in self.__prediction.keys():
            temp_list = [i[0] for i in self.__prediction[hashvalue]]
            # if browserid in temp_list:
            #     self.__match += 1
            if browserid not in temp_list:
                self.__prediction[hashvalue].append([browserid, temp_hash])
        else:
            self.__prediction[hashvalue] = [[browserid, temp_hash]]


    def update_prediction(self, rule_dict):
        """
        Update the predictions based on the rule.
        """
        predicts = self.__predicts
        predicts_before = self.__predicts_before
        df_new = self.df_predicts.loc[predicts_before:predicts]
        df_predicts = self.df_predicts.loc[:predicts]
        self.__predicts_before = predicts
        # for idx in df_new.index:
        #     self.insert_prediction(self.calculate_hash(df_new.loc[[idx]]), df_new.at[idx, 'browserid'])
        if rule_dict != {}:
            index = next((i for i, v in enumerate(self.__rules) if v[0] == rule_dict), None)
            if index == None:
                self.__rules.append([rule_dict, df_predicts.index[-1]])
                df_temp = df_predicts
            else:
                last_position = self.__rules[index][1]
                df_temp = df_predicts.loc[last_position:]
                df_predicts = df_temp
                self.__rules[index][1] = df_predicts.index[-1]
            for key in rule_dict.keys():
                df_temp = pd.merge(df_temp, df_predicts.loc[df_predicts[key] == rule_dict[key][0]])
            for idx in df_temp.index:
                feature_hash = ''
                for feature in fingerprint_change_feature_list:
                    if feature in rule_dict.keys():
                        feature_hash = feature_hash + rule_dict[feature][1]
                    else:
                        feature_hash = feature_hash + df_temp.at[idx, feature]
                hashvalue = hashlib.md5(feature_hash.encode('utf-8')).hexdigest()
                self.insert_prediction_with_rule(hashvalue, df_temp.at[idx, 'browserid'], rule_dict)

    def insert_prediction_without_rule(self, hashvalue, browserid, idx):
        """
        Insert the prediction into the prediction database.
        Used for no rule prediction.
        """
        #browserid_list = [i[0] for i in self.__prediction]
        #if hashvalue in self.__prediction.keys() and browserid in browserid_list:
        #    self.__prediction[hashvalue][browserid_list.index(browserid)] = idx
        #elif hashvalue in self.__prediction.keys() and browserid not in browserid_list:
        #    self.__prediction[hashvalue].append([browserid, idx])
        #else:
        #    self.__prediction[hashvalue] = [[browserid, idx]]
        if hashvalue in self.__prediction.keys():
            if [browserid, 'SelfPrediction']  not in self.__prediction[hashvalue]:
                self.__prediction[hashvalue].append([browserid, 'SelfPrediction'])
        else:
            self.__prediction[hashvalue] = [browserid, 'SelfPrediction']

    def get_result(self):
        """
        Get the result for the whole system.
        """
        for i in self.__featureDiff:
            print(i)
        file = open('foreprint_result.txt', 'a')
        file.write("precision is " + str(self.__match / self.__total) +
                   "\n recall is " + str(self.__per / self.__match) +  
                   "\n total match is " + str(self.__match) + 
                   "\n average match is " + str(self.__per / self.__total))
        file.close()

    def update_dataset(self, rule_dict):
        """
        update the dataset.
        """
        predicts = self.__predicts
        predicts_before = self.__predicts_before
        #df_new = self.df_predicts.loc[predicts_before:predicts]
        df_predicts = self.df_predicts.loc[:predicts]
        self.__predicts_before = predicts
        #start_time = time.time()
        # for idx in df_new.index:
        #     self.insert_prediction(self.calculate_hash(df_new.loc[[idx]]), df_new.at[idx, 'browserid'])
        if rule_dict != {}:
            index = next((i for i, v in enumerate(self.__rules) if v[0] == rule_dict), None)
            if index == None:
                self.__rules.append([rule_dict, df_predicts.index[-1]])
                df_temp = df_predicts
            else:
                last_position = self.__rules[index][1]
                df_temp = df_predicts.loc[last_position:]
                df_predicts = df_temp
                self.__rules[index][1] = df_predicts.index[-1]
            for key in rule_dict.keys():
                #if len(rule_dict.keys()) > 1:
                #    print('Multiple Rules')
                # feature_hash = ''
                for key in rule_dict.keys():
                    feature_hash = ''
                    for feature in fingerprint_change_feature_list:
                        if feature == key:
                            feature_hash = feature_hash + str(rule_dict[feature][1])
                        else:
                            feature_hash = feature_hash + str(df_temp.at[idx, feature])
                # for feature in fingerprint_change_feature_list:
                #     if feature in rule_dict.keys():
                #         feature_hash = feature_hash + rule_dict[feature][1]
                #     else:
                #         feature_hash = feature_hash + df_temp.at[idx, feature]
                        hashvalue = hashlib.md5(feature_hash.encode('utf-8')).hexdigest()
                        self.insert_prediction(hashvalue, df_temp.at[idx, 'browserid'], idx)
            #print(len(self.__prediction))
    
    def judge_rule(self, rule):
        """
        Judge if a rule is applicable for prediction.
        If the rule is more than 6 changes or has lied features, then return false.
        """
        if len(rule.keys()) > 6:
            return False
        if 'fp2_liedos' in rule.keys() or 'fp2_liedlanguages' in rule.keys() or 'fp2_liedresolution' in rule.keys() or 'fp2_liedbrowser' in rule.keys():
            return False
        return True

    def insert_fingerprint(self, idx):
        """
        Insert the fingerprint into the fingerprint data store
        """
        self.fingerprints.append(self.df_whole.loc[idx])

    def probablity_system(self, rule_dict, rule):
        """
        Not the probablity ranking for the rule data store.
        Calculating probablity for analysis.
        """
        temp_string = ''
        for value in rule.values():
            temp_string.append(value[0])
            temp_string.append(value[1])
        temp_hash = calculate_hash(temp_string)
        if temp_hash in rule_dict:
            rule_dict[temp_hash] += 1
        else:
            rule_dict[temp_hash] = 1

    def drop_predictions(self):
        """
        drop the predictions every 100K data.
        """
        for key in self._predictions.keys():
            if len(self._predictions[key]) == 1 and self.__rule[self._predictions[key][0]] < 3:
                   del self.__predictions[key]

    def is_browser_update(delta):
        return True if delta['browserversion'][1] > delta['browserversion'][0] else False

    def is_timezone_change(delta):
        return True if delta['timezone'][0] != delta['timezone'][1] else False

    def is_private_mode(delta):
        return True if delta['label'][0] != delta['label'][1] else False

    def is_zoom_in_out(delta):
        return True if delta['resolution'][0] != delta['resolution'][1] else False

    def is_language_change(delta):
        return True if delta['language'][0] != delta['language'][1] else False

    def is_cookie_enabled(delta):
        return True if delta['timezone'][0] != delta['timezone'][1] else False

    def is_local_storage(delta):
        return True if delta['localstorage'][0] != delta['localstorage'][1] else False

    def is_audio_change(delta):
        return True if delta['audio'][0] != delta['audio'][1] else False

    def is_colordepth_change(delta):
        return True if delta['fp2_colordepth'][0] != delta['fp2_colordepth'][1] else False

    def is_encoding_change(delta):
        return True if delta['encoding'][0] != delta['encoding'][1] else False

    def is_fonts_change(delta):
    """
    Detailed fonts change. Different fonts change means different software update.
    """
        return False

    def is_plugins_change(delta):
    """
    Detailed plugins change. Different plugins change means different software update.
    """
        return False

