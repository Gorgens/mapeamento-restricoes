CHPmodel = function(input, output, hbreak = 0.5, hground = 0.25, estrato = 2, norm = TRUE){
  
  # Variaveis do ambiente
  PLOT = input

  # Ativando pacotes
  #require(rgl)
  require(tools)
  require(ggplot2)
  require(gridExtra)
  require(lidR)
  require(MASS)
  require(jpeg)
  
  ## Para PLOT 1 -----------
  plot.las = readLAS(PLOT)
  plot.las = plot.las@data
  
  # Adjust negative values as ground
  plot.las[plot.las$Z <= 0.01,'Z'] = 0.01
  
  hmin=0.01
  
  if (isTRUE(norm)){
    plot.las$Znorm = plot.las$Z / max(plot.las$Z)
    gmax = 1
    bin = 0.02
    step = 0.01
  } else {
    plot.las$Znorm = plot.las$Z
    gmax = max(plot.las$Z)
    hbreak = hbreak * gmax
    hground = hground * gmax
    hmin = hmin * gmax
    bin = 0.02 * gmax
    step = 0.01 * gmax
  }
  
  # Grafico 2D
  g1d = ggplot(plot.las, aes(X, Z)) + 
    geom_point(alpha = 1/10, colour = "darkgreen", size = 0.8) +
    #geom_point(colour = "darkgreen", size = 0.8) +
    xlab("X Coordinate") + ylab("Height above ground") +
    theme(legend.background = element_blank(), 
          legend.key = element_blank(),
          panel.grid.minor = element_blank(),
          panel.grid.major = element_blank(),
          panel.background = element_blank(),
          panel.border = element_blank(),
          strip.background = element_blank(),
          plot.background = element_blank())

  # Histograma
  g1hist = ggplot(plot.las, aes(Znorm)) +
    geom_histogram(binwidth = bin, fill = "black") + coord_flip() +
    xlab("Height above ground") + ylab("Frequency") +
    xlim(0, gmax) +
    theme(legend.background = element_blank(), legend.key = element_blank(),
          panel.grid.minor = element_blank(),
          panel.grid.major = element_blank(),
          panel.background = element_blank(),
          panel.border = element_blank(),
          strip.background = element_blank(),
          plot.background = element_blank())

  if (estrato == 3){
    # Weibull para copa
    copa <- plot.las[plot.las$Znorm>hbreak,]
    fit.copa <- fitdistr(copa$Znorm, "weibull", start=list(scale=mean(copa$Znorm),shape=sd(copa$Znorm)))
    w1 = dweibull(seq(hbreak+0.01, gmax, step), shape = fit.copa$estimate[2], scale = fit.copa$estimate[1]) * dim(copa)[1] / dim(plot.las)[1]
    
    # Weibull para subbosque
    subBosque <- plot.las[plot.las$Znorm <= hbreak & plot.las$Znorm > hground,]
    fit.sub <- fitdistr(subBosque$Znorm, "weibull", start=list(scale=mean(subBosque$Znorm),shape=sd(subBosque$Znorm)))
    w2 = dweibull(seq(hground + 0.01, hbreak, step), shape = fit.sub$estimate[2], scale = fit.sub$estimate[1]) * dim(subBosque)[1] / dim(plot.las)[1]
    
    # Weibull para ground
    ground <- plot.las[plot.las$Znorm <= hground & plot.las$Znorm >= hmin,]
    fit.gnd <- fitdistr(ground$Znorm, "weibull", start=list(scale=mean(ground$Znorm),shape=sd(ground$Znorm)))
    w3 = dweibull(seq(hmin, hground, step), shape = fit.gnd$estimate[2], scale = fit.gnd$estimate[1]) * dim(ground)[1] / dim(plot.las)[1]
    
    # Weibull geral
    weibull = data.frame(x = c(seq(hmin, hground, step), seq(hground + 0.01, hbreak, step), seq(hbreak+0.01, gmax, step)), prob = c(w3, w2, w1))
    w1g = ggplot(weibull, aes(x, prob)) + 
      geom_line() +
      ylab("Probability") +
      xlab("Height (m)") +
      xlim(0, gmax) +
      theme_bw() + 
      theme(legend.background = element_blank(), 
            legend.key = element_blank(),
            panel.grid.minor = element_blank(),
            panel.grid.major = element_blank(),
            panel.background = element_blank(),
            panel.border = element_blank(),
            strip.background = element_blank(),
            plot.background = element_blank()) +
      coord_flip()
    outlist = list(gmax, fit.gnd, fit.sub, fit.copa, g1d, g1hist, w1g)
    jpeg(output)
    grid.arrange(g1d, g1hist, w1g, nrow=1, ncol=3, top = paste(PLOT))
    dev.off()
    return(outlist)
    
    } else if (estrato == 2){
      
      # Weibull para copa
      copa <- plot.las[plot.las$Znorm>hbreak,]
      fit.copa <- fitdistr(copa$Znorm, "weibull", start=list(scale=mean(copa$Znorm),shape=sd(copa$Znorm)))
      w1 = dweibull(seq(hbreak+0.01, gmax, step), shape = fit.copa$estimate[2], scale = fit.copa$estimate[1]) * dim(copa)[1] / dim(plot.las)[1]
      
      # Weibull para subbosque
      subBosque <- plot.las[plot.las$Znorm <= hbreak & plot.las$Znorm >= hmin,]
      fit.sub <- fitdistr(subBosque$Znorm, "weibull", start=list(scale=mean(subBosque$Znorm),shape=sd(subBosque$Znorm)))
      w2 = dweibull(seq(hmin, hbreak, step), shape = fit.sub$estimate[2], scale = fit.sub$estimate[1]) * dim(subBosque)[1] / dim(plot.las)[1]
      
      # Weibull geral
      weibull = data.frame(x = c(seq(hmin, hbreak, step), seq(hbreak+0.01, gmax, step)), prob = c(w2, w1))
      w1g = ggplot(weibull, aes(x, prob)) + 
        geom_line() +
        ylab("Probability") +
        xlab("Height (m)") +
        xlim(0, gmax) +
        theme_bw() + 
        theme(legend.background = element_blank(), 
              legend.key = element_blank(),
              panel.grid.minor = element_blank(),
              panel.grid.major = element_blank(),
              panel.background = element_blank(),
              panel.border = element_blank(),
              strip.background = element_blank(),
              plot.background = element_blank()) +
        coord_flip()
      outlist = list(gmax, fit.sub, fit.copa, g1d, g1hist, w1g)
      jpeg(output)
      grid.arrange(g1d, g1hist, w1g, nrow=1, ncol=3, top = paste(PLOT))
      dev.off()
      return(outlist)
  
    } else {
    
      # Weibull para copa
      copa <- plot.las[plot.las$Znorm >= hmin,]
      fit.copa <- fitdistr(copa$Znorm, "weibull", start=list(scale=mean(copa$Znorm),shape=sd(copa$Znorm)))
      w1 = dweibull(seq(hmin, gmax, step), shape = fit.copa$estimate[2], scale = fit.copa$estimate[1]) * dim(copa)[1] / dim(plot.las)[1]
      
      # Weibull geral
      weibull = data.frame(x = seq(hmin, gmax, step), prob = w1)
      w1g = ggplot(weibull, aes(x, prob)) + 
        geom_line() +
        ylab("Probability") +
        xlab("Height (m)") +
        xlim(0, gmax) +
        theme_bw() + 
        theme(legend.background = element_blank(), 
              legend.key = element_blank(),
              panel.grid.minor = element_blank(),
              panel.grid.major = element_blank(),
              panel.background = element_blank(),
              panel.border = element_blank(),
              strip.background = element_blank(),
              plot.background = element_blank()) +
        coord_flip()
      outlist = list(gmax, fit.copa, g1d, g1hist, w1g)
      jpeg(output)
      grid.arrange(g1d, g1hist, w1g, nrow=1, ncol=3, top = paste(PLOT))
      dev.off()
      return(outlist)      
  }
}