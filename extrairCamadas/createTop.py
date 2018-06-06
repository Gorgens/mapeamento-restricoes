'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\createTop.py')
'''

def doTop(CHMASC = "C:\\FUSION\\pcf637\\chm\\upa_1chm.asc", HEIGHT = "35", COPA = "9", TOPCROWN = "C:\\FUSION\\pcf637\\chm\\upa_1topCrowns.tif",  TOPMSK = "C:\\FUSION\\pcf637\\chm\\upa_1topMask.tif",TOPSHP = "C:\\FUSION\\pcf637\\chm\\upa_1topVec.shp",TOPTREE = "C:\\FUSION\\pcf637\\chm\\upa_1topTree.shp", EPSG = 31982):

	import processing
	show = True
	
	'define projecao a ser usada'
	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
	
	'''
	Importa o modelo digital de altura de dossel sobre a qual todo o calculo sera realizado.
	1. importa CHM salvo no computador em formato ASC para dentro de uma variavel
	2. define a projecao da camada importada na etapa 1
	3. carrega a camada no canvas do qgis
	'''
	chmlayer = QgsRasterLayer(CHMASC, "CHM")
	chmlayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	
	'''
	A partir do CHM importado anteriormente, filtra os pixels acima de uma determianda altura criando
	uma raster chamado de modelo digital de copas emergentes (MDCE).
	1. cria a string que define o filtro a ser aplicado no rastercalculator
	2. cria o MDCE aplicando o filtro via rastercalculator do SAGA sobre o CHM
	3. importa o MDCE para uma variavel
	4. define a projecao da camada MDCE
	5. carrega a camada no canvas qgis
	'''
	CALC1 = "ifelse(a<"+HEIGHT+",-99999,a)"
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC1, 3, False, 7, TOPCROWN)
	toplayer = QgsRasterLayer(TOPCROWN, "top crowns")
	toplayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(toplayer)
	
	'''
	A partir do CHM importado anteriormente, cria uma mascada para os pixels acima de uma 
	determianda altura criando.
	1. cria a string que define o filtro a ser aplicado no rastercalculator
	2. cria a mascara aplicando o filtro via rastercalculator do SAGA sobre o CHM
	3. importa a mascara para uma variavel
	4. define a projecao da mascara
	5. extrai a extensao da mascara
	6. carrega a mascara no canvas qgis
	'''
	CALC2 = "ifelse(a<"+HEIGHT+",-99999,1)"
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC2, 3, False, 7, TOPMSK)
	msklayer = QgsRasterLayer(TOPMSK, "mascara")
	msklayer.setCrs(crs)
	extent = msklayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(msklayer)
	
	'''
	A partir mascara de copas emergentes cria uma camada vetorial de poligonos.
	1. chama o comando grass para vetorizar uma mascara
	2. importa a camada de poligonos para uma variavel
	3. define a projecao da camada de poligonos
	4. carrega a camada no canvas qgis
	'''
	processing.runalg("grass7:r.to.vect", msklayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, TOPSHP)
	vlayer = QgsVectorLayer(TOPSHP, "crowns vectors", "ogr")
	vlayer.setCrs(crs)
	if show:
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
	TOPSHP2 = TOPSHP[0:len(TOPSHP)-4] + "Area.shp"
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
	
	'''
	A partir do vetor de copas, com as informacoes de area, filtro apenas as copas maiores que area 
	especificada pelo usuario.
	1. chama o comando grass para filtrar poligonos com area acima do limite espeficicado
	2. importa a camada de poligonos das copas emergente maiores que limite
	3. define a projecao da camada de poligonos
	4. carrega a camada no canvas qgis
	'''
	CROWN = "area > "+COPA
	processing.runalg("grass7:v.extract", crownlayer, CROWN, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), -1, 0, 0, TOPTREE)
	treelayer = QgsVectorLayer(TOPTREE, "top tree", "ogr")
	treelayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(treelayer)
	
	return "Done!"
