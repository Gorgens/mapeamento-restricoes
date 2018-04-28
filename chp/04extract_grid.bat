set LAS_TILES="D:\ALS\CENIBRA\NEPIAL00248_Serra_NP\NEPIAL00248_Serra_NP-*.las"
set FILTERED_FILE="D:\ALS\CENIBRA\NEPIAL00248_Serra_NP\NEPIAL00248_Serra_NPFilt.las"
set DTM_FILE="D:\ALS\CENIBRA\NEPIAL00248_Serra_DTM\NEPIAL00248_Serra_DTM.dtm"
set DTM_ASC="D:\ALS\CENIBRA\NEPIAL00248_Serra_DTM\NEPIAL00248_Serra_DTM.asc"
set SLICE_FILE="D:\ALS\CENIBRA\NEPIAL00248_Serra_MAPA\NEPIAL00248_Serra.csv"

REM FilterData [switches] FilterType FilterParms WindowSize OutputFile DataFile
c:\fusion\FilterData outlier 4 10 %FILTERED_FILE% %LAS_TILES%
pause

REM ASCII2DTM [switches] surfacefile xyunits zunits coordsys zone horizdatum vertdatum gridfile
c:\fusion\ASCII2DTM %DTM_FILE% m m 1 23 0 0 %DTM_ASC%
pause

REM DensityMetrics [switches] groundfile cellsize slicethickness outputfile datafile1
c:\fusion\DensityMetrics %DTM_FILE% 30 1 %SLICE_FILE% %FILTERED_FILE%
pause