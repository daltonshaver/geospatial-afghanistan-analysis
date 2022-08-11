
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Global/Local Spatial Autocorrelation Analysis
#
#**********************************************************************************************************************
###### CURRENTLY USING


#**********************************************************************************************************************
# Global Spatial Autocorrelation of Districts;

# Attaching aggregated counts of casualties and events per district to regions2.df;
cas_counts = df.groupby(['adm_2'], as_index = False)['best'].sum()
event_counts = df['adm_2'].value_counts().to_frame()
event_counts['district'] = event_counts.index
regions2 = regions2.merge(cas_counts, left_on = 'NAME_2', right_on = 'adm_2', how = 'outer')
regions2 = regions2.merge(event_counts, left_on = 'NAME_2', right_on = 'district', how = 'outer')
del(regions2['adm_2_x'])
del(regions2['district'])
regions2 = regions2.rename(columns={'adm_2_y': 'events', 'best': 'casualties'})
regions2['casualties'] = regions2['casualties'].fillna(0)
regions2['events'] = regions2['events'].fillna(0)

## Base Quantiles Plot of Conflict Events;
f, ax = plt.subplots(1, figsize=(12, 12))
regions2.plot(column='events', 
        cmap='YlOrRd',                  #YlOrRd, Reds
        scheme='quantiles',
        k=5, 
        edgecolor='black', 
        linewidth=0.25, 
        alpha=0.80, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax
       )
