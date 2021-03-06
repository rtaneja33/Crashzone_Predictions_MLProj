# -*- coding: utf-8 -*-
"""ML Project: Predicting Crashsite HotZones

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ffd3v7TODsmFMMDmm1_KuJih3s6_Dxgg
"""

# Commented out IPython magic to ensure Python compatibility.
## Final Project for CS 4774 
## Rohan Taneja, Noah Espiritu

## Insert common imports for clustering algorithms
import sklearn
assert sklearn.__version__ >= "0.20"
import numpy as np
import os

# stable output across runs
np.random.seed(42)
# To plot pretty figures
# %matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14) # plot formatting value taken from colab09 notebook
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

import pandas as pd 
#easier to work with dataframe vs array
data = pd.DataFrame(pd.read_csv("crash-samples.csv")) #(https://www.virginiaroads.org/datasets/virginia-crashes/data)

print(data.columns)

data.shape
data.head()

#removed features with nan
df = data.dropna(axis="columns")
df.shape

corr_matrix = df.corr()
corr_matrix["X"].sort_values(ascending=False)

corr_matrix["Y"].sort_values(ascending=False)

feature_freq = {}
for feature in data.columns:
  try:
    leading_attribute = data[feature].value_counts()
    leading_attribute_count = leading_attribute[0]
    leading_attribute_index = leading_attribute.index.tolist()[0]
    #print(data[feature].value_counts().index.tolist()[0])
    feature_freq[feature] = [leading_attribute_index, leading_attribute_count]
  except:
    ...
sorted_feature_freq = sorted(feature_freq.items(), key=lambda x: x[1][1], reverse = True)
print(sorted_feature_freq)
## LEADING VALUE COUNTS, TRY THESE 
### SCHOOL ZONE 3, DRY ROADWAY CONDITION, NON-ROAD, DAYLIGHT, REARENDS, NORTHERN VIRGINIA DISTRICT, DISTRACTED, YOUNG, SPEEDING, ALCOHOL RELATED, UNBELTED

categor_columns = df.select_dtypes(exclude=["number"]).columns
categor_columns.shape

numeric_columns = df._get_numeric_data().columns
numeric_columns.shape

df.head()

data.hist(bins=30, color='red',edgecolor='black', linewidth = 1.0, xlabelsize=8, ylabelsize=8,grid=False)
plt.tight_layout(rect=(0, 0, 1.2, 1.2))

from pandas.plotting import scatter_matrix

#scatter_matrix(df, figsize=(12, 8))

from six.moves import urllib
import matplotlib.image as mpimg
urllib.request.urlretrieve("https://www.mapsofworld.com/usa/states/virginia/maps/virginia-lat-long-map.jpg", "map.jpg")

virginia_img = mpimg.imread('map.jpg')

# Visualizing The Data Distribution

bounds = []
bounds.append(-83.71)
bounds.append(-75.29)
bounds.append(35.5)
bounds.append(40.1)


data.plot(kind="scatter", x="X", y="Y", figsize=(15,12),s=0.1)
plt.imshow(virginia_img, extent=bounds, alpha= 0.5)

crash_year_freq = data['Crash_Year']
crash_year_freq.describe()
plt.hist(crash_year_freq, bins=range(2013,2021))

crash_frequency = crash_year_freq.value_counts()
crash_frequency.head(10)

crash_road_freq = data['Route_Or_Street_Nm']
crash_road_frequency = crash_road_freq.value_counts()
crash_road_frequency.head(25)

crash_road_freq = data['FAC']
crash_road_frequency = crash_road_freq.value_counts()
crash_road_frequency.head(25)

district_freq = data['VDOT_District']
#district_freq = data['PLAN_DISTRICT']
districts = list(set(district_freq))
#districts.sort()
print("\n".join(districts))

data_by_district = data.groupby(['VDOT_District'])
bounds = []
bounds.append(-83.71)
bounds.append(-75.29)
bounds.append(35.5)
bounds.append(40.1)

print(data_by_district)
plt.figure(figsize=(15,12))
for name, district in data_by_district:
    plt.scatter(district['X'],district['Y'],s=0.1)
    #district.plot(kind="scatter", x="X", y="Y", figsize=(15,12),s=0.1)
