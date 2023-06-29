#the greatest code ever

#author Jana, Emanuele the greatest coder ever

"""
TBD:
   - open also conflicted files
   - 1 or 2 plot
   - a function for the for loop
   - add something that delate folder that cannot be found
   - some statistics (evaluate time difference for different condensations)
   
    
   
 """   


import numpy as np
import pandas as pd 
import scipy as sc
import matplotlib as plt
import os
import logfridge_functions as fn
from datetime import datetime

import matplotlib.pyplot as plt


file_path_0 = "Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\FRDGELOG_PROJECT"
#file_path_0 = "Z:\Lab\Bluefors\BlackFriedge_YL_backup\TUD1001003\Y"
file_path_maxigauge = file_path_0 + "\LOG_MAXIGAUGE"
#file_path_maxigauge = file_path_0 + "\log_maxigauge"
file_path_temperature = file_path_0 + "\LOG_TEMPERATURE"
#file_path_temperature = file_path_0 + "\log_Temperature" + "\log-data\192.168.1.206"

path_params = {}
path_params['file_path_0'] = file_path_0
path_params['file_path_maxigauge'] = file_path_maxigauge
path_params['file_path_temperature'] = file_path_temperature


folder_warm = '22-01-05'
warm_time = "00:00:00"

Cond_date = []
Cond_time = []
        
while True:
    try:
        mK_threshold_reached, mK_index, folder_at_mK, indexes_CH6, df_CH6 = fn.find_mK(folder_warm, path_params, warm_time)
        
        delta_folder, flow_threshold_reached, m, Folders_group_1, flow_data = fn.find_flow(mK_index, folder_warm)
        
        First_temperature_find, temp_0, indexes_CH6_1 = fn.find_T_condensation(delta_folder, mK_index, flow_threshold_reached)    
        
        Temperature, time, date_time = fn.condensation_data_analysis(Folders_group_1, m, mK_index, delta_folder, indexes_CH6_1, indexes_CH6)
        
        
        
        #Plotting        
        date_time = date_time.reset_index(drop=True) 
        time = time.reset_index(drop=True)        
        # not optimized way of evaluating the delta time for the condensation
        D_1 = date_time["date"] + " " + date_time["time"]
        D_1_0 = D_1[0]
        D_1_last = D_1.iloc[-1]
        start_time = datetime.strptime(D_1_0, "%d-%m-%y %H:%M:%S")
        last_time = datetime.strptime(D_1_last, "%d-%m-%y %H:%M:%S")
        delta = last_time - start_time
        hours = delta.total_seconds()/3600                
        dt = delta.total_seconds()/len(time)/3600
        new_time = np.linspace(0, delta.total_seconds()/3600, len(time))    
        # plotting the condensation curve
        fig, ax = plt.subplots(2)
        #fig.suptitle("Condensation time x")
        ax[0].plot(new_time, Temperature)
        ax[0].set_title("Condensation time" + " " + folder_at_mK, y=1.05)
        ax[0].set_ylabel('T (K) linear')
        ax[1].semilogy(new_time, Temperature)
        ax[1].set_ylabel('T (K) semilog')
        ax[1].set_xlabel("time (h)")
        #Save the plot
        plot_file_name = os.path.join("Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\Plots", "Condensation time " + folder_at_mK + ".png")
        plt.savefig(plot_file_name)
        plt.close()
        
        Cond_date.append(folder_at_mK)
        Cond_time.append(hours)
        

        
        warm_threshold_reached, warm_index, folder_warm, indexes_CH6_warm, warm_time = fn.find_next_cooldown(mK_index, folder_at_mK)
    except:
        break
    
    
    
fig2, ax2 = plt.subplots()              
ax2.plot(Cond_date, Cond_time, "o")
ax2.set_xlabel("Condensation date")
ax2.set_ylabel("Condensation time (h)")
ax2.set_title("Condensation time statistics (Black_fridge)")
plot2_file_name = os.path.join("Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\Plots\Condensations statistics", "Condensation statistics.png")
plt.savefig(plot2_file_name)
plt.close()































# def find_mK(folder_warm, path_params, warm_time):
#     # log_name = "CH6 T" 
#     # headers_name =  ["date", "time", "value"] 
#     # file_path_0 = "Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\FRDGELOG_PROJECT"
#     # file_path_temperature = file_path_0 + "\LOG_TEMPERATURE"
#     mK_threshold_reached = None
#     indexes_CH6 = None
#     log_name = "CH6 T" 
#     headers_name =  ["date", "time", "value"]  
#     file_path_0 = path_params['file_path_0']
#     file_path_temperature = path_params['file_path_temperature']        
#     file_path = file_path_temperature
#     folders = os.listdir(file_path)
#     start_folder = folders.index(folder_warm) #index of folder when you knwo fridge is warm
#     #num_folder_left = len(folders) - start_folder
#     folders = folders[start_folder:]    
    
