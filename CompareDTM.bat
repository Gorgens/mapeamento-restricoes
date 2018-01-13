:: Criar modelo digital de terreno com 1 metros de resolução
:: Algoritmo de filtragem Kraus & Pfeifer (1998, 2002)

:: Premissas:
:: 1. Fusion instalado no c:\fusion
:: 2. Nuvem de pontos na pasta do 'c:\fusion', na subpasta 'data'

C:\fusion\GroundFilter C:\fusion\data\NP_T-403_gdf.las 8 C:\fusion\data\NP_T-403.las

C:\fusion\GridSurfaceCreate C:\fusion\data\NP_T-403_dtm.dtm 1 M M 1 0 0 0 C:\fusion\data\NP_T-403_gdf.las
