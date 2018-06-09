'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\script\\tree.py')
'''

def doTop(CHMASC = "chm.asc", COPA = 9, TOPCROWN = "crownTop.tif", TOPMASK = "maskCrown.tif", TOPSHP = "crownVec.shp", TOPTREE = "emergentsVec.shp", EPSG = 31982, INPATH = "C:\\FUSION\\pcf637\\script\\", OUTPATH = "C:\\FUSION\\pcf637\\script\\"):

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
	chmlayer = QgsRasterLayer(INPATH+CHMASC, "CHM")
	chmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	
	
	'''
	Extrair valor maximo da camada CHM e utilizar como referencia para o parametro HEIGHT
	'''
	extent = chmlayer.extent()
	provider = chmlayer.dataProvider()
	stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)
	#HEIGHT = str(round(stats.maximumValue - 10))
	HEIGHT = str(round(stats.mean + 2. * stats.stdDev))
	
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
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC1, 3, False, 7, OUTPATH+TOPCROWN)
	toplayer = QgsRasterLayer(OUTPATH+TOPCROWN, "top crowns")
	toplayer.setCrs(crs)
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
	processing.runalg("saga:rastercalculator", chmlayer, None, CALC2, 3, False, 7, OUTPATH+TOPMASK)
	msklayer = QgsRasterLayer(OUTPATH+TOPMASK, "mascara")
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
	processing.runalg("grass7:r.to.vect", msklayer, 2, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, OUTPATH+TOPSHP)
	vlayer = QgsVectorLayer(OUTPATH+TOPSHP, "crownVectors", "ogr")
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
	TOPSHP2 = TOPSHP[0:len(TOPSHP)-4] + "2.shp"
	processing.runalg('qgis:fieldcalculator', vlayer, 'area', 0, 10, 2, True, '$area', OUTPATH+TOPSHP2)
	crownlayer = QgsVectorLayer(OUTPATH+TOPSHP2, "crownArea", "ogr")
	crownlayer.setCrs(crs)
	extent = crownlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	QgsMapLayerRegistry.instance().addMapLayer(crownlayer)
	
	'''
	A partir do vetor de copas, com as informacoes de area, filtro apenas as copas maiores que area 
	especificada pelo usuario.
	1. chama o comando grass para filtrar poligonos com area acima do limite espeficicado
	2. importa a camada de poligonos das copas emergente maiores que limite
	3. define a projecao da camada de poligonos
	4. carrega a camada no canvas qgis
	'''
	'''
	CROWN = "area > "+str(COPA)
	processing.runalg("grass7:v.extract", crownlayer, CROWN, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), -1, 0, 0, OUTPATH+TOPTREE)
	treelayer = QgsVectorLayer(TOPTREE, "topTrees", "ogr")
	treelayer.setCrs(crs)
	if show:
		QgsMapLayerRegistry.instance().addMapLayer(treelayer)
	'''
	
	'''
	1. calcula o centroid de cada poligono extraido como arvore
	2. salva num shape de pontos chamado centroid.shp
	3. esctrai as coordenadas x e y de cada ponto
	4. exporta as coordenadas num csv
	'''
	if export:
		ogr.UseExceptions()
		os.chdir(OUTPATH)
		
		ds = ogr.Open(OUTPATH+TOPSHP2)
		ly = ds.ExecuteSQL('SELECT ST_Centroid(geometry), * FROM crownVec2', dialect='sqlite')
		drv = ogr.GetDriverByName('Esri shapefile')
		ds2 = drv.CreateDataSource('centroid.shp')
		ds2.CopyLayer(ly, '')
		ly = treelayer = ds2 = None  # save, close
		
		pointslayer = QgsVectorLayer(OUTPATH+'centroid.shp', "treepoints", "ogr")
		pointslayer.setCrs(crs)
		processing.runalg('qgis:fieldcalculator', pointslayer, 'xcoord', 0, 10, 2, True, '$x', OUTPATH+'centroid2.shp')
		pointslayer = QgsVectorLayer(OUTPATH+'centroid2.shp', "treepoints", "ogr")
		pointslayer.setCrs(crs)
		processing.runalg('qgis:fieldcalculator', pointslayer, 'ycoord', 0, 10, 2, True, '$y', OUTPATH+'centroid3.shp')
		pointslayer = QgsVectorLayer(OUTPATH+'centroid3.shp', "treepoints", "ogr")
		pointslayer.setCrs(crs)
		
		QgsVectorFileWriter.writeAsVectorFormat(pointslayer, OUTPATH+"xy.csv", "utf-8", None, "CSV", layerOptions ='GEOMETRY=AS_WKT')
	return "Done!"

'''	
doTop(CHMASC = "chm.asc", COPA = 9, TOPCROWN = "crownTop.tif", TOPMASK = "maskCrown.tif", TOPSHP = "crownVec.shp", TOPTREE = "emergentsVec.shp", EPSG = 31982, INPATH = "C:\\FUSION\\pcf637\\script\\", OUTPATH = "C:\\FUSION\\pcf637\\script\\")
'''
