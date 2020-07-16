import os
import sys
import time
from datetime import date
import yfinance as yp
import csv
import pandas as pd
from get_all_tickers import get_tickers as gt
from yahooquery import Ticker
import numpy as np
#########################################################
spread = 0.002
columnIndexList = ['True','False','True %','False %','True Sum %','False Sum %','True Cut off','False Cut off','True Cut off %','False Cut off %','Net Cut off %','True Sum Cut off %','False Sum Cut off %','Net Sum Cut off %']
#########################################################
################CREATING SPY FILE########################

today_SPY_file_name = str(date.today()).replace('-','') + "_SPY" + ".csv"

spy = yp.download("SPY", period = "5y", end = "2020-7-7", interval="1wk")["Adj Close"].to_csv()

f_spy = open(today_SPY_file_name,"w+")

f_spy.write(spy)

f_spy.close()

df_spy = pd.read_csv(today_SPY_file_name)

df_spy.dropna(inplace=True)
df_spy.drop(df_spy.tail(1).index,inplace=True)#drop last row
df_spy.reset_index(drop=True, inplace=True)

df_spy['%SPYchange'] = None

for i in range(len(df_spy)):
    if i>=1:
        df_spy.at[i,'%SPYchange']=(df_spy.at[i,'Adj Close']-df_spy.at[i-1,'Adj Close'])/df_spy.at[i-1,'Adj Close']

df_spy.to_csv(today_SPY_file_name, index=True)

#########################################################
##############CREATING ALL TICKERS LIST#################
"""
list_of_tickers = gt.get_tickers()
with open("All_stock_list.csv","w+") as filehandle:
    filehandle.write("Stock Symbol"+"\n")
    for tickers in list_of_tickers:
        filehandle.write(tickers + "\n")
"""
df_tickers = pd.read_csv("All_stock_list.csv")

df_tickers["Price"] = None
df_tickers["Beta"] = None
df_tickers['Case in Last Week'] = None
df_tickers['True'] = None
df_tickers['False'] = None
df_tickers['True %'] = None
df_tickers['False %'] = None
df_tickers['True Sum %'] = None
df_tickers['False Sum %'] = None
df_tickers['True Cut off'] = None
df_tickers['False Cut off'] = None
df_tickers['True Cut off %'] = None
df_tickers['False Cut off %'] = None
df_tickers['Net Cut off %'] = None
df_tickers['True Sum Cut off %'] = None
df_tickers['False Sum Cut off %'] = None
df_tickers['Net Sum Cut off %'] = None

df_tickers.to_csv("All_stock_list.csv")

