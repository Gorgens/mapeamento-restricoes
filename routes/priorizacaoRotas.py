# Modelo de rota mínima para transporte madeireiro
# 
#-----------------------------------------------------------------------------------------
 
#Importar módulo arcpy

import arcpy
from arcpy import env
import os

# Workspace

arcpy.env.workspace = "C:\\gateados\\input"
arcpy.env.overwriteOutput = True

#-----------------------------------------------------------------------------------------

#Step 1 : Definição dos locais de ínicio (talhao) e fim da rota (destino)

# Lista de variáveis

destino = "C:\\gateados\\input\\componente\\fazenda.SHP"
#talhao = arcpy.ListFeatureClasses("talhao*","point") #corrigido para listar os talhoes corretamente


arcpy.env.workspace = "C:\\gateados\\input\\talhao"
talhao = arcpy.ListFeatureClasses()


# Processo: Looping Merge [unindo ponto de ínicio (talhao) e fim (destino) da rota]

for fc in talhao:

# Processo : Nomeclatura e armazenamento do output

	nome_local = arcpy.Describe(fc) .baseName + "_local"
	
	#folders = "C:\\araguaia\\input\\" + "\\"

	folders = "C:\\gateados\\input\\local\\" + "\\"
	
	local =  folders + nome_local

# Processo : Criando locais (shape file de talhao e destino) 

	arcpy.Merge_management([fc,destino],local)
	
print("Fim Step 1 ")

print("Iniciando Step 2") 

#Step 2: Crição das Rotas 

import arcpy
from arcpy import env
import os
arcpy.env.workspace = "C:\\gateados\\input\\local"
arcpy.env.overwriteOutput = True

# Lista de variáveis
estrada = "C:\\gateados\\input\\componente\\Rede_Gateados.SHP"
junction = "C:\\gateados\\input\\componente\\ND_JunctionsGateados.SHP"
network = "C:\\gateados\\input\\componente\\roads.gdb\\roadsDataSet_ND"


print("verificação variavéis ok")

# Listar inputs (lista de locais)

#talhao = arcpy.ListFeatureClasses("talhao*","point") 

talhao = arcpy.ListFeatureClasses()



for fc in talhao:

# Processo: Make Route Layer

	arcpy.MakeRouteLayer_na (network, "analise_rota", "Length", "FIND_BEST_ORDER", "PRESERVE_BOTH", "NO_TIMEWINDOWS", "", "ALLOW_UTURNS", "", "NO_HIERARCHY", "", "TRUE_LINES_WITH_MEASURES", "")
   


