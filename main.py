from pyomo.environ import *

ofertas = {
    "Maipo": 240,
    "Casablanca": 360,
    "Colchagua": 500
}

demandas = {
    "Valparaíso": 475,
    "San Antonio": 510
}

costos = {
    ("Maipo", "Valparaíso"): 22000,
    ("Maipo", "San Antonio"): 26000,
    ("Casablanca", "Valparaíso"): 18000,
    ("Casablanca", "San Antonio"): 23000,
    ("Colchagua", "Valparaíso"): 30000,
    ("Colchagua", "San Antonio"): 28000
}

# Crear el modelo
modelo = ConcreteModel()

VINEDOS = list(ofertas.keys())
PUERTOS = list(demandas.keys())

modelo.x = Var(VINEDOS, PUERTOS, domain=NonNegativeReals)

modelo.costoTransporte = Objective(
    expr=sum(costos[v, p] * modelo.x[v, p] for v in VINEDOS for p in PUERTOS),
    sense=minimize)

modelo.restriccionVinedo = ConstraintList()
for v in VINEDOS:
    modelo.restriccionVinedo.add(
        sum(modelo.x[v, p] for p in PUERTOS) <= ofertas[v]
    )

modelo.restriccionPuerto = ConstraintList()
for p in PUERTOS:
    modelo.restriccionPuerto.add(
        sum(modelo.x[v, p] for v in VINEDOS) >= demandas[p]
    )
    
# !apt-get install -y -qq glpk-utils

solucion = SolverFactory('glpk').solve(modelo)

print("costo total de transporte CLP: ", modelo.costoTransporte())
print("Con los siguientes envíos:")
for v in VINEDOS:
    for p in PUERTOS:
        if value(modelo.x[v, p]) > 0:
            print(f"Envie desde el viñedo en {v} al puerto {p}, {value(modelo.x[v, p])} cajas")