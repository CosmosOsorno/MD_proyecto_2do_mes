import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conexion = sqlite3.connect('sistemas_planetarios.db')

consulta_dm = "SELECT discoverymethod, AVG(pl_rade), count(pl_rade) FROM planetas GROUP BY discoverymethod ORDER BY discoverymethod;"

df_mthd_rad = pd.read_sql_query(consulta_dm, conexion)
total = df_mthd_rad['count(pl_rade)'].sum()
df_mthd_rad['%'] = np.round(df_mthd_rad['count(pl_rade)']/total*100, 2)
print("Radio promedio por método de descubrimiento de exoplanetas")
print(df_mthd_rad)

consulta_facility = "SELECT disc_facility, COUNT(*) AS cantidad FROM planetas GROUP BY disc_facility ORDER BY cantidad DESC;"
df_facility = pd.read_sql_query(consulta_facility, conexion)
print("--------------------------------")
print("Cantidad de planetas descubiertas por cada telescopio")
print(df_facility)

consulta_dm = "SELECT discoverymethod, AVG(pl_rade), count(pl_rade) FROM planetas WHERE pl_rade < 2.5 GROUP BY discoverymethod ORDER BY discoverymethod;"

df_mthd_rad = pd.read_sql_query(consulta_dm, conexion)
total = df_mthd_rad['count(pl_rade)'].sum()
df_mthd_rad['%'] = np.round(df_mthd_rad['count(pl_rade)']/total*100, 2)
print("--------------------------------")
print("Radio promedio por método de descubrimiento de exoplanetas rocosos pequeños")
print(df_mthd_rad)

trappist1 = "SELECT * FROM planetas where pl_name like '%TRAPPIST%';"
df = pd.read_sql_query(trappist1, conexion)
print("--------------------------------")
print("Cantidad de planetas descubiertas por TRAPPIST-South: ", len(df))

consulta_general = "SELECT pl_name, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum FROM planetas ORDER BY pl_name;"

df = pd.read_sql_query(consulta_general, conexion)
conexion.close()

#Filtro de planetas templados rocosos
rocosos_templados = df[(df['pl_eqt'] >= 200) & (df['pl_eqt'] <= 320) & (df['pl_rade'] < 2.5)] 
print("--------------------------------")
print("Cantidad de planetas templados rocosos: ", len(rocosos_templados))
print("Minima temperatura estrella: ", rocosos_templados['st_teff'].min())
print("Maxima temperatura estrella: ", rocosos_templados['st_teff'].max())
print("Minima temperatura planeta: ", rocosos_templados['pl_eqt'].min())
print("Maxima temperatura planeta: ", rocosos_templados['pl_eqt'].max())


#Calculo de la zona de habitabilidad optimista
df['T_ast'] = df['st_teff'] - 5780
df['Seff_rv'] = 1.7763 + 1.4335e-4*df['T_ast'] + 3.3954e-9*df['T_ast']**2 -7.6364e-12 * df['T_ast']**3 - 1.1950e-15*df['T_ast']**4
df['Seff_em'] = 0.3207 + 5.4471e-5*df['T_ast'] + 1.5275e-9*df['T_ast']**2 -2.1709e-12 * df['T_ast']**3 - 3.8282e-16*df['T_ast']**4
df['d_rv'] = (10**df['st_lum']/df['Seff_rv'])**0.5
df['d_em'] = (10**df['st_lum']/df['Seff_em'])**0.5

# Filtro de planetas rocosos en la zona de habitabilidad de Kopparapu (2013)
rocosos_ZH_optimista = df[(df['pl_orbsmax'] >= df['d_rv']) & (df['pl_orbsmax'] <= df['d_em']) & (df['pl_rade'] < 2.5) & (df['st_teff'] >= 2600) & (df['st_teff'] <= 7200)] 
print("--------------------------------")
print("Cantidad de planetas rocosos en la zona de habitabilidad de Kopparapu optimistas: ", len(rocosos_ZH_optimista))
print("Minima temperatura estrella: ", rocosos_ZH_optimista['st_teff'].min())
print("Maxima temperatura estrella: ", rocosos_ZH_optimista['st_teff'].max())
print("Minima temperatura planeta: ", rocosos_ZH_optimista['pl_eqt'].min())
print("Maxima temperatura planeta: ", rocosos_ZH_optimista['pl_eqt'].max())

