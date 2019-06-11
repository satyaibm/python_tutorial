# Chart income change over time using public data
import csv, matplotlib.pyplot as plt, urllib.request as request, pandas as pd
filename = "income.csv"

# Download Income Data
# You may download and use the Census Data packages (pip install censusdata, cenpy)
income_data  = request.urlopen('https://data.hawaii.gov/api/views/5gja-rp2f/rows.csv?accessType=DOWNLOAD')
income_csv = income_data.read()

# Save data to CSV file
income_str = str(income_csv).strip("b'")
records = income_str.split("\\n")
file = open(filename, "w")
for record in records:
   file.write(record + "\n")

file.close()

# Convert date and income columns to lists
income_pd = pd.read_csv(filename,header=0)
years = list(income_pd['Year'])
income = list(income_pd['Personal Income (U.S.), $million'])


# Chart the data
fig = plt.figure()
plt.title('Personal Per Capita Income')
plt.xlabel('Dates')
plt.ylabel('Income, $million')
plt.plot(years,income,color='green') 
plt.legend
fig.savefig('income.pdf') 
plt.show()

