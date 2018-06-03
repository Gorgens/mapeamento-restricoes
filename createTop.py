'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\createTop.py')
'''

def doTop(CHMASC = "C:\\FUSION\\pcf637\\chm\\upa_1chm.asc", HEIGHT = "35", COPA = "9", TOPCROWN = "C:\\FUSION\\pcf637\\chm\\upa_1topCrowns.tif",  TOPMSK = "C:\\FUSION\\pcf637\\chm\\upa_1topMask.tif",TOPSHP = "C:\\FUSION\\pcf637\\chm\\upa_1topVec.shp",TOPTREE = "C:\\FUSION\\pcf637\\chm\\upa_1topTree.shp",   EPSG = 31982):
	
	import processing
	show = True
	
	TOPSHP2 = TOPSHP[0:len(TOPSHP)-4] + "Area.shp"
	
	CROWN = "area > "+COPA

	'define expressao para filtro das arvores emergente'
	CALC1 = "ifelse(a<"+HEIGHT+",-99999,a)"
	CALC2 = "ifelse(a<"+HEIGHT+",-99999,1)"
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
	
	'importa arquivo *.asc com MDT'
	chmlayer = QgsRasterLayer(CHMASC, "CHM")
	chmlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	
	'cria raster de arvores emergentes'
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC1, 3, False, 7, TOPCROWN)
	toplayer = QgsRasterLayer(TOPCROWN, "top crowns")
	toplayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(toplayer)
	
	'cria mascara de arvores emergentes'
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC2, 3, False, 7, TOPMSK)
	msklayer = QgsRasterLayer(TOPMSK, "mascara")
	msklayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(msklayer)
	extent = msklayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	'transforma raster das emergentes em vetor'
	processing.runalg("grass7:r.to.vect", msklayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, TOPSHP)
	vlayer = QgsVectorLayer(TOPSHP, "crowns vectors", "ogr")
	vlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(vlayer)
	
	processing.runalg('qgis:fieldcalculator', vlayer, 'area', 0, 10, 2, True, '$area', TOPSHP2)
	crownlayer = QgsVectorLayer(TOPSHP2, "crown vectors", "ogr")
	crownlayer.setCrs(crs)
	extent = crownlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(crownlayer)
	
	processing.runalg("grass7:v.extract", crownlayer, CROWN, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), -1, 0, 0, TOPTREE)
	treelayer = QgsVectorLayer(TOPTREE, "top tree", "ogr")
	treelayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(treelayer)
	
	return "Done!"
