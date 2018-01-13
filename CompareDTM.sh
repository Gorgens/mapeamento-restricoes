# Criar modelo digital de terreno com 1 metros de resolução
# Algoritmo baseado em pontos mínimos e filtro de suavização com duas passagens

# Premissas:
# 1. GRASS instalado
# 2. Os produtos deverão ser utilizados dentro do GRASS
# 3. Nuvem de pontos na pasta do 'c:\grass', na subpasta 'data'


r.in.lidar -o -e --overwrite input=c:\grass\data\NP_T-403.las output=NP_T-403_min method=min resolution=1
g.region raster=NP_T-403_min@universal
r.neighbors --overwrite input=NP_T-403_min@universal output=NP_T-403_mdt method=min size=7
r.neighbors --overwrite input=NP_T-403_mdt@universal output=NP_T-403_mdt_v2 method=median size=11
