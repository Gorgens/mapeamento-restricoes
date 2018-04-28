# http://datascienceplus.com/perform-logistic-regression-in-r/
require(ggplot2)

#Ajustar função logística -------
logit.sub1 <- glm(tipo ~.,family=binomial(link='logit'),data.sub.logit[,c(1, 3)])
summary(logit.sub1)
logit.sub2 <- glm(tipo ~.,family=binomial(link='logit'),data.sub.logit[,c(1, 4)])
summary(logit.sub2)

# Criação do mapa ---------------

#PATH.MAPA = "C:\\Users\\gorge\\Dropbox\\3d4st Lab\\2016 Alessandra Projeto Sub-bosque\\11 Análise\\projetos\\"
PATH.MAPA = "./"

# Importar mapa
mapa = read.csv(paste(PATH.MAPA,"NEPIAL00248_Serra_all_returns.csv", sep=""))
# mapa = read.csv(paste(PATH.MAPA,"RDPOPO00454_Varao_all_returns.csv", sep=""))
# mapa = read.csv(paste(PATH.MAPA,"RDPOPO00435_Januaria_all_returns.csv", sep=""))
# mapa = read.csv(paste(PATH.MAPA,"NEPIAL00211_Morro_Agudo_all_returns.csv", sep=""))

#mapa = mapa[mapa$total.pt.count > 100,]
colnames(mapa) = c("row", "col", "max.ht", "total.pt", as.character(seq(0.5, dim(mapa)[2]-4, 1)))

# Ajustar weibull
library('fitdistrplus')
library('reshape2')

scale.s = NA
shape.s = NA
scale.c = NA
shape.c = NA

hbreak = 0.5

for (i in seq(1, dim(mapa)[1],1)){
  print(i)
  chp.celula = melt(mapa[i,-c(1:4)])
  chp.celula[,1] = (as.numeric(chp.celula[,1]) - 0.5) / (ceiling(mapa[i,"max.ht"])-0.5)

  # Subbosque
  
  sub.temp = chp.celula[chp.celula$variable <= hbreak,]
  chp.celula.sub = rep(sub.temp[,1],sub.temp[,2])
  
  if(sum(sub.temp$value) > 100 & dim(sub.temp)[1] > 1){
    tryCatch({params = fitdist(as.numeric(chp.celula.sub), "weibull")
              scale.s[i] = params$estimate[2]
              shape.s[i] = params$estimate[1]
    }, error=function(e){
      scale.s[i] = 0
      shape.s[i] = 0
    })
  } else {
    scale.s[i] = 0
    shape.s[i] = 0
  }
  
  # copa
  
  copa.temp = chp.celula[chp.celula$variable >= hbreak & chp.celula$variable <= 1, ]
  chp.celula.copa = rep(copa.temp[,1],copa.temp[,2])
  
  if(sum(copa.temp$value) > 100 & dim(copa.temp)[1] > 1){
    tryCatch({params = fitdist(as.numeric(chp.celula.copa), "weibull")
              scale.c[i] = params$estimate[2]
              shape.c[i] = params$estimate[1]   
    }, error=function(e){
      scale.c[i] = 0
      shape.c[i] = 0
    })
  } else {
    scale.c[i] = 0
    shape.c[i] = 0
  }
}

rm(chp.celula, copa.temp, sub.temp, chp.celula.copa, chp.celula.sub, i, params)

# Mapear plantadas ----------------------

mapa = cbind(mapa, scale.s, shape.s, scale.c, shape.c)
rm(scale.s, scale.c, shape.s, shape.c)

level.sub = NA
for (i in seq(1, dim(mapa)[1], 1)){
  print(i)
  if (is.na(mapa$scale.c[i]) & is.na(mapa$shape.c[i])) {
    level.sub[i] = -9999
  } else if  (is.na(mapa$scale.s[i]) & is.na(mapa$shape.s[i])) {
    level.sub[i] = -9999
  } else if (mapa$scale.s[i] == 0 & mapa$shape.s[i] == 0 & mapa$scale.c[i] == 0 & mapa$shape.c[i] == 0) {
    level.sub[i] = -9999
  } else if (mapa$scale.c[i] == 0 & mapa$shape.c[i] == 0) {
    level.sub[i] = -9999
  } else if (mapa$scale.s[i] == 0 & mapa$shape.s[i] == 0) {
    level.sub[i] = -9999
  } else {
    level.sub[i] = predict(logit.sub2, newdata=data.frame(shape.s = mapa$shape.s[i]),type='response')
  }
}
rm(i)

#mapa$level.nat = level.nat
mapa = cbind(mapa, level.sub)

mp <- ggplot(data=mapa[mapa$level.sub > 0,], aes(y=row, x=col)) 
mp + geom_raster(aes(fill=level.sub))
