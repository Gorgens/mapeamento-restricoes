# Author: Gorgens, E. B.
# Pourpose: Process LiDAR transects and extract trees of interest

# How to use: sh process_trans.sh NP_T-356 t356 35 6
# 1 = NP_T-356
# 2 = t356
# 3 = 35
# 4 = 6



# Criacao do MDT *******************
# Importar nuvem lidar criando um raster com pixels de 1 metro com respectivo valor minimo de elevacao
r.in.lidar -o -e --overwrite input=/home/gorgens/Documents/grassdata/INPE/d_universal/$1.las output=$2_min method=min resolution=1

#Definindo regiao de trabalho
g.region raster=$2_min@universal

# Aplicando filtro de suavizacao (primeiro minimo e segundo mediana) com janelas crescentes para obter MDT
r.neighbors --overwrite input=$2_min@universal output=$2_minfilt method=min size=7
r.neighbors --overwrite input=$2_minfilt@universal output=$2_mdt method=median size=11

# Corrigir depressoes espurias preenchidas
r.terraflow --overwrite elevation=$2_mdt@universal filled=$2_mdt_filled direction=$2_mdt_flowdirection swatershed=$2_mdt_watershed accumulation=$2_mdt_accumulation tci=$2_mdt_itu

# Gerar mapa de contorno
r.contour --overwrite input=$2_mdt_filled@universal output=$2_mdt_contour@universal step=3 cut=1000

# Calcular mapa de inclinacao e exposicao
r.slope.aspect --overwrite elevation=$2_mdt_filled@universal slope=$2_slope aspect=$2_aspect

# Suavizar o mapa de inclinacao
r.neighbors --overwrite input=$2_slope@universal output=$2_slope_soft method=median size=11

# Aplicar sombreamento
r.relief --overwrite input=$2_mdt@universal output=$2_shade altitude=45 azimuth=315



# Criacao dos hidrologicos  *******************
# Delimitacao de bacias com areas medias de 40 hectares
r.watershed --overwrite elevation=$2_mdt_filled@universal threshold=400000 basin=$2_basins

# Converter de raster para poligonos
r.to.vect --overwrite input=$2_basinss@universal output=$2_basins_vet type=area

# Extrair rede de drenagem e drenagem
r.watershed --overwrite elevation=$2_mdt_filled@universal threshold=120000 stream=$2_stream@universal drainage=$2_mdt_direction

# Instalar extensao para extrair a ordem
g.extension extension=r.stream.order

# Determinar ordem do curso de agua
r.stream.order stream_rast=$2_stream@universal direction=$2_mdt_direction elevation=$2_mdt_filled@universal strahler=$2_strahler --overwrite

# Afinar rede de drenagem
r.thin --overwrite input=$2_strahler@universal output=$2_strahler_thin

# Converter rede de drenagem para vetor
r.to.vect --overwrite input=$2_strahler_thin@universal output=$2_strahler_thin_vet type=line

# Instalar extensao para calacular distancias a rede de drenagem
g.extension extension=r.stream.distance

# Calcular distancias horizontal e vertical
r.stream.distance stream_rast=$2_strahler@universal direction=$2_mdt_direction@universal elevation=$2_mdt_filled@universal method=downstream distance=$2_distance_stream difference=$2_difference_stream --overwrite

# Instalar extensao para calculo de inundacao
g.extension extension=r.hazard.flood
g.extension extension=r.area

# Calcular area de sensibilidade
r.hazard.flood map=$2_mdt_filled@universal flood=$2_flood mti=$2_mti --overwrite

# Calcular regiao de cheias
r.lake --overwrite elevation=$2_mdt_filled@universal water_level=80 lake=$2_lake80 seed=$2_mdt_filled@universal

r.lake --overwrite elevation=$2_mdt_filled@universal water_level=85 lake=$2_lake85 seed=$2_mdt_filled@universal

r.lake --overwrite elevation=$2_mdt_filled@universal water_level=90 lake=$2_lake90 seed=$2_mdt_filled@universal

r.lake --overwrite elevation=$2_mdt_filled@universal water_level=95 lake=$2_lake95 seed=$2_mdt_filled@universal



# Criacao do MDS  *******************
# Importar nuvem lidar criando um raster com pixels de 1 metro com respectivo valor de percentil 95
r.in.lidar -o -e --overwrite input=/home/gorgens/Documents/grassdata/INPE/d_universal/$1.las output=$2_mds method=percentile pth=95 resolution=1



# Criacao do CHM  *******************
# Subtracao do MDS pelo MDT para obtencao de altura
r.mapcalc "$2_chm = $2_mds@universal - $2_mdt@universal" --overwrite

# Criar mascara das regioes menores que limiar de altura
r.mapcalc "$2_clareiras = ($2_chm@universal <= 10)" --overwrite

# Converter regioes em poligonos
r.to.vect -s --overwrite input=$2_clareiras@universal output=$2_clareiras_vet type=area

# Filtrar regioes do raster acima de um limiar de altura
r.mapcalc "$2_topcanopy = if( $2_chm@universal < $3 , null()  , $2_chm@universal)" --overwrite

# Criar um mascara das regioes acima de um limiar de altura
r.mapcalc "$2_topcanopyMask = if( $2_chm@universal < $3 , null()  , 1)" --overwrite

# Converter mascara de raster para poligonos
r.to.vect --overwrite input=$2_topcanopyMask@universal output=$2_topcanopy_vector type=area

# Adicionar a camada vetorial informacao de altura media do poligono
v.db.addcolumn map=$2_topcanopy_vector@universal columns="area_m DOUBLE PRECISION"
v.to.db map=$2_topcanopy_vector@universal option=area columns=area_m units=meters

# Filtrar poligonos inferiores a area minima
v.extract input=$2_topcanopy_vector@universal output=$2_topcanopy_vector6@universal where="area_m > $4"



# Exemplos para exportar raster *******************
r.out.gdal --overwrite input=$2_mdt_filled@universal output=/home/gorgens/Documents/grassdata/INPE/d_universal/CAU_flt_gdf_dtm$2_mdt_filled.tif format=GTiff

r.out.ascii --overwrite input=$2_chm@universal output=/home/gorgens/Documents/grassdata/INPE/d_universal/$2_chm precision=2 null_value=-9999
