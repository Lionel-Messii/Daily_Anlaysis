import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta, date
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')


def models_eval(df,temp):
	st.write(temp)
	fig = px.line(df, x="Date", y=temp,title = "Percentage of failed transactions")
	agree = st.checkbox('Show me numbers')
	if agree:
		st.write(df[['Date',temp]])
	st.plotly_chart(fig)

def models_eval2(qr,de,temp1,temp2):
	#st.write(type(temp2))
	df = qr.merge(de,on='Date')
	#st.write(df.columns)
	fig = px.line(df, x="Date", y=temp1,title = "Percentage of failed transactions")
	fig.add_scatter(x=df['Date'], y=df[temp2], mode='lines')
	agree = st.checkbox('Show me numbers')
	if agree:
		st.write(df[['Date',temp1,temp2]])
	st.plotly_chart(fig)




def all_orn_num(df1,df2,df3,df4,df5):

	select1 = st.sidebar.selectbox('Select journey', ['QR & DE', 'QR' ,'DE' , 'QR vs DE'], key='2')
	if not st.sidebar.checkbox("Hide", True, key='3'):
		if select1 == 'QR & DE':
			fig = px.line(df1, x="Date", y="Total_ORN",title = "count of orns")
			agree = st.checkbox('Display table for Date and num of ORNs')
			if agree:
				st.write(df1[['Date','Total_ORN']])
			st.plotly_chart(fig)

			fig2 = px.line(df1, x="Date", y="Total_200_per",title = "Percentage of succesfull orns")
			fig2.add_scatter(x=df1['Date'], y=df1['Total_422_per'], mode='lines')
			st.plotly_chart(fig2)

		elif select1 == 'QR':
			fig = px.line(df2, x="Date", y="QR_ORN",title = "count of orns")
			st.plotly_chart(fig)

			fig2 = px.line(df2, x="Date", y="QR_200_per",title = "Percentage of succesfull orns")
			fig2.add_scatter(x=df2['Date'], y=df2['QR_422_per'], mode='lines')
			st.plotly_chart(fig2)

			select_side = st.sidebar.selectbox('Select journey', ['POI', 'POA'])
			if select_side == 'POI':
				select_model = st.sidebar.selectbox('Select Model', ['macro','micro','redline','spoof',"blur"])
				temp_key = select1+"_"+select_side+"_"+select_model+"_422_per"
				models_eval(df3,temp_key)
			else:
				select_model = st.sidebar.selectbox('Select Model', ['macro','spoof',"blur"])
				temp_key1 = select1+"_"+select_side+"_"+select_model+"_422_per"
				models_eval(df3,temp_key)
					#temp_key = 'QR_POI_macro_422_per'
					#temp_key = select1+"_"+select_side+"_"+select_model+"_422_per"
					#models_eval(df3,temp_key)

		elif select1 == 'DE':
			fig = px.line(df4, x="Date", y="DE_ORN",title = "count of orns")
			st.plotly_chart(fig)

			fig2 = px.line(df4, x="Date", y="DE_200_per",title = "Percentage of succesfull orns")
			fig2.add_scatter(x=df4['Date'], y=df4['DE_422_per'], mode='lines')
			st.plotly_chart(fig2)

			select_side = st.sidebar.selectbox('Select journey', ['POI', 'POA'])
			if select_side == 'POI':
				select_model = st.sidebar.selectbox('Select Model', ['macro','micro','redline','spoof',"blur"])
				temp_key = select1+"_"+select_side+"_"+select_model+"_422_per"
				models_eval(df5,temp_key)
			else:
				select_model = st.sidebar.selectbox('Select Model', ['macro','spoof',"blur"])
				temp_key = select1+"_"+select_side+"_"+select_model+"_422_per"
				models_eval(df5,temp_key)

		elif select1 == 'QR vs DE':
		#select1 = st.sidebar.selectbox('Select side of the card', ['POI', 'POA' ,'BOTH' ], key='4')
			df7 = df1.merge(df2,on='Date')
			df6 = df7.merge(df4,on='Date')
			df6['QR_ORN_per'] = df6['QR_ORN']*100/df6['Total_ORN']
			df6['DE_ORN_per'] = df6['DE_ORN']*100/df6['Total_ORN']
			#st.markdown("QR Share in Total traffic")
			fig = px.line(df6, x="Date", y="QR_ORN_per",title="Percentage of QR journey in a day",
			width=600, height=400)
			fig.add_scatter(x=df6['Date'], y=df6['DE_ORN_per'], mode='lines')
			st.plotly_chart(fig)

			select_side = st.sidebar.selectbox('Select journey', ['POI', 'POA'])
			if select_side == 'POI':
				select_model = st.sidebar.selectbox('Select Model', ['macro','micro','redline','spoof',"blur"])
				temp_key1 = "QR_"+select_side+"_"+select_model+"_422_per"
				temp_key2 = "DE_"+select_side+"_"+select_model+"_422_per"
				models_eval2(df3,df5,temp_key1,temp_key2)
			else:
				select_model = st.sidebar.selectbox('Select Model', ['macro','spoof',"blur"])
				temp_key1 = "QR_"+select_side+"_"+select_model+"_422_per"
				temp_key2 = "DE_"+select_side+"_"+select_model+"_422_per"
				models_eval2(df3,df5,temp_key1,temp_key2)




