# Project_CSS503

* url used - https://arbuz.kz/#/

* Code Type - Python

Used Libraries

import pandas
import requests
import pandas as pd
from twisted.python import filepath

Project 1: Final Submissions

Date: November 13, 2022
Team: 3
ID: 221107078 

Instruction
In the first step, the URL page was converted to CSV file. The information of the converted files data values are taken with python code.
Code Introduction
When you execute the script, it will save the file arbuz.csv in the current working directory.

import pandas
import requests
import pandas as pd
from twisted.python import filepath



Importing Pandas in Python with the pd. Then, use .read_csv() to read in the dataset and store it as a DataFrame object in the variable nba
***
-	PyDev console: starting.
-	import pandas as pd
-	import pandas as pd
-	nba=pd.read_csv("arbuz.csv", sep='\t')
-	type(nba)
-	<class 'pandas.core.frame.DataFrame'>
 
Can see how much data nba contains
-	len(nba)
o	output - 10954
-	nba.shape
o	output - (10954, 1)
 

nba.head()
 

You can configure Pandas to display all columns like this
-	pd.set_option("display.max.columns", None)
 
To verify that changed the options successfully, execute .head() again, or you can display the last five rows with .tail() instead:
-	pd.set_option("display.precision", 2)
-	nba.tail()
 
display all columns and their data types with .info()
-	nba.info()
 
overview of the values each column contains. You can do this with .describe()
-	nba.describe()
 


