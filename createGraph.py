import requests 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


response = requests.get("https://api.bcra.gob.ar/estadisticas/v1/principalesvariables", verify=False)

responseInJson = response.json()
resultsVariables = responseInJson["results"]

def CreateGraph(idVariable, diaDesde, mesDesde, anioDesde, diaHasta, mesHasta, anioHasta):
    buscar = requests.get("https://api.bcra.gob.ar/estadisticas/v1/datosvariable/{v}/{ad}-{md}-{dd}/{ah}-{mh}-{dh}".format(v = idVariable, ad = anioDesde, md = mesDesde, dd =  diaDesde, ah = anioHasta, mh = mesHasta, dh = diaHasta), verify=False)

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
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
    ax.yaxis.grid(True)
    for variable in resultsVariables:
        if variable["idVariable"] == int(idVariable):
            plt.title(variable["descripcion"])
    plt.legend()
    plt.show()


print("Ingrese el ID deseado:")
id = input()
print("Ingrese fecha desde cuando inice el grafico (dd/mm/yyyy):")
fechaDesde = input().split("/")
print("Ingrese fecha hasta cuando mostrar los datos (dd/mm/yyyy):")
fechaHasta = input().split("/")

CreateGraph(id, fechaDesde[0],fechaDesde[1], fechaDesde[2], fechaHasta[0], fechaHasta[1], fechaHasta[2])