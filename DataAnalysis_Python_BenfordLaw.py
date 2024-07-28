import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Benfordlaw_rawdata2.csv')

#df.info()
#if the data type of the column contains $ sign or any other symbols, you can replace it into float.
df['First_digit'] = df['First_digit'].str.replace("$","",regex = True).replace(",","",regex = True).astype(float)

#extract the first digit from the invoice amounts
df = df.reset_index()
df['extract_digit'] = df['Invoice_amount_received'].astype(str).str[:1]
print(df.set_index(['Invoice_amount_received', 'extract_digit']))

# frequency by first_digits in invoice amounts
first_digit_count = df.pivot_table(values = ['Invoice_amount_received'], 
                                   index = 'First_digit', aggfunc = len, fill_value = '')

# sum total of invoice amounts by first digit
total_invoice_amt = df.pivot_table(values = ['Invoice_amount_received'], 
                                   index = 'First_digit', aggfunc = sum, fill_value = '')

#merge two tables
df = total_invoice_amt.merge(first_digit_count, how = "left", left_on = 'First_digit', 
                             right_index = True, suffixes = ['','_frequency'])

#Weighted percentage occurrence distribution for the subject data
df['subjectData_distribution'] = df['Invoice_amount_received_frequency']/df['Invoice_amount_received_frequency'].sum()

#Benford's Law distribution log10(1+1/n)
range = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
df['Benfordlaw_distribution'] = np.log10(1 / range + 1)
df['leading_digit'] = range
print(df)

#Visualization
fig, ax = plt.subplots(figsize = (8, 5))
df.reset_index()['Benfordlaw_distribution'].plot(kind = "line", ax = ax, secondary_y = False, color =  'red')
ax.legend(["Benford curve"])
df.plot(kind = 'bar', x = 'leading_digit', y = ['subjectData_distribution','Benfordlaw_distribution'], 
        ax = ax, color = ['salmon','dodgerblue'], rot = 0)

plt.show()