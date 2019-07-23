##############################################
#                USP WAR BOT                 #
#         Autor: Felipe R. Serras            #
#                Versão 1.3                  #
##############################################
'''
Código Produzido para a Página USP WAR BOT, 
coadministrada com Danilo Bissoli Apendino e Luccas Cairolli
(A Samantha Condessa foi testemunha de paz.)

Esse código está disponibilizado sob  a GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007).
Para mais detalhe consulte o arquivo LICENSE.txt

Esse programa se utiliza da biblioteca namedlist sem realizar nenhuma alteração nela.
Ela não está inclusa no código fonte e deveria ser instalada separadamente.
Ela foi desenvolvida por  Eric V. Smith e está disponibilizada sob a licença Apache Software License  2.0
(https://pypi.org/project/namedlist/)

'''

#IMPORTAÇÕES:
from namedlist import namedlist
import random
import pickle

#Algumas rodadas foram sorteadas usando a seed automática. Para maior variedade em algumas rodadas 
#foram escolhidas seeds específicas sem saber quais seriam os resultados gerados. Algumas das seeds usadas
#estão listadas à seguir:
#Rodada 87, seed:198976798976798976797676 (Com Reataque 0.7)
#Ultimas Rodadas: O dia que a página começou: 1062019; O dia em que o Dobby entrou n projeto (invertido):91026050 ; O dia em que sorteamos as ultimas rodada (sem o ano ) 1607

random.seed()

#VARIÁVEIS GLOBAIS:
#Probabilidade de ao vencer uma batalha, um território batalhar na mesma rodada com outro território do Dominante vencido:
prob_reAtaque=0.0 #Setado para 0.0, como estava no começo do jogo.

#Objeto Correspondente a Unidade, que carrega todos os seus atributos
#(Nome, Graduandos, Pós-Graduandos, Docentes, Funcionários, Pontos de Ataque Especial, Pontos de Defesa Especial e UNidades Vizinhas)
fields='id grad posgrad doc func esp_atak esp_def vizinhos'
Unidade=namedlist('Unidade', fields)

#Objeto correspondente a Árvore de dominância de uma unidade. Juntas todas as arvores de dominância caracterizam a divisão do
#território. Cada Árovre contám o Nome do Dominante e a lista dos nomes dos dominados:
fields_dom='id dominados'
Dominancia=namedlist('Dominancia', fields_dom)


#FUNÇÕES AUXILIARES:


#Função que sorteia com igual probabilidade uma das Unidades que domina ao menos um territŕoio 
#para ser o Dominante atacante:
def sorteia_dominante(ref_dom):
	return random.choice(ref_dom).id

#Função que sorteaia uma unidade dominada dado um dominante, para ser a unidade atacante da rodada:
def sorteia_unidade_dominada(id_dom,ref_dom):
	dom=search(id_dom,ref_dom)
	return random.choice(dom.dominados)

#Função que busca numa lista de unidades a unidade que possui o ide fornecido e retorna seu objeto de Unidade
#correspondente, permitindo acessar as informações reevantes e alterá-las:
def search(id,ref_unidades):
	for unidade in ref_unidades:
		if(id==unidade.id):
			return unidade
	print("UNIDADE NÃO ENCONTRADA!")
	return "NULL"

#Função que busca, numa lista de árvores de dominância, o nome da unidade que tem em sua lista de dominados
#a unidade cujo nome está representado na variável de entrada id, permitindo que se descobra quem é o dominante
#de um determinado território a qualquer momento do jogo.
def search_dominante(id,ref_dom):
	for unidade in ref_dom:
		for id_unidade_dominada in unidade.dominados:
			if id_unidade_dominada==id:
				return unidade.id
	print("Erro: Unidade sem domínio")
	return "NULL"


