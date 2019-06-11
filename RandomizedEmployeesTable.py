# This script will create an "Employee Table" with randomized employee names and hire dates and export to a CSV file.
# Change the rows variable to control the number of rows exported.
# pip install --upgrade names, pandas, pandas_datareader, scipy, matplotlib, pyodbc, pycountry, azure

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

import names, random, datetime, numpy as np, pandas as pd, time, string, csv
rows = 10000
id = np.array(range(1,10001))
lastname = np.array([''.join(names.get_last_name()) for _ in range(rows)])
firstname = np.array([''.join(names.get_first_name()) for _ in range(rows)])
nowdate = datetime.date.today()
hiredate = np.array([nowdate - datetime.timedelta(days=(random.randint(30,180))) for _ in range(rows)])
hiretime = np.array([str(random.randint(7,20)) + ':' + str(random.randint(0,59)) + ':00' for _ in range(rows)])
inputzip = zip(id,lastname,firstname,hiredate,hiretime)
inputlist = list(zip(id,lastname,firstname,hiredate,hiretime))
df = pd.DataFrame(inputlist)
df.to_csv('input.csv',index=False,header=["ID","LastName","FirstName","HireDate","HireTime"])
