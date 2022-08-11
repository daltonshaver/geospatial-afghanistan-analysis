
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Functions File
#
#**********************************************************************************************************************


# Casualty Rates and associated mean distances;
def rates(dataframe):
    # Finding frequencies of casualties and events per province;
    cas_per_province = dataframe.groupby(dataframe.adm_1, as_index=False).agg({'best':'sum'}).sort_values(['best'], ascending=False)
    events_per_province = dataframe.adm_1.value_counts().rename_axis('adm_1').reset_index(name='events')
    # Aggregated average road_distance by adm_1
    avg_road_distance = dataframe.groupby(dataframe.adm_1, as_index=False).agg({'road_distance':'mean'}).sort_values(['road_distance'], ascending=False)

    # Calculating rate of death (casualties/events) per province;
    rates = cas_per_province.merge(events_per_province, on='adm_1')
    rates['cas_rate'] = rates.best / rates.events
    rates = rates.sort_values(['cas_rate'], ascending=False)
    
    # Created subset of provincial dataset to merge with rates df;
    provincial_subdf = provincial_df[['province', 'capital', 'region']]
    # Calculating mean distance from nearest capital city;
    distance_per_capital = dataframe.groupby(dataframe.nearest_capital, as_index=False).agg({'distance':'mean'}).sort_values(['distance'], ascending=True)
    distance_per_capital = distance_per_capital.merge(provincial_subdf, left_on='nearest_capital', right_on='capital')
    del distance_per_capital['capital']
    
    # Merging distance dataset with rates dataset;
    rates = rates.merge(distance_per_capital, left_on='adm_1', right_on='province')
    rates = rates.merge(avg_road_distance, left_on='adm_1', right_on='adm_1')

    del rates['province']

    # Reordering columns of rates dataframe;
    global rates_df 
    rates_df = rates[['adm_1', 'nearest_capital', 'distance', 'best', 'events', 'cas_rate']]    
    rates_df = rates_df.merge(avg_road_distance, left_on='adm_1', right_on='adm_1')
    return rates

rates_df = rates_df.merge(provincial_df, left_on='adm_1', right_on='province')
rates_df = rates_df.merge(provincial_df2, left_on='adm_1', right_on='Province')

del rates_df['province']
del rates_df['Province']
del rates_df['capital']

rates_df.to_csv(r'C:\Users\Slaye\Documents\Analysis Projects\STAT_3120\Final_project\clean_provincial_data.csv')

#**********************************************************************************************************************

# K-Means Clustering Function
def cluster(dataframe):
    df_clustering = dataframe[['latitude', 'longitude', 'low']]
    # z-score normalization
    df_clustering_scaled = (df_clustering - df_clustering.mean())/df_clustering.std()
    km = KMeans(n_clusters=6, init='k-means++', max_iter=100)
    label = km.fit_predict(df_clustering_scaled)
    df_clustering['cluster'] = label #Appending cluster value onto df
    dataframe['cluster'] = label
    sns.lmplot(data=df_clustering, x='latitude', y='longitude', hue='cluster', fit_reg=False)

#**********************************************************************************************************************

# Statistical Analysis of profiles
def clusterval(dataframe):
    print(dataframe['cluster'].value_counts()) # Number of events
    print(dataframe.groupby(['cluster']).agg({'low':'sum'})) # Casualties per cluster
# Divide aggregate sums by frequency of clusters to get distribution of causalties

# Ignoring the two outlier clusters, we can determine if there is a higher concentration of causalties in the north, south, or east.

#**********************************************************************************************************************

# Function that loops through both provincial capitals and every event of the dataframe, 
# computes distance in km, and finally stores minimum value in a designated variable in the original dataframe;
def distance_calculator():
    provincial_dict = {}    #Created temporary dictionary to store distance per row of dataset;
    df['distance'] = 0
    df['distance'] = df['distance'].astype(float)
    df['nearest_capital'] = 0      #Created 'distance' and 'nearest_province' columns;
    
    # for loop - looping all rows of dataset;
    for a in range(31658):
            
        # for loop - looping provinces, calculating distance;
        for b in range(34):
            
            #Assigning lat and long values to x1, x2, y1, & y2  variables;
            lat1 = df['latitude'][a]
            lon1 = df['longitude'][a]
            lat2 = provincial_df['latitude'][b]
            lon2 = provincial_df['longitude'][b]
    
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])   #Converts degrees to radians;
            delta_lat = (lat2 - lat1)
            delta_lon = (lon2 - lon1)
           
            #Haversine Formula
            inner_fun = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2  
            outer_fun = 2 * math.asin(math.sqrt(inner_fun))
            
            R = 6371000 # Radius of earth in km. (3956 for miles. Determines return value units.);
            
            meters = R * outer_fun  #Output distance in meters;
            km = meters / 1000.0  #Output distance in kilometers;
            km = round(km, 3)
            
            provincial_dict[provincial_df['Capital'][b]] = km  #Storing calculated distance and associated province name in a temp dictionary;
            pass
        
        #Stores the minimum value of the calculated distances into the observation, as well as the associated province name;
        min_val = min(provincial_dict.values())        
        df['distance'][a] = min_val
        df['nearest_capital'][a] = min(provincial_dict, key=provincial_dict.get)
        
#**********************************************************************************************************************
        