# Processo: adicionar locais

	#arcpy.AddLocations_na  ('analise_rota', "stops", fc, "", "5000 Meters", "", "estrada SHAPE;junction NONE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "INCLUDE", "estrada #;junction #")

	arcpy.AddLocations_na  ('analise_rota', "stops", fc, "", "5000 Meters", "",[["estrada","SHAPE"],["junction","NONE"]], "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "INCLUDE", "estrada #;junction #")

	
# Processo : checkout de extensão

	arcpy.CheckOutExtension("Network")

# Processo : Solve

	arcpy.Solve_na('analise_rota', "SKIP", "TERMINATE", "")

# Processo: Selecionar Dados

	#arcpy.SelectData_management('analise_rota', "Routes")

#Processo: Nomeclatura outputs 

	arcpy.Describe(fc) .baseName + "_rota"

	nome_rota = arcpy.Describe(fc) .baseName + "_rota"

# Processo: Determinar  armazenamento do output

	folder = "C:\\gateados\\output" + "\\"

	rota =  folder + nome_rota

# Process: Salvar output

	arcpy.CopyFeatures_management('analise_rota\\Routes', rota, "", "0", "0", "0")
print("fim do step2")	



#Step 3: Obtençao das rotas (Pedro)

import arcpy
from arcpy import env
import os
arcpy.env.workspace = "C:\\gateados\\output"
arcpy.env.overwriteOutput = True

#variaveis
trechos = arcpy.ListFeatureClasses()
junction = "C:\\gateados\\input\\componente\\ND_JunctionsGateados.SHP"
estrada = "C:\\gateados\\input\\componente\\Rede_Gateados.SHP"

#para fc até talhao, faça o intersect e grave no output2
# testar esse intersect  com o shape RutasFC e nao com o junction....



for fc in trechos:

#nome do output
	rota = arcpy.Describe(fc) .baseName + "_seq"
	
	files = "C:\\gateados\\output2\\" + "\\"
	files2 =  files + rota

	#arcpy.Intersect_analysis([fc,junction],files2)
	arcpy.Intersect_analysis([fc,estrada],files2)
	

print("Fim Step 3 ")


#Step 4: #Coloca o nomo de shapefile(para identificar o talhao) dentro da tabela de atributos

# Import standard library modules
import arcpy, os, sys
from arcpy import env

# Allow for file overwrite
arcpy.env.overwriteOutput = True

# Set the workspace directory 
env.workspace = "C:\\gateados\\output2" 

# Get the list of the featureclasses to process
fc_tables = arcpy.ListFeatureClasses()

# Loop through each file and perform the processing
for fc in fc_tables:
    print str("processing " + fc)

# Define field name and expression
    field = "FILENAME"
    expression = str(fc) #populates field  

# Create a new field with a new name
    arcpy.AddField_management(fc,field,"TEXT")

# Calculate field here
    arcpy.CalculateField_management(fc, field, '"'+expression+'"', "PYTHON")

# step 5
#unido os shapefiles, gerando o banco de dados (CSV)
################
import arcpy
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



f = open(r'C:\\gateados\\input\\Local\\Exports.txt', 'w')
w = csv.writer(f, lineterminator='\n')


arcpy.env.workspace = "C:\\gateados\\input\\local"

shapefileList = arcpy.ListFeatureClasses("*.shp")

for table in shapefileList:
	f.write("Shapefile:\n")
	f.write(table + "\n")
	fieldList = arcpy.ListFields(table)
	field_names = [field.name for field in fieldList]
	w.writerow(field_names)
	for row in arcpy.SearchCursor(table):
        field_vals = []
        for field in fieldList:
            val = row.getValue(field.name)
            # See if it's a geometry field; if so, use WKT
            try:
                val = val.WKT
            except AttributeError:
                # It's not a geometry, and that's okay
                pass
				field_vals.append(val)
				w.writerow(field_vals)

				
#Mesmo atividade, programada no R:
#Definir drecciÃ³n de trabalho
setwd("~/Dropbox/ShapesPedro/")
#Clean
rm(list = ls())
# Pasta Resultados
if(file.exists("Resultados") == FALSE) dir.create("Resultados")#para almacenar tabla csv
#Librarias
library(foreign)
#Lista de arquivos
################################
#gera uma lista
lista <- list.files("Shapefile", pattern=".dbf", full.names=TRUE)
#Conformar base de dados
##########################################
#Armazena na tabela data.frame "Tablas"
Tablas <- do.call("rbind",lapply(lista, function(x) read.dbf(x)))
#################################
#Contar o numero de linhas do Shapefile
Conteo <- lapply(lista, function(x) read.dbf(x))
#Criar data.frame
Narchivo <- data.frame(Lecturas = NA, Archivo = NA)
#Quantidade de registros por arquivo#
#######################################
#Bucle
for (i in 1:length(Conteo)){
  Narchivo[i,1] <- dim(as.data.frame((Conteo)[i]))[1]
  Narchivo[i,2] <- lista[i]
}
#Agregar nombre de archivo origen a cada registro#
######################################################
#Gerar vetor
Etiquetas <- rep(Narchivo$Archivo, Narchivo$Lecturas)
#Agregar etiquetas
#
Tablas$Origen <- Etiquetas
#Guardar
write.csv(Tablas, file="Resultados/TabelasFinal.csv")
