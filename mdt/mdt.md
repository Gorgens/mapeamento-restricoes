# Comparação de  dois métodos de criação de Modelo Digital de Terreno em uma área da floresta amazônica

## Sobre 

Resumo apresentado no VI SINTEGRA - 2018

Autores: Silva BHL*, Andrade MSS, Reis CR, Gorgens EB.

## Resumo 

O presente estudo teve como objetivo comparar dois métodos de criação de Modelo Digital de Terreno (MDT). Um método foi baseado na filtragem dos retornos que interceptaram o terreno, e outro método baseado nos valores mínimos. A área de estudo está localizada na fazenda Cauaxi, município de Paragominas, estado do Pará, e faz parte da Área de Manejo Florestal (AMF) Rio Capim sob gestão do Instituto Floresta Tropical. Os dados foram obtidos de um escaneamento laser aerotransportado cujo sobrevoo ocorreu a 850 metros de altitude, utilizando um sensor ALTM 3100 operando em uma frequência de escaneamento de 59,8 Hz e ângulo de visada de 11 graus. Um modelo digital de terreno (MDT) foi criado associando à um pixel o menor valor dentre os retornos coincidentes e em seguida aplicando um filtro de suavização com duas passagens (a primeira considerando uma janela de 7 metros e a segunda uma janela de 11 metros). O outro modelo digital de terreno foi criado utilizando algoritmo de filtragem Kraus e Pfeifer para filtragem dos retornos com maior probabilidade de terem interceptado o terreno, seguido pela associação à cada pixel do valor médio dos retornos de terreno. O primeiro MDT foi gerado no software GRASS e o segundo no FUSION. Os modelos gerados foram comparados criando-se uma superfície com a diferença pixel a pixel de cada modelo digital criado. Com a superfície das diferenças, calculou-se desvio médio e o desvio padrão. O desvio padrão foi de 7,73 metros e o erro médio de 0,70 metros. Distinguir retornos de solo e não solo pode ser um grande desafio em alguns tipos de situações, como por exemplo regiões com grandes variações do relevo, ou com a presença de uma densa cobertura vegetal. O uso de algoritmo baseado em valor mínimo pode apresentar maiores erros em ambientes com a presença de telhados ou grande objetos cobrindo a superfície do que algoritmo baseado em interpoladores (o caso do Kraus e Pfeifer), o que não é o caso de áreas florestais. A qualidade do modelo de terreno depende da correta classificação dos retornos de solo. A diferença entre produtos foi submétrica, sendo portanto, a decisão uma questão de preferência. 

## Apoio financeiro

Paisagens sustentáveis (EMBRAPA,USDA - FS). Chamada Universal CNPq - Processo: 403297/2016-8. CAPES, FAPEMIG  e UFVJM.

# MODELAGEM DIGITAL DE TERRENO EM ÁREAS DE FLORESTA OMBRÓFILA

## Sobre

Autor: Mariana Silva Andrade

Orientador: Eric Gorgens

Apresentado em 2017

Graduação em Engenharia Florestal

Universidade Federal dos Vales do Jequitinhonha e Mucuri

## Resumo

O primeiro passo em grande parte das análises baseadas em levantamentos laser (ALS) é a criação do modelo digital de terreno (MDT). Os erros relacionados à criação do modelo digital de terrenos estão geralmente relacionados à erros de classificação, durante a separação dos retornos entre terrenos e não terreno. Um das formas de minimizar é aumentando a densidade de pulsos, visando aumentar a probabilidade de se atingir o solo efetivamente. No entanto, o aumento da densidade de pulsos também implica no aumento do custo associado ao levantamento laser. Dessa forma, o objetivo deste estudo é qual a redução na densidade de pulsos que não compromete a qualidade do modelo digital de terreno. Os dados foram coletados em três áreas de floresta tropical: fazenda Cauaxi, no estado do Pará e em duas áreas na floresta nacional do Jamari, no estado de Rondônia. As nuvens de pontos foram processadas utilizando três algoritmos desenvolvidos por Kraus e Pfeifer, Hudak e Evans e Axelsson. Os modelos digitais gerados a partir de diferentes densidade de pulsos foram comparados pelo erro padrão da estimativa (RMSE) com os respectivos modelos digitais de terreno gerados a partir da nuvem original. Como resultado observa-se que o algoritmo de Kraus e Pfeifer apresentou o melhor desempenho em relação aos demais, seguido do algoritmo proposto por Axelsson. Foi possível reduzir a densidade até 4 pulsos/m² mantendo uma resolução de 1 metro sem perda na qualidade do MDT.

## Abstract

The first step in most analyzes based on airborne laser scanning (ALS) is the creation of the digital terrain model (DTM). The errors related to the DTM creation are generally related to misclassification of ground points. One alternative to minimize those errors is to increase the density of pulses, in order to increase the probability of reaching effectively the ground. However, increasing the pulse density also implies in the increase of the cost associated with the laser survey. The purpose of this study is to reduce the pulse density that does not compromise the quality of the digital terrain model. The data sets were collected in three tropical forest areas: Cauaxi farm, in the state of Pará, and in the Jamari National Forest (two flights), in the state of Rondônia. The point clouds were processed using three algorithms developed by Kraus and Pfeifer, Hudak and Evans and Axelsson. The digital models generated from different pulse densities were compared by root mean square error (RMSE) with the respective digital terrain models generated from the original cloud. As a result, the algorithm of Kraus and Pfeifer presented the best performance, followed by the algorithm proposed by Axelsson. It was possible to reduce the density up to 4 pulses / m² maintaining a resolution of 1 meter without loss in the DTM quality.

# INFLUÊNCIA DA DENSIDADE DE PULSOS NA MODELAGEM DIGITAL DE TERRENO EM FLORESTA OMBRÓFILA

## Sobre

Autor: Mariana Silva Andrade

Orientador: Eric Gorgens

Apresentado em 2017.

Iniciação Científica UFVJM, CNPq, FAPEMIG.

Universidade Federal dos Vales do Jequitinhonha e Mucuri.

## Resumo

O primeiro passo em grande parte das análises baseadas em levantamentos laser (ALS) é a criação do modelo digital de terreno (MDT). Os erros relacionados à criação do modelo digital de terrenos estão geralmente relacionados à erros de classificação, durante a separação dos retornos entre terrenos e não terreno. Uma das formas de minimizar é aumentando a densidade de pulsos, visando aumentar a probabilidade de se atingir o solo efetivamente. No entanto, o aumento da densidade de pulsos também implica no aumento do custo associado ao levantamento laser. Dessa forma, o objetivo deste estudo é qual a redução na densidade de pulsos que não compromete a qualidade do modelo digital de terreno. Os dados foram coletados em três áreas de floresta tropical: fazenda Cauaxi, no estado do Pará e em duas áreas na floresta nacional do Jamari, no estado de Rondônia. As nuvens de pontos foram processadas utilizando três algoritmos desenvolvidos por Kraus e Pfeifer, Hudak e Evans e Axelsson. Os modelos digitais gerados a partir de diferentes densidadse de pulsos foram comparados pelo erro padrão da estimativa (RMSE) com os respectivos modelos digitais de terreno gerados a partir da nuvem original. Como resultado observa-se que o algoritmo de Kraus e Pfeifer apresentou o melhor desempenho em relação aos demais, seguido do algoritmo proposto por Axelsson. Foi possível reduzir a densidade até 4 pulsos/m² mantendo uma resolução de 1 metro sem perda na qualidade do MDT.
