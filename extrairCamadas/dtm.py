'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\pcf637\\python\\dtm.py')
'''

def dtm(INLAS =  "C:\\FUSION\\pcf637\\las\\upa_1.laz", DTM  = "C:\\FUSION\\pcf637\\mdt\\upa_1.dtm", FILTERCELL = "8", GNDLAS = "C:\\FUSION\\pcf637\\mdt\\upa_1gnd.laz", DTMCELL = "1", ASCDTM = "C:\\FUSION\\pcf637\\mdt\\upa_1.asc", EPSG = 31982):
	
	import subprocess
	show = True
	
	GNDFUN = "c:\\fusion\\groundfilter"
	DTMFUN = "c:\\fusion\\gridsurfacecreate"
	ASCFUN = "c:\\fusion\\dtm2ascii"
	
	ch=subprocess.call([GNDFUN, GNDLAS, FILTERCELL, INLAS], shell=True)
	if ch == 0:
		print "Ground filtered!"
	else:
		print "Check the code, and try again."
		return

	ch=subprocess.call([DTMFUN, DTM, DTMCELL, "m", "m",  "1",  "22",  "0",  "0", GNDLAS], shell=True)
	if ch == 0:
		print "DTM created!"
	else:
		print "Check the code, and try again."
		return
		
	ch=subprocess.call([ASCFUN, DTM, ASCDTM], shell=True)
	if ch == 0:
		print "DTM created in ASCII!"
	else:
		print "Check the code, and try again."
		return
		
	if show:
		crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
		rlayer = QgsRasterLayer(ASCDTM, "DTM")
		rlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(rlayer)
	
	return "Done!"
