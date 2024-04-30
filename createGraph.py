import requests 
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


response = requests.get("https://api.bcra.gob.ar/estadisticas/v1/principalesvariables", verify=False)

responseInJson = response.json()
resultsVariables = responseInJson["results"]

date = datetime.datetime.now()
day = date.strftime("%d")
month = date.strftime("%m")

buscar = requests.get("https://api.bcra.gob.ar/estadisticas/v1/datosvariable/1/2024-01-01/2024-{m}-{d}".format(m=month, d=day), verify=False)

buscarInJson = buscar.json()
buscarResults = buscarInJson["results"]

values = []
dates = []

for data in buscarResults:
    valueWithNoDot = data["valor"].replace(".", "")
    valuewithnoComaAndDot = valueWithNoDot.replace(",", ".")
    values.append(float(valuewithnoComaAndDot))
    dates.append(data["fecha"])

fig, ax = plt.subplots()
ax.plot(dates, values)
ax.axis((0, len(dates), 0, max(values)*1.3))
ax.xaxis.set_major_locator(plt.MaxNLocator(7))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: 'US$ ' + '{:,.0f}'.format(x)))
ax.yaxis.grid(True)

for varialbe in resultsVariables:
    if varialbe["idVariable"] == 1:
        plt.title(varialbe["descripcion"])

plt.legend()
plt.show()