##############################################
#            USP WAR BOT verifier            #
#         Autor: Felipe R. Serras            #
#                Versão 1.1                  #
##############################################
'''
Código auxiliar Ppoduzido para a Página USP WAR BOT, 
coadministrada com Danilo Bissoli Apendino e Luccas Cairolli
(A Samantha Condessa foi testemunha de paz.)

Esse código está disponibilizado sob  a GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007).
Para mais detalhe consulte o arquivo LICENSE.txt

Esse programa se utiliza da biblioteca namedlist sem realizar nenhuma alteração nela.
Ela não está inclusa no código fonte e deveria ser instalada separadamente.
Ela foi desenvolvida por  Eric V. Smith e está disponibilizada sob a licença Apache Software License  2.0
(https://pypi.org/project/namedlist/)

A função desse script é imprimir na tela o estado da lista de unidades e arvore de dominancias de uma
rodada específica, especificada pela variavel rodada_verificada. Isso foi utilizado para a verificação da
corretude do código e resultados, rodada-a-rodada.

'''


from namedlist import namedlist
import pickle

rodada_verificada='91'

fields_dom='id dominados'
Dominancia=namedlist('Dominancia', fields_dom)
fields='id grad posgrad doc func esp_atak esp_def vizinhos'
Unidade=namedlist('Unidade', fields)
with open('usp_war_bot_'+rodada_verificada+'.dom', 'rb') as f:
	lista_dom=pickle.load(f)
with open('usp_war_bot_'+rodada_verificada+'.units' ,'rb') as f:
	units=pickle.load(f) 

print(lista_dom)
print("**************************************************************")
print("**************************************************************")
for unit in units:
	print(unit)
	print("-----------------------------------------------------------")
