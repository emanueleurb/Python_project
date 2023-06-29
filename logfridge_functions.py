# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:55:58 2023

@author: Jana & Emanuele the greatest coder ever

logfridge_functions
"""

import numpy as np
import pandas as pd 
import scipy as sc
import matplotlib as plt
import os

from datetime import datetime

import matplotlib.pyplot as plt


file_path_0 = "Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\FRDGELOG_PROJECT"
file_path_maxigauge = file_path_0 + "\LOG_MAXIGAUGE"
file_path_temperature = file_path_0 + "\LOG_TEMPERATURE"

path_params = {}
path_params['file_path_0'] = file_path_0
path_params['file_path_maxigauge'] = file_path_maxigauge
path_params['file_path_temperature'] = file_path_temperature


def find_mK(folder_warm, path_params, warm_time):
    
    mK_threshold_reached = None
    indexes_CH6 = None
    log_name = "CH6 T" 
    headers_name =  ["date", "time", "value"]  
    file_path_0 = path_params['file_path_0']
    file_path_temperature = path_params['file_path_temperature']        
    file_path = file_path_temperature
    folders = os.listdir(file_path)
    start_folder = folders.index(folder_warm) 
    folders = folders[start_folder:]    
    
    for mK_index, folder_at_mK in enumerate(folders):
        file_name = file_path + "\\" + folder_at_mK + "\\" + log_name + " "   + folder_at_mK + '.log'  
        if len(folder_at_mK)<9:
            try:
                df_CH6 = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
                indexes_CH6 = np.where(np.logical_and(df_CH6["value"]<0.03, df_CH6["time"]>warm_time))
                if len(indexes_CH6[0])>1:
                    mK_threshold_reached = (indexes_CH6[0][0], folder_at_mK, mK_index, df_CH6["time"][indexes_CH6[0][0]])
                    print(f" Find_threshold at:", df_CH6["value"][indexes_CH6[0][0]], "the", folder_at_mK )
                    break                                 
            except:
                print(f"Find_mK_File in folder", folder_at_mK, " not found, skip it")
    return mK_threshold_reached, mK_index, folder_at_mK, indexes_CH6, df_CH6


def find_flow(mK_index, folder_warm):
    log_name = "Flowmeter" 
    headers_name =  ["date", "time", "value"] 
    file_path = file_path_maxigauge
    folders = os.listdir(file_path)
    start_folder = folders.index(folder_warm)
    folders = folders[start_folder:] 
    delta_folder = 0
    while delta_folder <= mK_index:
        file_name = file_path + "\\" + folders[mK_index-delta_folder] + "\\" + log_name + " "   + folders[mK_index-delta_folder] + '.log'  #+ folder +
        print(file_name)
        if len(folders[mK_index-delta_folder])<9:
            try:
                df_flow = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
                indexes_flow = np.where(df_flow["value"]>1)
                flow_data = df_flow["value"]
                if len(indexes_flow[0])>1:
                    flow_threshold_reached = (indexes_flow[0][0], folders[mK_index-delta_folder], df_flow["time"][indexes_flow[0][0]])
                    break
                else:
                    delta_folder = delta_folder + 1
            except:
                print(f"Find_flow_File in folder", folders[mK_index-delta_folder], " not found, skip it")
    
    m = mK_index - delta_folder
    Folders_group_1 = folders[mK_index-delta_folder:mK_index+1]
    
    return delta_folder, flow_threshold_reached, m, Folders_group_1, flow_data


def find_T_condensation(delta_folder, mK_index, flow_threshold_reached):
    k=0
    log_name = "CH6 T" 
    headers_name =  ["date", "time", "value"] 
    file_path = file_path_temperature
    folders = os.listdir(file_path)
    while k <= delta_folder:        
        file_name = file_path + "\\" + folders[mK_index-delta_folder+k] + "\\" + log_name + " "   + folders[mK_index-delta_folder+k] + '.log'  #+ folder +
        if len(folders[mK_index-delta_folder+k])<9:
            try:
                df_CH6_1 = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
                indexes_CH6_1 = np.where(df_CH6_1["time"]>flow_threshold_reached[2])
                if len(indexes_CH6_1[0])>1:
                    First_temperature_find = indexes_CH6_1[0][0]
                    temp_0 = df_CH6_1["value"][indexes_CH6_1[0][0]]            
                    break
                else:
                    k = k + 1
            except:
                print(f"Find_T_condensation_File in folder", folders[mK_index-delta_folder+k], " not found, skip it")   
                k = k + 1
    return First_temperature_find, temp_0, indexes_CH6_1


def condensation_data_analysis(Folders_group_1, m, mK_index, delta_folder, indexes_CH6_1, indexes_CH6):
    log_name = "CH6 T" 
    headers_name =  ["date", "time", "value"] 
    file_path = file_path_temperature
    for folder in Folders_group_1:
        file_name = file_path + "\\" + folder + "\\" + log_name + " "   + folder + '.log'  #+ folder +
        if m == mK_index - delta_folder:
            try:
                df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
                Temperature = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,2]
                time = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,1]
                date_time = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,[0,1]] 
                m = m+1 
            except: 
                  print(f"Condensation_data_analysis_File in folder", folder, " not found, skip it")                    
        elif m > mK_index-delta_folder and m < mK_index:
            try:
                df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
                Temperature = Temperature.append(df_CH6_T_and_t.iloc[:,2])
                time = time.append(df_CH6_T_and_t.iloc[:,1])
                date_time = date_time.append(df_CH6_T_and_t.iloc[:,[0,1]])
                m = m+1
            except:
                print(f"Condensation_data_analysis_File in folder", folder, " not found, skip it") 
        elif m == mK_index:
            try:
                df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
                Temperature = Temperature.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,2])
                time = time.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,1])
                date_time = date_time.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,[0,1]])
                m = m+1
            except:
                print(f"Condensation_data_analysis_File in folder", folder, " not found, skip it") 
        else:
            break
    return Temperature, time, date_time


def find_next_cooldown(mK_index, folder_at_mK):
    log_name = "CH6 T" 
    headers_name =  ["date", "time", "value"]  
    file_path_0 = path_params['file_path_0']
    file_path_temperature = path_params['file_path_temperature']        
    file_path = file_path_temperature
    folders = os.listdir(file_path)
    start_folder = folders.index(folder_at_mK) #index of folder from previous cooldown
    folders = folders[start_folder:]    
    warm_threshold_reached = None
    warm_time = None
    for warm_index, folder_warm in enumerate(folders):
        file_name = file_path + "\\" + folder_warm + "\\" + log_name + " "   + folder_warm + '.log'  #+ folder +
        if len(folder_warm)<9:
            try:
                df_CH6_warm = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
                indexes_CH6_warm = np.where(df_CH6_warm["value"]>100)
                if len(indexes_CH6_warm[0])>1:
                    warm_threshold_reached = (indexes_CH6_warm[0][0], folder_warm, warm_index, df_CH6_warm["time"][indexes_CH6_warm[0][0]])   
                    warm_time = warm_threshold_reached[3]                
                    break                                 
            except:
                print(f"Find_next_cooldown_File in folder", folder_warm, " not found, skip it")
    return warm_threshold_reached, warm_index, folder_warm, indexes_CH6_warm, warm_time