#     for mK_index, folder_at_mK in enumerate(folders):
#         file_name = file_path + "\\" + folder_at_mK + "\\" + log_name + " "   + folder_at_mK + '.log'  #+ folder +
#         if len(folder_at_mK)<9:
#             try:
#                 df_CH6 = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#                 indexes_CH6 = np.where(np.logical_and(df_CH6["value"]<0.01, df_CH6["time"]>warm_time))
#                 # indexes_CH6 = np.where(df_CH6["value"]<0.01)
#                 if len(indexes_CH6[0])>1:
#                     mK_threshold_reached = (indexes_CH6[0][0], folder_at_mK, mK_index, df_CH6["time"][indexes_CH6[0][0]])                   
#                     break                                 
#             except:
#                 print(f"File in folder", folder_at_mK, " not found, skip it")
#     return mK_threshold_reached, mK_index, folder_at_mK, indexes_CH6




# def find_mK(folder_warm, path_params):
#     # log_name = "CH6 T" 
#     # headers_name =  ["date", "time", "value"] 
#     # file_path_0 = "Z:\People\Emanuele\AAA_MY_STUFFS\COURSES\PYTHON\FRDGELOG_PROJECT"
#     # file_path_temperature = file_path_0 + "\LOG_TEMPERATURE"
    
#     log_name = "CH6 T" 
#     headers_name =  ["date", "time", "value"]  
#     file_path_0 = path_params['file_path_0']
#     file_path_temperature = path_params['file_path_temperature']        
#     file_path = file_path_temperature
#     folders = os.listdir(file_path)
#     start_folder = folders.index(folder_warm) #index of folder when you knwo fridge is warm
#     #num_folder_left = len(folders) - start_folder
#     folders = folders[start_folder:]    
    
#     for mK_index, folder_at_mK in enumerate(folders):
#         file_name = file_path + "\\" + folder_at_mK + "\\" + log_name + " "   + folder_at_mK + '.log'  #+ folder +
#         if len(folder_at_mK)<9:
#             try:
#                 df_CH6 = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#                 indexes_CH6 = np.where(df_CH6["value"]<0.01)
#                 if len(indexes_CH6[0])>1:
#                     mK_threshold_reached = (indexes_CH6[0][0], folder_at_mK, mK_index, df_CH6["time"][indexes_CH6[0][0]])                   
#                     break                                 
#             except:
#                 print(f"File in folder", folder_at_mK, " not found, skip it")
#     return mK_threshold_reached, mK_index, folder_at_mK, indexes_CH6, df_CH6


# folder_warm = '22-01-05'
# mK_threshold_reached, mK_index, folder_at_mK, indexes_CH6, df_CH6 = find_mK(folder_warm, path_params)



#Flowmeter
# def find_flow(mK_index):
#     log_name = "Flowmeter" 
#     headers_name =  ["date", "time", "value"] 
#     file_path = file_path_maxigauge
#     folders = os.listdir(file_path)
#     delta_folder = 0
#     while delta_folder <= mK_index:
#         file_name = file_path + "\\" + folders[mK_index-delta_folder] + "\\" + log_name + " "   + folders[mK_index-delta_folder] + '.log'  #+ folder +
#         if len(folders[mK_index-delta_folder])<9:
#             try:
#                 df_flow = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#                 indexes_flow = np.where(df_flow["value"]>1)
#                 if len(indexes_flow[0])>1:
#                     flow_threshold_reached = (indexes_flow[0][0], folders[mK_index-delta_folder], df_flow["time"][indexes_flow[0][0]])
#                     break
#                 else:
#                     delta_folder = delta_folder + 1
#             except:
#                 print(f"File in folder", folder, " not found, skip it")
    
#     m = mK_index - delta_folder
#     Folders_group_1 = folders[mK_index-delta_folder:mK_index+1]
    
#     return delta_folder, flow_threshold_reached, m, Folders_group_1

    



#find first temperature corresponding to the time where the flow treshold has been reached 
#create also a set of folder that start from the one where 10 mk has been reached
# def find_T_condensation(delta_folder, mK_index):
#     k=0
#     log_name = "CH6 T" 
#     headers_name =  ["date", "time", "value"] 
#     file_path = file_path_temperature
#     folders = os.listdir(file_path)
#     while k <= delta_folder:        
#         file_name = file_path + "\\" + folders[mK_index-delta_folder+k] + "\\" + log_name + " "   + folders[mK_index-delta_folder+k] + '.log'  #+ folder +
#         if len(folders[mK_index-delta_folder+k])<9:
#             try:
#                 df_CH6_1 = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#                 indexes_CH6_1 = np.where(df_CH6_1["time"]>flow_threshold_reached[2])
#                 if len(indexes_CH6_1[0])>1:
#                     First_temperature_find = indexes_CH6_1[0][0]
#                     temp_0 = df_CH6_1["value"][indexes_CH6_1[0][0]]            
#                     break
#                 else:
#                     k = k + 1
#             except:
#                 print(f"File in folder", folders[mK_index-delta_folder+k], " not found, skip it")      
#     return First_temperature_find, temp_0, indexes_CH6_1


                                              

