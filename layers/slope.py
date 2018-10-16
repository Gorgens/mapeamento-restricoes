'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\daad\\slope.py')

Adicionar:
- 
'''

def slope(ASCDTM = "upa6dtm.asc", MDD = "upa6mdd.tif", RULESKIDDER = "ruleSkidder.txt", MDCEXTRACAO = "upa6mdcex.tif", RULETRUCK = "ruleTruck.txt", MDCTRANSPORTE = "upa6mdctr.tif", RULEAPP45 = "ruleApp45.txt", MDCAPP45 = "upa6mdc45.tif", INPATH = "C:\\FUSION\\daad\\", OUTPATH = "C:\\FUSION\\daad\\", EPSG = 31982, OPEN = True):
	
	import processing
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
	processing.runalg("grass7:r.slope", dtmlayer, 0, False, 1, 0, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+MDD)
	mddlayer = QgsRasterLayer(OUTPATH+MDD, "mdd")
	mddlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(mddlayer)
	
	if RULESKIDDER != None:
		print "Computing skidder surface cost."
		processing.runalg("grass7:r.reclass", mddlayer, INPATH+RULESKIDDER, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+MDCEXTRACAO)
		if OPEN == True:
			mdcexlayer = QgsRasterLayer(OUTPATH+MDCEXTRACAO, "mdcex")
			mdcexlayer.setCrs(crs)
			QgsMapLayerRegistry.instance().addMapLayer(mdcexlayer)
	
	if RULETRUCK != None:	
		print "Computing load truck surface cost."
		processing.runalg("grass7:r.reclass", mddlayer, INPATH+RULETRUCK, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+MDCTRANSPORTE)
		if OPEN == True:
			mdctrlayer = QgsRasterLayer(OUTPATH+MDCTRANSPORTE, "mdctr")
			mdctrlayer.setCrs(crs)
			QgsMapLayerRegistry.instance().addMapLayer(mdctrlayer)

	if RULEAPP45 != None:	
		print "Computing app 45 surface cost."
		processing.runalg("grass7:r.reclass", mddlayer, INPATH+RULEAPP45, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+MDCAPP45)
		if OPEN == True:
			mdc45layer = QgsRasterLayer(OUTPATH+MDCAPP45, "mdc45")
			mdc45layer.setCrs(crs)
			QgsMapLayerRegistry.instance().addMapLayer(mdc45layer)
		
	print "Cleaning QGIS canvas."
	QgsMapLayerRegistry.instance().removeMapLayer(dtmlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(mddlayer.id())
	
	return "Done!"
