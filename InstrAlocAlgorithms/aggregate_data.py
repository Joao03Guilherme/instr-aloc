"""Aggregates data from different form files.
    Form file structure: Nome, Email, Contacto telefónico, Preferências
"""
import pandas as pd

df_03 = pd.read_csv("03.csv")
df_04 = pd.read_csv("04.csv")
df_05 = pd.read_csv("05.csv")
df_06 = pd.read_csv("06.csv")

df_list = [df_03, df_04, df_05, df_06]

df = pd.concat(df_list)

df.to_excel("data.xlsx")