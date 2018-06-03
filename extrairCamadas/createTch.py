'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\createTch.py')
'''

def doTch(CHMASC = "C:\\FUSION\\pcf637\\chm\\upa_1chm.asc", TCHCELL = 50, TCH = "C:\\FUSION\\pcf637\\chm\\upa_1tch.tif", MDVOL = "C:\\FUSION\\pcf637\\chm\\upa_1vol.tif",EPSG = 31982):
	
	import processing
	show = True

	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	'Importar CHM criado'
	chmlayer = QgsRasterLayer(CHMASC, "CHM")
	chmlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	extent = chmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	processing.runalg('grass7:r.resamp.stats', chmlayer,0,False,False,False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), TCHCELL, TCH)
	tchlayer = QgsRasterLayer(TCH, "TCH")
	tchlayer.setCrs(crs)
	if show:	
		QgsMapLayerRegistry.instance().addMapLayer(tchlayer)
		
	processing.runalg("saga:rastercalculator", tchlayer, None, "(0.054*((a)^1.76))*2", 3, False, 7, MDVOL)	
	vollayer = QgsRasterLayer(MDVOL, "VOL")
	vollayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(vollayer)
	
	return "Done!"
