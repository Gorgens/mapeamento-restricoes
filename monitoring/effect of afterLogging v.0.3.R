require(ggplot2)                                 # Activate packages
require(gridExtra)
require(grid)
require(ggpubr)
require(raster)

# Function ---------------

fig_label <- function(text, region="figure", pos="topleft", cex=NULL, ...) {
  
  region <- match.arg(region, c("figure", "plot", "device"))
  pos <- match.arg(pos, c("topleft", "top", "topright", 
                          "left", "center", "right", 
                          "bottomleft", "bottom", "bottomright"))
  
  if(region %in% c("figure", "device")) {
    ds <- dev.size("in")
    # xy coordinates of device corners in user coordinates
    x <- grconvertX(c(0, ds[1]), from="in", to="user")
    y <- grconvertY(c(0, ds[2]), from="in", to="user")
    
    # fragment of the device we use to plot
    if(region == "figure") {
      # account for the fragment of the device that 
      # the figure is using
      fig <- par("fig")
      dx <- (x[2] - x[1])
      dy <- (y[2] - y[1])
      x <- x[1] + dx * fig[1:2]
      y <- y[1] + dy * fig[3:4]
    } 
  }
  
  # much simpler if in plotting region
  if(region == "plot") {
    u <- par("usr")
    x <- u[1:2]
    y <- u[3:4]
  }
  
  sw <- strwidth(text, cex=cex) * 60/100
  sh <- strheight(text, cex=cex) * 60/100
  
  x1 <- switch(pos,
               topleft     =x[1] + sw, 
               left        =x[1] + sw,
               bottomleft  =x[1] + sw,
               top         =(x[1] + x[2])/2,
               center      =(x[1] + x[2])/2,
               bottom      =(x[1] + x[2])/2,
               topright    =x[2] - sw,
               right       =x[2] - sw,
               bottomright =x[2] - sw)
  
  y1 <- switch(pos,
               topleft     =y[2] - sh,
               top         =y[2] - sh,
               topright    =y[2] - sh,
               left        =(y[1] + y[2])/2,
               center      =(y[1] + y[2])/2,
               right       =(y[1] + y[2])/2,
               bottomleft  =y[1] + sh,
               bottom      =y[1] + sh,
               bottomright =y[1] + sh)
  
  old.par <- par(xpd=NA)
  on.exit(par(old.par))
  
  text(x1, y1, text, cex=cex, ...)
  return(invisible(c(x,y)))
}

# Teste de influência do tempo após a colheita nos indicadores ---------------

indicators = read.csv("indicators.csv")          # Import data
  names(indicators)                              # Check header and variable names                           

f.top = glm(top ~ after, data = indicators, family = gaussian(link = "log"))      # effect of after over TOP
  summary(f.top)                                                                  # check the significance of the coefficient
    
f.agb = glm(agb ~ after, data = indicators, family = gaussian(link = "log"))      # effect of after over AGB
  summary(f.agb)                                                                  # check the significance of the coefficient

f.gap = glm(gap ~ after, data = indicators, family = quasibinomial())             # effect of after over GAP
  summary(f.gap)                                                                  # check the significance of the coefficient

f.lrd = glm(lrd ~ poly(after,2), data = indicators, family = quasibinomial())             # effect of after over LRD
  summary(f.lrd)                                                                  # check the significance of the coefficient
  
  
# Figura 1

g1 = ggplot(indicators, aes(after, top)) + geom_point() + geom_smooth(se = TRUE, colour = "black") + theme_bw() + 
  xlab("Time after logging (years)") + ylab(expression(paste("TOP (ind .", ha^{-1}, ")", sep=" "))) +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        axis.line = element_line(colour = "black"))

g2 = ggplot(indicators, aes(after, agb)) + geom_point() + geom_smooth(se = TRUE, colour = "black") + theme_bw() + 
  xlab("Time after logging (years)") + ylab(expression(paste("AGB (kg .", m^{-2}, ")", sep=" "))) +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        axis.line = element_line(colour = "black"))

g3 = ggplot(indicators, aes(after, gap)) + geom_point() + geom_smooth(se = TRUE, colour = "black") + theme_bw() + 
  xlab("Time after logging (years)") + ylab(expression(paste("GAP (ha .", ha^{-1}, ")", sep=" "))) +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        axis.line = element_line(colour = "black"))


