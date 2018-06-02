require(raster); require(Hmisc); require(directlabels); require(rgdal)

# ASC com NA representado por -9999

dtmFusion = raster("NP_T-403_dtm.asc")
plot(dtmFusion)

dtmGrass = raster("NP_T-403_dtm.asc")
plot(dtmGrass)

# RMSE
dtmFusion <- resample(dtmFusion, dtmGrass)
dtmDiff = dtmFusion - dtmGrass
dtmSqr <- calc(dtmDiff, fun=function(x){x * x})
sqrt(cellStats(dtmSqr, sum)/length(dtmDiff))

#KS test
dtmFusion = as(dtmFusion, "SpatialPixelsDataFrame")
dtmFusion = as.data.frame(dtmFusion)
colnames(dtmFusion) = c("value", "x", "y")

dtmGrass = as(dtmGrass, "SpatialPixelsDataFrame")
dtmGrass = as.data.frame(dtmGrass)
colnames(dtmGrass) = c("value", "x", "y")

ks.test(dtmFusion$value, dtmGrass$value)
