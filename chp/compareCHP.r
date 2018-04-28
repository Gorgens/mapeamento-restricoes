compareCHP = function(x, y = NA, hbreak = 3){
  
  # Variaveis do ambiente
  PLOT = x
  PLOT2 = y
  #source("ReadLAS.r")
  
  # Ativando pacotes
  #require(rgl)
  require(tools)
  require(ggplot2)
  require(gridExtra)
  require(rLiDAR)
  require(MASS)
  
  if (file_ext(PLOT) == "las"){
    ## Para PLOT 1 -----------
    plot.las = as.data.frame(readLAS(PLOT))
    
    # Adjust negative values as ground
    for (i in row.names(plot.las[plot.las$Z < 0, ])){
      
      plot.las[as.numeric(i),"Z"] = 0 
      
    }
    
    # Prepara grafico 3D
    # open3d(windowRect=c(100,100,800,800))
    # plot3d(plot.las$X, plot.las$Y, plot.las$Z, 
    #        col = "darkgreen", 
    #        alpha = 1/10,
    #        xlab = "X coord. (m)",
    #        ylab = "Y coord. (m)",
    #        zlab = "Elevation (m)",
    #        axes = FALSE)
    # axes3d(edges=c("x--", "y--", "z-+"))
    #rgl.postscript("cloud.eps")
    
    # Gr?fico 2D
    #tiff("2b TwoDimention.tif", width = 15, height = 10, units = "cm", res = 600)
    g1d = ggplot(plot.las, aes(X, Z)) + 
      geom_point(alpha = 1/10, colour = "darkgreen", size = 0.8) +
      #geom_point(colour = "darkgreen", size = 0.8) +
      xlab("X Coordinate") + ylab("Height above ground") +
      ylim(0, 80) +
      theme(legend.background = element_blank(), 
            legend.key = element_blank(),
            panel.grid.minor = element_blank(),
            panel.grid.major = element_blank(),
            panel.background = element_blank(),
            panel.border = element_blank(),
            strip.background = element_blank(),
            plot.background = element_blank())
    #dev.off()
    
    # Histograma
    #tiff("2c canopyHist.tif", width = 8, height = 10, units = "cm", res = 600)
    g1hist = ggplot(plot.las, aes(Z)) +
      geom_histogram(binwidth = 1, fill = "black") + coord_flip() +
      xlab("Height above ground") + ylab("Frequency") +
      xlim(0, 80) +
      theme(legend.background = element_blank(), legend.key = element_blank(),
            panel.grid.minor = element_blank(),
            panel.grid.major = element_blank(),
            panel.background = element_blank(),
            panel.border = element_blank(),
            strip.background = element_blank(),
            plot.background = element_blank())
    #dev.off()
    
    # Weibull para subbosque
    subBosque <- plot.las[plot.las$Z<=hbreak & plot.las$Z > 0,]
    if(dim(subBosque)[1] > 20){
      fit.sub <- fitdistr(subBosque$Z, "weibull", start=list(scale=mean(subBosque$Z),shape=sd(subBosque$Z)))
      w2 = dweibull(seq(0.1, hbreak, 0.1), 
                    shape = fit.sub$estimate[2], 
                    scale = fit.sub$estimate[1]) * dim(subBosque)[1] / dim(plot.las)[1]
    } else {
      w2 = NA
      fit.sub$estimate = c(scale = 0, shape = 0)
    }
    
    # Weibull para copa
    copa <- plot.las[plot.las$Z>hbreak,]
    if(dim(copa)[1] > 20){
      fit.copa <- fitdistr(copa$Z, "weibull", start=list(scale=mean(copa$Z),shape=sd(copa$Z)))
      w1 = dweibull(seq(hbreak+0.1, max(copa$Z), 0.1), 
                    shape = fit.copa$estimate[2], 
                    scale = fit.copa$estimate[1]) * dim(copa)[1] / dim(plot.las)[1]
    } else {
      w1 = NA
      fit.copa = fit.sub
      fit.copa$estimate = c(scale = 0, shape = 0)
    }
    
    # Weibull geral
    
    if(is.na(w1)){
      weibull = data.frame(x = c(seq(0.1, hbreak, 0.1)), prob = c(w2))
    } else if(is.na(w2)){
      weibull = data.frame(x = c(seq(hbreak+0.1, max(copa$Z), 0.1)), prob = c(w1))
    } else {
      weibull = data.frame(x = c(seq(0.1, hbreak, 0.1), seq(hbreak+0.1, max(copa$Z), 0.1)), prob = c(w2, w1))
    }
    
    w1g = ggplot(weibull, aes(x, prob)) + 
      geom_line() +
      ylab("Probability") +
      xlab("Height (m)") +
      xlim(0, 80) +
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
    
    if (!is.na(PLOT2)){
      if (file_ext(PLOT2) == "las"){
        ## Para PLOT 2 -----------
        plot2.las = as.data.frame(readLAS(PLOT2))
        
        # Adjust negative values as ground
        for (i in row.names(plot2.las[plot2.las$Z < 0, ])){
          
          plot2.las[as.numeric(i),"Z"] = 0 
          
        }
        
        # Prepara gr?fico 3D
        # open3d(windowRect=c(100,100,800,800))
        # plot3d(plot2.las$X, plot2.las$Y, plot2.las$Z, 
        #        col = "darkgreen", 
        #        alpha = 1/10,
        #        xlab = "X coord. (m)",
        #        ylab = "Y coord. (m)",
        #        zlab = "Elevation (m)",
        #        axes = FALSE)
        # axes3d(edges=c("x--", "y--", "z-+"))
        # #rgl.postscript("cloud.eps")
        
        # Gr?fico 2D
        #tiff("2b TwoDimention.tif", width = 15, height = 10, units = "cm", res = 600)
        g2d = ggplot(plot2.las, aes(X, Z)) + 
          geom_point(alpha = 1/10, colour = "darkgreen", size = 0.8) +
          #geom_point(colour = "darkgreen", size = 0.8) +
          xlab("X Coordinate") + ylab("Height above ground") +
          ylim(0, 80) +
          theme(legend.background = element_blank(), 
                legend.key = element_blank(),
                panel.grid.minor = element_blank(),
                panel.grid.major = element_blank(),
                panel.background = element_blank(),
                panel.border = element_blank(),
                strip.background = element_blank(),
                plot.background = element_blank())
        #dev.off()
        
        # Histograma
        #tiff("2c canopyHist.tif", width = 8, height = 10, units = "cm", res = 600)
        g2hist = ggplot(plot2.las, aes(Z)) +
          geom_histogram(binwidth = 1, fill = "black") + coord_flip() +
          xlab("Height above ground") + ylab("Frequency") +
          xlim(0, 80) +
          theme(legend.background = element_blank(), legend.key = element_blank(),
                panel.grid.minor = element_blank(),
                panel.grid.major = element_blank(),
                panel.background = element_blank(),
                panel.border = element_blank(),
                strip.background = element_blank(),
                plot.background = element_blank())
        #dev.off()
        
        # Weibull para subbosque
        subBosque2 <- plot2.las[plot2.las$Z<=hbreak & plot2.las$Z > 0,]
        if(dim(subBosque2)[1] > 20){
          fit.sub2 <- fitdistr(subBosque2$Z, "weibull", start=list(scale=mean(subBosque2$Z),shape=sd(subBosque2$Z)))
          w2 = dweibull(seq(0.1, hbreak, 0.1), shape = fit.sub2$estimate[2], scale = fit.sub2$estimate[1]) * dim(subBosque2)[1] / dim(plot2.las)[1]
        } else {
          w2 = NA
          fit.sub2$estimate = c(scale = 0, shape = 0)
        }
        
        # Weibull para copa
        copa2 <- plot2.las[plot2.las$Z>hbreak,]
        if(dim(copa2)[1] > 20){
          fit.copa2 <- fitdistr(copa2$Z, "weibull", start=list(scale=mean(copa2$Z),shape=sd(copa2$Z)))
          w1 = dweibull(seq(hbreak+0.1, max(copa2$Z), 0.1), shape = fit.copa2$estimate[2], scale = fit.copa2$estimate[1]) * dim(copa2)[1] / dim(plot2.las)[1]
        } else {
          w1 = NA
          fit.copa2 = fit.sub2
          fit.copa2$estimate = c(scale = 0, shape = 0)
        }  

        # Weibull geral
        if(is.na(w1)){
          weibull2 = data.frame(x = c(seq(0.1, hbreak, 0.1)), prob = c(w2))
        } else if(is.na(w2)){
          weibull2 = data.frame(x = c(seq(hbreak+0.1, max(copa2$Z), 0.1)), prob = c(w1))
        } else {
          weibull2 = data.frame(x = c(seq(0.1, hbreak, 0.1), seq(hbreak+0.1, max(copa2$Z), 0.1)), prob = c(w2, w1))
        }
        
        w2g = ggplot(weibull2, aes(x, prob)) + 
          geom_line() +
          ylab("Probability") +
          xlab("Height (m)") +
          xlim(0, 80) +
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
        
        #tiff("canopy profile.tif", width = 50, height = 30, units = "cm", res = 72)
        result = list()
        #dev.off()
        graph = grid.arrange(g1d, g1hist, w1g, g2d, g2hist, w2g, nrow = 2, ncol = 3, 
                             top = paste(PLOT, " and ", PLOT2))
        print(graph)
        result[[1]] = graph
        # Compara as duas distribuicoes
        result[[2]] = ks.test(plot.las$Z,plot2.las$Z)
        result[[3]] = fit.sub
        result[[4]] = fit.copa
        result[[5]] = fit.sub2
        result[[6]] = fit.copa2
        
        return(result)
      } else {"y should be a las file!"}
    } else {
      result = list()
      #tiff("canopy profile.tif", width = 50, height = 30, units = "cm", res = 72)
      graph = grid.arrange(g1d, g1hist, w1g, nrow = 1, ncol = 3, top = paste(PLOT))
      print(graph)
      result[[1]] = graph
      result[[2]] = fit.sub
      result[[3]] = fit.copa
      
      return(result)
      #dev.off()
    }
  } else {
    print("x should be a las file!")
  }
}
