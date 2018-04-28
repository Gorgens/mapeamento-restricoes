source("CHPmodel.r")

PATH = "./plots2/"

data.sub.logit = data.frame(tipo = NA, maxh = NA, scale.s = NA, shape.s = NA, scale.c = NA, shape.c = NA)
#data.sub.logit = data.frame(tipo = NA, maxh = NA, scale.g = NA, shape.g = NA, scale.s = NA, shape.s = NA, scale.c = NA, shape.c = NA)

# Processar parcelas do projeto Serra -------------------
for (i in seq(1, 17, 1)){
  print(paste("serra_plot ", i, sep=""))
	saida = CHPmodel(paste(PATH, "serra_plot", i, ".las", sep=""), estrato=2)
	data.sub.logit[i, 1] = 1
	data.sub.logit[i, 2] = saida[[1]]
	data.sub.logit[i, 3] = saida[[2]]$estimate[1]
	data.sub.logit[i, 4] = saida[[2]]$estimate[2]
	data.sub.logit[i, 5] = saida[[3]]$estimate[1]
	data.sub.logit[i, 6] = saida[[3]]$estimate[2]
	#data.sub.logit[i, 7] = saida[[4]]$estimate[1]
	#data.sub.logit[i, 8] = saida[[4]]$estimate[2]
}

# Processar parcelas do projeto Januária ----------------
for (i in seq(1, 23, 1)){
  print(paste("jan_plot", i, sep=""))
  saida = CHPmodel(paste(PATH, "jan_plot", i, ".las", sep=""), estrato=2)
  data.sub.logit[17 + i, 1] = 0
  data.sub.logit[17 + i, 2] = saida[[1]]
  data.sub.logit[17 + i, 3] = saida[[2]]$estimate[1]
  data.sub.logit[17 + i, 4] = saida[[2]]$estimate[2]
  data.sub.logit[17 + i, 5] = saida[[3]]$estimate[1]
  data.sub.logit[17 + i, 6] = saida[[3]]$estimate[2]
  #data.sub.logit[17 + i, 7] = saida[[4]]$estimate[1]
  #data.sub.logit[17 + i, 8] = saida[[4]]$estimate[2]
}

# Explore logit relations -----------------


plot(data.sub.logit$maxh, data.sub.logit$tipo)

plot(data.sub.logit$shape.c, data.sub.logit$tipo)
plot(data.sub.logit$scale.c, data.sub.logit$tipo)

plot(data.sub.logit$shape.s, data.sub.logit$tipo)
plot(data.sub.logit$scale.s, data.sub.logit$tipo)

# Export paramters
write.csv(x = data.sub.logit, file = paste(PATH, "logit.csv", sep=""))
