# -*- coding: utf-8 -*-
"""org_prjct

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-uh5hr11kVoeK91-G3pCHMaSEKjrfF52

### **REAL ESTATE HOUSE PRICE PREDICTION**

**Objective**


*   Predict the price of houses from the given dataset by applying different regression based machine learning algorithms.
*   Applying different performance boosting methods like feature selection, Hyper parameter tuning etc.


*   Utilizing different EDA tools for visualization and data manipulation
*   Comparing the performance of the different regression models

**About the Dataset**


1.   title

> Shows the number of bedrooms if it is house. and the details of the location



2.   price

> price of the house or the plot

3.   size

> size of the house in square feet


4.   price_per_sqft

> per square feet price for the house or plot

5.   status

> whether the place is open for living or under construction
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df=pd.read_excel('/content/raw_data.xlsx')
df.head()

df.sample(5)

df.dtypes

df.info()

df.shape

df.drop_duplicates()

"""# Forming a new column and adding the number bedroom into it from the 'title' column"""

df['space']=df['title'].str.split().str[:2].str.join(' ')
df.head()

"""# Drop unnecessary columns"""

df.drop(['Unnamed: 0','title','status'],inplace=True,axis=1)

"""# Removing irrelevent characters and units from the features"""

df['price_per_sqft']=df['price_per_sqft'].str.replace('/ sq ft','')
df['price_per_sqft']=df['price_per_sqft'].str.replace(',','')       #5,751
df['price_per_sqft']=df['price_per_sqft'].str.replace('per sqft','')
df['price_per_sqft']=df['price_per_sqft'].str.replace('₹','')
df['size']=df['size'].str.replace('sqft','')
df['size']=df['size'].str.replace('sqm','')
df.head()

df['space'].value_counts()

"""# Replacing values in space column other than 'BHK' and 'Bedroom' into 'plot'"""

df['space']=df['space'].map(lambda x: x if 'BHK' in x or 'Bedroom' in x else 'plot'  )
df.head()

# def take(sp):
#   if 'BHK' in sp:
#     pass
#   elif 'Bedroom' in sp:
#     pass
#   else:
#     sp='plot'
#   return sp

# df['space']=df['space'].apply(take)

df['space'].value_counts()

"""# Removing rows having plot value in space column"""

df.drop(df[df['space'] == 'plot'].index, inplace=True)
df.reset_index(drop=True,inplace=True)
df.head()

"""# Removing 'BHK' and 'Bedroom' from the space column"""

df['space']=df['space'].str.replace('Bedroom','')
df['space']=df['space'].str.replace('BHK','')
df.head()

df.shape

df['space'].value_counts()

df.isna().sum()

df.dropna(subset=['price_per_sqft'],inplace=True)

df.isna().sum()

df.dtypes

"""# string replace"""

df['price']=df['price'].str.replace('₹','')

"""# Converting price into numbers"""

def convert_prize(cash):
  if 'Cr' in cash:
    return float(cash.replace(' Cr',''))*10000000
  elif 'Lac' in cash:
    return float(cash.replace(' Lac',''))*100000
  elif 'L' in cash:
    return float(cash.replace(' L',''))*100000
  else:
    return float(cash)

df['price']=df['price'].apply(convert_prize)

df['price'].unique()

"""# Datatype changing"""

df['size']=df['size'].astype(float)
df['price_per_sqft']=df['price_per_sqft'].astype(float)
df['space']=df['space'].astype(int)
df['price']=df['price'].astype(int)

df.isna().sum()

df.shape

"""# Dealing missing values"""

sns.distplot(df['size'])

# distribution is not normal so median is used to fill the missing value
df['size']=df['size'].fillna(df['size'].median())

df.isna().sum()

df.dtypes

df.head()

"""# **Graphical representation of the Data**"""

sns.pairplot(df)

sns.heatmap(df.corr(),annot=True)

sns.countplot(x='space',data=df)

x_axis=['size', 'price_per_sqft', 'space']
y_axis=df['price']

for i in x_axis:
 print(sns.regplot(x=df[i],y=y_axis))
 plt.show()

sns.boxplot(df)

"""**there is outliers in price column **

"""

sns.boxplot(df['price_per_sqft'])

sns.boxplot(df['size'])

sns.boxplot(df['space'])

# before removing outliers

sns.boxplot(df['price'])

"""# dealing outliers with mean **iqr - method**"""

# interquartile range
ds=['size', 'price_per_sqft','price']
for i in ds:
  q1=df[i].quantile(0.25)
  q3=df[i].quantile(0.75)
  iqr=q3-q1
  lower=q1-(iqr*1.5)
  upper=q3+(iqr*1.5)

  df[i] = df[i].apply(lambda x: x if lower <= x <= upper else df[i].mean())

# after dealing outliers
plt.figure(figsize=(10,3.3))

