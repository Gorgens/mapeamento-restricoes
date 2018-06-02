'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\createChm.py')
'''

def doChm(INLAS =  "C:\\FUSION\\pcf637\\las\\upa_1.laz", DTM  = "C:\\FUSION\\pcf637\\mdt\\upa_1.dtm", CHM = "C:\\FUSION\\pcf637\\chm\\upa_1chm.dtm", CHMCELL = "1", show = True, EPSG = 31982):
	
	import subprocess
	'Padrao do fusion'
	GND = "/ground:" + DTM
	ASC = "/ascii"
	CHMFUN = "c:\\fusion\\canopymodel"
	CHMASC = CHM[0:len(CHM)-4] + ".asc"
		
	ch=subprocess.call([CHMFUN, GND, ASC, CHM, CHMCELL, "m", "m",  "1",  "22",  "0",  "0", INLAS], shell=True)
	if ch == 0:
		print "CHM created!"
	else:
		print "Check the code, and try again."
		return
	
	if show:
		crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)

		'Importar CHM criado'
		rlayer = QgsRasterLayer(CHMASC, "CHM")
		rlayer.setCrs(crs)

		QgsMapLayerRegistry.instance().addMapLayer(rlayer)
		
	return "Done!"
