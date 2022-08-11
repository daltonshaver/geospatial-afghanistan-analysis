
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Initialization/Cleaning File
#
#**********************************************************************************************************************

# Package Installation
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from shapely import wkt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import math
from math import radians
import sys

pd.set_option('display.max_columns', None)

#**********************************************************************************************************************
# Formatting & Cleaning Dataset (Startup)
#**********************************************************************************************************************

# Reading in datasets/shapefiles
raw_df = pd.read_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\conflict_data_afg.csv')
provincial_df = pd.read_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\provincial_data_afg.csv')
regions1 = gpd.read_file(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\afg_shapefiles\AFG_adm1.shp')
regions2 = gpd.read_file(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\afg_shapefiles\AFG_adm2.shp')
# airports = gpd.read_file(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\afg_shapefiles\hotosm_afg_airports_points.dbf')

# Subsetting dataset
df = raw_df[['id', 'year', 'type_of_violence', 'side_a', 'side_b', 'source_article', 'source_date', 'where_prec', 
             'adm_1', 'adm_2', 'latitude', 'longitude', 'event_clarity', 'date_prec', 'deaths_a', 'deaths_b', 
             'deaths_civilians', 'deaths_unknown', 'best', 'high', 'low', 'date_start']]

del(raw_df)
df = df.drop(df.index[0])

# Convert columns to numerical
num_cols = ['year', 'latitude', 'longitude']
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce', axis=1)
del(num_cols)

# Only include conflict events after 2000
df = df.loc[df['year'] >= 2001]

# Creating ~ year, month, & day ~ date variables
df['date_start'] = df['date_start'].str.replace(' 00:00:00.000', '')
df['month'] = df['date_start'].str[5:7]
df['day'] = df['date_start'].str[8:10]
df = df.drop(['date_start'], axis=1)

# Dropping 'province' and 'district' from region columns
df['adm_1'] = df['adm_1'].str.replace(' province', '')
df['adm_2'] = df['adm_2'].str.replace(' district', '')

# Resetting the index
df = df.reset_index(drop=True)

provincial_df['longitude'] = provincial_df['longitude'].str.replace('\xa0', '')
provincial_df['longitude'] = provincial_df['longitude'].apply(pd.to_numeric)

#**********************************************************************************************************************
# Filled in missing values in adm_1 & adm_2 columns
#**********************************************************************************************************************

# Created an array to fill in missing values by conditionals;
df["latitude"] = pd.to_numeric(df["latitude"])
df["longitude"] = pd.to_numeric(df["longitude"])
arr = np.array((df.latitude, df.longitude, df.adm_1, df.adm_2)).T
arr[:,0] = arr[:,0].astype(float)
arr[:,1] = arr[:,1].astype(float)

# Created list of unique coordinates that were not assigned adm_1 & adm_2 values;
nan_df = df.loc[df.adm_1.isnull() == True]
replace_arr = np.array((nan_df.latitude.unique(), nan_df.longitude.unique())).T

# Assigned districts to array based on latitude and longitude;
arr[:,2][(arr[:,0] == 31.480806) & (arr[:,1] == 64.875154)] = "Kandahar"
arr[:,3][(arr[:,0] == 31.480806) & (arr[:,1] == 64.875154)] = "Maywand"
#1
arr[:,2][(arr[:,0] == 33.394734) & (arr[:,1] == 69.549621)] = "Khost"
arr[:,3][(arr[:,0] == 33.394734) & (arr[:,1] == 69.549621)] = "Nadir Shah Kot"

arr[:,2][(arr[:,0] == 31.689623) & (arr[:,1] == 68.051427)] = "Zabul"
arr[:,3][(arr[:,0] == 31.689623) & (arr[:,1] == 68.051427)] = "Shamulzayi"

arr[:,2][(arr[:,0] == 31.830848) & (arr[:,1] == 64.817112)] = "Kandahar"
arr[:,3][(arr[:,0] == 31.830848) & (arr[:,1] == 64.817112)] = "Ghorak"

arr[:,2][(arr[:,0] == 32.437563) & (arr[:,1] == 65.972462)] = "Kandahar"
arr[:,3][(arr[:,0] == 32.437563) & (arr[:,1] == 65.972462)] = "Shah Wali Kot"

arr[:,2][(arr[:,0] == 32.313372) & (arr[:,1] == 66.418528)] = "Kandahar"
arr[:,3][(arr[:,0] == 32.313372) & (arr[:,1] == 66.418528)] = "Shah Wali Kot"
#6
arr[:,2][(arr[:,0] == 33) & (arr[:,1] == 65)] = "Hilmand"
arr[:,3][(arr[:,0] == 33) & (arr[:,1] == 65)] = "Baghran"

arr[:,2][(arr[:,0] == 34.011698) & (arr[:,1] == 69.073448)] = "Logar"
arr[:,3][(arr[:,0] == 34.011698) & (arr[:,1] == 69.073448)] = "Puli Alam"

arr[:,2][(arr[:,0] == 36.791111) & (arr[:,1] == 66.460112)] = "Jawzjan"
arr[:,3][(arr[:,0] == 36.791111) & (arr[:,1] == 66.460112)] = "Fayzabad (Jawzjan)"

arr[:,2][(arr[:,0] == 36.223248) & (arr[:,1] == 68.120033)] = "Samangan"
arr[:,3][(arr[:,0] == 36.223248) & (arr[:,1] == 68.120033)] = "Aybak"
#10
arr[:,2][(arr[:,0] == 34.015449) & (arr[:,1] == 62.739639)] = "Hirat"
arr[:,3][(arr[:,0] == 34.015449) & (arr[:,1] == 62.739639)] = "Adraskan"

arr[:,2][(arr[:,0] == 33.65232) & (arr[:,1] == 69.539312)] = "Paktya"
arr[:,3][(arr[:,0] == 33.65232) & (arr[:,1] == 69.539312)] = "Jani Khel (Paktya)"

arr[:,2][(arr[:,0] == 34.499112) & (arr[:,1] == 69.886222)] = "Laghman"
arr[:,3][(arr[:,0] == 34.499112) & (arr[:,1] == 69.886222)] = "Qarghayi"
#13
arr[:,2][(arr[:,0] == 35.366384) & (arr[:,1] == 71.365915)] = "Nuristan"
arr[:,3][(arr[:,0] == 35.366384) & (arr[:,1] == 71.365915)] = "Kamdesh"

arr[:,2][(arr[:,0] == 34.537709) & (arr[:,1] == 70.234252)] = "Laghman"
arr[:,3][(arr[:,0] == 34.537709) & (arr[:,1] == 70.234252)] = "Qarghayi"

arr[:,2][(arr[:,0] == 36.251363) & (arr[:,1] == 64.457196)] = "Faryab"
arr[:,3][(arr[:,0] == 36.251363) & (arr[:,1] == 64.457196)] = "Shirin Tagab"

arr[:,2][(arr[:,0] == 32.058438) & (arr[:,1] == 62.416585)] = "Nimroz"
arr[:,3][(arr[:,0] == 32.058438) & (arr[:,1] == 62.416585)] = "Chakhansur"

arr[:,2][(arr[:,0] == 33.426118) & (arr[:,1] == 62.288398)] = "Hirat"
arr[:,3][(arr[:,0] == 33.426118) & (arr[:,1] == 62.288398)] = "Shindand"
#18
arr[:,2][(arr[:,0] == 36.447093) & (arr[:,1] == 65.819185)] = "Jawzjan"
arr[:,3][(arr[:,0] == 36.447093) & (arr[:,1] == 65.819185)] = "Shibirghan"

arr[:,2][(arr[:,0] == 37.093774) & (arr[:,1] == 69.270837)] = "Kunduz"
arr[:,3][(arr[:,0] == 37.093774) & (arr[:,1] == 69.270837)] = "Archi"

arr[:,2][(arr[:,0] == 32.130515) & (arr[:,1] == 63.557985)] = "Nimroz"
arr[:,3][(arr[:,0] == 32.130515) & (arr[:,1] == 63.557985)] = "Khash Rod"

arr[:,2][(arr[:,0] == 32.547043) & (arr[:,1] == 63.218387)] = "Farah"
arr[:,3][(arr[:,0] == 32.547043) & (arr[:,1] == 63.218387)] = "Bakwa"


nan_df2 = df.loc[df.adm_2.isnull() == True]
nan_df2 = nan_df2.drop_duplicates(subset = ['longitude'])
#replace_arr2 = np.array((nan_df2.latitude, nan_df2.longitude)).T
convert_df = nan_df2[['adm_2', 'latitude', 'longitude']]
convert_df = convert_df.reset_index(drop=True)
complete_arr = convert_df.to_numpy()


for i in range(147):
    if (i == 33 | i == 118):
        continue
    point = Point(complete_arr[i][2], complete_arr[i][1])
    
    for j in range(len(regions2)):
        if ((regions2[j:j+1].contains(point)).any() == True):
            complete_arr[i][0] = regions2.NAME_2[j:j+1].item()

complete_arr[33][0] = "Tani"
complete_arr[118][0] = "Shirin Tagab"

test_df = df

for i in range(len(test_df)):
    for j in range(147):
        if ((test_df.latitude[i] == complete_arr[j][1]) & (test_df.longitude[i] == complete_arr[j][2])):
            test_df.adm_2[i] = complete_arr[j][0]


nan_df3 = test_df.loc[test_df.adm_2.isnull() == True]
nan_df3 = nan_df3.drop_duplicates(subset = ['longitude'])
convert_df = nan_df3[['adm_2', 'latitude', 'longitude']]
convert_df = convert_df.reset_index(drop=True)
complete_arr = convert_df.to_numpy()

for i in range(5):
    if (i == 33 | i == 118):
        continue
    point = Point(complete_arr[i][2], complete_arr[i][1])
    
    for j in range(len(regions2)):
        if ((regions2[j:j+1].contains(point)).any() == True):
            complete_arr[i][0] = regions2.NAME_2[j:j+1].item()

for i in range(len(test_df)):
    for j in range(5):
        if ((test_df.latitude[i] == complete_arr[j][1]) & (test_df.longitude[i] == complete_arr[j][2])):
            test_df.adm_2[i] = complete_arr[j][0]

df = test_df

#**********************************************************************************************************************

split_df = df[['adm_2', 'latitude', 'longitude']]
df_arr = split_df.to_numpy()

for i in range(len(df)):
    #if (i == 33 | i == 118):
        #continue
    point = Point(df_arr[i][2], df_arr[i][1])
    
    for j in range(len(regions2)):
        if ((regions2[j:j+1].contains(point)).any() == True):
            df_arr[i][0] = regions2.NAME_2[j:j+1].item()

district_df = pd.DataFrame(df_arr)
district_df.to_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\district_df.csv', index=False)    

df['adm_2'] = district_df['adm_2']
df.to_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\clean_conflict_data_afg.csv', index=False)    


















#**********************************************************************************************************************



# Replaced adm_1 column with newly created (filled in) column from temp array;
df.adm_1 = arr[:,2].tolist()
# Confirm no missing values in adm_1 column;
list = df.adm_1.unique().tolist()

df = df.merge(provincial_df, left_on=df.adm_1, right_on=provincial_df.Province)
del df["key_0"]

# Exporting clean CSV file;
df.to_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\clean_conflict_data_afg.csv', index=False)    




