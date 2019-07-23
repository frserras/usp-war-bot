Este código foi produzido para a página USP WAR Bot, uma página de War Bot no facebook para a a Cidade Universitária da USP. 

Dois scripts compõe o código: usp_war_bot.py e verifier.py

O arquivo usp_war_bot.py implementa um mecanismo simples de um War Bot baseado em dados demográficos relativos. Para tal, ele precisa partir de um arquivo serializado do tipo pickle, que contenha os dados populacionais e de vizinhança das unidades originais. Ele também precisa de um arquivo rodada.txt que contenha o número da próxima rodada a ser rrealizada, começando em 1. Para as rodadas seguintes à rodada 1, é necessário que o programa tenha acesso, no mesmo diretório, aos arquivos de dominância (.dom) e unidades(.units) da rodada imetiatamente anterior, assim como ao arquivo original, que é necessário em todas as rodadas. 

Cada chamada do script (sem argumentos) equivale a uma rodada. Parâmetros como seed do gerador aleatório e probabilidade de reataque devem ser definidas diretamente no código fonte. As variáveis correspondentes estão sinalizadas.

O programa funcionará para qualquer mapa, contanto que seja fornecido um arquivo inicial de unidades que mapeia as unidades existentes, suas populações e relações de vizinhança de maneira correta. Cada unidade contém também pontos especiais de ataque e defesa. No jogo original esses pontos foram utilizados para atribuir poder de ataque e defesa a regiões sem população ou com dados demograficos desconhecidos, como a Raia, e em escala menor, para equilibrar o jogo e torná-lo factível em função das simulações realizadas. Tais pontos foram definidos antes da primeira rodada e nunca mais alterados.

O arquivo verifier.py simplesmente extrai as informações das unidades e a árvore de dominância para uma rodada específica, a ser especificada diretamente no código, e imprime essas informações para que o usuário possa realizar verificação da corretude da simulação, se necessário.

O programa está disponibilizado sob Licença GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007). Mais detalhes podem ser encontrados no arquivo LICENSE.txt

Para fins de verificação, no diretório compactado arquivos_jogo_original.zip estão disponibilizados todos os arquivos das unidades e árvores de dominância para todas as rodadas do jogo original, narrado na Página do facebook. Para que as rodadas sejam resimuladas é necessário extrair esses arquivos para o mesmo diretório dos scripts. Mais detalhes sobre as seeds pode ser encontrado no usp_war_bot.py.

É necessário esclarecer que na narração de algumas rodadas foi invertido o atacante, para fins narrativos. O território conquistado e o conquistador foram sempre preservados. As últimas 3 rodadas foram narradas como uma rodada única. Nenhuma modificação foi realizada no código ou resultados em função da narrativa. 

Esse projeto é apenas um projeto de ficção e entretenimento, assim como um exercício de programação realizado por alunos. Ele não possui nenhuma conexão oficial com a USP ou qualquer uma de suas unidades.
