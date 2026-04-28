# Proyecto 2: Arquitectura Planetaria y la Búsqueda de “Tierra 2.0”

## Problema:

No todos los planetas orbitan estrellas como nuestro Sol. Muchos orbitan enanas rojas frías o estrellas gigantes calientes. Queremos descubrir qué tipos de telescopios y métodos de descubrimiento son más eficientes para encontrar exoplanetas pequeños (rocosos) que existan en zonas donde el agua podría ser líquida.

El Filtro de Habitabilidad: "Mundos Rocosos Templados": Temperatura de equilibrio (pl_eqt) entre 200 K y 320 K, y Radio (pl_rade) menor a 2.5 radios terrestres.
Investiga cuántos planetas descubrió el telescopio terrestre “TRAPPIST-South”.

## Toma de datos

A la fecha de verificar la consulta (27 abril 2026) la NASA reporta 6273 exoplanetas descubiertos [1], la consulta obtenida inicialmente con el ADQL fue:

```sql
SELECT pl_name, discoverymethod, disc_facility, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum
FROM ps
WHERE pl_rade IS NOT NULL AND pl_eqt IS NOT NULL
ORDER BY pl_name
```

retorna 17070 datos, siendo casi el triple de los exoplanetas reales descubiertos, evidenciando la duplicidad de los objetos, esto es debido a que cada fila de datos corresponde a un paper que trabajó sobre el exoplaneta y los datos encontrados, para esto no se usará entonces la tabla ps, sino la tabla PSCompPars que presenta el concenso de los datos de los planetas [2]. Usando el siguiente ADQL:

```sql
SELECT pl_name, discoverymethod, disc_facility, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum
FROM PSCompPars
```

Con este cambio se obtiene un total de 6273 exoplanetas, que es el valor exacto de los planetas descubiertos que reporta la NASA. (Nota: si este valor se verifica en una fecha posterior, estos números pueden variar). Ahora se trae solo los datos que no tengan ni radio ni temperatura de equilibrio nula obteniendo un total de 4661 exoplanetas:

```sql
SELECT pl_name, discoverymethod, disc_facility, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum
FROM PSCompPars
WHERE pl_rade IS NOT NULL
AND pl_eqt IS NOT NULL
ORDER BY pl_name
```

Para este proyecto se consideran los exoplanetas pequeños como aquellos con radio menor a $2.5 R_{\oplus}$, aunque esto no garantiza composición rocosa, este dato se comprobó en el trabajo del primer mes, ya que podrían ser también miniNeptunos.

# Método

Este proyecto tiene como objetivo encontrar planetas rocosos pequeños, dónde pueda existir agua líquida y para esto un factor importante para esta condición es la temperatura de equilibrio del planeta que según el paso a paso del proyecto se puede tomar el rango de 200 a 320 K. El agua líquida es una de las bases para que un planeta sea habitable, este trabajo ampliará un poco más el alcance y comparará de estos planetas cuales también se encuentran en la zona de habitabilidad de Kopparapu, quien define un modelo que define los límites de la zona de habitabilidad de una estrella,y para planetas rocosos que cumplen condiciones como tener agua líquida en su superficie de pero también se deben cumplir más condiciones como modelo climático 1D radiativo–convectivo, sin nubes y se fija en la temperatura superficial calculando el flujo estelar necesario para mantenerla, además supone planetas tipo Tierra, una atmósfera rica en $H_2O$ o $CO_2$ [3].
El modelo de Kopparapu define una zona de una estrella entre la que los planetas que se encuentran dentro de esta zona tienes mayor probabilidad de ser habitables, que a veces se puede llamar la zona risitos de oro. En el trabajo de Kopparapu el límite más cerca a la estrella es el límite interno y el más lejano es el límite exterior, además se dividen en límites optimistas y conservadores [3]. Un dato importante es que este método solo aplica para estrellas con temperatura efectiva entre 2600 - 7200 K.

| Límite                     | Tipo                   |
| -------------------------- | ---------------------- |
| Venus reciente (RV)        | Optimista (interior)   |
| Invernadero desbocado (RG) | Conservador (interior) |
| Invernadero húmedo (MG)    | Conservador (interior) |
| Máximo invernadero (MaxG)  | Conservador (exterior) |
| Marte temprano (EM)        | Optimista (exterior)   |

Para calcular la distancia ($d$) a la que se encuentra el límite, se usan las siguientes ecuaciones [3]:

$$T_\star= T_{\rm eff} - 5780$$

