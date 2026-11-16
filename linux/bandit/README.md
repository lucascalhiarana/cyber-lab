\# Notas do Bandit (OverTheWire)



\## Bandit 0



Objetivo: entrar no servidor do jogo por SSH. O usuário e a senha do nível 0 estão na página do nível.



\- `ssh bandit0@bandit.labs.overthewire.org -p 2220`: conecta numa máquina remota e abre um terminal nela

&#x20; - `bandit0` é o usuário e `bandit.labs.overthewire.org` é o servidor, no formato `usuario@servidor`

&#x20; - `-p 2220` define a porta, porque o servidor não usa a 22, que é a padrão do SSH



O que deu errado: rodei o comando sem o `bandit0@` e o SSH tentou entrar com o meu usuário local (`lucas`, e na VM `root`). A resposta foi "Permission denied" mesmo com a senha certa, porque o usuário estava errado. O servidor avisou isso na tela e o prompt mostrava o usuário que ele estava tentando. Resolvi escrevendo o usuário antes do `@`.



O que aprendi: o SSH usa o usuário local quando não informo outro, e o prompt de senha diz qual usuário está sendo tentado. Na primeira conexão ele pergunta se confio no servidor (fingerprint) e eu respondo `yes` (rever).


## Bandit 0 → 1

Objetivo: achar a senha do próximo nível num arquivo chamado `readme` na pasta home.

- `ls`: lista os arquivos da pasta atual
- `cat readme`: mostra o conteúdo do arquivo `readme` no terminal

O que aprendi: depois de entrar no servidor, o primeiro passo é ver o que tem na pasta com `ls`, e depois ler o arquivo com `cat`.

## Bandit 1 → 2

Objetivo: ler um arquivo cujo nome é `-` (só um traço), na pasta home.

- `cat ./-`: mostra o conteúdo do arquivo chamado `-`

O que deu errado: `cat -` não funcionou, porque o `-` sozinho é interpretado como "ler da entrada do teclado", e não como o nome de um arquivo. O `./` na frente mostra que é um caminho, e não uma opção do comando.

O que aprendi: arquivos com nome começando em `-` precisam do `./` na frente, senão o comando acha que é uma opção.

## Bandit 1 → 2

Objetivo: ler um arquivo cujo nome é `-` (só um traço), na pasta home do usuário bandit1.

- `exit`: fecha a conexão SSH e volta ao terminal local
- `cat ./-`: mostra o conteúdo do arquivo chamado `-`
- `pwd`: mostra a pasta em que estou

O que deu errado: tentei `cat ./-` logado como bandit0 e deu "No such file or directory". O arquivo estava na pasta do bandit1, e eu ainda estava no usuário do nível anterior. Resolvi lendo a senha do bandit1 no nível 0, saindo com `exit` e entrando de novo por SSH como bandit1.

O que aprendi: cada nível guarda a senha do próximo, então preciso sair e logar com o usuário do nível seguinte antes de procurar o arquivo. O `./` na frente do nome faz o `-` ser lido como nome de arquivo, e não como opção do comando.



## Bandit 2 → 3

Objetivo: ler um arquivo cujo nome contém espaços e começa por traços (`--spaces in this filename--`), na pasta home do usuário bandit2.

- `cat "./--spaces in this filename--"`: mostra o conteúdo do arquivo com espaços e traços no nome
- `ls -la`: lista todos os arquivos do diretório atual, incluindo detalhes de permissão e arquivos ocultos

O que deu errado: tentei procurar a pasta `inhere` (do Level 3) enquanto ainda estava logado como bandit2. Ao tentar ler o arquivo, comandos como `cat "--spaces in this filename--"` falharam com "unexpected argument" porque o `cat` interpretou os traços iniciais (`--`) como opções/flags do próprio comando.

O que aprendi: antes de procurar os arquivos do nível, preciso confirmar no prompt se já estou logado no usuário correto (`bandit2` vs `bandit3`). Quando o nome de um arquivo começa por traços (`--`), o Linux entende como parâmetro de comando; adicionar `./` na frente (`./--spaces...`) força o terminal a interpretar a entrada como o caminho de um arquivo no diretório atual, e as aspas `""` tratam os espaços como parte do mesmo nome.


## Bandit 3 → 4

Objetivo: ler um arquivo oculto chamado `...Hiding-From-You` localizado dentro do diretório `inhere` (na pasta home do usuário bandit3).

- `cd inhere`: navega para o diretório `inhere`
- `ls -a`: lista todos os arquivos do diretório atual, incluindo arquivos ocultos
- `cat ./...Hiding-From-You`: exibe o conteúdo do arquivo oculto com múltiplos pontos no nome

O que deu errado: tentei ler o arquivo diretamente usando apenas o nome com `cat`, mas deu erro de "No such file or directory" porque o nome do arquivo começa com três pontos (`...`), fazendo o terminal interpretar o caminho de forma incorreta.

O que aprendi: arquivos ocultos no Linux começam com ponto, e quando o nome possui múltiplos pontos no início, é necessário colocar o `./` na frente (`./...Hiding-From-You`) para o terminal entender que se trata de um arquivo no diretório atual.

## Bandit 4 → 5

Objetivo: ler o único arquivo legível por humanos (*human-readable*) no diretório `inhere`, na pasta home do usuário bandit4.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `pwd`: mostra a pasta em que estou
- `cd inhere`: navega para o diretório `inhere`
- `ls -a`: lista todos os arquivos do diretório atual, incluindo os ocultos
- `file ./-*`: identifica o tipo de cada arquivo no diretório para achar o que é texto legível
- `cat ./-file07`: mostra o conteúdo do arquivo legível por humanos

