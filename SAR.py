#!/home/p/anaconda3/bin/python
import pandas as pd
from flask import Flask, jsonify, abort
from flask import request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from pandas import read_csv
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
from flask_cors import CORS

data = pd.read_csv('sales_data_sample.csv')
data['ORDERDATE'] = data['ORDERDATE'].astype('datetime64[ns]')
weekly_data = data.resample('W-Wed', label='right', closed = 'right', on='ORDERDATE').sum().reset_index().sort_values(by='ORDERDATE')
weekly_data.set_index('ORDERDATE', inplace=True)
weekly_data.index = pd.to_datetime(weekly_data.index)
weekly_data.replace(0,weekly_data.mean(axis=0),inplace=True)
X = weekly_data.values

#error = mean_squared_error(test, predictions)
#print('Test MSE: %.3f' % error)

app = Flask(__name__)
CORS(app)
analyser = SentimentIntensityAnalyzer()

def classify_review(review):
    score = analyser.polarity_scores(review)
    if score["compound"] >= 0.5:
        return score, "positive"
    elif score["compound"] <= -0.5:
        return score, "negative"
    elif score["compound"] < 0.5 and score["compound"] > -0.5:
        return score, "neutral"
    else:
        return score, "error"

@app.route('/', methods=['GET'])
def check_server_status():
    return ("Server Running!")

@app.route('/sentimentForReview', methods=['POST'])
def get_sentiment_for_review():
    if not request.json or not 'review' in request.json:
        abort(400)
    score, sentiment = classify_review(request.json["review"])
    return jsonify({"Sentiment": sentiment,
                    "Negative Score": score['neg'],
                    "Positive Score": score['pos'],
                    "Neutral Score": score['neu'],
                    "Compound Score": score['compound']
                    }), 201

@app.route('/nextWeekSalesPrediction', methods=['GET'])
def prediction_weekly_sales():
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
    nextWeekSales = int((predictions[2]/1000))
    return jsonify({"Weekly Sales": nextWeekSales}), 201

if __name__ == '__main__':
    app.run(debug=True)
