'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\drainage.py')

Implementar:
- calculo de buffer
- distancia de drenagem
- custo relacionado a distancia de drenagem
'''

def drainage(ASCDTM = "upa6dtm.asc", RSTREAM = "upa6stream.tif", IDSTREAM = "upa6streamId.shp", DIRECTION = "upa6direction.tif", VSTREAM = "upa6stream.shp", DISTANCE = "upa6horDistance.tif", NEAREST = "upa6nearestCell.tif", COSTDIST = "upa6drainageCost.tif", INPATH = "C:\\FUSION\\daad\\", OUTPATH = "C:\\FUSION\\daad\\", MINFLOW = 55000, EPSG = 31982):
	
	import subprocess
	import os
	from osgeo import ogr
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	print "Loading the digital terrain model."
	dtmlayer = QgsRasterLayer(INPATH+ASCDTM, "mdt")
	dtmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(dtmlayer)
	extent = dtmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	print "Extracting drainage network."
	processing.runalg("grass7:r.stream.extract", dtmlayer, "", "", MINFLOW, 0, 0, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, 0, OUTPATH+RSTREAM, OUTPATH+IDSTREAM, OUTPATH+DIRECTION)
	streamlayer = QgsRasterLayer(OUTPATH+RSTREAM, "stream")
	streamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(streamlayer)
	
	print "Converting drainage raster to vector."
	processing.runalg("grass7:r.to.vect", streamlayer, 0, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+VSTREAM)
	vstreamlayer = QgsVectorLayer(OUTPATH+VSTREAM, "vector stream", "ogr")
	vstreamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(vstreamlayer)
	
	print "Extracting horizontal distance to drainage."
	processing.runalg("grass7:r.grow.distance", streamlayer, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+DISTANCE, OUTPATH+NEAREST)
	hordistance = QgsRasterLayer(OUTPATH+DISTANCE, "hor distance")
	hordistance.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(hordistance)
	
	print "Creating cost surface based on to horizontal distance."
	extent = hordistance.extent()
	provider = hordistance.dataProvider()
	stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)
	MAX = str(round(stats.maximumValue))
	processing.runalg("saga:rastercalculator", hordistance, None, '"('+MAX+'-a)/'+MAX+'"', 3, False, 7, OUTPATH+COSTDIST)	
	costdrainage = QgsRasterLayer(OUTPATH+COSTDIST, "cost drainage dist")
	costdrainage.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(costdrainage)
	
	print "Cleaning QGIS canvas."
	QgsMapLayerRegistry.instance().removeMapLayer(dtmlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(hordistance.id())
	QgsMapLayerRegistry.instance().removeMapLayer(streamlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(vstreamlayer.id())
	
	return "Done!"
