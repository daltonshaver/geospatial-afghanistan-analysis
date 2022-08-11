
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Descriptive Statistics File 
#
#**********************************************************************************************************************
###### CURRENTLY USING

# Histogram of Nearest Provincial Capital distance;
f, ax = plt.subplots(1, figsize=(10, 8))
plt.hist(df.distance, bins=25, color='sandybrown', edgecolor='black')
plt.xlabel("Kilometers")
plt.ylabel("Frequency")
plt.title("Figure 8: Distance From Nearest Provincial Capital", fontsize=14)
plt.grid()

# Histogram of Nearest National Highway distance;
f, ax = plt.subplots(1, figsize=(10, 8))
plt.hist(df.road_distance, bins=25, color='darkred', edgecolor='black')
plt.xlabel("Kilometers")
plt.ylabel("Frequency")
plt.title("Figure 9: Distance From Nearest National Highway", fontsize=14)
plt.grid()


# Bar Chart of Events by Year;
year_count_events = df.year.value_counts(ascending=True)
x_axis = np.arange(len(year_count_events))

f, ax = plt.subplots(1, figsize=(10, 8))
plt.bar(x_axis, year_count_events, color = 'palegoldenrod', edgecolor = 'black')
plt.xticks(x_axis, year_count_events.index)
plt.ylabel('Frequency')
plt.xlabel('Year')
plt.title("Figure 10: Bar Chart of Conflict Events by Year", fontsize=14)
plt.grid(axis='y')
plt.show()

# Multiple Bar Chart of Casualties and Event Counts by Province;
cas_count = df.groupby(['adm_1'], as_index = False)['best'].sum()
cas_count['relative'] = round((cas_count['best'] / cas_count['best'].sum()), 3)

event_count = pd.crosstab(index=df['adm_1'], columns='count')
event_count['relative'] = round((event_count['count'] / event_count['count'].sum()), 3)

# Set two different axes, one offset of the other;
x_axis = []
for i in range(34):
    x_axis.append(i * 3) 
x_axis2 = []
for i in range(34):
    x_axis2.append(i * 3 + 1.2) 

f, ax = plt.subplots(1, figsize=(12, 7))
plt.bar(x_axis, event_count['relative'], label = 'Events', color = 'sandybrown', width = 1.3)
plt.bar(x_axis2, cas_count['relative'], label = 'Casualties', color = 'darkred', width = 1.3)
plt.xticks(x_axis, cas_count.adm_1, rotation = 90, fontsize = 12)
plt.ylabel('Relative Frequency')
plt.xlabel('Provinces')
plt.title("Figure 11: Multiple Bar Chart of Casualties and Events by Province", fontsize=14)
plt.grid(axis='y')
plt.legend()
plt.show()









#**********************************************************************************************************************
####### NOT CURRENTLY USING;

# Histogram and density plot of latitude;
kde_lat = gaussian_kde(df.latitude)(df.latitude)
plt.hist(kde_lat, bins=30, color='orange', edgecolor='black')
fig, ax1 = plt.subplots()
sns.kdeplot(data=df, x="latitude", ax=ax1, bw_adjust=2)
ax1.set_xlim((df["latitude"].min(), df["latitude"].max()))
ax2 = ax1.twinx()
sns.histplot(data=df, x="latitude", discrete=False, ax=ax2)

# Histogram and density plot of longitude;
kde_lon = gaussian_kde(df.longitude)(df.longitude)
plt.hist(kde_lon, bins=30, color='orange', edgecolor='black')
fig, ax1 = plt.subplots()
sns.kdeplot(data=df, x="longitude", ax=ax1, bw_adjust=2)
ax1.set_xlim((df["longitude"].min(), df["longitude"].max()))
ax2 = ax1.twinx()
sns.histplot(data=df, x="longitude", discrete=False, ax=ax2)

# Bivariate Density Plot;
xy = np.vstack([df.longitude, df.latitude])
kde_points = gaussian_kde(xy)(xy)
plt.hist(kde_points, bins=20, edgecolor='black')
sns.kdeplot(data=df, x="longitude", y="latitude", fill=True, levels=100, cmap="mako")

# Empirical Cumulative Distribution Plot for Road Distance;
df2 = df.loc[df.road_distance < 100]
sns.ecdfplot(data=df2, x="road_distance", hue="region")

# Empirical Cumulative Distribution Plot for capital Distance;
df2 = df.loc[df.distance < 125]
sns.ecdfplot(data=df2, x="distance", hue="region")

# Boxplots;
columns = [df.distance, df.road_distance]

f, ax = plt.subplots(1, figsize=(12, 8))
ax.boxplot(columns, vert=0, meanline=True, showmeans=True)
plt.xticks([1, 2], ['Provincial Capital', 'National Highway'])
plt.xlabel("Kilometers")
plt.ylabel("Frequency")
colors = ['#0000FF', '#00FF00',
          '#FFFF00', '#FF00FF']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
plt.show()




