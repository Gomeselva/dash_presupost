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
list_considered_period_p = []
list_porcent_revenue_p = []
list_until_now_p = []
list_porcentage_reveneu_2 = []
totais = []
total_p = []
total_porcent_p =[]
total_until_now = []
total_untilnow_percent = []
data = []



with open("report\october\GL_FinancialReportOct.csv", "r") as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    for i, linha in enumerate(arquivo_csv):
        # print(linha)
        list_origin.append(linha[13])
        list_OE.append(linha[14])
        list_account.append(linha[16])
        list_considered_period.append(linha[18])
        list_porcent_revenue.append(linha[19])
        list_until_now.append(linha[20])
        list_porcent_revenue_1.append(linha[21])
        list_account_description.append(linha[27])
        list_account_name.append(linha[28])
        list_considered_period_p.append(linha[29])
        list_porcent_revenue_p.append(linha[30])
        list_until_now_p.append(linha[31])
        list_porcentage_reveneu_2.append(linha[32])
        totais.append(linha[44])
        total_p.append(linha[45])
        total_porcent_p.append(linha[46])
        total_until_now.append(linha[47])
        total_untilnow_percent.append(linha[48])
        data.append(linha[1])
        

df_distri = pd.read_excel("distribuicao.xlsx")



dict_dados = {"Data": data,
              "Origin": list_origin, 
              "Object_expenses": list_OE, 
              # "Account": list_account, 
              # "whithin_current_period": list_considered_period, 
              # "proportion_revenue":list_porcent_revenue, 
              # "until_now": list_until_now, 
              # "proportion_revenue_1":list_porcent_revenue_1, 
              "Account_description":list_account_description, 
              "Account_name": list_account_name, 
              "outro_periodo": list_considered_period_p,
              "outro_periodo_porcente": list_porcent_revenue_p,
              "outro_until_now": list_until_now_p,
              "until_now_percentage_revenue":list_porcentage_reveneu_2,
              "totais": totais,
              "totais_p": total_p,
              "total_percentual": total_porcent_p,
              "total_until": total_until_now,
              "total_until_percent": total_untilnow_percent
              }


df = pd.DataFrame(dict_dados)



df["Data"] = df["Data"].apply(lambda x: x[25:])
df["Data"] = df["Data"].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').date())


# df["proportion_revenue"] = df["proportion_revenue"].apply(lambda x: x.replace("%", ""))
# df["proportion_revenue"] = df["proportion_revenue"].astype("float")

# df["proportion_revenue_1"] = df["proportion_revenue_1"].apply(lambda x: x.replace("%", ""))
# df["proportion_revenue_1"] = df["proportion_revenue_1"].astype("float")

# df["until_now"] = df["until_now"].apply(lambda x: x.replace("$", ""))
# df["until_now"] = df["until_now"].apply(lambda x: x.replace(",", ""))
# df["until_now"] = df["until_now"].astype("float")


# df["whithin_current_period"] = df["whithin_current_period"].apply(lambda x: x.replace("$", ""))
# df["whithin_current_period"] = df["whithin_current_period"].apply(lambda x: x.replace(",", ""))
# df["whithin_current_period"] = df["whithin_current_period"].astype("float")


df["outro_periodo"] = df["outro_periodo"].apply(lambda x: x.replace("$", ""))
df["outro_periodo"] = df["outro_periodo"].apply(lambda x: x.replace(",", ""))
df["outro_periodo"] = df["outro_periodo"].astype("float")

df["outro_periodo_porcente"] = df["outro_periodo_porcente"].apply(lambda x: x.replace("%", ""))
df["outro_periodo_porcente"] = df["outro_periodo_porcente"].astype("float")

df["outro_until_now"] = df["outro_until_now"].apply(lambda x: x.replace("$", ""))
df["outro_until_now"] = df["outro_until_now"].apply(lambda x: x.replace(",", ""))
df["outro_until_now"] = df["outro_until_now"].astype("float")

df["until_now_percentage_revenue"] = df["until_now_percentage_revenue"].apply(lambda x: x.replace("%", ""))
df["until_now_percentage_revenue"] = df["until_now_percentage_revenue"].astype("float")

df["totais_p"] = df["totais_p"].apply(lambda x: x.replace("$", ""))
df["totais_p"] = df["totais_p"].apply(lambda x: x.replace(",", ""))
df["totais_p"] = df["totais_p"].astype("float")

df["total_percentual"] = df["total_percentual"].apply(lambda x: x.replace("%", ""))
df["total_percentual"] = df["total_percentual"].astype("float")

df["total_until"] = df["total_until"].apply(lambda x: x.replace("$", ""))
df["total_until"] = df["total_until"].apply(lambda x: x.replace(",", ""))
df["total_until"] = df["total_until"].astype("float")

df["total_until_percent"] = df["total_until_percent"].apply(lambda x: x.replace("%", ""))
df["total_until_percent"] = df["total_until_percent"].astype("float")




dict_1 = {
          "Data": "Date",
          "Object_expenses": "Object",
          "Account_description": "Account_Number" ,
          "Account_name": "Sub-object",
          "outro_periodo": "monthly_occurrence" ,
          "outro_periodo_porcente": "%_of_Total_origin_month",
          "outro_until_now": "until_now_occurrence" ,
          "until_now_percentage_revenue": "%_of_Total_origin_until_now",
          "totais": "Expense/revenue", 
          "totais_p": "total_occurrence_month" ,
          "total_percentual":"%_occurrence_month" ,
          "total_until":"total_occurrence_until_now" ,
          "total_until_percent": "%_occurrence_until_now"

}


dict_2 = {"Acc No": "Account_Number",
          # "Category": ,
          # "Object": ,
          "Exp. Acc": "Sub-object" ,
          # "Instituição": ,
          # "Organ": ,
          # "CY23 Others BUDGET": ,
          # "TOTAL BUDGET IADB/OAS": ,
          # "TOTAL BUDGET IADC/OAS": ,
          # "DOD CY23 Cash flow YTD": ,
          "Total distribuido_set": "estimated_budget" ,
          "Total gasto_set": "total_expenditure"
}

df_distri.rename(columns= dict_2, inplace=True)


df.rename(columns= dict_1, inplace=True)

df_new = pd.merge(df_distri, df, on= "Sub-object", how="left" )
df_new.columns

df_final = df_new.loc[:, ["Date", 
                          "Instituição",
                          "Category",
                          "Organ", 
                          "Account_Number_x", 
                          "Object_x",
                          "Sub-object",
                          "CY23 Others BUDGET",
                          "TOTAL BUDGET IADB/OAS",
                          "TOTAL BUDGET IADC/OAS",
                          "DOD CY23 Cash flow YTD", 
                          "estimated_budget",
                          "monthly_occurrence",
                          "until_now_occurrence"]
                          ]

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

planilha(df_final)

