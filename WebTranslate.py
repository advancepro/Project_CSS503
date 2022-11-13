#python3 -m pip install requests pandas matplotlib



import pandas
import requests
import pandas as pd
from twisted.python import filepath

download_url = "https://arbuz.kz/"
target_csv_path = "arbuz.csv"

response = requests.get(download_url)
response.raise_for_status()    # Check that the request was successful
with open(target_csv_path, "wb") as f:
    f.write(response.content)
print("Download ready.")

nba=pd.read_csv("arbuz.csv", sep='\t')
type(nba)

len(nba)

#Commands

#>>> import pandas as pd
#>>> nba=pd.read_csv("arbuz.csv", sep='\t')
#>>> type(nba)

#>>> len(nba)
#>>> nba.shape

#>>> nba.head()

#>>> pd.set_option("display.max.columns", None)
#>>> pd.set_option("display.precision", 2)
#>>> nba.tail()

#>>> nba.info()

#>>> nba.describe()