plt.subplot(1,3,1)
sns.boxplot(df['price'])
plt.title('price')

plt.subplot(1,3,2)
sns.boxplot(df['size'])
plt.title('size')

plt.subplot(1,3,3)
sns.boxplot(df['price_per_sqft'])
plt.title('price_per_sqft')
plt.show()

df.dtypes

x=df.drop(['price'],axis=1).astype(int)
y=df['price'].astype(int)

"""# Feature selection using **chi_square test**"""

# from sklearn.feature_selection import SelectKBest,chi2

# chi=SelectKBest(chi2,k=3)
# best=chi.fit_transform(x,y)
#print(best.shape)
# x_indes=chi.get_support(indices=True)
# print(df.columns[x_indes])

# x_chi=df.drop(['space','price'],axis=1)
# x_chi.dtypes

from sklearn.model_selection import train_test_split
xtr,xts,ytr,yts=train_test_split(x,y,random_state=42,test_size=0.30)

from sklearn.preprocessing import StandardScaler
std=StandardScaler()
std.fit(xtr)
xtr=std.transform(xtr)
xts=std.transform(xts)

"""# **Model creation**"""

from sklearn.linear_model import LinearRegression
model=LinearRegression()

"""# Hyperparmeter tuning for linear Regression"""

# to get the default values for the parameters
model.get_params()

from sklearn.model_selection import GridSearchCV

parameter={'copy_X': [True,False], 'fit_intercept': [True,False], 'n_jobs': [None,1,5,7,6], 'positive':[True, False]}
gsv=GridSearchCV(model,parameter,cv=10,scoring='accuracy')
gsv.fit(xtr,ytr)

gsv.best_params_

"""# Multiple linear regression model creation"""

from sklearn.linear_model import LinearRegression
model1=LinearRegression(positive=True)
model1.fit(xtr,ytr)
ypr=model1.predict(xts)

df1=pd.DataFrame({'actual':yts,'predicted':ypr,'differance':yts-ypr})
df1

plt.figure(figsize=(8, 6))
plt.scatter(df1['actual'], df1['predicted'], marker='o', color='blue', label='Actual vs. Predicted')
plt.plot([min(df1['actual']), max(df1['actual'])], [min(df1['actual']), max(df1['actual'])], linestyle='--', color='red', label='Perfect Prediction')
plt.legend()

print('slope is ')
print(list(zip(x,model1.coef_)))
print('constant is ',model1.intercept_)

from sklearn.metrics import r2_score,mean_absolute_percentage_error,mean_squared_error

r0=r2_score(yts,ypr)
print('r2 score',r2_score(yts,ypr))
print('maep ',mean_absolute_percentage_error(ypr,yts))

"""# Polynomial Regression"""

from sklearn.preprocessing import PolynomialFeatures
poly=PolynomialFeatures(degree=3)
poly.fit(x,y)
xply=poly.fit_transform(x)

xtrp,xtsp,ytrp,ytsp=train_test_split(xply,y,random_state=42,test_size=0.30)

model2=LinearRegression()
model2.fit(xtrp,ytrp)
yp=model2.predict(xtsp)

xply.shape

r1=r2_score(ytsp,yp)
print('r2 score',r1)
print('maep ',mean_absolute_percentage_error(yp,ytsp))

"""# Decision tree algorithm"""

from sklearn.tree import DecisionTreeRegressor
dec=DecisionTreeRegressor()
dec.fit(xtr,ytr)
ypr1=dec.predict(xts)

r2=r2_score(yts,ypr1)
print('r2 score',r2)
print('maep ',mean_absolute_percentage_error(ypr1,yts))

"""# Random forest algorithm"""

from sklearn.ensemble import RandomForestRegressor
random=RandomForestRegressor()
random.fit(xtr,ytr)
ypr2=random.predict(xts)

r3=r2_score(yts,ypr2)
print('r2 score',r3)
print('maep ',mean_absolute_percentage_error(ypr2,yts))

"""# Ridge Regression"""

from sklearn.linear_model import Ridge
rdg=Ridge(alpha=2)
rdg.fit(xtr,ytr)
yr=rdg.predict(xts)

r4=r2_score(yts,yr)
print('r2 score',r4)
print('maep ',mean_absolute_percentage_error(yr,yts))

al=['mlp','polynomial','decision','random']
result=[r0,r1,r2,r3]

plt.bar(al,result)
plt.xlabel('model name')
plt.ylabel('r2_score')
plt.title('accuracy with different models')

"""

# **Pickling**"""

import pickle

with open('random_forest.pickle', 'wb') as dump_var:
    pickle.dump(random, dump_var)

pickle_in = open('random_forest.pickle', 'rb')
pickle_clf = pickle.load(pickle_in)

accuracy_pkl = pickle_clf.score(xts,yts)
accuracy_pkl