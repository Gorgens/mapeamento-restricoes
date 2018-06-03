'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\createTop.py')
'''

def doTop(CHMASC = "C:\\FUSION\\pcf637\\chm\\upa_1chm.asc", HEIGHT = "35", TOP = "C:\\FUSION\\pcf637\\chm\\upa_1top.tif",  TOPSHP = "C:\\FUSION\\pcf637\\chm\\upa_1topVec.shp", EPSG = 31982):
	
	import processing
	show = True
	
	'define expressao para filtro das arvores emergente'
	CALC = "ifelse(a<"+HEIGHT+",-99999,a)"
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
	
	'importa arquivo *.asc com MDT'
	chmlayer = QgsRasterLayer(CHMASC, "CHM")
	chmlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	
	'extrai arvores emergente'
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC, 3, False, 7, TOP)
	
	toplayer = QgsRasterLayer(TOP, "TOP")
	toplayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(toplayer)
	extent = toplayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	
	processing.runalg("grass7:r.to.vect", toplayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, TOPSHP)
	vlayer = QgsVectorLayer(TOPSHP, "top trees", "ogr")
	vlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(vlayer)
	processing.runalg("grass7:r.to.vect", toplayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, TOPSHP)
	
	v.db.addcolumn map=$2_topcanopy_vector@bruno columns="area_m DOUBLE PRECISION"
	v.to.db map=$2_topcanopy_vector@bruno option=area columns=area_m units=meters

		
	return "Done!"
