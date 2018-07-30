'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\slope.py')
'''

def slope(ASCDTM = "upa6dtm.asc", SLOPE = "upa6slope.tif", RULESKIDDER = "ruleSkidder.txt", SKIDDEREST = "upa6SkidderCost.tif", RULETRUCK = "ruleTruck.txt", TRUCKREST = "upa6TruckCost.tif", INPATH = "C:\\FUSION\\daad\\", OUTPATH = "C:\\FUSION\\daad\\", EPSG = 31982):
	
	import subprocess
	import os
	from osgeo import ogr
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	print "Loading digital terrain model."
	dtmlayer = QgsRasterLayer(INPATH+ASCDTM, "mdt")
	dtmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(dtmlayer)
	extent = dtmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	print "Computing slope."
	processing.runalg("grass7:r.slope", dtmlayer, 0, False, 1, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+SLOPE)
	slopelayer = QgsRasterLayer(OUTPATH+SLOPE, "slope")
	slopelayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(slopelayer)
	
	if RULESKIDDER != None:
		print "Computing skidder surface cost."
		processing.runalg("grass7:r.reclass", slopelayer, INPATH+RULESKIDDER, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+SKIDDEREST)
		skidderlayer = QgsRasterLayer(OUTPATH+SKIDDEREST, "skidder cost")
		skidderlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(skidderlayer)
	
	if RULETRUCK != None:	
		print "Computing load truck surface cost."
		processing.runalg("grass7:r.reclass", slopelayer, INPATH+RULETRUCK, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+TRUCKREST)
		trucklayer = QgsRasterLayer(OUTPATH+TRUCKREST, "truck cost")
		trucklayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(trucklayer)

	print "Cleaning QGIS canvas."
	QgsMapLayerRegistry.instance().removeMapLayer(dtmlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(slopelayer.id())
	
	return "Done!"
