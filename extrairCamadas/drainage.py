'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\drainage.py')
'''

def drainage(ASCDTM = "C:\\FUSION\\daad\\upa6dtm.asc", RSTREAM = "C:\\FUSION\\daad\\upa6stream.tif", IDSTREAM = "C:\\FUSION\\daad\\upa6streamId.shp", DIRECTION = "C:\\FUSION\\daad\\upa6direction.tif", VSTREAM = "C:\\FUSION\\daad\\upa6stream.shp", MINFLOW = 55000, EPSG = 31982):
	
	import subprocess
	import os
	from osgeo import ogr
	
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
	
	processing.runalg("grass7:r.stream.extract", dtmlayer, "", "", MINFLOW, 0, 0, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, 0, RSTREAM, IDSTREAM, DIRECTION)
	streamlayer = QgsRasterLayer(RSTREAM, "stream")
	streamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(streamlayer)
	
	processing.runalg("grass7:r.to.vect", streamlayer, 0, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, VSTREAM)
	vstreamlayer = QgsVectorLayer(VSTREAM, "vector stream", "ogr")
	vstreamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(vstreamlayer)
	
	
	return "Done!"