#Função que sorteia, dado um território um dentre os seus vizinhos atacáveis, ou seja,
#um de seus vizinhos que não pertença ao mesmo domínio que ele:
def sorteia_vizinho(id_unidade, ref_unidades,ref_dom):
	unidade=search(id_unidade,ref_unidades)
	dom_unidade=search_dominante(id_unidade,ref_dom)
	vizinhos_atacaveis=[]
	for id_vizinho in unidade.vizinhos:
		dom_vizinho=search_dominante(id_vizinho,ref_dom)
		if dom_unidade!=dom_vizinho:
			vizinhos_atacaveis.append(id_vizinho)
	if len(vizinhos_atacaveis)==0:
		return "0"
	else:
		return random.choice(vizinhos_atacaveis)

#FUNÇÕES PRINCIPAIS

#Função que reoganiza a lista de unidades e a lista de árvore de dominâncias após um conflito. Usada como função auxiliar
#para a função executa_batalha()
def reorganiza_unidades(id_vencedor,id_vencido,id_dom_vencedor,id_dom_vencido,ref_unidades,ref_dom,ref_orig):
	#Carrega as fatias das árvores de dominância e os objetos de unidade necessários:
	dom_vencedor=search(id_dom_vencedor,ref_dom)
	dom_vencido=search(id_dom_vencido,ref_dom)
	stats_originais=search(id_vencido,ref_orig)
	vencido=search(id_vencido,ref_unidades)
	vencedor=search(id_vencedor,ref_unidades)

	#Incrementa os stats de todas as unidades do domínio vencedor:
	for id_unidade in dom_vencedor.dominados:
		unidade=search(id_unidade,ref_unidades)
		unidade.grad=unidade.grad+stats_originais.grad
		unidade.posgrad=unidade.posgrad+stats_originais.posgrad
		unidade.doc=unidade.doc+stats_originais.doc
		unidade.func=unidade.func+stats_originais.func
		unidade.esp_atak=unidade.esp_atak+stats_originais.esp_atak
		unidade.esp_def=unidade.esp_def+stats_originais.esp_def

	#Atualiza os stats da unidade vencida de forma a igualá-los as unidades do domínio vencedor:
	vencido.grad=vencedor.grad
	vencido.posgrad=vencedor.posgrad
	vencido.doc=vencedor.doc
	vencido.func=vencedor.func
	vencido.esp_atak=vencedor.esp_atak
	vencido.esp_def=vencedor.esp_def

	#Remove a Unidade dominada da árvore de dominância do domínio vencido e adiciona ela a do domínio vencedor:
	dom_vencido.dominados.remove(vencido.id)
	dom_vencedor.dominados.append(vencido.id)

	#Atualiza o domínio vencido. Se sua árvore de  dominância está vazia o domínio perdeu o jogo e é excluído
	#da lista de árvores de dominância. Caso contrário subtrai os stats originais da unidade vencida de todas
	#as unidades remanescentes do domínio vencido:
	if(len(dom_vencido.dominados)==0):
		ref_dom.remove(dom_vencido)
	else:
		for id_unidade in dom_vencido.dominados:
			unidade=search(id_unidade,ref_unidades)
			unidade.grad=unidade.grad-stats_originais.grad
			unidade.posgrad=unidade.posgrad-stats_originais.posgrad
			unidade.doc=unidade.doc-stats_originais.doc
			unidade.func=unidade.func-stats_originais.func
			unidade.esp_atak=unidade.esp_atak-stats_originais.esp_atak
			unidade.esp_def=unidade.esp_def-stats_originais.esp_def

	#Reataque:
	if random.random()<prob_reAtaque:
		print("REATAQUE")
		id_atacado=sorteia_vizinho(id_vencido,ref_unidades,ref_dom)
		if(id_atacado!="0" and search_dominante(id_atacado,ref_dom)==id_dom_vencido):
			executa_batalha(id_vencido,id_atacado,ref_unidades,ref_dom,ref_orig)





