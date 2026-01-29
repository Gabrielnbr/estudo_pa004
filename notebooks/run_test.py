import requests
import json
import pickle as pkl
import pandas as pd

df_test = pkl.load(open("data/processed/x_validacao.pkl", 'rb'))
df_test = df_test.sample(10)
df = json.dumps(df_test.to_dict(orient = 'records'))

url = "https://estudo-pa004.onrender.com/predict"
header = {'Content-type': 'application/json'}

r = requests.post(url, data = df, headers = header)

print(r.status_code)

df_response = pd.DataFrame(r.json())
print(df_response.sort_values(by="prediction"))