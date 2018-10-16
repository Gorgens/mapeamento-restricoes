'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\drainage.py')

Implementar:
- calculo de buffer
- distancia de drenagem
- custo relacionado a distancia de drenagem
'''

def drainage(ASCMDT = "upa6MDT.asc", RSTREAM = "upa6stream.tif", IDSTREAM = "upa6streamId.shp", DIRECTION = "upa6direction.tif", VSTREAM = "upa6stream.shp", MDH = "upa6mdh.tif", NEAREST = "upa6nearest.tif", MDCH = "upa6mch.tif", INPATH = "C:\\FUSION\\daad\\", OUTPATH = "C:\\FUSION\\daad\\", MINFLOW = 55000, EPSG = 31982, OPEN = True):
	
	import processing
	import subprocess
	import os
	from osgeo import ogr
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	print "Loading the digital terrain model."
	mdtlayer = QgsRasterLayer(INPATH+ASCMDT, "mdt")
	mdtlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(mdtlayer)
	extent = mdtlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	print "Extracting drainage network."
	processing.runalg("grass7:r.stream.extract", mdtlayer, "", "", MINFLOW, 0, 0, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, 0, OUTPATH+RSTREAM, OUTPATH+IDSTREAM, OUTPATH+DIRECTION)
	streamlayer = QgsRasterLayer(OUTPATH+RSTREAM, "stream")
	streamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(streamlayer)
	
	print "Converting drainage raster to vector."
	processing.runalg("grass7:r.to.vect", streamlayer, 0, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+VSTREAM)
	vstreamlayer = QgsVectorLayer(OUTPATH+VSTREAM, "vector stream", "ogr")
	vstreamlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(vstreamlayer)
	
	print "Extracting horizontal distance to drainage."
	processing.runalg("grass7:r.grow.distance", streamlayer, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+MDH, OUTPATH+NEAREST)
	mdhlayer = QgsRasterLayer(OUTPATH+MDH, "mdh")
	mdhlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(mdhlayer)
	
	print "Creating cost surface based on to horizontal distance."
	extent = mdhlayer.extent()
	provider = mdhlayer.dataProvider()
	stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)
	MAX = str(round(stats.maximumValue))
	processing.runalg("saga:rastercalculator", mdhlayer, None, '"('+MAX+'-a)/'+MAX+'"', 3, False, 7, OUTPATH+MDCH)	
	mdchlayer = QgsRasterLayer(OUTPATH+MDCH, "mdch")
	mdchlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(mdchlayer)
	
	print "Cleaning QGIS canvas."
	QgsMapLayerRegistry.instance().removeMapLayer(mdtlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(mdhlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(streamlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(vstreamlayer.id())
	
	return "Done!"