#Calculo de la zona de habitabilidad conservador
df['Seff_rg'] = 1.0385 + 1.2456e-4*df['T_ast'] + 1.4612e-8*df['T_ast']**2 -7.6345e-12 * df['T_ast']**3 - 1.7511e-15*df['T_ast']**4
df['Seff_mxg'] = 0.3507 + 5.9578e-5*df['T_ast'] + 1.6707e-9*df['T_ast']**2 -3.0058e-12 * df['T_ast']**3 - 5.1925e-16*df['T_ast']**4
df['d_rg'] = (10**df['st_lum']/df['Seff_rg'])**0.5
df['d_mxg'] = (10**df['st_lum']/df['Seff_mxg'])**0.5

# Filtro de planetas rocosos en la zona de habitabilidad de Kopparapu (2013)
rocosos_ZH_conservador = df[(df['pl_orbsmax'] >= df['d_rg']) & (df['pl_orbsmax'] <= df['d_mxg']) & (df['pl_rade'] < 2.5) & (df['st_teff'] >= 2600) & (df['st_teff'] <= 7200)] 
print("--------------------------------")
print("Cantidad de planetas rocosos en la zona de habitabilidad de Kopparapu conservadores: ", len(rocosos_ZH_conservador))
print("Minima temperatura estrella: ", rocosos_ZH_conservador['st_teff'].min())
print("Maxima temperatura estrella: ", rocosos_ZH_conservador['st_teff'].max())
print("Minima temperatura planeta: ", rocosos_ZH_conservador['pl_eqt'].min())
print("Maxima temperatura planeta: ", rocosos_ZH_conservador['pl_eqt'].max())

plt.figure(figsize=(7, 3))
plt.scatter(df['st_teff'], df['pl_eqt'], color='gray', s=10, label='Planetas de la base de datos')
plt.scatter(rocosos_templados['st_teff'], rocosos_templados['pl_eqt'], color='blue', s=10, label='planetas con temperatura (200-320 K)')
plt.scatter(rocosos_ZH_optimista['st_teff'], rocosos_ZH_optimista['pl_eqt'], color='cyan', alpha=0.7,s=6, label= 'Planetas en ZH Kopparapu optimista')
plt.scatter(rocosos_ZH_conservador['st_teff'], rocosos_ZH_conservador['pl_eqt'], color='magenta', alpha=0.7,s=3, label= 'Planetas en ZH Kopparapu conservador')
plt.title('Gráfica 1: Temperatura Estrella vs Temperatura Planeta')
plt.xlabel('Temperatura Estrella [K]')
plt.ylabel('Temperatura Planeta [K]')
plt.ylim(0,6000)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('grafica_1.png')
plt.close()


plt.figure(figsize=(7, 3))
plt.scatter(df['st_teff'], df['pl_eqt'], color='gray', s=10, label='Planetas de la base de datos')
plt.scatter(rocosos_templados['st_teff'], rocosos_templados['pl_eqt'], color='blue', s=10, label='planetas con temperatura (200-320 K)')
plt.scatter(rocosos_ZH_optimista['st_teff'], rocosos_ZH_optimista['pl_eqt'], color='cyan', alpha=0.7,s=6, label= 'Planetas en ZH Kopparapu optimista')
plt.scatter(rocosos_ZH_conservador['st_teff'], rocosos_ZH_conservador['pl_eqt'], color='magenta', alpha=0.7,s=3, label= 'Planetas en ZH Kopparapu conservador')
plt.title('Gráfica 2: Zoom en Temperatura Estrella vs Temperatura Planeta')
plt.xlabel('Temperatura Estrella [K]')
plt.xlim(2000,6000)
plt.ylim(0,400)
plt.ylabel('Temperatura Planeta [K]')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('grafica_2.png')
plt.close()