#data_by_district.plot(kind="scatter", x="X", y="Y", figsize=(15,12),s=0.1)
plt.imshow(virginia_img, extent=bounds, alpha= 0.5)

district_frequency = district_freq.value_counts()
district_frequency.head(25)

#Data Pre-Processing

data_columns = ['X','Y','Crash_Year', 'Route_Or_Street_Nm', 'Carspeedlimit']
df_processed = df[data_columns]
category_columns = list([ 'Route_Or_Street_Nm'])
num_columns = ['X','Y','Crash_Year','Carspeedlimit']

def getDate(input_date):
    return (input_date[0:4], input_date[5:7], input_date[8:10]) #Year, Month, Day

print(getDate('2016-02-16T00:00:00.000Z'))

import matplotlib.pyplot as plt
import pandas
timeData = data['Crash_Dt'].value_counts().sort_index()

dateIndexes = [getDate(date) for date in data['Crash_Dt']]
dateData = pd.DataFrame()
dateData["Year"] = [i[0] for i in dateIndexes]
dateData["Month"] = [i[1] for i in dateIndexes]
dateData["Day"] = [i[2] for i in dateIndexes]

dateData['Year'].value_counts().sort_index().plot.bar()

dateData['Month'].value_counts().sort_index().plot.bar()

timeData.plot.hist(bins=12*8)
print(timeData[35])

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd 

num_pipeline = Pipeline([
                         ('imputer', SimpleImputer(strategy="median")),
                         ("scale", StandardScaler()),
                         ])

full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_columns),
        #("cat", OneHotEncoder(), category_columns), Using a OneHotEncoder on even just 1 feature made our runtime crash.
    ])
df_processed.head()
data_scaled = full_pipeline.fit_transform(df_processed)
print(data_scaled[[0]])
#df_scaled = pd.DataFrame(data_scaled,columns = df_processed.columns)

print(type(df))

def plot_data(X):
    plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2)

def plot_centroids(centroids, weights=None, circle_color='w', cross_color='k'):
    if weights is not None:
        centroids = centroids[weights > weights.max() / 10]
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='o', s=30, linewidths=8,
                color=circle_color, zorder=10, alpha=0.9)
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=50, linewidths=50,
                color=cross_color, zorder=11, alpha=1)

def plot_decision_boundaries(clusterer, X, resolution=1000, show_centroids=True,
                             show_xlabels=True, show_ylabels=True):
    mins = X.min(axis=0) - 0.1
    maxs = X.max(axis=0) + 0.1
    xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    Z = clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                cmap="Pastel2")
    plt.contour(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                linewidths=1, colors='k')
    plot_data(X)
    if show_centroids:
        plot_centroids(clusterer.cluster_centers_)

    if show_xlabels:
        plt.xlabel("$x_1$", fontsize=14)
    else:
        plt.tick_params(labelbottom=False)
    if show_ylabels:
        plt.ylabel("$x_2$", fontsize=14, rotation=0)
    else:
        plt.tick_params(labelleft=False)

print(data_scaled.shape)

## Experiment - Analyze clusters using alcohol-related feature and locations  
data_columns_alc = ['X','Y','Crash_Year', 'Route_Or_Street_Nm', 'Pedestrians_Killed']
df_alc = data.copy(deep=True)
df_alc["Alcohol_Notalcohol"].fillna("NOT ALCOHOL", inplace = True) 
df_alc.dropna(axis="columns")
print(df_alc.columns)
df_processed_alc = df_alc[df_alc['Alcohol_Notalcohol'] == "ALCOHOL"]
category_columns_alc = list([ 'Route_Or_Street_Nm'])
num_columns_alc = ['X','Y','Crash_Year','Carspeedlimit','Pedestrians_Killed']

num_pipeline_alc = Pipeline([
                         ('imputer', SimpleImputer(strategy="median")),
                         ("scale", StandardScaler()),
                         ])

full_pipeline_alc = ColumnTransformer([
        ("num", num_pipeline_alc, num_columns_alc),
        #("cat", OneHotEncoder(), category_columns), Using a OneHotEncoder on even just 1 feature made our runtime crash.
    ])
