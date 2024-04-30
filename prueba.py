import requests 

response = requests.get("https://api.bcra.gob.ar/estadisticas/v1/principalesvariables", verify=False)

print(response.content)