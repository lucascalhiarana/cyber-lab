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
- `find . -type f -size 1033c ! -executable -exec file {} +`: busca arquivos com 1033 bytes, não executáveis, e verifica o tipo de cada um[cite: 8]
- `cat ./maybehere07/.file2`: mostra o conteúdo do arquivo correto de texto ASCII[cite: 8]

O que deu errado: ao tentar buscar arquivos inicialmente, acabei caindo em um arquivo que gerou um texto gigantesco na tela e a senha não funcionou, pois era apenas um texto com linhas muito longas e não a credencial correta.

O que aprendi: o comando `find` combinado com `-size 1033c`, `! -executable` e `-exec file {} +` permite filtrar perfeitamente o arquivo exato que procuramos entre dezenas de subpastas[cite: 8].