$$S_{\rm eff}=S_{\rm eff,\odot}+aT_\star+bT_\star^2+cT_\star^3+dT_\star^4$$

$$d=\sqrt{(L_\star/L_\odot)/S_{\rm eff}}$$
En los datos de la Nasa st_lum representa $log*{10}(L*\star/L*\odot)$, por eso se transforma con $10^{st_lum}$

Los valores correspondientes a las variables $S_{eff,⊙}$, $a$, $b$, $c$, $d$ dependen de cuál límite se está calculando y se expresa en la siguiente tabla [4]:

| Límite                     | $S_{eff,⊙}$ | a           | b           | c             | d             |
| -------------------------- | ----------- | ----------- | ----------- | ------------- | ------------- |
| RV (Venus reciente)        | 1.7763      | 1.4335×10⁻⁴ | 3.3954×10⁻⁹ | −7.6364×10⁻¹² | −1.1950×10⁻¹⁵ |
| RG (Invernadero desbocado) | 1.0385      | 1.2456×10⁻⁴ | 1.4612×10⁻⁸ | −7.6345×10⁻¹² | −1.7511×10⁻¹⁵ |
| MG (Invernadero húmedo)    | 1.0146      | 8.1884×10⁻⁵ | 1.9394×10⁻⁹ | −4.3618×10⁻¹² | −6.8260×10⁻¹⁶ |
| MaxG (Máximo invernadero)  | 0.3507      | 5.9578×10⁻⁵ | 1.6707×10⁻⁹ | −3.0058×10⁻¹² | −5.1925×10⁻¹⁶ |
| EM (Marte temprano)        | 0.3207      | 5.4471×10⁻⁵ | 1.5275×10⁻⁹ | −2.1709×10⁻¹² | −3.8282×10⁻¹⁶ |

# Análisis

## Métodos de detección

Primero observemos de la totalidad de exoplanetas descubiertos cuales son los métodos usados y cuántos planetas se descubrieron por dicho método:

| Método de descubrimiento      | Radio prom $\overline{R_{\oplus}}$ | Cant. de planetas | %     |
| ----------------------------- | ---------------------------------- | ----------------- | ----- |
| Imaging                       | 15.873417                          | 60                | 1.29  |
| Microlensing                  | 10.762000                          | 5                 | 0.11  |
| Orbital Brightness Modulation | 15.244240                          | 1                 | 0.02  |
| Radial Velocity               | 5.477395                           | 193               | 4.14  |
| Transit                       | 4.420317                           | 4381              | 93.99 |
| Transit Timing Variations     | 4.219476                           | 21                | 0.45  |

Se observa que el método de descubrimiento más usado en la detección de exoplanetas es el método de tránsito con el 93.99% de los planetas descubiertos por este método.
Ahora realizando un filtro por planetas rocosos pequeños ($R < 2.5 R_{\oplus}$) se obtiene:

| Método de descubrimiento  | Radio prom $\overline{R_{\oplus}}$ | Cant. de planetas | %     |
| ------------------------- | ---------------------------------- | ----------------- | ----- |
| Microlensing              | 2.210000                           | 1                 | 0.04  |
| Radial Velocity           | 1.621965                           | 81                | 3.48  |
| Transit                   | 1.675284                           | 2232              | 95.96 |
| Transit Timing Variations | 1.709083                           | 12                | 0.52  |

Al igual que el caso anterior se observa que el método de tránsito es el más usado para encontrar planetas rocosos pequeños con el 95.96 % de los planetas descubiertos por este método.

Con la base de datos descargada a continuación se lista el ranking de los 10 telescopios que que descubierto más exoplanetas:

| disc_facility                                | cantidad |
| -------------------------------------------- | -------- |
| Kepler                                       | 2745     |
| Transiting Exoplanet Survey Satellite (TESS) | 835      |
| K2                                           | 371      |
| SuperWASP                                    | 120      |
| Multiple Observatories                       | 77       |
| HATSouth                                     | 73       |
| HATNet                                       | 67       |
| La Silla Observatory                         | 52       |
| SuperWASP-South                              | 32       |
| CoRoT                                        | 28       |

Por mucho el telescopio que más exoplanetas ha descubierto es el Kepler.

Aunque no está dentro de la lista de telescopios que más exoplanetas ha descubierto, el telescopio TRAPPIST-South descubrio 7 planetas todos en un mismo sitema planetario y es el sistema planetario TRAPPIST-1. Es uno de los sistemas planetarios más estudiado y varios de sus planetas se encuentra dentro de la zona habitable de esta estrella.

## Habitabilidad de los exoplanetas rocosos pequeños

