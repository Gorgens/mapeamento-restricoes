'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\slope.py')
'''

def slope(ASCDTM = "C:\\FUSION\\daad\\upa6dtm.asc", SLOPE = "C:\\FUSION\\daad\\upa6slope.tif", RULESKIDDER = "C:\\FUSION\\daad\\ruleSkidder.txt", SKIDDEREST = "C:\\FUSION\\daad\\upa6restSkidder.tif", RULETRUCK = "C:\\FUSION\\daad\\ruleTruck.txt", TRUCKREST = "C:\\FUSION\\daad\\upa6restTruck.tif", EPSG = 31982):
	
	import subprocess
	import os
	from osgeo import ogr
	
	show = True
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	'carrega modelo digital de terreno'
	dtmlayer = QgsRasterLayer(ASCDTM, "mdt")
	dtmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(dtmlayer)
	extent = dtmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	processing.runalg("grass7:r.slope", dtmlayer, 0, False, 1, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, SLOPE)
	slopelayer = QgsRasterLayer(SLOPE, "slope")
	slopelayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(slopelayer)
	
	if RULESKIDDER != None:
		processing.runalg("grass7:r.reclass", slopelayer, RULESKIDDER, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, SKIDDEREST)
		skidderlayer = QgsRasterLayer(SKIDDEREST, "skidder")
		skidderlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(skidderlayer)
	
	if RULETRUCK != None:	
		processing.runalg("grass7:r.reclass", slopelayer, RULETRUCK, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, TRUCKREST)
		trucklayer = QgsRasterLayer(TRUCKREST, "truck")
		trucklayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(trucklayer)

	
	return "Done!"
