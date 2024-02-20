url = 'http://127.0.0.1:8000/datas/list_datas_analyse'
doc =  requests.get(url)
doc = doc.json()

data = json_util.dumps(doc) 
datas = pd.read_json(data)

#Nota: Os códigos completos estão em: jupyter-notbook/projeto-iot-ca