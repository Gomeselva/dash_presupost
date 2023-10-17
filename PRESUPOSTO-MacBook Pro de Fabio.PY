import csv
import pandas as pd
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
from datetime import datetime

list_origin = []
list_OE = []
list_account = []
list_considered_period = []
list_porcent_revenue = []
list_until_now = []
list_porcent_revenue_1 = []
list_account_description = []
list_account_name = []
with open("GL_FinancialReportSept.csv", "r") as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    for i, linha in enumerate(arquivo_csv):
        print(linha)
        list_origin.append(linha[13])
        list_OE.append(linha[14])
        list_account.append(linha[16])
        list_considered_period.append(linha[18])
        list_porcent_revenue.append(linha[19])
        list_until_now.append(linha[20])
        list_porcent_revenue_1.append(linha[21])
        list_account_description.append(linha[27])
        list_account_name.append(linha[28])

dict_dados = {"Origin": list_origin, "Object_expenses": list_OE, "Account": list_account, "whithin_current_period": list_considered_period, "proportion_revenue":list_porcent_revenue, "until_now": list_until_now, "proportion_revenue_1":list_porcent_revenue_1, "Account_description":list_account_description, "Account_name": list_account_name }


df = pd.DataFrame(dict_dados)

df["proportion_revenue"] = df["proportion_revenue"].apply(lambda x: x.replace("%", ""))
df["proportion_revenue"] = df["proportion_revenue"].astype("float")

df["proportion_revenue_1"] = df["proportion_revenue_1"].apply(lambda x: x.replace("%", ""))
df["proportion_revenue_1"] = df["proportion_revenue_1"].astype("float")

df["until_now"] = df["until_now"].apply(lambda x: x.replace("$", ""))
df["until_now"] = df["until_now"].apply(lambda x: x.replace(",", ""))
df["until_now"] = df["until_now"].astype("float")


df["whithin_current_period"] = df["whithin_current_period"].apply(lambda x: x.replace("$", ""))
df["whithin_current_period"] = df["whithin_current_period"].apply(lambda x: x.replace(",", ""))
df["whithin_current_period"] = df["whithin_current_period"].astype("float")

def planilha(dataframe=0):
  wb = Workbook()
  ws = wb.active
  excel = dataframe_to_rows(dataframe, index=True, header=True)
  for r in excel:
    ws.append(r)
  diahora = datetime.today()
  stample = diahora.strftime("%Y_%m_%d_%H_%M_%S")
  wb.save("gastos" + stample + ".xlsx")
  print("Planilha gerada com sucesso!!")

planilha(df)



