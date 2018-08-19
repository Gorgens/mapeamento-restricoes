'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\zf2\\julia\\lidar\\dtm.py')
Adicionar:
- 
'''

def dtm(INLAS =  "NP_T-400.las", DTM  = "NP_T-400dtm.dtm", FILTERCELL = "8", GNDLAS = "NP_T-400gnd.laz", DTMCELL = "1", ASCDTM = "NP_T-400.asc", INPATH = "C:\\FUSION\\las\\", OUTPATH = "C:\\FUSION\\zf2\\julia\\lidar\\", EPSG = 31980, OPEN = True):
	
	import processing
	import subprocess
	
	GNDFUN = "c:\\fusion\\groundfilter"
	DTMFUN = "c:\\fusion\\gridsurfacecreate"
	ASCFUN = "c:\\fusion\\dtm2ascii"
	
	print "Filtering ground points."
	ch=subprocess.call([GNDFUN, OUTPATH+GNDLAS, FILTERCELL, INPATH+INLAS], shell=True)
	if ch == 0:
		print "Ground filtered!"
	else:
		print "Check the code, and try again."
		return
	
	print "Creating DTM."
	ch=subprocess.call([DTMFUN, OUTPATH+DTM, DTMCELL, "m", "m",  "1",  "22",  "0",  "0", OUTPATH+GNDLAS], shell=True)
	if ch == 0:
		print "DTM created!"
	else:
		print "Check the code, and try again."
		return
	
	print "Converting dtm to asc."
	ch=subprocess.call([ASCFUN, OUTPATH+DTM, OUTPATH+ASCDTM], shell=True)
	if ch == 0:
		print "DTM created in ASCII!"
	else:
		print "Check the code, and try again."
		return
	
	if OPEN:
		print "Loading raster to canvas."
		crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
		rlayer = QgsRasterLayer(OUTPATH+ASCDTM, "DTM")
		rlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(rlayer)
	
	return "Done!"