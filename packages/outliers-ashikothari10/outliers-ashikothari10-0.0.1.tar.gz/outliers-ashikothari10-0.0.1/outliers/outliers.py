# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:37:20 2020

@author: HP
"""

#from sklearn.datasets import load_boston
import pandas as pd
'''
boston = load_boston()
x = boston.data
y = boston.target
columns = boston.feature_names

boston_df = pd.DataFrame(boston.data)
boston_df.columns = columns
print(boston_df.shape)
boston_df.head()'''
def rem_out(data):
	df = data.copy()
	Q1 = df.quantile(0.25)
	Q3 = df.quantile(0.75)
	IQR = Q3 - Q1
	#print(IQR)
	#(boston_df<(Q1 - 1.5 * IQR))|(boston_df > (Q3 + 1.5 * IQR))
	df_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]
	print("Number of removed rows is:",df.shape[0]-df_out.shape[0])
	return df_out
	#df_out.to_csv(newdata,index=False)
	#boston_df_out.shape
import sys

try:
	dataset=pd.read_csv(sys.argv[1])
	df_out = rem_out(dataset)
	#newdataset=sys.argv[2]
except OSError:
	print(sys.argv[1],"Enter correct file name with correct path")
'''except:
	flag_name = True
	print('Some error in entering name of csv file.')
	print("Correct format is: python otlier.py path_of\\input_file.csv path_of\\output_file.csv")'''
