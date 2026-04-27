

# Proyecto 2: Arquitectura Planetaria y la Búsqueda de “Tierra 2.0”

## Problema:
No todos los planetas orbitan estrellas como nuestro Sol. Muchos orbitan enanas rojas frías o estrellas gigantes calientes. Queremos descubrir qué tipos de telescopios y métodos de descubrimiento son más eficientes para encontrar exoplanetas pequeños (rocosos) que existan en zonas donde el agua podría ser líquida.

## Toma de datos

A la fecha de verificar la consulta (22 abril 2026) la NASA reporta 6160 exoplanetas descubiertos [1], la consulta obtenida inicialmente con el ADQL fue:

```sql
SELECT pl_name, discoverymethod, disc_facility, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum 
FROM ps 
WHERE pl_rade IS NOT NULL AND pl_eqt IS NOT NULL 
ORDER BY pl_name
```

retorna 17070 datos, siendo casi el triple de los exoplanetas reales descubiertos, evidenciando la duplicidad de los objetos, esta situación se aborda agrupando las filas por nombre del planeta, y para los valore de los datos numéricos se realizará un promedio de los valores y se trabajará con este promedio. Usando el siguiente ADQL:

```sql
SELECT pl_name, discoverymethod, disc_facility, AVG(pl_rade) AS pl_rade, AVG(pl_eqt) AS pl_eqt, AVG(pl_orbsmax) AS pl_orbsmax, AVG(st_teff) AS st_teff, AVG(st_lum) AS st_lum 
FROM ps 
WHERE pl_rade IS NOT NULL AND pl_eqt IS NOT NULL 
GROUP BY pl_name, discoverymethod, disc_facility 
ORDER BY pl_name
```

Con este cambio se obtiene un total de 4378 exoplanetas, un valor menor al reportado por la NASA y más cercano a los exoplanetas reales descubiertos.

Para este proyecto se consideran los exoplanetas pequeños como aquellos con radio menor a $2.5 R_{\oplus}$. 


# Resultados

Se realiza una consulta para identificar para cada método de descubrimiento cuál es el promedio de los planetas que descubren:

| Método de descubrimiento        | Promedio de radio $\overline{R_{\oplus}}$ | Cantidad de planetas descubiertos |
|---------------------------------|------------------|------------|
| Imaging                         | 19.067979        | 30         |
| Orbital Brightness Modulation   | 13.247917        | 1          |
| Radial Velocity                 | 4.248897         | 32         |
| Transit                         | 6.689011         | 4302       |
| Transit Timing Variations       | 2.776713         | 13         |


Se observa que el método de descubrimiento más eficiente para encontrar planetas es el método de tránsito,
Ahora realizando un filtro por planetas rocosos pequeños ($R < 2.5 R_{\oplus}$) se obtiene: 

| Método de descubrimiento       | Promedio de radio $\overline{R_{\oplus}}$ | Cantidad de planetas descubiertos |
|-------------------------------|------------------|----------------|
| Radial Velocity               | 1.686156         | 17             |
| Transit                       | 1.676916         | 2241           |
| Transit Timing Variations     | 1.690909         | 8              |

Al igual que el caso anterior se observa que el método de tránsito es el más eficiente para encontrar planetas rocosos pequeños.



# Referencias

[1] NASA. (s.f.). Exoplanets. NASA Science Exoplanets. Recuperado el 22 de abril de 2026, de https://science.nasa.gov/exoplanets/


