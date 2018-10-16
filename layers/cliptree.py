'''
TO CALL ON PYTHON SHELL
execfile('c:\\fusion\\msa\\las\\clipTree.py')
'''

def clipTree(INLAS =  "NP_T-0128_dn_g_n_ch1_5.laz", OUTLAS  = "tree.las", LASPATH = "C:\\FUSION\\msa\\las\\", OUTPATH = "C:\\FUSION\\msa\\las\\", CENTERX = 243350, CENTERY = 80398, RADIUS = 100, INFO = True):
	
	import processing
	import subprocess

	CLIPFUN = "c:\\fusion\\ClipData"
	INFOFUN = "c:\\fusion\\Catalog"
	
	if INFO:
		print "Extracting internal data..."
		ch1=subprocess.call([INFOFUN, LASPATH+INLAS, OUTPATH+INLAS[0:len(INLAS)-4]], shell=True)
		if ch1 == 0:
			print "Catalog extracted!"
		else:
			print "Check the code, and try again."
			return
		
	print "Extracting the tree..."
	ch2=subprocess.call([CLIPFUN, "/shape:1", LASPATH+INLAS, OUTPATH+OUTLAS, str(CENTERX - RADIUS), str(CENTERY - RADIUS), str(CENTERX + RADIUS), str(CENTERY + RADIUS)], shell=True)
	if ch2 == 0:
		print "Tree clipped!"
	else:
		print "Check the code, and try again."
		return
	
	return "Done!"