def filter_date(df,start,end):
	mask = (df['Date'] >= start) & (df['Date'] <= end)
	df = df.loc[mask]
	return df

def main(): 

	st.markdown('<style>h1{color: Tomato;}</style>', unsafe_allow_html=True)
	st.markdown('<style>h4{color: Blue;}</style>', unsafe_allow_html=True)

	st.sidebar.title("Built with chiraku by Root from:")
	st.sidebar.image("logo.jpeg")

	st.write("""
	# DKYC Read Document API Analysis

	#### This app Analyses the **Read Document API** Data from Production !
	""")

	st.sidebar.header('Read Document API')

	# Read all files
	df1 = pd.read_csv("Final/Total_read.csv")
	df2 = pd.read_csv("Final/QR_read.csv")
	df3 = pd.read_csv("Final/QR_models.csv")
	df4 = pd.read_csv("Final/DE_read.csv")
	df5 = pd.read_csv("Final/DE_models.csv")

	#st.write(df1.info())
	#conver date column to datetime format
	df1['Date']= pd.to_datetime(df1['Date'])
	df2['Date']= pd.to_datetime(df2['Date'])
	df3['Date']= pd.to_datetime(df3['Date'])
	df4['Date']= pd.to_datetime(df4['Date'])
	df5['Date']= pd.to_datetime(df5['Date'])

	df1['Date2']= (df1['Date'])
	df2['Date2']= (df2['Date'])
	df3['Date2']= (df3['Date'])
	df4['Date2']= (df4['Date'])
	df5['Date2']= (df5['Date'])


	#Get range of dates in csv and create a slider for user to choose from
	min_date = df1['Date'].min()
	max_date = df1['Date'].max()

	Date_Range = st.sidebar.date_input('Select Timeline', [min_date,max_date])
	#st.write(type(Date_Range))
	#st.write(Date_Range)


	
	df1 = df1.set_index(['Date2'])
	df2 = df2.set_index(['Date2'])
	df3 = df3.set_index(['Date2'])
	df4 = df4.set_index(['Date2'])
	df5 = df5.set_index(['Date2'])

	df11 = df1.loc[Date_Range[0]:Date_Range[1]]
	df22 = df2.loc[Date_Range[0]:Date_Range[1]]
	df33 = df3.loc[Date_Range[0]:Date_Range[1]]
	df44 = df4.loc[Date_Range[0]:Date_Range[1]]
	df55 = df5.loc[Date_Range[0]:Date_Range[1]]
	#df11 = filter_date(df1,Date_Range[0],Date_Range[1])
	st.write("Number of Days selected : ",len(df11))

	all_orn_num(df11,df22,df33,df44,df55)

	




if __name__ == "__main__":
    main()
