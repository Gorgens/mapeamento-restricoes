'''
TO CALL ON PYTHON SHELL
execfile('C:\\FUSION\\zf2\\julia\\lidar\\chm.py')
'''

def chm(INLAS =  "NP_T-400.las", DTM  = "NP_T-400dtm.dtm", CHM = "NP_T-400chm.dtm", LASPATH = "C:\\FUSION\\las\\", DTMPATH = "C:\\FUSION\\zf2\\julia\\lidar\\", OUTPATH = "C:\\FUSION\\zf2\\julia\\lidar\\", CHMCELL = "1", EPSG = 31982, OPEN = True):
	
	import processing
	import subprocess
	
	GND = "/ground:" + DTMPATH + DTM
	ASC = "/ascii"
	CHMFUN = "c:\\fusion\\canopymodel"
	CHMASC = OUTPATH+CHM[0:len(CHM)-4] + ".asc"
	
	print 'Creating CHM...'
	ch=subprocess.call([CHMFUN, GND, ASC, OUTPATH+CHM, CHMCELL, "m", "m",  "1",  "22",  "0",  "0", LASPATH+INLAS], shell=True)
	if ch == 0:
		print "CHM created!"
	else:
		print "Check the code, and try again."
		return
	
	if OPEN:
		print "Loading raster to canvas."
		crs = QgsCoordinateReferenceSystem(EPSG, QgsCoordinateReferenceSystem.PostgisCrsId)
		rlayer = QgsRasterLayer(CHMASC, "CHM")
		rlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(rlayer)
		
	return "Done!"