#FUNÇÃO QUE EXECUTA A BATALHA ENTRE DUAS UNIDADES
def executa_batalha(id_atacante,id_atacado,ref_unidades,ref_dom,ref_orig):
	#Carregam-se os objetos de unidade  e as árvores de dominância necessárias:
	atacante=search(id_atacante,ref_unidades)
	id_atacante_dom=search_dominante(id_atacante,ref_dom)
	atacado=search(id_atacado,ref_unidades)
	id_atacado_dom=search_dominante(id_atacado,ref_dom)

	print(id_atacante +"("+id_atacante_dom+") ataca "+id_atacado +"("+id_atacado_dom+")"+".")
	
	#Calcula-se os fatores de ataque e defesa para o atacante e o atacado, respectivamente:
	fator_ataque= atacante.grad/23391+atacante.posgrad/16308 +atacante.esp_atak
	print('f_atak: '+str(fator_ataque))
	fator_defesa= atacado.doc/2221+atacado.func/4467 +atacado.esp_def
	print('f_def: '+str(fator_defesa))
	#Calcula=-se a probabilidade de o ataque ser bem sucedido:
	prob_atak=fator_ataque/(fator_ataque+fator_defesa)
	print('p_atak: '+str(prob_atak))

	#Sorteia o resultado do ataque e reorganiza o mapa em função do resultado
	if(random.random()< prob_atak):
		print(id_atacante+" vence e conquista "+id_atacado+" para "+id_atacante_dom+".")
		reorganiza_unidades(id_atacante,id_atacado,id_atacante_dom,id_atacado_dom,ref_unidades,ref_dom,ref_orig)
	else:
		print(id_atacado+ " vence e conquista "+id_atacante+" para "+id_atacado_dom+".")
		reorganiza_unidades(id_atacado,id_atacante,id_atacado_dom,id_atacante_dom,ref_unidades,ref_dom,ref_orig)


#PROCEDIMENTO PRINCIPAL:

#Carrega o número da rodada atua do arquivo:
with open('rodada.txt', 'r') as f:
	rodada=int(f.readline())

#Carrega os objetos de unidade da rodada anterior:
file_rodada_anterior="usp_war_bot_"+str(int(rodada)-1)+".units"
with open(file_rodada_anterior, 'rb') as f:
	unidades=pickle.load(f)

#Carrega o ós dados originais das unidades:
file_rodada_0="usp_war_bot_0.units"
with open(file_rodada_0, 'rb') as f:
	ref_orig=pickle.load(f)

#Carrega a arvore de dominancia da rodada anterior:
file_dominancia_anterior="usp_war_bot_"+str(int(rodada)-1)+".dom"
with open(file_dominancia_anterior, 'rb') as f:
	lista_dom=pickle.load(f)

#Sorteia o domínio atacante
id_dom=sorteia_dominante(lista_dom)

#Sorteia uma unidade desse domínio como a unidade atacante:
continuar=True
while(continuar):
	id_atacante=sorteia_unidade_dominada(id_dom,lista_dom)
	id_atacado=sorteia_vizinho(id_atacante,unidades,lista_dom)
	continuar=False
	if id_atacado=="0":
		continuar=True


#Executa a batalha:
executa_batalha(id_atacante,id_atacado,unidades,lista_dom,ref_orig)
print("____________________________________________")

#Se o jogo acabou notifica e imprime a árvore de dominância final para verificação:
if len(lista_dom)==1:
	print("FIM")
	print(rodada)
	print(lista_dom)

#Salva os objetos de unidades para a próxima rodada:
file_resultado_rodada="usp_war_bot_"+str(rodada)+".units"
with open(file_resultado_rodada, 'wb') as f:
	pickle.dump(unidades,f)

#Salva a árvore de domínio para a próxima rodada:
file_resultado_rodada_dom="usp_war_bot_"+str(rodada)+".dom"
with open(file_resultado_rodada_dom, 'wb') as f:
	pickle.dump(lista_dom,f)

#Salva o número atualizado da próxima rodada:
with open('rodada.txt' ,'w') as f:
	f.write(str(rodada+1))