En este trabajo se compara la habitabilidad simple dada por un rango de temperatura de equilibrio del planeta con los límites conservador y optimistas dadas por Kopparapu.

La siguiente gráfica muestra todos los planetas encontrados destacando sobre ellos los 3 filtros de habitabilidad para este trabajo.
![Resultado](grafica_1.png)

La gráfica 2 es un zoom a los datos dónde se encuentran los candidatos de las zonas habitables.
![Resultado](grafica_2.png)

# Resultados

La siguiente tabla resume los resultados obtenidos por los 3 métodos:

| Categoría                  | Cantidad | T° estrella mín. (K) | T° estrella máx. (K) | T° planeta mín. (K) | T° planeta máx. (K) |
| -------------------------- | -------- | -------------------- | -------------------- | ------------------- | ------------------- |
| Planetas templados rocosos | 86       | 2566                 | 5818                 | 202                 | 320                 |
| HZ Kopparapu (optimista)   | 55       | 2850                 | 5757                 | 177                 | 381                 |
| HZ Kopparapu (conservador) | 28       | 2900                 | 5596                 | 177                 | 279                 |

Se observa que para el método de kopparapu tanto en límite optimista como en límite conservador, los planetas se encuentran con temperaturas en un rango diferente al de 200 -320 K propuesto por el ejercicio esto debido a que los criterios de Kopparapu se basa principalmente en el flujo de la estrella, la atmósfera y no solo en la temperatura del planeta y por esto la diferencia.

Ahora analicemos los tipos de estrellas en las que aparecen estos planetas con condiciones habitables. La siguiente tabla muestra las estrellas de secuencia principal y su porcentaje de la secuencia principal[5]:

| Clase | Temperatura (K) | Color convencional    | Fracción de la secuencia principal |
| ----- | --------------- | --------------------- | ---------------------------------- |
| O     | ≥ 33000         | azul                  | ~0.00003 %                         |
| B     | 10000 – 33000   | azul a blanco azulado | 0.13 %                             |
| A     | 7500 – 10000    | blanco                | 0.6 %                              |
| F     | 6000 – 7500     | blanco amarillento    | 3 %                                |
| G     | 5200 – 6000     | amarillo              | 7.6 %                              |
| K     | 3700 – 5200     | naranja               | 12.1 %                             |
| M     | ≤ 3700          | rojo                  | 76.45 %                            |

se observa que el rango inferior de la temperatura es igual para todos los métodos de estrellas de 2566 K de temperatura, y un máximo de 5818 K. Esto abarca las estrellas clase M, K, G (tipo Sol) y según la tabla anterior esto corresponde a caso el 96.15 % de las estrellas de secuencia principal por lo tanto las más abundantes.

# Conclusiones

Más del 95% de los exoplanetas (y de los rocosos pequeños) se detectan por el método de tránsito, evidenciando un fuerte sesgo observacional.
Los candidatos a habitabilidad se concentran en estrellas tipo M, K y G, que representan la gran mayoría de la secuencia principal.
Los criterios de temperatura de equilibrio y zona habitable no coinciden completamente, mostrando la importancia de modelos climáticos más complejos.

# Referencias

[1] NASA. (s.f.). Exoplanets. NASA Science Exoplanets. Recuperado el 22 de abril de 2026, de https://science.nasa.gov/exoplanets/

[2] NASA Exoplanet Archive. (2025, julio 14). Planetary systems and planetary systems composite parameters data column definitions. https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html

[3] Kopparapu, R. K., Ramirez, R., Kasting, J. F., Eymet, V., Robinson, T. D., Mahadevan, S., Terrien, R. C., Domagal-Goldman, S., Meadows, V., & Deshpande, R. (2013). Habitable zones around main-sequence stars: New estimates. The Astrophysical Journal, 765(2), Article 131. https://doi.org/10.1088/0004-637X/765/2/131

[4] Kopparapu, R. K., Ramirez, R., Kasting, J. F., Eymet, V., Robinson, T. D., Mahadevan, S., Terrien, R. C., Domagal-Goldman, S., Meadows, V., & Deshpande, R. (2013). Erratum: Habitable zones around main-sequence stars: New estimates. The Astrophysical Journal, 770(1), 82. https://doi.org/10.1088/0004-637X/770/1/82

[5] Wikipedia contributors. (s. f.). Clasificación estelar. En Wikipedia, la enciclopedia libre. Recuperado el 27 de abril de 2026, de https://es.wikipedia.org/wiki/Clasificaci%C3%B3n_estelar
