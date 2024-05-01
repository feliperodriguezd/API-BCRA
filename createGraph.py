import requests 
import urllib3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

urllib3.disable_warnings()
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
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
    ax.yaxis.grid(True)
    for variable in resultsVariables:
        if variable["idVariable"] == idVariable:
            plt.title(variable["descripcion"])
    plt.show()


def ConfirmarGrafico(id):
    for variable in resultsVariables:
        if variable["idVariable"] == id:
            print(variable["descripcion"])

confirmacion = "N"
while (confirmacion != "Y"):
    print("Ingrese el ID deseado:")
    id = input()
    try:
        ConfirmarGrafico(int(id))
        print("¿Es este el grafico que desea generar? (y/n)")
        confirmacion = input().upper()
        if confirmacion != "Y":
            if confirmacion != "N":
                print("Opción no valida")
    except:
         print("Opción no valida")

print("Ingrese fecha desde cuando inice el grafico (dd/mm/yyyy):")
fechaDesde = input().split("/")
print("Ingrese fecha hasta cuando mostrar los datos (dd/mm/yyyy):")
fechaHasta = input().split("/")
try:
    CreateGraph(int(id), fechaDesde[0],fechaDesde[1], fechaDesde[2], fechaHasta[0], fechaHasta[1], fechaHasta[2])
except IndexError:
    print("Error el formato de la fecha colocada")
except ValueError:
    print("Error en el id")
