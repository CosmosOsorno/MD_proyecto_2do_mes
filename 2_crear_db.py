import pandas as pd
import sqlite3

df = pd.read_csv('exoplanetas_bruto.csv')
df = df.dropna(subset=['pl_rade', 'pl_eqt'])
conexion = sqlite3.connect('sistemas_planetarios.db')
df.to_sql('planetas', conexion, if_exists='replace', index=False)
conexion.close()
