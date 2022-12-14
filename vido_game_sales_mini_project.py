# -*- coding: utf-8 -*-
"""Mini_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hiah3PHRF7P-98PAjeOjRhMzHPe-y0Rq
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import Lasso
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

sales = pd.read_csv("C:/Users/91892/Desktop/vgsales.csv")
sales.head()

import seaborn as sns
s = sales[(sales.NA_Sales.notnull() & sales.JP_Sales.notnull())]
s = sales[((sales.NA_Sales > 0) & (sales.JP_Sales > 0))]
s = s.sample(100, random_state=0)
s = s.loc[s.NA_Sales.rank().sort_values().index]
sns.jointplot(s.NA_Sales.rank(), s.JP_Sales)

NA_sales_ranks = s.NA_Sales.rank().values[:, np.newaxis]
JP_sales = s.JP_Sales.values[:, np.newaxis]

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def predict(degree):
    poly = PolynomialFeatures(degree=degree)
    NA_sales_ranks_poly = poly.fit_transform(NA_sales_ranks)
    clf = LinearRegression()
    clf.fit(NA_sales_ranks_poly, JP_sales)
    JP_sale_predictions = clf.predict(NA_sales_ranks_poly)
    result = np.dstack((JP_sales.flatten(), JP_sale_predictions.flatten())).reshape((100, 2))
    return result

result = predict(1)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("Regression with Degree 1")

result = predict(3)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("Regression with Degree 3")

result = predict(10)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("Regression with Degree 10")

def get_model(degree):
    poly = PolynomialFeatures(degree=degree)
    NA_sales_ranks_poly = poly.fit_transform(NA_sales_ranks)
    clf = LinearRegression()
    clf.fit(NA_sales_ranks_poly, JP_sales)
    return clf

m1_coef = get_model(1).coef_
m3_coef = get_model(3).coef_
m10_coef = get_model(10).coef_

m1_coef

m3_coef

m10_coef

from sklearn.linear_model import Lasso

def get_Lasso_model(degree, alpha):
    poly = PolynomialFeatures(degree=degree)
    NA_sales_ranks_poly = poly.fit_transform(NA_sales_ranks)
    clf = Lasso(alpha=alpha)
    clf.fit(NA_sales_ranks_poly, JP_sales)
    return clf

def Lasso_predict(degree, alpha):
    poly = PolynomialFeatures(degree=degree)
    NA_sales_ranks_poly = poly.fit_transform(NA_sales_ranks)
    clf = get_Lasso_model(degree, alpha)
    JP_sale_predictions = clf.predict(NA_sales_ranks_poly)
    result = np.dstack((JP_sales.flatten(), JP_sale_predictions.flatten())).reshape((100, 2))
    return result

result = Lasso_predict(10, 10)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("degree=10, alpha=$10^1$")

result = Lasso_predict(10, 10**15)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("degree=10, alpha=$10^{15}$")

"""Here , coefficient become equal to 0 which is not possible in the case of Ridge regression"""

result = Lasso_predict(10, 10**20)
plt.plot(range(len(result[:, 1])), result[:, 1])
plt.scatter(range(len(result[:, 0])), result[:, 0], color='black')
plt.gca().set_title("degree=10, alpha=$10^{20}$")

"""So, here the Lasso regression is used to feature selection because it make the coefficient "0" of the data which has less impact to the model ."""

X,y = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1,noise=20,random_state=13)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

plt.scatter(X,y)

from sklearn.linear_model import LinearRegression

reg = LinearRegression()
reg.fit(X_train,y_train)
print(reg.coef_)
print(reg.intercept_)

alphas = [0,1,5,10,30]
plt.figure(figsize=(12,6))
plt.scatter(X,y)
for i in alphas:
    L = Lasso(alpha=i)
    L.fit(X_train,y_train)
    plt.plot(X_test,L.predict(X_test),label='alpha={}'.format(i))
plt.legend()
plt.show()

"""In this plot we see that as we increase the value of alpha coefficient is decreasing and there also a condition of underfitting at some value of alpha and at some value of alpha some coeffiecient become "0" so the points whose coefficient is 0 has no impact on the dataset."""