O que deu errado: tentei ler os arquivos diretamente sem saber qual era texto, e ao usar apenas o nome com `cat`, o terminal dava erro porque os nomes começam com traço (`-file00`, etc.), sendo interpretados como opções do comando. Além disso, tentar ler arquivos binários diretamente no terminal desconfigura a tela.

O que aprendi: o comando `file` permite identificar o tipo de arquivo (*ASCII text* vs *data*) antes de abri-lo. Para arquivos cujos nomes começam com traço (`-`), é necessário usar o `./` na frente (`./-file07`) para evitar que o Linux interprete o nome como uma flag do comando.

## Bandit 5 → 6

Objetivo: encontrar e ler um arquivo em subdiretórios de `inhere` que seja legível por humanos (*human-readable*), tenha exatamente 1033 bytes e não seja executável.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `pwd`: mostra a pasta em que estou
- `cd inhere`: navega para o diretório `inhere`
- `find . -type f -size 1033c ! -executable -exec file {} +`: busca arquivos com 1033 bytes, não executáveis, e verifica o tipo de cada um
- `cat ./maybehere07/.file2`: mostra o conteúdo do arquivo correto de texto ASCII

O que deu errado: ao tentar buscar arquivos inicialmente, acabei caindo em um arquivo que gerou um texto gigantesco na tela e a senha não funcionou, pois era apenas um texto com linhas muito longas e não a credencial correta.

O que aprendi: o comando `find` combinado com `-size 1033c`, `! -executable` e `-exec file {} +` permite filtrar perfeitamente o arquivo exato que procuramos entre dezenas de subpastas.

## Bandit 6 → 7

Objetivo: encontrar um arquivo armazenado em algum lugar do servidor que pertença ao usuário `bandit7`, ao grupo `bandit6` e tenha exatamente 33 bytes de tamanho.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`: busca em todo o sistema de arquivos pelo arquivo com 33 bytes, pertencente ao usuário `bandit7` e grupo `bandit6`, ocultando erros de permissão
- `cat <caminho_do_arquivo>`: mostra o conteúdo do arquivo correto para obter a senha do próximo nível

O que deu errado: ao executar o comando no terminal, a falta de atenção na sintaxe dos parâmetros ou tentar ler o arquivo antes de filtrar corretamente gerou erro de sintaxe e de leitura no `cat`.

O que aprendi: o comando `find /` combinado com `-user bandit7`, `-group bandit6` e `-size 33c` permite rastrear todo o sistema de arquivos da raiz até encontrar o arquivo correto que atende a todos os critérios simultaneamente.

## Bandit 7 → 8

Objetivo: encontrar a senha para o próximo nível armazenada no arquivo `data.txt` ao lado da palavra `millionth`.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `ls`: lista os arquivos do diretório atual para confirmar a presença do `data.txt`
- `cat data.txt | grep millionth`: lê o conteúdo do arquivo e filtra usando o pipe (`|`) e o `grep` para exibir apenas a linha que contém a palavra "millionth"
- `grep millionth data.txt`: forma direta de buscar a palavra "millionth" dentro do arquivo `data.txt`

O que deu errado: tentar ler o arquivo `data.txt` inteiro sem filtrar com o `grep` resulta em milhares de linhas de texto na tela, tornando impossível localizar a senha manualmente.

O que aprendi: o uso do operador pipe (`|`) combinado com o `grep` (ou passando o arquivo direto para o `grep`) permite pesquisar e filtrar strings específicas dentro de arquivos extensos rapidamente.

## Bandit 8 → 9

Objetivo: encontrar a única linha de texto no arquivo `data.txt` que ocorre apenas uma vez.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `sort data.txt | uniq -u`: ordena o arquivo alfabeticamente para agrupar as linhas duplicadas e filtra com `uniq -u` para exibir apenas a linha que não se repete

O que deu errado: usar apenas o comando `uniq -u` sem ordenar o arquivo antes não funciona, pois o `uniq` só identifica linhas duplicadas se elas estiverem adjacentes (uma ao lado da outra).

O que aprendi: o comando `uniq` requer que a entrada esteja previamente ordenada com o `sort` para detectar duplicatas corretamente, e a flag `-u` isola exclusivamente o elemento único do arquivo.

## Bandit 9 → 10

Objetivo: encontrar a senha para o próximo nível armazenada no arquivo `data.txt` como uma das poucas sequências legíveis por humanos (*human-readable*), precedida por vários caracteres `=`.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `strings data.txt | grep "="`: extrai todas as cadeias de texto legíveis do arquivo binário `data.txt` e filtra com o `grep` para exibir apenas as linhas que contêm o caractere `=`

O que deu errado: tentar ler o arquivo `data.txt` diretamente com o comando `cat` exibe caracteres binários e desconfigura o terminal, pois o arquivo não é um texto simples.

O que aprendi: o comando `strings` é essencial para extrair texto legível contido dentro de arquivos binários ou de dados brutos, e a combinação com o `grep` permite localizar rapidamente a chave correta baseada no padrão de caracteres.

## Bandit 10 → 11

Objetivo: decodificar os dados codificados em Base64 armazenados no arquivo `data.txt` para descobrir a senha do próximo nível.

- `exit`: fecha a conexão atual (SSH ou terminal)
- `base64 -d data.txt`: lê diretamente o arquivo codificado em Base64 e aplica a descodificação para revelar o texto original
- `cat data.txt | base64 -d`: lê o conteúdo do arquivo com o `cat` e envia o fluxo através de um pipe para o comando `base64 -d` executar a descodificação

O que deu errado: tentar ler o arquivo `data.txt` com o `cat` sem decodificar mostrava apenas strings corrompidas e ilegíveis cheias de caracteres estranhos.

O que aprendi: o comando `base64` com a flag `-d` (*decode*) permite reverter o formato de codificação Base64 de volta para texto plano legível.
