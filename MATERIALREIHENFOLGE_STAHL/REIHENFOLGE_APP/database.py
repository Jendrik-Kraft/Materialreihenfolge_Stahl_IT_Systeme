import pandas as pd
def get_coils_from_database():
    dummy_coils=pd.read_excel("./default_database_dummy_coils.xlsx")
    print(dummy_coils.head())
    coils=pd.read_excel("./default_database1.xlsx")
    #print(coils["Hight"][5])
