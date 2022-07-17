import numpy as np
import pandas as pd
import mail_demo
mail_sent = 0
count = 0

file1 = open("file.txt","r")

X_test = []

df=pd.read_csv("Data1.csv")
X=df[['A','B','C','D']]
Y=df['Circumference']

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X, Y)

for item in file1:
    item=item[1:-1]
    X_test=item.split(" ")

res = []
for ele in X_test:
    if ele.strip():
        res.append(ele)
    
for item in res:
    float(item)
res=np.array(res)
res=res.reshape(1, -1)
# print(res)
Y_pred=regressor.predict(res)
# print(Y_pred)
if mail_sent == 0:
    count+=1
    mail_demo.send_mail2(Y_pred)
    mail_sent = 1

