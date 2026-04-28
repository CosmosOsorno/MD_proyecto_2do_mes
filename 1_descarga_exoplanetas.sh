ADQL="SELECT pl_name, discoverymethod, disc_facility, pl_rade, pl_eqt, pl_orbsmax, st_teff, st_lum FROM PSCompPars WHERE pl_rade IS NOT NULL AND pl_eqt IS NOT NULL ORDER BY pl_name"

URL_ADQL=$(echo $ADQL | sed 's/ /+/g')

TAP_URL="https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

wget -O consulta.csv "$TAP_URL$URL_ADQL&amp;format=csv"

grep -v '^#' consulta.csv > exoplanetas_bruto.csv

rm consulta.csv
