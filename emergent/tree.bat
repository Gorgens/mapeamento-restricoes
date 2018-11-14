REM PolyClipData [switches] PolyFile OutputFile DataFile
c:\fusion\PolyClipData C:\FUSION\msa\inpa\julia\regiao1\regiao1poly.shp C:\FUSION\msa\inpa\julia\regiao1\NP400.las C:\FUSION\msa\las\NP_T-400.las
c:\fusion\PolyClipData C:\FUSION\msa\inpa\julia\regiao1\regiao1poly.shp C:\FUSION\msa\inpa\julia\regiao1\NP401.las C:\FUSION\msa\las\NP_T-401.las
c:\fusion\PolyClipData C:\FUSION\msa\inpa\julia\regiao1\regiao1poly.shp C:\FUSION\msa\inpa\julia\regiao1\NP402.las C:\FUSION\msa\las\NP_T-402.las

REM MergeData [switches] DataFile OutputFile
c:\fusion\MergeData C:\FUSION\msa\inpa\julia\regiao1\np.txt C:\FUSION\msa\inpa\julia\regiao1\regiao1.las

REM GroundFilter [switches] outputfile cellsize datafile1
c:\fusion\GroundFilter C:\FUSION\msa\inpa\julia\regiao1\regiao1gnd.las 8 C:\FUSION\msa\inpa\julia\regiao1\regiao1.las

REM GridSurfaceCreate [switches] surfacefile cellsize xyunits zunits coordsys zone horizdatum vertdatum datafile1
c:\fusion\GridSurfaceCreate C:\FUSION\msa\inpa\julia\regiao1\regiao1dtm.dtm 1 m m 1 0 0 0 C:\FUSION\msa\inpa\julia\regiao1\regiao1gnd.las

REM CanopyModel [switches] surfacefile cellsize xyunits zunits coordsys zone horizdatum vertdatum datafile1
c:\fusion\CanopyModel /ground:C:\FUSION\msa\inpa\julia\regiao1\regiao1dtm.dtm /ascii C:\FUSION\msa\inpa\julia\regiao1\regiao1chm.dtm 1 m m 1 0 0 0 C:\FUSION\msa\inpa\julia\regiao1\regiao1.las

REM CanopyMaxima [switches] inputfile outputfile
c:\fusion\CanopyMaxima /wse:50,0,0,0 /shape C:\FUSION\msa\inpa\julia\regiao1\regiao1chm.dtm C:\FUSION\msa\inpa\julia\regiao1\regiao1trees

pause

del C:\FUSION\msa\inpa\julia\regiao1\NP400.las
del C:\FUSION\msa\inpa\julia\regiao1\NP401.las
del C:\FUSION\msa\inpa\julia\regiao1\NP402.las
del C:\FUSION\msa\inpa\julia\regiao1\regiao1gnd.las