########################################################
for x in range(len(df_tickers)):
    try:
        p = Ticker(df_tickers.at[x, 'Stock Symbol'])
        p_data = p.financial_data
        df_tickers.at[x, 'Price'] = p_data[str(df_tickers.at[x, 'Stock Symbol'])]['currentPrice']
    except:
        df_tickers.at[x, 'Price'] = 0

    try:
        today_myData_file_name = str(date.today()).replace('-','') + "_" + df_tickers.at[x,"Stock Symbol"] + ".csv"

        myData = yp.download(df_tickers.at[x,"Stock Symbol"], period = "5y", end = "2020-7-7", interval="1wk").to_csv()

        f_myData = open(today_myData_file_name,"w+")

        f_myData.write(myData)

        f_myData.close()

        df_myData = pd.read_csv(today_myData_file_name)

        df_myData.dropna(inplace=True)
        df_myData.drop(df_myData.tail(1).index,inplace=True)#drop last row
        df_myData.reset_index(drop=True, inplace=True)
        #################################
        #########Eliminate those stocks do not have enough data#########
        if len(df_myData)!=len(df_spy):
            print("Length of stock data: " + len(df_myData))
            print(0/0)
        #################################
        df_myData['Stock%change'] = None
        for i in range(len(df_myData)):
            if i>=1:
                df_myData.at[i,'Stock%change'] = (df_myData.at[i,'Adj Close'] - df_myData.at[i-1,'Adj Close'])/df_myData.at[i-1,'Adj Close']
        #################################
        df_myData['StockWeekly%change'] = None
        for i in range(len(df_myData)):
            df_myData.at[i,'StockWeekly%change'] = (df_myData.at[i,'Close'] - df_myData.at[i,'Open'])/df_myData.at[i,'Open']
        #################################
        df_myData['%SPYchange'] = None
        df_myData['%SPYchange'] = df_spy['%SPYchange']
        #################################
        df_myData['Case'] = None
        for i in range(len(df_myData)):
            if i >= 1:
                if df_myData.at[i, '%SPYchange'] > 0 and df_myData.at[i, 'Stock%change'] > df_myData.at[i, '%SPYchange']:
                    df_myData.at[i, 'Case'] = 1
                if df_myData.at[i, '%SPYchange'] > 0 and df_myData.at[i, 'Stock%change'] <= df_myData.at[i, '%SPYchange']:
                    df_myData.at[i, 'Case'] = 2
                if df_myData.at[i, '%SPYchange'] > 0 and df_myData.at[i, 'Stock%change'] <= 0:
                    df_myData.at[i, 'Case'] = 3
                if df_myData.at[i, '%SPYchange'] <= 0 and df_myData.at[i, 'Stock%change'] > 0:
                    df_myData.at[i, 'Case'] = 4
                if df_myData.at[i, '%SPYchange'] <= 0 and df_myData.at[i, 'Stock%change'] <= 0 and df_myData.at[i, 'Stock%change'] > df_myData.at[i, '%SPYchange']:
                    df_myData.at[i, 'Case'] = 5
                if df_myData.at[i, '%SPYchange'] <= 0 and df_myData.at[i, 'Stock%change'] <= 0 and df_myData.at[i, 'Stock%change'] <= df_myData.at[i, '%SPYchange']:
                    df_myData.at[i, 'Case'] = 6
        ##################################################
        df_myData['Case Summary'] = None
        df_myData.at[0,'Case Summary'] = 'True'
        df_myData.at[1,'Case Summary'] = 'False'
        df_myData.at[2,'Case Summary'] = 'True %'
        df_myData.at[3,'Case Summary'] = 'False %'
        df_myData.at[4,'Case Summary'] = 'True Sum %'
        df_myData.at[5,'Case Summary'] = 'False Sum %'
        df_myData.at[6,'Case Summary'] = 'True Cut off'
        df_myData.at[7,'Case Summary'] = 'False Cut off'
        df_myData.at[8,'Case Summary'] = 'True Cut off %'
        df_myData.at[9,'Case Summary'] = 'False Cut off %'
        df_myData.at[10,'Case Summary'] = 'Net Cut off %'
        df_myData.at[11,'Case Summary'] = 'True Sum Cut off %'
        df_myData.at[12,'Case Summary'] = 'False Sum Cut off %'
        df_myData.at[13,'Case Summary'] = 'Net Sum Cut off %'
        ##################################################
        class CaseClass:
            TrueCase = 0
            FalseCase = 0
            TrueCasePer = 0
            FalseCasePer = 0
            TrueCase_CutOff = 0
            FalseCase_CutOff = 0
            TrueCasePer_CutOff = 0
            FalseCasePer_CutOff = 0
        #################################################

        Case1 = CaseClass()
        Case2 = CaseClass()
        Case3 = CaseClass()
        Case4 = CaseClass()
        Case5 = CaseClass()
        Case6 = CaseClass()
        #################################################
        df_myData['Case 1 Summary'] = None
        df_myData['Case 2 Summary'] = None
        df_myData['Case 3 Summary'] = None
        df_myData['Case 4 Summary'] = None
        df_myData['Case 5 Summary'] = None
        df_myData['Case 6 Summary'] = None
        ##################################################
        for i in range(len(df_myData)-1):
            if i>=1: #cut out first row
                if (df_myData.at[i,'Case'] == 1) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case1.TrueCase = Case1.TrueCase + 1
                    Case1.TrueCasePer = Case1.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case1.TrueCase_CutOff = Case1.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 1) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case1.FalseCase = Case1.FalseCase + 1
                    Case1.FalseCasePer = Case1.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']
                if (df_myData.at[i,'Case'] == 2) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case2.TrueCase = Case2.TrueCase + 1
                    Case2.TrueCasePer = Case2.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case2.TrueCase_CutOff = Case2.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 2) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case2.FalseCase = Case2.FalseCase + 1
                    Case2.FalseCasePer = Case2.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']
                if (df_myData.at[i,'Case'] == 3) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case3.TrueCase = Case3.TrueCase + 1
                    Case3.TrueCasePer = Case3.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case3.TrueCase_CutOff = Case3.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 3) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case3.FalseCase = Case3.FalseCase + 1
                    Case3.FalseCasePer = Case3.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']
                if (df_myData.at[i,'Case'] == 4) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case4.TrueCase = Case4.TrueCase + 1
                    Case4.TrueCasePer = Case4.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case4.TrueCase_CutOff = Case4.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 4) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case4.FalseCase = Case4.FalseCase + 1
                    Case4.FalseCasePer = Case4.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']
                if (df_myData.at[i,'Case'] == 5) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case5.TrueCase = Case5.TrueCase + 1
                    Case5.TrueCasePer = Case5.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case5.TrueCase_CutOff = Case5.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 5) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case5.FalseCase = Case5.FalseCase + 1
                    Case5.FalseCasePer = Case5.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']
                if (df_myData.at[i,'Case'] == 6) and (df_myData.at[i+1,'StockWeekly%change'] > 0):
                    Case6.TrueCase = Case6.TrueCase + 1
                    Case6.TrueCasePer = Case6.TrueCasePer + df_myData.at[i+1,'StockWeekly%change']
                    if df_myData.at[i+1,'StockWeekly%change'] > spread:
                        Case6.TrueCase_CutOff = Case6.TrueCase_CutOff + 1
                if (df_myData.at[i,'Case'] == 6) and (df_myData.at[i+1,'StockWeekly%change'] <= 0):
                    Case6.FalseCase = Case6.FalseCase + 1
                    Case6.FalseCasePer = Case6.FalseCasePer + df_myData.at[i+1,'StockWeekly%change']

        ################################################################
        df_myData.at[0,'Case 1 Summary'] = Case1.TrueCase
        df_myData.at[1,'Case 1 Summary'] = Case1.FalseCase
        df_myData.at[2,'Case 1 Summary'] = Case1.TrueCase / (Case1.TrueCase + Case1.FalseCase)
        df_myData.at[3,'Case 1 Summary'] = Case1.FalseCase / (Case1.TrueCase + Case1.FalseCase)
        df_myData.at[4,'Case 1 Summary'] = Case1.TrueCasePer
        df_myData.at[5,'Case 1 Summary'] = Case1.FalseCasePer
        df_myData.at[6,'Case 1 Summary'] = Case1.TrueCase_CutOff
        df_myData.at[7,'Case 1 Summary'] = Case1.TrueCase + Case1.FalseCase - Case1.TrueCase_CutOff
        df_myData.at[8,'Case 1 Summary'] = df_myData.at[6,'Case 1 Summary'] / (df_myData.at[6,'Case 1 Summary'] + df_myData.at[7,'Case 1 Summary'])
        df_myData.at[9,'Case 1 Summary'] = df_myData.at[7,'Case 1 Summary'] / (df_myData.at[6,'Case 1 Summary'] + df_myData.at[7,'Case 1 Summary'])
        df_myData.at[10,'Case 1 Summary'] = df_myData.at[8,'Case 1 Summary'] - df_myData.at[9,'Case 1 Summary']
        df_myData.at[11,'Case 1 Summary'] = Case1.TrueCasePer - spread * Case1.TrueCase
        df_myData.at[12,'Case 1 Summary'] = Case1.FalseCasePer - spread * Case1.FalseCase
        df_myData.at[13,'Case 1 Summary'] = df_myData.at[11,'Case 1 Summary'] - abs(df_myData.at[12,'Case 1 Summary'])
        ############################################################
        df_myData.at[0,'Case 2 Summary'] = Case2.TrueCase
        df_myData.at[1,'Case 2 Summary'] = Case2.FalseCase
        df_myData.at[2,'Case 2 Summary'] = Case2.TrueCase / (Case2.TrueCase + Case2.FalseCase)
        df_myData.at[3,'Case 2 Summary'] = Case2.FalseCase / (Case2.TrueCase + Case2.FalseCase)
        df_myData.at[4,'Case 2 Summary'] = Case2.TrueCasePer
        df_myData.at[5,'Case 2 Summary'] = Case2.FalseCasePer
        df_myData.at[6,'Case 2 Summary'] = Case2.TrueCase_CutOff
        df_myData.at[7,'Case 2 Summary'] = Case2.TrueCase + Case2.FalseCase - Case2.TrueCase_CutOff
        df_myData.at[8,'Case 2 Summary'] = df_myData.at[6,'Case 2 Summary'] / (df_myData.at[6,'Case 2 Summary'] + df_myData.at[7,'Case 2 Summary'])
        df_myData.at[9,'Case 2 Summary'] = df_myData.at[7,'Case 2 Summary'] / (df_myData.at[6,'Case 2 Summary'] + df_myData.at[7,'Case 2 Summary'])
        df_myData.at[10,'Case 2 Summary'] = df_myData.at[8,'Case 2 Summary'] - df_myData.at[9,'Case 2 Summary']
        df_myData.at[11,'Case 2 Summary'] = Case2.TrueCasePer - spread * Case2.TrueCase
        df_myData.at[12,'Case 2 Summary'] = Case2.FalseCasePer - spread * Case2.FalseCase
        df_myData.at[13,'Case 2 Summary'] = df_myData.at[11,'Case 2 Summary'] - abs(df_myData.at[12,'Case 2 Summary'])
        ##################################################
        df_myData.at[0,'Case 3 Summary'] = Case3.TrueCase
        df_myData.at[1,'Case 3 Summary'] = Case3.FalseCase
        df_myData.at[2,'Case 3 Summary'] = Case3.TrueCase / (Case3.TrueCase + Case3.FalseCase)
        df_myData.at[3,'Case 3 Summary'] = Case3.FalseCase / (Case3.TrueCase + Case3.FalseCase)
        df_myData.at[4,'Case 3 Summary'] = Case3.TrueCasePer
        df_myData.at[5,'Case 3 Summary'] = Case3.FalseCasePer
        df_myData.at[6,'Case 3 Summary'] = Case3.TrueCase_CutOff
        df_myData.at[7,'Case 3 Summary'] = Case3.TrueCase + Case3.FalseCase - Case3.TrueCase_CutOff
        df_myData.at[8,'Case 3 Summary'] = df_myData.at[6,'Case 3 Summary'] / (df_myData.at[6,'Case 3 Summary'] + df_myData.at[7,'Case 3 Summary'])
        df_myData.at[9,'Case 3 Summary'] = df_myData.at[7,'Case 3 Summary'] / (df_myData.at[6,'Case 3 Summary'] + df_myData.at[7,'Case 3 Summary'])
        df_myData.at[10,'Case 3 Summary'] = df_myData.at[8,'Case 3 Summary'] - df_myData.at[9,'Case 3 Summary']
        df_myData.at[11,'Case 3 Summary'] = Case3.TrueCasePer - spread * Case3.TrueCase
        df_myData.at[12,'Case 3 Summary'] = Case3.FalseCasePer - spread * Case3.FalseCase
        df_myData.at[13,'Case 3 Summary'] = df_myData.at[11,'Case 3 Summary'] - abs(df_myData.at[12,'Case 3 Summary'])
        ##################################################
        df_myData.at[0,'Case 4 Summary'] = Case4.TrueCase
        df_myData.at[1,'Case 4 Summary'] = Case4.FalseCase
        df_myData.at[2,'Case 4 Summary'] = Case4.TrueCase / (Case4.TrueCase + Case4.FalseCase)
        df_myData.at[3,'Case 4 Summary'] = Case4.FalseCase / (Case4.TrueCase + Case4.FalseCase)
        df_myData.at[4,'Case 4 Summary'] = Case4.TrueCasePer
        df_myData.at[5,'Case 4 Summary'] = Case4.FalseCasePer
        df_myData.at[6,'Case 4 Summary'] = Case4.TrueCase_CutOff
        df_myData.at[7,'Case 4 Summary'] = Case4.TrueCase + Case4.FalseCase - Case4.TrueCase_CutOff
        df_myData.at[8,'Case 4 Summary'] = df_myData.at[6,'Case 4 Summary'] / (df_myData.at[6,'Case 4 Summary'] + df_myData.at[7,'Case 4 Summary'])
        df_myData.at[9,'Case 4 Summary'] = df_myData.at[7,'Case 4 Summary'] / (df_myData.at[6,'Case 4 Summary'] + df_myData.at[7,'Case 4 Summary'])
        df_myData.at[10,'Case 4 Summary'] = df_myData.at[8,'Case 4 Summary'] - df_myData.at[9,'Case 4 Summary']
        df_myData.at[11,'Case 4 Summary'] = Case4.TrueCasePer - spread * Case4.TrueCase
        df_myData.at[12,'Case 4 Summary'] = Case4.FalseCasePer - spread * Case4.FalseCase
        df_myData.at[13,'Case 4 Summary'] = df_myData.at[11,'Case 4 Summary'] - abs(df_myData.at[12,'Case 4 Summary'])
        ##################################################
        df_myData.at[0,'Case 5 Summary'] = Case5.TrueCase
        df_myData.at[1,'Case 5 Summary'] = Case5.FalseCase
        df_myData.at[2,'Case 5 Summary'] = Case5.TrueCase / (Case5.TrueCase + Case5.FalseCase)
        df_myData.at[3,'Case 5 Summary'] = Case5.FalseCase / (Case5.TrueCase + Case5.FalseCase)
        df_myData.at[4,'Case 5 Summary'] = Case5.TrueCasePer
        df_myData.at[5,'Case 5 Summary'] = Case5.FalseCasePer
        df_myData.at[6,'Case 5 Summary'] = Case5.TrueCase_CutOff
        df_myData.at[7,'Case 5 Summary'] = Case5.TrueCase + Case5.FalseCase - Case5.TrueCase_CutOff
        df_myData.at[8,'Case 5 Summary'] = df_myData.at[6,'Case 5 Summary'] / (df_myData.at[6,'Case 5 Summary'] + df_myData.at[7,'Case 5 Summary'])
        df_myData.at[9,'Case 5 Summary'] = df_myData.at[7,'Case 5 Summary'] / (df_myData.at[6,'Case 5 Summary'] + df_myData.at[7,'Case 5 Summary'])
        df_myData.at[10,'Case 5 Summary'] = df_myData.at[8,'Case 5 Summary'] - df_myData.at[9,'Case 5 Summary']
        df_myData.at[11,'Case 5 Summary'] = Case5.TrueCasePer - spread * Case5.TrueCase
        df_myData.at[12,'Case 5 Summary'] = Case5.FalseCasePer - spread * Case5.FalseCase
        df_myData.at[13,'Case 5 Summary'] = df_myData.at[11,'Case 5 Summary'] - abs(df_myData.at[12,'Case 5 Summary'])
        ##################################################
        df_myData.at[0,'Case 6 Summary'] = Case6.TrueCase
        df_myData.at[1,'Case 6 Summary'] = Case6.FalseCase
        df_myData.at[2,'Case 6 Summary'] = Case6.TrueCase / (Case6.TrueCase + Case6.FalseCase)
        df_myData.at[3,'Case 6 Summary'] = Case6.FalseCase / (Case6.TrueCase + Case6.FalseCase)
        df_myData.at[4,'Case 6 Summary'] = Case6.TrueCasePer
        df_myData.at[5,'Case 6 Summary'] = Case6.FalseCasePer
        df_myData.at[6,'Case 6 Summary'] = Case6.TrueCase_CutOff
        df_myData.at[7,'Case 6 Summary'] = Case6.TrueCase + Case6.FalseCase - Case6.TrueCase_CutOff
        df_myData.at[8,'Case 6 Summary'] = df_myData.at[6,'Case 6 Summary'] / (df_myData.at[6,'Case 6 Summary'] + df_myData.at[7,'Case 6 Summary'])
        df_myData.at[9,'Case 6 Summary'] = df_myData.at[7,'Case 6 Summary'] / (df_myData.at[6,'Case 6 Summary'] + df_myData.at[7,'Case 6 Summary'])
        df_myData.at[10,'Case 6 Summary'] = df_myData.at[8,'Case 6 Summary'] - df_myData.at[9,'Case 6 Summary']
        df_myData.at[11,'Case 6 Summary'] = Case6.TrueCasePer - spread * Case6.TrueCase
        df_myData.at[12,'Case 6 Summary'] = Case6.FalseCasePer - spread * Case6.FalseCase
        df_myData.at[13,'Case 6 Summary'] = df_myData.at[11,'Case 6 Summary'] - abs(df_myData.at[12,'Case 6 Summary'])
        ##################################################

        ##################################################
        ######Sending data to All_stock_list.csv####################
        for caseNo in range(1,7):
            if df_myData.at[len(df_myData)-1,'Case'] == caseNo:
                df_tickers.at[x, 'Case in Last Week'] = df_myData.at[len(df_myData) - 1, 'Case']
                for columnNo in range(14):
                    df_tickers.at[x, columnIndexList[columnNo]] = df_myData.at[columnNo, 'Case '+ str(caseNo)+' Summary']

        ##################################################
        df_myData.to_csv(today_myData_file_name, index=True)
        os.remove(today_myData_file_name)
        print(str(x + 1) + " of " + str(len(df_tickers)) + " completed")
    except:
        os.remove(today_myData_file_name)
        print(str(df_tickers.at[x,"Stock Symbol"]) + " fail")
##################################################

df_tickers.to_csv("All_stock_list.csv", index=False)