import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo
df = pd.read_excel("dataset_notas_22_alumnos.xlsx")

# Convertir puntajes que usan coma
df["Puntaje"] = df["Puntaje"].astype(str).str.replace(",", ".")
df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors="coerce")

# Filtrar notas menores a 60
df_bajas = df[df["Puntaje"] < 60]

# ----------- Grafico 1: Materias con notas bajas -----------

materias = df_bajas["Materia"].value_counts()

plt.bar(materias.index, materias.values)
plt.title("Notas menores a 60 por materia")
plt.xlabel("Materia")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------- Grafico 2: Alumnos con notas bajas -----------

alumnos = df_bajas["Nombre"].value_counts()

plt.bar(alumnos.index[:10], alumnos.values[:10])  # Mostrar solo 10 alumnos
plt.title("Alumnos con notas menores a 60")
plt.xlabel("Alumno")
plt.ylabel("Cantidad")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
