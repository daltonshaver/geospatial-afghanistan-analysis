
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Point Pattern Analysis
#
#**********************************************************************************************************************
###### CURRENTLY USING

# Afghanistan's Ring Road;
roads_main = roadsmap1.loc[(roadsmap1.onme == "NH0101") | (roadsmap1.onme == "NH0102") | (roadsmap1.onme == "NH0103")
                           | (roadsmap1.onme == "NH0104")  | (roadsmap1.onme == "NH65")
                           | (roadsmap1.onme == "NH93") | (roadsmap1.onme == "NH09") | (roadsmap1.onme == "NH12")
                           | (roadsmap1.onme == "NH17") | (roadsmap1.onme == "NH08") | (roadsmap1.onme == "NH49")
                           | (roadsmap1.onme == "NH53") | (roadsmap1.onme == "NH89") | (roadsmap1.onme == "NH87")
                           | (roadsmap1.onme == "NH37") | (roadsmap1.onme == "NH15") | (roadsmap1.onme == "NH97")
                           | (roadsmap1.onme == "NH63")]




# Determining best epsilon value k-distance graph;
neighbors = NearestNeighbors(n_neighbors=20)
neighbors_fit = neighbors.fit(df[["longitude", "latitude"]])
distances, indices = neighbors_fit.kneighbors(df[["longitude", "latitude"]])
distances = np.sort(distances, axis=0) # Sort values and plot
distances = distances[:,1]
plt.plot(distances)
plt.xlim([31600, 31700])
plt.show()

# DBSCAN Clustering Model Setup;
clusterer = DBSCAN(eps = 0.2, min_samples = 550) # (eps = 0.15, min=600)
clusterer.fit(df[["longitude", "latitude"]])
df['cluster'] = clusterer.fit_predict(df[["longitude", "latitude"]])
labels = pd.Series(clusterer.labels_, index=df.index)
noise = df.loc[labels==-1, ['longitude', 'latitude']] # Points not a part of a cluster (noise);

# DBSCAN Clustering Model Plot;
f, ax5 = plt.subplots(1, figsize=(12, 12))
regions1.plot(color='lightyellow', ax=ax5, edgecolor='black', linewidth=0.25)
ax5.scatter(noise['longitude'], noise['latitude'], color='sandybrown', s=2) # Plot noise;
roads_main.plot(ax=ax5, color='black', linewidth=1.1)
ax5.scatter(df.loc[df.index.difference(noise.index), 'longitude'], \
            df.loc[df.index.difference(noise.index), 'latitude'], \
            c='darkred', linewidth=0)
ax5.set_title("Figure 4: DBSCAN Model of Conflict Events", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")


df['longitude'] = df['longitude'].astype(np.float16)
df['latitude'] = df['latitude'].astype(np.float16)


# Silhouette Score (-1 to 1, 1 shows the clusters are well apart and clearly distinguished);
clustering_labels = clusterer.fit_predict(df[["longitude", "latitude"]])
metrics.silhouette_score(df[["longitude", "latitude"]], clustering_labels)

#**********************************************************************************************************************
####### DENSITY;


# Kernel Density Estimation Plot;
f, ax3 = plt.subplots(1, figsize=(12, 12))
regions1.plot(color='lightgray', ax=ax3, edgecolor='dimgray')
sns.kdeplot(data = df, x="longitude", y="latitude", cmap="viridis_r", shade=True, alpha=0.55)

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



# Overlay mapping with matplotlib;
xy = np.vstack([df.longitude, df.latitude])
z = gaussian_kde(xy)(xy)
plt.hist(z, bins=20, edgecolor='black')

# General Overlay;
fig, ax1 = plt.subplots(sharex=True, sharey = True)
roads_main.plot(ax=ax1, color='red', edgecolor='red')
#bigrivers = rivers.loc[rivers.CLASS == 1]
#bigrivers.plot(ax=ax1, edgecolor='blue')
regions1.plot(ax=ax1, color='grey', edgecolor='black')
plt.scatter(df.longitude, df.latitude, c=z, s=10)
fig.set_figheight(10)
fig.set_figwidth(10)
plt.show()


#**********************************************************************************************************************
####### NOT CURRENTLY USING;




# Sub df testing for DBSCAN clustering;
lbls = pd.Series(clusterer.labels_, index=sub_df.index)

f, ax5 = plt.subplots(1, figsize=(12, 12))
regions1.plot(color='bisque', ax=ax5)
ax5.scatter(sub_df['longitude'], sub_df['latitude'], s=0.75)
# Subset points that are not part of any cluster (noise)
noise = sub_df.loc[lbls==-1, ['longitude', 'latitude']]
# Plot noise in grey
ax5.scatter(noise['longitude'], noise['latitude'], color='gray', s=0.85, linewidth=0)
# Plot all points that are not noise in red
# NOTE how this is done through some fancy indexing, where
#      we take the index of all points (tw) and substract from
#      it the index of those that are noise
ax5.scatter(sub_df.loc[sub_df.index.difference(noise.index), 'longitude'], \
           sub_df.loc[sub_df.index.difference(noise.index), 'latitude'], \
          c='darkslategrey', linewidth=0)
# Display the figure
plt.show()


# Casualties by cluster;
cluster_cas = df.groupby(['cluster'], as_index=False)['best'].sum()
cluster_events = df.cluster.value_counts()
cluster_df = cluster_cas
cluster_df['events'] = cluster_events









