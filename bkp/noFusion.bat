:: Transecto INPE _ Sobrevoo na ZF2 em Manaus (INPA)
::------------------------------------------------------------------------------
:: Definir variaveis
set INPDIR= F:\3D\ALS\INPE\NUVENS
set IMGDIR= F:\3D\ALS\INPE\IMAGNS
set STADIR= F:\3D\ALS\INPE\ESTATS
::------------------------------------------------------------------------------
:: Afericao
::------------------------------------------------------------------------------
:: Criar imagem de referência: ImageCreate [switches] ImageFileName PixelSize DataFile1 DataFile2 ..

mkdir %INPDIR%\BMP
c:\fusion_35\ImageCreate /bmp %INPDIR%\BMP\NP_T-403.bmp 10 %INPDIR%\ORIG\LAS\NP_T-403.las

:: Obter informações básicas da nuvem: Catalog [switches] datafile [catalogfile]

mkdir %INPDIR%\CAT
C:\FUSION_35\Catalog /index /density:1,4,6 %INPDIR%\ORIG\LAS\NP_T-403.las %INPDIR%\CAT\NP_T-403_catalog

::------------------------------------------------------------------------------------
::Preparacao
::------------------------------------------------------------------------------------
:: Janela utilizada no gdf de 8 metros
::------------------------------------------------------------------------------------
:: Filtrar outliers
REM FilterData [switches] FilterType FilterParms WindowSize OutputFile DataFile 

mkdir %INPDIR%\FLT
C:\fusion_35\FilterData outlier 3.0 20 %INPDIR%\FLT\NP_T-403_flt.las %INPDIR%\ORIG\LAS\NP_T-403.las

:: Filtrar os pontos do terreno
REM GroundFilter [switches] outputfile cellsize datafile1 datafile2 ... 

mkdir %INPDIR%\GDF
C:\FUSION_35\GroundFilter %INPDIR%\GDF\NP_T-403_gdf.las 8 %INPDIR%\ORIG\LAS\NP_T-403.las

::------------------------------------------------------------------------------------
:: Produtos
::------------------------------------------------------------------------------------
:: Resolução de 1 metro no produto final
::------------------------------------------------------------------------------------

:: Criar o DTM dos pontos filtrados: GridSurfaceCreate [switches] surfacefile cellsize xyunits zunits coordsys zone horizdatum vertdatum datafile1 datafile2...

mkdir %IMGDIR%\DTM
C:\fusion_35\GridSurfaceCreate %IMGDIR%\DTM\NP_T-403_dtm.dtm 1 M M 1 0 0 0 %INPDIR%\GDF\NP_T-403_gdf.las

:: Normalizar a nuvem
REM CanopyModel [switches] surfacefile cellsize xyunits zunits coordsys zone horizdatum vertdatum datafile1 datafile2 … 

mkdir %IMGDIR%\CHM
C:\fusion_35\CanopyModel /ground:F:\3D\ALS\INPE\IMAGNS\DTM\NP_T-403_dtm.dtm %IMGDIR%\CHM\NP_T-403_chm.dtm 1 M M 1 0 0 0 %INPDIR%\FLT\NP_T-403_flt.las

::------------------------------------------------------------------------------------
:: Processamento
::------------------------------------------------------------------------------------

REM ClipDTM [switches] InputDTM OutputDTM MinX MinY MaxX MaxY

set MinX= 814703
set MinY= 9707694
set MaxX= 817588
set MaxY= 9710308

c:\fusion_35\ClipDTM %IMGDIR%\CHM\NP_T-403_chm.dtm %IMGDIR%\CHM\NP_T-403_clip_chm.dtm %MinX% %MinY% %MaxX% %MaxY%

REM CanopyMaxima
REM Localização de árvores individuais dominantes e codominantes

mkdir %STADIR%\canopymaxima
set A=10000
set B=0
set C=0
set D=0
set E=0
set F=0

C:\fusion_35\CanopyMaxima /wse:%A%,%B%,%C%,%D%,%E%,%F% %IMGDIR%\CHM\NP_T-403_clip_chm.dtm %STADIR%\canopymaxima\NP_T-403_chm_clip_10000.csv

::------------------------------------------------------------------------------------
:: VISUALIZAÇÃO QGIS
::------------------------------------------------------------------------------------

mkdir %IMGDIR%\ASC

:: DTM

C:\FUSION_35\DTM2ASCII %IMGDIR%\DTM\NP_T-403_dtm.dtm %IMGDIR%\ASC\NP_T-403_dtm.asc

:: CHM

C:\FUSION_35\DTM2ASCII %IMGDIR%\CHM\NP_T-403_chm.dtm %IMGDIR%\ASC\NP_T-403_chm.asc

:: Clip CHM

C:\FUSION_35\DTM2ASCII %IMGDIR%\CHM\NP_T-403_clip_chm.dtm %IMGDIR%\ASC\NP_T-403_clip_chm.asc

::------------------------------------------------------------------------------------
:: Mantem a janela do DOS aberta e esperando.
CMD /k
