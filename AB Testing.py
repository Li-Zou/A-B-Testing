#We developed a new webpage and want to test its effcts on purchase conversion.
import pandas as pd
from scipy.stats import chi2_contingency
import datetime
df=pd.read_csv(r"C:\Users\li\Desktop\all\job\python\2.ABtesting\ab_data.csv")#download the data
print(df.sample(2))#show 2 items
#part 1.data analysis
a=datetime.datetime.strptime(df["timestamp"].min(),'%Y-%m-%d %H:%M:%S.%f')
b=datetime.datetime.strptime(df["timestamp"].max(),'%Y-%m-%d %H:%M:%S.%f')
c=(b-a).days
print(f"the duration of the data: {c}")
a=df["user_id"].unique()
print(f"the number of unique users: {len(a)}")
a=df["landing_page"].unique().tolist()
print(f"landing page to compare: {a}")
a=round(sum(df["group"]=="control")/len(df["group"])*100)
print(f"the percentage of users in control group is : {a}%")
del a,b,c

sample=df[df['user_id'].isin([746755,722274])]
print(sample)#a user can have multiple buckets
#If a user can have multiple buckets, get timestamp of its first exposure
a=df.groupby("user_id")["timestamp"].min().to_frame().reset_index()
b=pd.merge(a,df,on=["user_id","timestamp"],how='left')

#perform chi-sauqre test
#Pearson’s Chi-Square is a statistical hypothesis test for independence between categorical variables
#Null pypothesis:There is no significant difference between Control and Treatment group
x1=b.groupby("group")["converted"].sum()#the number of users purchase the items in each group
x2=b.groupby("group")["converted"].size()-x1#the number of users do not purchase the items in each group
x3=pd.concat([x1,x2],axis=1)
x4=x3.to_numpy()#chi-square table
stat, p,_,_ = chi2_contingency(x4)
print(f'the p-value of chi-sauqre is: {p}')
if p<0.05:
    print("Control and Treatment group are dependent")
else:
    print("Control and Treatment group are independent")

