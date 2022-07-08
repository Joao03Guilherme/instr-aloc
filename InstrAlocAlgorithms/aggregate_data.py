import pandas as pd

df_05 = pd.read_csv("05.csv")
df_06 = pd.read_csv("06.csv")

df = pd.concat([df_05, df_06])
print(df)
df.to_excel("data.xlsx")