# takes the meaningful folders for the condensation, create two series files with 
# Temperature and time from the starting of the condensation(flow>1) to the end (T<10mK)
# m = mK_index - delta_folder
# Folders_group_1 = folders[mK_index-delta_folder:mK_index+1]
# def condensation_data_analysis(Folders_group_1, m, mK_index, delta_folder):
#     log_name = "CH6 T" 
#     headers_name =  ["date", "time", "value"] 
#     file_path = file_path_temperature
#     for folder in Folders_group_1:
#         file_name = file_path + "\\" + folder + "\\" + log_name + " "   + folder + '.log'  #+ folder +
#         if m == mK_index - delta_folder:
#             df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
#             Temperature = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,2]
#             time = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,1]
#             date_time = df_CH6_T_and_t.iloc[indexes_CH6_1[0][0]:,[0,1]] 
#             m = m+1                       
#         elif m > mK_index-delta_folder and m < mK_index:
#             df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
#             Temperature = Temperature.append(df_CH6_T_and_t.iloc[:,2])
#             time = time.append(df_CH6_T_and_t.iloc[:,1])
#             date_time = date_time.append(df_CH6_T_and_t.iloc[:,[0,1]])
#             m = m+1
#         elif m == mK_index:
#             df_CH6_T_and_t = pd.read_csv(file_name, delimiter=",",  names=headers_name,)
#             Temperature = Temperature.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,2])
#             time = time.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,1])
#             date_time = date_time.append(df_CH6_T_and_t.iloc[:indexes_CH6[0][0]+1,[0,1]])
#             m = m+1
#         else:
#             break
#     return Temperature, time, date_time


#
#for t, line in enumerate(time) :    
#     time[t] = datetime.strptime(line, "%H:%M:%S")
#
#

# plt.plot(time, Temperature)



# find the next cooldown
# def find_next_cooldown(mK_index):
#     log_name = "CH6 T" 
#     headers_name =  ["date", "time", "value"]  
#     file_path_0 = path_params['file_path_0']
#     file_path_temperature = path_params['file_path_temperature']        
#     file_path = file_path_temperature
#     folders = os.listdir(file_path)
#     start_folder = folders.index(folder_at_mK) #index of folder from previous cooldown
#     folders = folders[start_folder:]    
    
#     for warm_index, folder_warm in enumerate(folders):
#         file_name = file_path + "\\" + folder_warm + "\\" + log_name + " "   + folder_warm + '.log'  #+ folder +
#         if len(folder_warm)<9:
#             try:
#                 df_CH6_warm = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#                 indexes_CH6_warm = np.where(df_CH6_warm["value"]>100)
#                 if len(indexes_CH6_warm[0])>1:
#                     warm_threshold_reached = (indexes_CH6_warm[0][0], folder_warm, warm_index, df_CH6_warm["time"][indexes_CH6_warm[0][0]])   
#                     warm_time = warm_threshold_reached[3]                
#                     break                                 
#             except:
#                 print(f"File in folder", folder_warm, " not found, skip it")
#     return warm_threshold_reached, warm_index, folder_warm, indexes_CH6_warm, warm_time













#for mK_index, folder in enumerate(folders):
#    file_name = file_path + "\\" + folder + "\\" + log_name + " "   + folder + '.log'  #+ folder +
#    if len(folder)<9:
#        try:
#            df_CH6_warm = pd.read_csv(file_name, delimiter=",",  names=headers_name,) 
#            indexes_CH6_warm = np.where(df_CH6_warm["value"]>50)
#            if len(indexes_CH6_warm[0])>1:
#                mK_treshold_reached = (indexes_CH6[0][0], folder, mK_index, df_CH6["time"][indexes_CH6[0][0]])
#                break                                 
#        except:
#            print(f"File in folder", folder, " not found, skip it")








#date_time_str = date_time["date"].to_string()
#
#date_time_str_0 = date_time_str[1]
#
#
#        
# 
#
#
#
#
##plot temperature
#Temp_list=df_CH6_1.groupby(axis=1)
#
#
#
#
#
#
#s=First_temperature_find           
#Temperature = [temp_0]
#Temperature.append(df_CH6_1[s+1])
#
#
#
#
##evaluate how much time from the condensation start to reach <10mK
#
#datetime_mk_treshold_reached_str = mK_treshold_reached[1] + " " + mK_treshold_reached[3]
#datetime_flow_threshold_reached_str = flow_threshold_reached[1] + " " + flow_threshold_reached[2]
#datetime_mk_treshold_reached_str = "20"+datetime_mk_treshold_reached_str
#
#datetime_mk_treshold_reached_obj = datetime.strptime(datetime_mk_treshold_reached_str, '%y-%m-%d %H:%M:%S')
#
#
#df_CH6_T_and_t["datetime"] = pd.to_datetime(df_CH6_T_and_t["date"] + " " + df_CH6_T_and_t["time"], format = "%d")
#
#
#
#end = datetime.now()