g4 = ggplot(indicators, aes(after, lrd)) + geom_point() + geom_smooth(se = TRUE, colour = "black") +
  xlab("Time after logging (years)") + ylab(expression(paste("LRD (ha .", ha^{-1}, ")", sep=" "))) +
  theme_bw() + theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        axis.line = element_line(colour = "black"))

jpeg("figure1.jpg", width = 20, height = 20, units = "cm", res = 300)
ggarrange(g1, g2, g3, g4,
          labels = c("a", "b", "c", "d"),
          ncol = 2, nrow = 2)
dev.off()


# Figura 2 - AGB --------------------

chm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_3/chm", full.names = TRUE)
chm_list2 = lapply(chm_list, raster)
chm = do.call(merge, chm_list2)
kernel = matrix(1,3,3)
schm = raster::focal(chm, w = kernel, fun = median, na.rm = TRUE)
tch = aggregate(schm, fact = 100, fun = mean)
AGB3 = (0.054 * tch ^ 1.76)*2

chm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_5/chm", full.names = TRUE)
chm_list2 = lapply(chm_list, raster)
chm = do.call(merge, chm_list2)
kernel = matrix(1,3,3)
schm = raster::focal(chm, w = kernel, fun = median, na.rm = TRUE)
tch = aggregate(schm, fact = 100, fun = mean)
AGB5 = (0.054 * tch ^ 1.76)*2

jpeg("figure2.jpg", width = 20, height = 12, units = "cm", res = 300)
par(mfrow=c(1,2))
plot(AGB3, col = grey(seq(1, 0, length =256)))
fig_label("a", cex=2) 

plot(AGB5, col = grey(seq(1, 0, length =256)))
fig_label("b", cex=2) 
dev.off()

# Figura 3 - GAP ---------------
chm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_2/chm", full.names = TRUE)
chm_list2 = lapply(chm_list, raster)
chm = do.call(merge, chm_list2)
kernel = matrix(1,3,3)
schm = raster::focal(chm, w = kernel, fun = median, na.rm = TRUE)
m = c(0, 10, 1,  10, 100, 0)
GAP2 = reclassify(schm, m)

chm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_6/chm", full.names = TRUE)
chm_list2 = lapply(chm_list, raster)
chm = do.call(merge, chm_list2)
kernel = matrix(1,3,3)
schm = raster::focal(chm, w = kernel, fun = median, na.rm = TRUE)
m = c(0, 10, 1,  10, 100, 0)
GAP6 = reclassify(schm, m)

jpeg("figure3.jpg", width = 20, height = 12, units = "cm", res = 300)
par(mfrow=c(1,2))
plot(GAP6, col = grey(seq(1, 0, length = 2)), legend = FALSE)
fig_label("a", cex=2) 

plot(GAP2, col = grey(seq(1, 0, length = 2)), legend = FALSE)
fig_label("b", cex=2) 
dev.off()

# Figura 4 - LRD ------------------
rdm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_8/rdm", full.names = TRUE)
rdm_list2 = lapply(rdm_list, raster)
rdm = do.call(merge, rdm_list2)
m = c(-1, 0.1, 1,  0.1, 2, 0)  
LRD = reclassify(rdm, m)
kernel = matrix(1,3,3)
LRD = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)
LRD = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)
LRD8 = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)

rdm_list = list.files("D:/Dados de Usuario/Downloads/manuscript monitoring SFM/las processed/UPA_7/rdm", full.names = TRUE)
rdm_list2 = lapply(rdm_list, raster)
rdm = do.call(merge, rdm_list2)
m = c(-1, 0.1, 1,  0.1, 2, 0)  
LRD = reclassify(rdm, m)
kernel = matrix(1,3,3)
LRD = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)
LRD = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)
LRD7 = raster::focal(LRD, w = kernel, fun = median, na.rm = TRUE)

jpeg("figure4.jpg", width = 20, height = 12, units = "cm", res = 300)
par(mfrow=c(1,2))
plot(LRD7, col = grey(seq(1, 0, length = 2)), legend = FALSE)
fig_label("a", cex=2) 

plot(LRD8, col = grey(seq(1, 0, length = 2)), legend = FALSE)
fig_label("b", cex=2) 
dev.off()