# Calculates dot product of each line segment, then outputs the nearest 
# point on that given line to the conflict event's coordinates;        
def minimum_distance(pointx, pointy, x1, y1, x2, y2):
    A = pointx - x1
    B = pointy - y1
    C = x2 - x1
    D = y2 - y1
    
    # Dot product, u^T*v;
    dot_prod = (A * C) + (B * D) 
    len_sq = (C * C) + (D * D)
    
    if (len_sq != 0):
        param = dot_prod / len_sq
    if (param < 0):
        xx = x1
        yy = y1
    elif (param > 1):
        xx = x2
        yy = y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D
        
    dx = pointx - xx
    dy = pointy - yy
    # math.sqrt((dx * dx) + (dy * dy))
    return (xx, yy)

#**********************************************************************************************************************
# Create masterlist of linestrings;
masterlist = []

for row in roads.geometry:
    subdata = row.split(" ")
    masterlist.append(subdata)

min_val_list = []

def infrastructure_distance_calculator(stop):
    count = 0
    for a in range(0, stop):
        distance_from_road_list = []
        for row in range(0, len(masterlist)):
            temp_list = []
            for i,j in zip(masterlist[row][0::2], masterlist[row][1::2]):
                temp_list.append(i)
                temp_list.append(j)
                #print(temp_list)
                
                if (len(temp_list) < 4):
                    continue
                elif (len(temp_list) == 4):
                    #print(i, j, k, l)  
                    event_lat = df['latitude'][a]
                    event_lon = df['longitude'][a]
                    lat1 = float(temp_list[0])
                    lon1 = float(temp_list[1])
                    lat2 = float(temp_list[2])
                    lon2 = float(temp_list[3])
                    nearlon, nearlat = minimum_distance(event_lat, event_lon, lat1, lon1, lat2, lon2)
                    #print("Nearest point:", nearlon, nearlat)
                    
                    lat1 = nearlat
                    lon1 = nearlon
                    
                    event_lon, event_lat, lon1, lat1 = map(radians, [event_lon, event_lat, lon1, lat1])   #Converts degrees to radians;
                    delta_lat = (lat1 - event_lat)
                    delta_lon = (lon1 - event_lon)
                    
                    #Haversine Formula
                    inner_fun = math.sin(delta_lat / 2) ** 2 + math.cos(event_lat) * math.cos(lat1) * math.sin(delta_lon / 2) ** 2  
                    outer_fun = 2 * math.asin(math.sqrt(inner_fun))
                    
                    R = 6371000 # Radius of earth in km. (3956 for miles. Determines return value units.);
                    
                    meters = R * outer_fun  #Output distance in meters;
                    km = meters / 1000.0  #Output distance in kilometers;
                    km = round(km, 3)
                    #print(km)
                    distance_from_road_list.append(km)
                    count += 1
                    
                elif (len(temp_list) > 4):
                    del(temp_list[0:2])
                    #print(i, j, k, l)  
                    event_lat = df['latitude'][a]
                    event_lon = df['longitude'][a]
                    lat1 = float(temp_list[0])
                    lon1 = float(temp_list[1])
                    lat2 = float(temp_list[2])
                    lon2 = float(temp_list[3])
                    nearlon, nearlat = minimum_distance(event_lat, event_lon, lat1, lon1, lat2, lon2)
                    #print("Nearest point:", nearlon, nearlat)
                    
                    lat1 = nearlat
                    lon1 = nearlon
                    
                    event_lon, event_lat, lon1, lat1 = map(radians, [event_lon, event_lat, lon1, lat1])   #Converts degrees to radians;
                    delta_lat = (lat1 - event_lat)
                    delta_lon = (lon1 - event_lon)
                    
                    #Haversine Formula
                    inner_fun = math.sin(delta_lat / 2) ** 2 + math.cos(event_lat) * math.cos(lat1) * math.sin(delta_lon / 2) ** 2  
                    outer_fun = 2 * math.asin(math.sqrt(inner_fun))
                    
                    R = 6371000 # Radius of earth in km. (3956 for miles. Determines return value units.);
                    
                    meters = R * outer_fun  #Output distance in meters;
                    km = meters / 1000.0  #Output distance in kilometers;
                    km = round(km, 3)
                    #print(km)
                    distance_from_road_list.append(km)
                    count += 1
        
        min_val = min(distance_from_road_list)
        min_val_list.append(min_val)
        #print("Closest distance to major highway:", min_val)
    print(count)

#df['distance_road'] = min_val_list

#**********************************************************************************************************************
# OLD:
    
# Creates geo dataframe to overlay conflict points on shapefiles;
def to_geo_df(dataframe):
   latitude_list = dataframe['latitude'].to_list()
   latitude = [float(i) for i in latitude_list]
   longitude_list = dataframe['longitude'].to_list()
   longitude = [float(i) for i in longitude_list]
   # Creating a coordinate dataset
   dataframe['Coordinates'] = list(zip(dataframe.longitude, dataframe.latitude))
   dataframe['Coordinates'] = dataframe['Coordinates'].apply(Point)
   # Creating a GeoDataFrame for conflict coordinates using coordinate dataset;
   global geo_df
   geo_df = gpd.GeoDataFrame(dataframe, crs="EPSG:4326", geometry = dataframe['Coordinates'])                                           

conflict = geo_df.geometry