plt.title("Figure 1: Conflict Events Quantiles", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Spatial Weights;
w_rook = Rook.from_dataframe(regions2)
w_rook.neighbors
w_rook.histogram # Shows the most frequent k value;
w_rook.pct_nonzero # Percent non-zero cells in the n × n weights;

w_queen = Queen.from_dataframe(regions2)
w_queen.histogram
w_queen.pct_nonzero
w_queen.weights

# Spatial-lag of Conflict Events;
w = weights.Queen.from_dataframe(regions2) # Generate W Spatial weight matrix (Can use KNN, Rook, or Queen);
w.transform = 'R' # Row-standardization: Number of events divided by sum of weights (Queen);
regions2['events_lag'] = weights.spatial_lag.lag_spatial(w, regions2['events'])

# Spatial-lag Quantiles Plot of Conflict Events;
f, ax2 = plt.subplots(1, figsize=(12, 12))
regions2.plot(column='events_lag', 
        cmap='YlOrRd', 
        scheme='quantiles',
        k=5,                    # Experiment with k values;
        edgecolor='black', 
        linewidth=0.25, 
        alpha=0.80, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax2
       )
ax2.set_title("Figure 2: Spatially Lagged Conflict Events", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Moran's I Statistic;
regions2['events_std'] = (regions2['events'] - regions2['events'].mean()) # Standardized events;
regions2['events_lag_std'] = (regions2['events_lag'] - regions2['events_lag'].mean()) # Standardized lag of events;
moran = esda.moran.Moran(regions2['events'], w)
moran.I # Moran's I Statistic (Slope of regression line);
moran.p_sim # p-value generated from simulations;

# Moran Plot;
f, ax = plt.subplots(1, figsize=(12, 8))
sns.regplot(x='events_std', y='events_lag_std', 
                ci=None, data=regions2, scatter_kws={'color':'dimgray'}, line_kws={'color':'darkred'})
ax.axvline(0, c='k', alpha=0.5)
ax.axhline(0, c='k', alpha=0.5)
ax.set_title('Figure 7: Moran Plot of Conflict Events', fontsize=14)
plt.xlabel("Standardized Events")
plt.ylabel("Standardized Events Spatial Lag")
#plot_moran(moran);


# Local Spatial Autocorrelation of Districts;
loc_moran = esda.moran.Moran_Local(regions2['events'], w)
loc_moran.Is # Moran's I Statistics (Shows positive or negative local autocorrelation), Length = 328;
loc_moran.p_sim
loc_moran.q #1 HH, 2 LH, 3 LL, 4 HL;
pd.value_counts(loc_moran.q) # 61 districts that show a high concentration (HH) of conflict;
(loc_moran.p_sim < 0.05).sum() # 64 districts are statistically significant;
loc_moran.permutations # 999 permutations;

# Local Spatial-lagged Quantiles Plot of Conflict Events;
regions2['local_lag'] = loc_moran.Is

f, ax = plt.subplots(1, figsize=(12, 12))
regions2.plot(column='local_lag', 
        cmap='YlOrRd', 
        scheme='quantiles',
        k=5,                    
        edgecolor='black', 
        linewidth=0.25, 
        alpha=0.80, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax
       )
ax.set_title("Figure 3: Local Moran's I Coefficient Map", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
     



# Local Moran Quadrant Map;
f, ax = plt.subplots(1, figsize=(12, 12))
esdaplot.lisa_cluster(loc_moran, regions2, p=1, ax=ax, legend_kwds={"loc": 'upper left'}, alpha=0.90);
ax.set_title("Figure 5: Local Moran Quandrant Map", fontsize=14)


# Local Moran Statistically Signficant Quadrant Map;
f, ax = plt.subplots(1, figsize=(12, 12))
esdaplot.lisa_cluster(loc_moran, regions2, p=0.05, ax=ax, legend_kwds={"loc": 'upper left'}, alpha=0.90);
ax.set_title("Figure 6: Local Moran Statistically Signficant Quandrant Map", fontsize=14)

# Percentage of districts considered to be in a spatial cluster;
(loc_moran.p_sim < 0.05).sum() * 100 / len(loc_moran.p_sim)


#**********************************************************************************************************************
####### NOT CURRENTLY USING;

# Local Significance Level Map;
labels = pd.Series(1 * (loc_moran.p_sim < 0.05), # Assign 1 if significant, 0 if not;
                   index=regions2.index).map({1: 'Significant', 0: 'Non-Significant'})
regions2['significance_level'] = labels

f, ax = plt.subplots(1, figsize=(12, 12))
regions2.plot(column='significance_level', 
        cmap='YlOrRd', 
        categorical=True,
        k=2,                           
        edgecolor='black', 
        linewidth=0.25, 
        alpha=0.85, 
        legend=True,
        ax=ax
       )
ax.set_title("Local Moran Significance Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Spatial-lag of Conflict Events;
w = weights.Queen.from_dataframe(regions2) # Generate W Spatial weight matrix (Can use KNN, Rook, or Queen);
w.transform = 'R' # Row-standardization: Number of events divided by sum of weights (Queen);
regions2['events_lag'] = weights.spatial_lag.lag_spatial(w, regions2['events'])

# Global Spatial Autocorrelation of Provinces;
regions1 = regions1.merge(pdf, left_on = 'NAME_1', right_on = 'province')
del(regions1['province'])
del(regions1['capital'])
del(regions1['region'])

# Local Moran Plot;
f, ax = plt.subplots(1, figsize=(12, 12))
f, ax = moran_scatterplot(loc_moran, p=0.05)
ax.axvline(0, c='k', alpha=0.5)
ax.axhline(0, c='k', alpha=0.5)
ax.set_title('Figure 7: Local Moran Plot of Conflict Events', fontsize=14)
plt.xlabel("Standardized Events")
plt.ylabel("Standardized Events Spatial Lag")
#plot_moran(moran);


# Moran Plot;                                       ?????????????????????????????? Bivariate?
f, ax = plt.subplots(1, figsize=(12, 8))
sns.regplot(x='events_std', y='local_lag', 
                ci=None, data=regions2, scatter_kws={'color':'dimgray'}, line_kws={'color':'darkred'})
ax.axvline(0, c='k', alpha=0.5)
ax.axhline(0, c='k', alpha=0.5)
ax.set_title('Figure 7: Moran Plot of Conflict Events', fontsize=14)
plt.xlabel("Standardized Events")
plt.ylabel("Standardized Events Spatial Lag")
#plot_moran(moran);

results = sp.linregress(regions2['events_std'], regions2['events_lag_std'])
results.rvalue
results.rvalue**2
results.pvalue
results.slope


# Base Quantiles Plot of Conflict Events;
f, ax = plt.subplots(1, figsize=(12, 12))
regions1.plot(column='events', 
        cmap='viridis', 
        scheme='quantiles',
        k=5, 
        edgecolor='white', 
        linewidth=0., 
        alpha=0.75, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax
       )
plt.title("Casualty Events Quantiles")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Spatial-lag of Conflict Events;
w = weights.KNN.from_dataframe(regions1, k=8) # Generate W Spatial weight matrix;
w.transform = 'R' # Row-standardization;
regions1['events_lag'] = weights.spatial_lag.lag_spatial(w, regions1['events'])

#w_queen = weights.contiguity.Queen.from_dataframe(regions2['events'])


# Spatial-lag Quantiles Plot of Conflict Events;
f, ax = plt.subplots(1, figsize=(12, 12))
regions1.plot(column='events_lag', 
        cmap='viridis', 
        scheme='quantiles',
        k=5, 
        edgecolor='white', 
        linewidth=0., 
        alpha=0.75, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax2
       )
ax2.set_title("Casualty Events - Spatial Lag")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Moran's I Statistic;
regions1['events_std'] = (regions1['events'] - regions1['events'].mean()) # Standardized events;
regions1['events_lag_std'] = (regions1['events_lag'] - regions1['events_lag'].mean()) # Standardized lag of events;
moran = esda.moran.Moran(regions1['events'], w)
moran.I # Moran's I Statistic (Slope of regression line);
moran.p_sim # p-value generated from simulations;

# Moran Plot;
f, ax = plt.subplots(1, figsize=(12, 12))
sns.regplot(x='events_std', y='events_lag_std', 
                ci=None, data=regions1, line_kws={'color':'r'})
ax.axvline(0, c='k', alpha=0.5)
ax.axhline(0, c='k', alpha=0.5)
ax.set_title('Moran Plot - Events')
plt.show()


# Overlay mapping of Hilmand province;
hilmand = regions1.loc[regions1.NAME_1 == "Hilmand"]
hilmand_events = df.loc[df.adm_1 == "Hilmand"]

xy = np.vstack([hilmand_events.longitude, hilmand_events.latitude])
z = gaussian_kde(xy)(xy)
fig, ax1 = plt.subplots(sharex=True, sharey = True)
plt.plot(64.3692, 31.5831,'ro') # Hilmand capital - Lashkargah;
hilmand.plot(ax=ax1, color='grey', edgecolor='black')
plt.scatter(hilmand_events.longitude, hilmand_events.latitude, c=z, s=10)
fig.set_figheight(10)
fig.set_figwidth(10)
plt.show()

f, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
# Make the axes accessible with single indexing
axs = axs.flatten()
       


