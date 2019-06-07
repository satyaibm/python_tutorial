# This script will create an "Orders Table" dataset and export up to 1 million rows to a CSV file.
# Change the rows variable to control the number of rows exported.
# pip install --upgrade pandas, pandas_datareader, scipy, matplotlib, pyodbc, pycountry, azure

rows = 1000000
import random, decimal, string, csv, datetime, numpy as np, pandas as pd
orderid = np.array(range(1,1000001))
customerid = np.array([''.join(random.choice(string.ascii_uppercase) for _ in range(2)) + ''.join(random.choice(string.digits) for _ in range(2)) for _ in range(rows)])
managerid = np.array(['man' + ''.join(random.choice(string.digits) for _ in range(2)) for _ in range(rows)])
quantity = np.array([random.randint(1,100) for _ in range(rows)])
price = np.array([round(random.uniform(20, 100),2) for _ in range(rows)])
freight = np.array([round(random.uniform(10, 30),2) for _ in range(rows)])
now = datetime.date.today()
orderdate = np.array([now - datetime.timedelta(days=(random.randint(360,420))) for _ in range(rows)])
shippeddate = np.array([now - datetime.timedelta(days=(random.randint(330,360))) for _ in range(rows)])
orderdata = zip(orderid,customerid,managerid,quantity,price,freight,orderdate,shippeddate)
orderdata1 = list(zip(orderid,customerid,managerid,quantity,price,freight,orderdate,shippeddate))
df = pd.DataFrame(orderdata1)
df.to_csv('orderdata.csv',index=False,header=["OrderID","CustomerID","ManagerID","Quantity","Price","Freight","OrderDate","ShippedDate"])



