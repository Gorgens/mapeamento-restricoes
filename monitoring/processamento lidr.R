#
# Author: Prof. Eric Bastos Gorgens
# Title: Extreção de árvores usando o LiDR - Transecto
#
############################################################################33

require(lidR)
require(magrittr)
require(dynatopmodel)
require(raster)

rm(list = ls(globalenv()))
gc()

PATH = "C:\\Users\\gorge\\Documents\\GIS DataBase\\cauaxi\\"

# Importa o catalog do transecto -------------------------------------------
ctg = catalog(paste(PATH, 'upa3.laz', sep=""))
projection(ctg) = '+init=epsg:31982'

#summary(ctg)
opt_chunk_size(ctg) = 100         # define o tamanho em metros do tile
opt_chunk_buffer(ctg) = 5         # define o buffer em metros de cada tile

opt_output_files(ctg) = paste(PATH, "gnd\\gnd_{ID}", sep="")
ctg %>% plot(chunk_pattern = TRUE)

# Filtra pontos do terreno -------------

gndClassification = function(cloud){
  las = cloud %>% readLAS()
  if(is.empty(las)) return(NULL)
  lascsf = las %>% lasground(csf())
  lascsf %<>% lasfilter(buffer == 0)
  return(lascsf)
}

lascsf_list = catalog_apply(ctg, gndClassification)


# Cria o mdt -----------------------------------------------
ctg = catalog(paste(PATH, "gnd\\", sep=""))

opt_output_files(ctg) = paste(PATH, "dtm\\dtm_{ID}", sep="")
ctg %>% plot(chunk_pattern = TRUE)

dtmCreation = function(cloud)
{
  lascsf = cloud %>% readLAS()
  if(is.empty(lascsf)) return(NULL)
  dtm = lascsf %>% grid_terrain(1, knnidw())
  return(dtm)
}

dtm_list = catalog_apply(ctg, dtmCreation)

dtm_list2 = lapply(dtm_list,raster)
dtm = do.call(merge, dtm_list2)
plot(dtm)

# Normaliza a nuvem --------------------
ctg = catalog(paste(PATH, "gnd\\", sep=""))

opt_output_files(ctg) = paste(PATH, "norm\\norm_{ID}", sep="")
ctg %>% plot(chunk_pattern = TRUE)

normalization = function(cloud)
{
  lascsf = cloud %>% readLAS()
  if(is.empty(lascsf)) return(NULL)
  lasnorm = lascsf %>% lasnormalize(knnidw())
  lasnorm %<>% lasfilter(buffer == 0)             # remover buffer
  return(lasnorm)
}

lasnorm_list = catalog_apply(ctg, normalization)

# Cria CHM ---------------------
ctg = catalog(paste(PATH, "norm\\", sep=""))

opt_output_files(ctg) = paste(PATH, "chm\\chm_{ID}", sep="")
ctg %>% plot(chunk_pattern = TRUE)

chmCreation = function(cloud)
{
  lasnorm = cloud %>% readLAS()
  if(is.empty(lasnorm)) return(NULL)
  chm = lasnorm %>% grid_canopy(0.5, p2r(subcircle = 0.15))
  return(chm)
}

chm_list = catalog_apply(ctg, chmCreation)

chm_list2 = lapply(chm_list, raster)
chm = do.call(merge, chm_list2)
plot(chm)

# Extrai top trees ------------------
kernel = matrix(1,3,3)
schm = raster::focal(chm, w = kernel, fun = median, na.rm = TRUE)
ttops = tree_detection(schm, lmf(30))   # Encontrar pontos de máximo
  head(ttops)
  length(ttops)
ttops = ttops[ttops$Z>35,]
  col1 = height.colors(50)
  plot(schm, col = col1)
  plot(ttops, col = "black", add = T)

# Limpar memória -----------------
rm(ctg, chm_list2, dtm_list2, lascsf_list, lasnorm_list, kernel)
  
  
# Calcula área de clareiras ---------------
m = c(0, 10, 1,  10, 100, 0)
gaps = reclassify(schm, m)
  plot(gaps)

freq(gaps, value = 1) * 1      # área de clareiras em hectares

# Calcula biomassa acima do solo via TCH ------------
tch = aggregate(schm, fact = 100, fun = mean)
  plot(tch)
BAS = 0.054 * tch ^ 1.76       # formula baseada em Longo et al.
  plot(BAS)
sum(BAS[])                     # biomassa total

# Calcula área de ramais ----------------
rdmComputation = function(z){
  zbase = z[z < 5]
  n = length(zbase)
  density = ifelse(n == 0, 2, length(zbase[zbase > 1]) / n )
  return(density)
}

ctg = catalog(paste(PATH, "norm\\", sep=""))

opt_output_files(ctg) = paste(PATH, "rdm\\rdm_{ID}", sep="")
ctg %>% plot(chunk_pattern = TRUE)

rdmCreation = function(cloud)
{
  lasnorm = cloud %>% readLAS()
  if(is.empty(lasnorm)) return(NULL)
  rdm = lasnorm %>% grid_metrics(rdmComputation(Z), 1)
  return(rdm)
}

rdm_list = catalog_apply(ctg, rdmCreation)

rdm_list2 = lapply(rdm_list, raster)
rdm = do.call(merge, rdm_list2)
  plot(rdm)

m = c(-1, 0.1, 1,  0.1, 2, 0)  
roads = reclassify(rdm, m)
  kernel = matrix(1,3,3)
  sroads = raster::focal(roads, w = kernel, fun = median, na.rm = TRUE)
  sroads = raster::focal(sroads, w = kernel, fun = median, na.rm = TRUE)
  sroads = raster::focal(sroads, w = kernel, fun = median, na.rm = TRUE)
  plot(sroads)
  
freq(sroads, value = 1) * 1        # área de estradas em ha
  