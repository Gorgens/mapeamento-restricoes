'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\script\\tch.py')
'''

def tch(CHMASC="chm.asc", TCHCELL=50, TCH="tch.tif", MDVOL="mdb.tif", EPSG=31982, INPATH="C:\\FUSION\\pcf637\\script\\", OUTPATH="C:\\FUSION\\pcf637\\script\\out\\"):
	
	import processing

	crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

	'''
	Importa o CHM para computar o top canopy height, formado pela media da altura do pixel de 1 metro
	reamostrados para pixel de 50 metros.
	1. importa CHM em formato asc
	2. define projecao do CHM
	3. carrega CHM no canvas qgis
	4. extrai a extensao do CHM
	5. reamostra o CHM de 1 metro em uma grade de 50 m utilizando a media como funcao agrupadora. Cria o TCH
	6. Importa o TCH
	7. define a projecao do TCH
	8. exibe o TCH no canvas do qgis
	'''
	chmlayer = QgsRasterLayer(INPATH+CHMASC, "CHM")
	chmlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(chmlayer)
	extent = chmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	processing.runalg('grass7:r.resamp.stats', chmlayer, 0, False, False, False, "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), TCHCELL, OUTPATH+TCH)
	tchlayer = QgsRasterLayer(OUTPATH+TCH, "TCH")
	tchlayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(tchlayer)
	
	'''
	Cria o mapa de biomassa usando a metodologia proposta por Longo et al.
	1. aplica a funcao proposta por longo nos pixels do TCH
	2. importa modelo digial de volume para pixels de 50 metros
	3. define a projecao da camada.
	4. carrega camada no canvas qgis
	'''
	processing.runalg("saga:rastercalculator", tchlayer, None, "(0.054*((a)^1.76))*2", 3, False, 7, OUTPATH+MDVOL)	
	vollayer = QgsRasterLayer(OUTPATH+MDVOL, "MDB")
	vollayer.setCrs(crs)
	QgsMapLayerRegistry.instance().addMapLayer(vollayer)
	
	return "Done!"
	
	
tch(CHMASC="chm.asc", TCHCELL=50, TCH="tch.tif", MDVOL="mdb.tif", EPSG=31982, INPATH="C:\\FUSION\\pcf637\\script\\", OUTPATH="C:\\FUSION\\pcf637\\script\\")