df_processed_alc.head()
data_scaled_alc = full_pipeline_alc.fit_transform(df_processed_alc)
print(data_scaled_alc[[0]])
#df_scaled = pd.DataFrame(data_scaled,columns = df_processed.columns)

print(data_scaled_alc.shape)

## Experiment - Analyze clusters using alcohol-related feature and locations  
from sklearn.cluster import KMeans
import numpy as np

k_alc = 10

kmeans_alc = KMeans(n_clusters=k_alc, random_state=42)
kmeans_alc.fit(data_scaled_alc)
plt.figure(figsize=(15, 12))

data_scaled_frame_alc = pd.DataFrame(data_scaled_alc)
print(data_scaled_frame_alc.columns)
data_scaled_frame_alc['cluster_id'] = (pd.DataFrame(kmeans_alc.labels_))
print(data_scaled_frame_alc.columns)


print(data_scaled_frame_alc.shape)

#data_scaled_frame_alc.head()

for i in range(k_alc):
    data_scaled_array_alc = data_scaled_frame_alc.loc[data_scaled_frame_alc['cluster_id'] == i].to_numpy()
    plt.scatter(data_scaled_array_alc[: , 0], data_scaled_array_alc[:, 1], s=0.6)

plot_centroids(kmeans_alc.cluster_centers_)

print(kmeans_alc.cluster_centers_)

plt.figure(figsize=(15, 12))
## VISUALIZATION OVER VIRGINIA CITIES
urllib.request.urlretrieve("https://www.bls.gov/regions/mid-atlantic/images/18768.png", "map2.jpg")

virginia_img2 = mpimg.imread('map.jpg')
plt.imshow(virginia_img2, extent=[-4.2,1.8,-2.6,2.5], alpha= 0.9, aspect =1)

kmeans_k10_alc = kmeans_alc

centroids_alc = kmeans_k10_alc.cluster_centers_
plt.scatter(centroids_alc[:, 0], centroids_alc[:, 1],
            marker='o', s=80, linewidths=8,
            color="k", zorder=10, alpha=0.9)
plt.scatter(centroids_alc[:, 0], centroids_alc[:, 1],
            marker='x', s=100, linewidths=20,
            color="r", zorder=11, alpha=1)
plt.title("Centroids for Alcohol-Related Vehicle Accidents")
print(kmeans_k10_alc.cluster_centers_)

kmeans_optimal_alc = [KMeans(n_clusters=i, random_state=42).fit(data_scaled_alc) for i in range(5,35, 5)]
inertias_optimal_alc = [clusters.inertia_ for clusters in kmeans_optimal_alc]
plt.figure(figsize=(8, 3.5))
plt.plot(range(5, 35, 5), inertias_optimal_alc, "bo-")
plt.xlabel("$k value$", fontsize=14)
plt.ylabel("inertia", fontsize=14)
plt.title("k value vs inertia for Clustering Virginia Crashes Data")
plt.show() # elbow at k=10

## NORMAL EXPERIMENT - Crash Dates/Locations/Speed Limits
from sklearn.cluster import KMeans
import numpy as np

k = 10

kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(data_scaled)
plt.figure(figsize=(15, 12))

data_scaled_frame = pd.DataFrame(data_scaled)
print(data_scaled_frame.columns)
data_scaled_frame['cluster_id'] = (pd.DataFrame(kmeans.labels_))
print(data_scaled_frame.columns)


print(data_scaled_frame.shape)

#data_scaled_frame.head()

for i in range(k):
    data_scaled_array = data_scaled_frame.loc[data_scaled_frame['cluster_id'] == i].to_numpy()
    plt.scatter(data_scaled_array[: , 0], data_scaled_array[:, 1], s=0.2)

plot_centroids(kmeans.cluster_centers_)

print(kmeans.cluster_centers_)

plt.figure(figsize=(15, 12))
## VISUALIZATION OVER VIRGINIA CITIES
urllib.request.urlretrieve("https://www.bls.gov/regions/mid-atlantic/images/18768.png", "map2.jpg")


virginia_img2 = mpimg.imread('map.jpg')
plt.imshow(virginia_img2, extent=[-4.2,1.8,-2.75,2.8], alpha= 0.5, aspect =1)

