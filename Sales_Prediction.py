from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd

data = pd.read_csv('sales_data_sample.csv')
#data.head()
data['ORDERDATE'] = data['ORDERDATE'].astype('datetime64[ns]')
weekly_data = data.resample('W-Wed', label='right', closed = 'right', on='ORDERDATE').sum().reset_index().sort_values(by='ORDERDATE')
weekly_data.set_index('ORDERDATE', inplace=True)
weekly_data.index = pd.to_datetime(weekly_data.index)
weekly_data.replace(0,weekly_data.mean(axis=0),inplace=True)
X = weekly_data.values
print(X)
#X

#modeling
size = int(len(X) * 0.9)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(2,1,0))
    model_fit = model.fit(disp=1)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    #print('predicted=%f, expected=%f' % (yhat, obs))
print(predictions)
print(type(predictions[0]))
print([p/1000.round() for p in predictions])

#error = mean_squared_error(test, predictions)
#print('Test MSE: %.3f' % error)
