'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\script\\gap.py')
'''

def gap(CHMASC = "chm.asc", HEIGHT = 10, AREAMIN = 10, GAPMASK = "gapMask.tif", GAPSHP = "gap.shp", EPSG = 31982, INPATH = "C:\\FUSION\\pcf637\\script\\", OUTPATH = "C:\\FUSION\\pcf637\\script\\out\\"):

	import processing
	import os
	from osgeo import ogr
	
	export = True
		
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
	
	'''
	Importa o modelo digital de altura de dossel sobre a qual todo o calculo sera realizado.
	1. importa CHM salvo no computador em formato ASC para dentro de uma variavel
	2. define a projecao da camada importada na etapa 1
	3. carrega a camada no canvas do qgis
	'''
	chmlayer = QgsRasterLayer(INPATH+CHMASC, "chm")
	chmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	

	'''
	A partir do CHM importado anteriormente, cria uma mascada para os pixels abaixo de uma 
	determianda altura criando.
	1. cria a string que define o filtro a ser aplicado no rastercalculator
	2. cria a mascara aplicando o filtro via rastercalculator do SAGA sobre o CHM
	3. importa a mascara para uma variavel
	4. define a projecao da mascara
	5. extrai a extensao da mascara
	6. carrega a mascara no canvas qgis
	'''
	print "Creating gap's mask"
	CALC = "ifelse(a>"+str(HEIGHT)+",-99999,1)"
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC, 3, False, 7, OUTPATH+GAPMASK)
	msklayer = QgsRasterLayer(OUTPATH+GAPMASK, "gapmascara")
	msklayer.setCrs(crs)
	extent = msklayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	QgsMapLayerRegistry.instance().addMapLayer(msklayer)
	
	'''
	A partir mascara de copas emergentes cria uma camada vetorial de poligonos.
	1. chama o comando grass para vetorizar uma mascara
	2. importa a camada de poligonos para uma variavel
	3. define a projecao da camada de poligonos
	4. carrega a camada no canvas qgis
	'''
	print "Creating 1 of 3"
	GAPTEMP = GAPSHP[0:len(GAPSHP)-4] + "temp.shp"
	processing.runalg("grass7:r.to.vect", msklayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+GAPTEMP)
	vlayer = QgsVectorLayer(OUTPATH+GAPTEMP, "gaptemp1", "ogr")
	vlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(vlayer)
	
	'''
	A partir camada vetorial de poligonos, cria uma nova camada contendo o atributo de area. Esta camada
	indica uma aproximacao das copas das arvores emergentes.
	1. cria o nome da nova camada acrescido do indice 2
	2. roda o comando fieldcalculador para obter area de cada poligono
	3. importa a camada de poligonos para uma variavel
	4. define a projecao da camada de poligonos
	5. extrai a extensao da mascara
	6. carrega a camada no canvas qgis
	'''
	print "Creating 2 of 3"
	GAPTEMP2 = GAPSHP[0:len(GAPSHP)-4] + "temp2.shp"
	processing.runalg('qgis:fieldcalculator', vlayer, 'area', 0, 10, 2, True, '$area', OUTPATH+GAPTEMP2)
	vlayer2 = QgsVectorLayer(OUTPATH+GAPTEMP2, "gaptemp2", "ogr")
	vlayer2.setCrs(crs)
	extent = vlayer2.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	QgsMapLayerRegistry.instance().addMapLayer(vlayer2)
	
	'''
	A partir do vetor de copas, com as informacoes de area, filtro apenas as copas maiores que area 
	especificada pelo usuario.
	1. chama o comando grass para filtrar poligonos com area acima do limite espeficicado
	2. importa a camada de poligonos das copas emergente maiores que limite
	3. define a projecao da camada de poligonos
	4. carrega a camada no canvas qgis
	'''
	print "Creating 3 of 3"
	GAP = "area>"+str(AREAMIN)
	processing.runalg("grass7:v.extract", vlayer2, GAP, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), -1, 0, 0, OUTPATH+GAPSHP)
	gapLayer = QgsVectorLayer(OUTPATH+GAPSHP, "gap", "ogr")
	gapLayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(gapLayer)
	print "Gaps layer created"
	
	print "Cleaning temporary files"
	QgsMapLayerRegistry.instance().removeMapLayer(msklayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(vlayer.id())
	QgsMapLayerRegistry.instance().removeMapLayer(vlayer2.id())
	
	driver = ogr.GetDriverByName("ESRI Shapefile")
	if os.path.exists(OUTPATH+GAPTEMP):
		 driver.DeleteDataSource(OUTPATH+GAPTEMP)
	if os.path.exists(OUTPATH+GAPTEMP2):
		 driver.DeleteDataSource(OUTPATH+GAPTEMP2)

	return "Done!"
	
gap(CHMASC = "chm.asc", HEIGHT = 10, AREAMIN = 10, GAPMASK = "gapMask.tif", GAPSHP = "gap.shp", EPSG = 31982, INPATH = "C:\\FUSION\\pcf637\\script\\", OUTPATH = "C:\\FUSION\\pcf637\\script\\out\\")
