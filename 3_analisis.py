import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conexion = sqlite3.connect('sistemas_planetarios.db')

consulta_dm = "SELECT discoverymethod, AVG(pl_rade), count(pl_rade) FROM planetas GROUP BY discoverymethod ORDER BY discoverymethod;"

df_mthd_rad = pd.read_sql_query(consulta_dm, conexion)
print("Radio promedio por método de descubrimiento de planetas")
print(df_mthd_rad)

consulta_dm = "SELECT discoverymethod, AVG(pl_rade), count(pl_rade) FROM planetas WHERE pl_rade < 2.5 GROUP BY discoverymethod ORDER BY discoverymethod;"

df_mthd_rad = pd.read_sql_query(consulta_dm, conexion)
print("Radio promedio por método de descubrimiento de planetas rocosos pequeños")
print(df_mthd_rad)

trappist1 = "SELECT * FROM planetas where pl_name like 'TRAPPIST-1%';"

consulta_general = "SELECT pl_name, AVG(pl_rade) AS pl_rade, AVG(pl_eqt) AS pl_eqt, AVG(pl_orbsmax) AS pl_orbsmax, AVG(st_teff) AS st_teff, AVG(st_lum) AS st_lum FROM planetas GROUP BY pl_name ORDER BY pl_name;"

df = pd.read_sql_query(consulta_general, conexion)
conexion.close()

#Filtro de planetas templados rocosos
rocosos_templados = df[(df['pl_eqt'] >= 200) & (df['pl_eqt'] <= 320) & (df['pl_rade'] < 2.5)] 

#Calculo de la zona de habitabilidad 
df['T_ast'] = df['st_teff'] - 5780
df['Seff_rg'] = 1.0385 + 1.2456e-4*df['T_ast'] + 1.4612e-8*df['T_ast']**2 -7.6345e-12 * df['T_ast']**3 - 1.7511e-15*df['T_ast']**4
df['Seff_mxg'] = 0.3507 + 5.9578e-5*df['T_ast'] + 1.6707e-9*df['T_ast']**2 -3.0058e-12 * df['T_ast']**3 - 5.1925e-16*df['T_ast']**4

df['d_rg'] = (10**df['st_lum']/df['Seff_rg'])**0.5
df['d_mxg'] = (10**df['st_lum']/df['Seff_mxg'])**0.5

df.to_csv("archivo.csv")
# Filtro de planetas rocosos en la zona de habitabilidad de Kopparapu (2013)
rocosos_ZH = df[(df['pl_orbsmax'] >= df['d_rg']) & (df['pl_orbsmax'] <= df['d_mxg']) & (df['pl_rade'] < 2.5)] 

plt.figure(figsize=(6, 8))
# Graficar Color vs Magnitud
plt.scatter(df['st_teff'], df['pl_eqt'], color='gray')
plt.scatter(rocosos_templados['st_teff'], rocosos_templados['pl_eqt'], color='blue', label='Temperatura planetaria')
plt.scatter(rocosos_ZH['st_teff'], rocosos_ZH['pl_eqt'], color='green', alpha=0.5, label= 'ZH Kopparapu')
plt.title('Gráfica 1: Temperatura Estrella vs Temperatura Planeta')
plt.xlabel('Temperatura Estrella [K]')
plt.ylabel('Temperatura Planeta [K]')
plt.savefig('grafica_1.png')

