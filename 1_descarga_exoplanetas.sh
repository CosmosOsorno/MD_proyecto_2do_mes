ADQL="SELECT pl_name, discoverymethod, disc_facility, AVG(pl_rade) AS pl_rade, AVG(pl_eqt) AS pl_eqt, AVG(pl_orbsmax) AS pl_orbsmax, AVG(st_teff) AS st_teff, AVG(st_lum) AS st_lum FROM ps WHERE pl_rade IS NOT NULL AND pl_eqt IS NOT NULL GROUP BY pl_name, discoverymethod, disc_facility ORDER BY pl_name"

URL_ADQL=$(echo $ADQL | sed 's/ /+/g')

TAP_URL="https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

wget -O consulta.csv "$TAP_URL$URL_ADQL&amp;format=csv"

grep -v '^#' consulta.csv > exoplanetas_bruto.csv

rm consulta.csv
