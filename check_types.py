import pandas as pd

df = pd.read_excel("EnquiryList.xlsx", sheet_name="EnquiryList")
print(df.dtypes)