for i in range(k):
    data_scaled_array = data_scaled_frame.loc[data_scaled_frame['cluster_id'] == i].to_numpy()
    plt.scatter(data_scaled_array[: , 0], data_scaled_array[:, 1], s=0.2)
plt.legend(list(range(k)), markerscale=10)
plot_centroids(kmeans.cluster_centers_)

for i in range(k):
    data_scaled_array = data_scaled_frame.loc[data_scaled_frame['cluster_id'] == i].to_numpy()
    data_stats = pd.DataFrame()
    data_stats['Mean'] = data_scaled_array.mean(axis=0);
    data_stats['Standard Deviation'] = data_scaled_array.std(axis=0);
    #print(data_stats)
    stats = data_scaled_frame.loc[data_scaled_frame['cluster_id'] == i].describe()
    stats = stats.drop(['cluster_id'], axis=1)
    stats.columns = ['Longitude','Latitude','Year','Speed Limit (mph)']
    print(stats.to_latex())
    #data_stats.head(100)

### Find optimal k 

kmeans_optimal = [KMeans(n_clusters=i, random_state=42).fit(data_scaled) for i in range(5,35, 5)]
inertias_optimal = [clusters.inertia_ for clusters in kmeans_optimal]
plt.figure(figsize=(8, 3.5))
plt.plot(range(5, 35, 5), inertias_optimal, "bo-")
plt.xlabel("$k value$", fontsize=14)
plt.ylabel("inertia", fontsize=14)
plt.title("k value vs inertia for Clustering Virginia Crashes Data")
plt.show() ##CLEAR ELBOW AT k = 10

plt.figure(figsize=(15, 12))
## VISUALIZATION OVER VIRGINIA CITIES
urllib.request.urlretrieve("https://www.bls.gov/regions/mid-atlantic/images/18768.png", "map2.jpg")

virginia_img2 = mpimg.imread('map.jpg')
plt.imshow(virginia_img2, extent=[-4.2,1.8,-2.6,2.5], alpha= 0.9, aspect =1)

kmeans_k10 = kmeans_optimal[1]

centroids = kmeans_k10.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='o', s=80, linewidths=8,
            color="k", zorder=10, alpha=0.9)
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=100, linewidths=20,
            color="r", zorder=11, alpha=1)

print(kmeans_k10.cluster_centers_)

data_scaled
#These are the first two columns: X, Y

#X predictor
label_x = data_scaled[:,0]
label_y = data_scaled[:,1]

data_for_x_pred = data_scaled.copy()
#data_for_x_pred = np.delete(data_for_x_pred, 0, 0)
data_for_x_pred = np.delete(data_for_x_pred, 1, 1) #deletes y column
data_for_x_pred = data_for_x_pred[:,1:] #deletes column 

label_x.shape

from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge

X_train, X_test, y_train, y_test = train_test_split(data_for_x_pred, label_x,  test_size=0.1, random_state = 42)

reg = LinearRegression().fit(X_train, y_train)
reg.score(X_test, y_test)

regr = Ridge().fit(X_train, y_train)
regr.score(X_test, y_test)

from sklearn import linear_model
regrr = linear_model.SGDRegressor().fit(X_train, y_train)
regrr.score(X_test, y_test)

#For Poisson Regression, we need a series of discrete areas from which to sample frequencies
#To be able to generate a heatmap, I decided to split everything up into a uniform grid.
#It's not great, but I don't see a much better way to do it.
#from there, I'm rearranging the data to be in regards to time.

min_bounds = np.min(data[["X","Y"]], axis=0)
max_bounds = np.max(data[["X","Y"]], axis=0)
print(min_bounds)
print(max_bounds)
sampleResolution = 10

indexX = np.floor(((data["X"] - min_bounds[0])/(max_bounds[0]- min_bounds[0]))*sampleResolution)
indexY = np.floor(((data["Y"] - min_bounds[1])/(max_bounds[1]- min_bounds[1]))*sampleResolution)

data["GridSpaceCoordX"] = indexX
data["GridSpaceCoordY"] = indexY

