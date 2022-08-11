
#**********************************************************************************************************************
#
# Written by: DS
# Project Title: A Geospatial Analysis of Conflict in Afghanistan
# Project Goal: Determine the spatial distribution of high concentrations of conflict in Afghanistan
# Project File: Univariate & Multivariate Linear Regression 
#
#**********************************************************************************************************************
###### CURRENTLY USING

sns.lmplot(data=pdf, x='events', y='casualties')
results = sp.linregress(pdf['events'], pdf['casualties'])
results.rvalue
results.rvalue**2
results.pvalue

sns.lmplot(data=regions2, x='events', y='casualties')
results = sp.linregress(regions2['events'], regions2['casualties'])
results.rvalue
results.rvalue**2
results.pvalue





#**********************************************************************************************************************
####### NOT CURRENTLY USING;

sns.lmplot(data=pdf, x='distance_highway', y='events')
results = sp.linregress(pdf['distance_highway'], pdf['events'])

results.rvalue
results.rvalue**2
results.pvalue

# Create residual plots;
# Add in data from World Bank province dashboard;

sns.lmplot(data=rates_df, x='road_distance', y='distance')
sp.linregress(rates_df['road_distance'], rates_df['distance'])


# RUN MAIN FIRST
provincial_df2 = provincial_df2[0:34]

rates_df = rates_df.merge(provincial_df2, left_on='adm_1', right_on='Province')
del(rates_df['Province'])

# MULTIPLE LINEAR REGRESSION;

from sklearn.linear_model import LinearRegression

# create linear regression object
mlr = LinearRegression()

# fit linear regression
mlr.fit(rates_df[['poverty_rate', 'unemployment', 'literacy', 'pop_farming', 'pop_electrical_grid']], rates_df['cas_rate'])

print(mlr.intercept_)
print(mlr.coef_)
# R squared;
print(mlr.score(rates_df[['poverty_rate', 'unemployment', 'literacy', 'pop_farming', 'pop_electrical_grid']], rates_df['cas_rate']))

#.sort_values(['best'], ascending=False)
casdf = df.groupby(['year', 'adm_1'], as_index=False)['best'].sum()
casdf2 = casdf.groupby(['adm_1'], as_index=False)['best'].mean()

X = pdf[['distance_capital', 'distance_highway', 'pop_density_km2', 'area_km2', 'agricultural_land_km2', 'poverty_rate', 'unemployment',
'pop_electrical_grid', 'literacy', 'pop_farming']]

X = df[['month', 'day', 'distance']]

y = df['road_distance']
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()
est.summary()





