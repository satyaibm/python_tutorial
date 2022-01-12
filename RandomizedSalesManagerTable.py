# This script will create a "Sales Table" dataset and export up to 1 million rows to a CSV file.
# Change the rows variable to control the number of rows exported.
# pip install --upgrade pandas, pandas_datareader, scipy, matplotlib, pyodbc, pycountry, azure
# pip freeze > requirements

### This looping operation will install the modules not already configured.
import importlib, os, sys
packages = ['numpy', 'pandas']
for package in packages:
  try:
    module = importlib.__import__(package)
    globals()[package] = module
  except ImportError:
    cmd = 'pip install --user ' + package
    os.system(cmd)
    module = importlib.__import__(package)

rows = 10000
import random, decimal, string, csv, datetime, numpy as np, pandas as pd
invoiceid = np.array(range(10001,20001))
customerid = np.array([''.join(random.choice(string.ascii_uppercase) for _ in range(2)) + ''.join(random.choice(string.digits) for _ in range(2)) for _ in range(rows)])
creditcard = np.array([''.join(random.choice(string.digits) for _ in range(4)) + '-' + ''.join(random.choice(string.digits) for _ in range(4)) + '-' + ''.join(random.choice(string.digits) for _ in range(4)) + '-' + ''.join(random.choice(string.digits) for _ in range(4)) for _ in range(rows)])
supervisorid = np.array(['sup' + ''.join(random.choice(string.digits) for _ in range(2)) for _ in range(rows)])
quantity = np.array([random.randint(1,100) for _ in range(rows)])
price = np.array([round(random.uniform(20, 100),2) for _ in range(rows)])
freight = np.array([round(random.uniform(10, 30),2) for _ in range(rows)])
now = datetime.date.today()
orderdate = np.array([now - datetime.timedelta(days=(random.randint(360,420))) for _ in range(rows)])
salesdata = zip(invoiceid,customerid,creditcard,supervisorid,quantity,price,freight,orderdate)
salesdata1 = list(zip(invoiceid,customerid,creditcard,supervisorid,quantity,price,freight,orderdate))
df = pd.DataFrame(salesdata1)
df.to_csv('salesdata.csv',index=False,header=["InvoiceID","CustomerID","CreditCard","SupervisorID","Quantity","Price","Freight","OrderDate"])