split = [pd.DataFrame(y) for x, y in data.groupby(['GridSpaceCoordX','GridSpaceCoordY'], as_index=False)]
freqThreshold = 250

split = [a for a in split if len(a.index) > freqThreshold]
#plt.scatter(data["X"],data["Y"], c=color)
for i in split:
    plt.scatter(i["X"],i["Y"], s=0.05)

counts = pd.DataFrame([len(i.index) for i in split])
counts.sort_values(by=counts.columns[0], ascending=False).head()

print(pd.to_datetime(['2016-02-16T00:00:00.000Z']))
numeric_columns = df._get_numeric_data().columns
timeData = [i.astype({'Crash_Dt': 'datetime64[ns, UTC]'}).set_index('Crash_Dt')._get_numeric_data() for i in split]
print(timeData[0].dtypes)
timeData[0]['2018'].head()
#timeData[0].plot()
test_data = timeData[0].groupby(by=[timeData[0].index.year])
testX = test_data.mean()
testY = test_data.count()

#OK. Turns out the model I wanted to use was part of a dev build that hasn't been released yet. I tried following their instructions on how to install it, but 
#I can't seem to install it.

#from sklearn.linear_model import PoissonRegressor
#testModel = PoissonRegressor(alpha=1/df_train.shape[0], max_iter=1000)
#testMode.fit(testX, testY)

data_by_district = data.groupby(['VDOT_District'])
bounds = []
bounds.append(-83.71) 
bounds.append(-75.29)
bounds.append(35.5)
bounds.append(40.1)

district_bounds = {
    "1.Bristol District" : [-3.2,6,-5,8],
    "2.Salem District" : [-2,2,-1,2],
    "3.Lynchburg District" : [-2,2,-1,2],
    "4.Richmond District" : [-2,2,-1,2],
    "5.Hampton Roads District" : [-2,2,-1,2],
    "6.Fredericksburg District" : [-2,2,-1,2],
    "7.Culpeper District" : [-2,2,-1,2],
    "8.Staunton District" : [-2,2,-1,2],
    "9.Northern Virginia District" : [-2,2,-1,2]
    }

print(data_by_district)
plt.figure(figsize=(15,12))
virginia_img2 = mpimg.imread('map.jpg')
for name, district in data_by_district:
    print(name)
    print(district_bounds[name])
    #plt.scatter(district['X'],district['Y'],s=0.1)
    district_scaled = full_pipeline.fit_transform(district)
    kmeans_optimal = [KMeans(n_clusters=i, random_state=42).fit(district_scaled) for i in range(5,35, 5)]
    inertias_optimal = [clusters.inertia_ for clusters in kmeans_optimal]
    plt.figure(figsize=(8, 3.5))
    plt.plot(range(5, 35, 5), inertias_optimal, "bo-")
    plt.xlabel("$k value$", fontsize=14)
    plt.ylabel("inertia", fontsize=14)
    plt.title("k value vs inertia in " + name) #clear elbow at 10 for each
    plt.show() 

    district_scaled_frame = pd.DataFrame(district_scaled)
    district_scaled_frame['cluster_id'] = (pd.DataFrame(kmeans_optimal[1].labels_))
    plt.figure()

    #plt.imshow(virginia_img2, extent=district_bounds[name], alpha= 0.5, aspect =1)
    for i in range(10):
        district_scaled_array = district_scaled_frame.loc[district_scaled_frame['cluster_id'] == i].to_numpy()
        plt.scatter(district_scaled_array[: , 0], district_scaled_array[:, 1], s=0.2)
    plot_centroids(kmeans_optimal[1].cluster_centers_)
    plt.legend(list(range(10)), markerscale=10)
    plt.show()
    print("\\resizebox{\columnwidth}{!}{")
    for i in range(10):
        stats = district_scaled_frame.loc[district_scaled_frame['cluster_id'] == i].describe()
        stats = stats.drop(['cluster_id'], axis=1)
        stats.columns = ['Longitude','Latitude','Year','Speed Limit']
        stats = stats.round(2)
        stats = stats.iloc[0:3]
        print(stats.to_latex())
        if (i-1)%2 == 0:
            print("}\n\n")
            print("\\resizebox{\columnwidth}{!}{")