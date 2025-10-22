# Vxiex11 ;)

import pandas as pd
import os
from ydata_profiling import ProfileReport
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import StandardScaler

# dataset
df = pd.read_csv("./phishing_email/Phishing_Email.csv")

# delete Unamed because it is only numbers
df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
df['Email Text'].fillna('', inplace=True)
df['Email Type'] = df['Email Type'].astype(str)
df.shape  # number of rows and columns
df.info()  # data type
df.head()  # first columns

# EDA 
profile = ProfileReport(df, title="EDA Report")
profile.to_file("report.html")

# +10% lost data
missing_percent = df.isnull().mean() * 100
cols_to_drop = missing_percent[missing_percent > 10].index
df.drop(columns=cols_to_drop, inplace=True)
df.fillna(df.mean(), inplace=True)

# winsorize for outliers
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col] = winsorize(df[col], limits=[0.05, 0.05])

# encoding categorical variables
df = pd.get_dummies(df, drop_first=True)

# normalization
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

print("Dataset processed successfully") # If this message appear, the program was successfully
print("Shape final:", df.shape)
