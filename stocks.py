import yfinance as yf
import pandas as pd
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
#plots an x axis and a y axis upon a shared data frame, used for graphing date vs predicted (date is supposed to be in the future, not my code)
def df_plot(data, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
#plots 2 data frames against eachother, not used in current lab but useful in graphing predicted vs real data (again not my code, however making it a definition was my idea)
def df_plot2(data, dfr, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(dfr.Actual_Price, color='black')
    plt.plot(dfr.Predicted_Price, color='lightblue')    
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
#trains dataframe for certain ticker to predict data 20 days in the future and graphs it
def train(ticker):
    #decides what stock it is 
    stock =yf.Ticker(f'{ticker}')
    #sets the period for that stock to the max aka maximum time it can be
    history = stock.history(period="Max")
    #creates a datrame using the max period stock already preset columns
    df=pd.DataFrame(history)
    #not my code (not fully sure what it does)
    df.head(10)
    df.reset_index(inplace=True)
    #limits the dataframe to certain columnns in the dataframe
    df=df[["Date","Open","High","Low","Close","Volume"]]
    #limits x value to 4 columns given
    x = df[['Open', 'High','Low', 'Volume']]
    #limits y value to 1 column given
    y = df['Close']
    #creates 3 new data frames that are empty but still have columns that match each variable
    new_x=pd.DataFrame(columns=['Open', 'High','Low', 'Volume'])
    leftover_x=pd.DataFrame(columns=[ 'Open', 'High','Low', 'Volume'])
    new_y=pd.DataFrame(columns=['Close'])
    df = df.reset_index()  # make sure indexes pair with number of rows
    #What for loop does it goes from start of the array to 20th index before the end and puts that in the train data for the new x
    for i in range(0, len(df)-20):
        #print(df.iloc[i]['Open'], df.iloc[i]['High'],df.iloc[i]['Low'],df.iloc[i]['Volume'])
        new_row={'Open':df.iloc[i]['Open'], 'High':df.iloc[i]['High'],'Low':df.iloc[i]['Low'],'Volume':df.iloc[i]['Volume']}
        new_x.loc[i]=new_row
    #For loop goes from 20th index to the end and insterts current y values for location (makes it so that the lengths of new_x and new_y are same)
    for i in range(20, len(df)):
        #print(df.iloc[i]['Close'])
        new_row={'Close':df.iloc[i]['Close']}
        new_y.loc[i]=new_row
    #For loop goes from 20th to last index to the last index for x values and insterts it in leftovers (used in future predictions)
    for i in range(len(df)-20,len(df)):
        new_row={'Open':df.iloc[i]['Open'], 'High':df.iloc[i]['High'],'Low':df.iloc[i]['Low'],'Volume':df.iloc[i]['Volume']}
        #print(new_row)
        leftover_x.loc[i]=new_row
    #does a train test split (takes 15% of data to train on and then tests data to see how good it is) 
    train_x, test_x, train_y, test_y = train_test_split(new_x, new_y, test_size=0.15 , shuffle=False,random_state = 0)
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import confusion_matrix, accuracy_score
    #for i in range(int(len(df.index)*.15)):
        #test_y=y[len(df.index)-int(len(df.index)*.15)+i]
        #train_y=y[len(df.index)-int(len(df.index)*.15)+i]
    #makes a regression and fits it to train data
    regression = LinearRegression()
    regression.fit(train_x, train_y)
    plt.style.use('fivethirtyeight')
    #print(test_x)
    #print(test_y)
    #calculates r^2 value based off of test_x and test_y data and previous regression
    regression_confidence = regression.score(test_x, test_y)
    #prints it
    print(regression_confidence)
    #predicted=regression.predict(test_x)
    #dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
    #predicted2=regression.predict(b)
    #dfr.head(10)
    #x2 = dfr.Actual_Price.mean()
    #y2 = dfr.Predicted_Price.mean()
    #Accuracy1 = x2/y2*100
    #dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted2})
    #print("The accuracy of the model is " , Accuracy1)
    #df_plot2(df,dfr,title=f"{ticker}",xlabel='Date', ylabel='Value',dpi=100)
    #predicts y value based off of leftover x data
    predicted=regression.predict(leftover_x)
    predicted.shape
    #plots this data using date and predicted value (date is actually 20 days in future but it doesn't say that)
    df_plot(df, df.iloc[leftover_x.index]['Date'], predicted, title=f"{ticker}",xlabel='Date', ylabel='Value',dpi=100)
#Data predicts stock values for 1 day in the future
def train1(ticker):
    #chooses stock
    stock =yf.Ticker(f'{ticker}')
    #picks max history for the stock
    history = stock.history(period="Max")
    #creates a dataframe with max history stock
    df=pd.DataFrame(history)
    df.head(10)
    df.reset_index(inplace=True)
    #limits data frame to certain columns
    df=df[["Date","Open","High","Low","Close","Volume"]]
    #sets x values to those 4 columns
    x = df[['Open', 'High','Low', 'Volume']]
    #sets y values to singular column
    y = df['Close']
    #creates a empty data frame with 4 columns
    new_x=pd.DataFrame(columns=['Open', 'High','Low', 'Volume'])
    #creates a empty data frame with 4 columns
    leftover_x=pd.DataFrame(columns=[ 'Open', 'High','Low', 'Volume'])
    #creates empty data frame with 1 column
    new_y=pd.DataFrame(columns=['Close'])
    df = df.reset_index()  # make sure indexes pair with number of rows
    #goes from start of array to end of array and takes out one value which is last index
    for i in range(0, len(df)-1):
        #print(df.iloc[i]['Open'], df.iloc[i]['High'],df.iloc[i]['Low'],df.iloc[i]['Volume'])
        new_row={'Open':df.iloc[i]['Open'], 'High':df.iloc[i]['High'],'Low':df.iloc[i]['Low'],'Volume':df.iloc[i]['Volume']}
        new_x.loc[i]=new_row
    #goes from index 1 to end of array
    for i in range(1, len(df)):
        #print(df.iloc[i]['Close'])
        new_row={'Close':df.iloc[i]['Close']}
        new_y.loc[i]=new_row
    #goes from last index-1 to last index and inserts in that leftover
    for i in range(len(df)-1,len(df)):
        new_row={'Open':df.iloc[i]['Open'], 'High':df.iloc[i]['High'],'Low':df.iloc[i]['Low'],'Volume':df.iloc[i]['Volume']}
        #print(new_row)
        leftover_x.loc[i]=new_row
    # does a train test split with 15% of the robot
    train_x, test_x, train_y, test_y = train_test_split(new_x, new_y, test_size=0.15 , shuffle=False,random_state = 0)
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import confusion_matrix, accuracy_score
    #creates a regression
    regression = LinearRegression()
    #fits it to the trainy and x data
    regression.fit(train_x, train_y)
    plt.style.use('fivethirtyeight')
    #print(test_x)
    #print(test_y)
    #gives r^2 data from regression vs test data
    regression_confidence = regression.score(test_x, test_y)
    #prints r^2 value
    print(regression_confidence)
    #predicted=regression.predict(test_x)
    #dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
    #empty data frame with 1 column
    predicted_frame=pd.DataFrame(columns=['Close'])
    #adds 1 value to it so that data frame is going to have 2 values, 1 value before the day and the predicted day
    predicted_frame.loc[len(df)-2]=df.iloc[len(df)-2]['Close']
    #print(regression.predict(leftover_x))
    predicted=regression.predict(leftover_x)
    #sets final frame to the predicted value
    predicted_frame.loc[len(df)-1]=predicted[0]
    #creates a date dataframe
    date=pd.DataFrame(columns=[['Date']])
    #adds dates to it for last 2 days
    for i in range(len(df)-2,len(df)):
        new_row={'Date':df.iloc[i]['Date']}
        #print(new_row)
        date.loc[i]=new_row
    #prints the percent increase from current day to predicted day
    print(f"Predicted percent increase {((predicted[0][0]-df.iloc[len(df)-2]['Close'])/df.iloc[len(df)-2]['Close'])*100}%")
    #prints days date
    print(f"Todays Date f{df.iloc[len(df)-1]['Date']}")
    #print(df)
    #plots the data frame of the date and the predicted values
    df_plot(df, df.iloc[date.index]['Date'], predicted_frame, title=f"{ticker}",xlabel='Date', ylabel='Value',dpi=100)
#train('MSFT')
#train('AAPL')
#train('NVDA')
train1('MSFT')
train1('AAPL')
train1('NVDA')
