\- `ssh usuario@servidor -p PORTA`: conecta a uma máquina remota

- `ls`: lista os arquivos da pasta atual
- `cat arquivo`: mostra o conteúdo de um arquivo
- `cat ./-arquivo`: o `./` na frente serve pra arquivos cujo nome começa com `-`, senão o comando acha que é uma opção

- `exit`: fecha a conexão atual (SSH ou terminal)
- `pwd`: mostra a pasta em que estou

- `ls -la`: lista todos os arquivos do diretório atual, incluindo permissões e arquivos ocultos
- `cat "./--spaces in this filename--"`: mostra o conteúdo do arquivo com espaços e traços no nome

- `exit`: fecha a conexão atual (SSH ou terminal)
- `pwd`: mostra a pasta em que estou
- `cd inhere`: navega para o diretório `inhere`
- `ls -a`: lista todos os arquivos do diretório atual, incluindo os ocultos
- `cat ./...Hiding-From-You`: mostra o conteúdo do arquivo oculto com múltiplos pontos no nome

- `cd inhere`: navega para o diretório `inhere`
- `ls -a`: lista todos os arquivos do diretório atual, incluindo os ocultos
- `file ./-*`: identifica o tipo de cada arquivo no diretório para achar o que é texto legível
- `cat ./-file07`: mostra o conteúdo do arquivo legível por humanos

- `cd inhere`: navega para o diretório `inhere`
- `find . -type f -size 1033c ! -executable -exec file {} +`: busca arquivos com 1033 bytes, não executáveis, e verifica o tipo de cada um
- `cat ./maybehere07/.file2`: mostra o conteúdo do arquivo correto de texto ASCII

- `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`: busca em todo o sistema de arquivos pelo arquivo com 33 bytes, pertencente ao usuário `bandit7` e grupo `bandit6`, ocultando erros de permissão
- `cat <caminho_do_arquivo>`: mostra o conteúdo do arquivo correto para obter a senha do próximo nível

- `ls`: lista os arquivos do diretório atual para confirmar a presença do `data.txt`
- `cat data.txt | grep millionth`: lê o conteúdo do arquivo e filtra usando o pipe (`|`) e o `grep` para exibir apenas a linha que contém a palavra "millionth"
- `grep millionth data.txt`: forma direta de buscar a palavra "millionth" dentro do arquivo `data.txt`

- `sort data.txt | uniq -u`: ordena o arquivo alfabeticamente para agrupar as linhas duplicadas e filtra com `uniq -u` para exibir apenas a linha que não se repete

- `strings data.txt | grep "="`: extrai todas as cadeias de texto legíveis do arquivo binário `data.txt` e filtra com o `grep` para exibir apenas as linhas que contêm o caractere `=`

- `base64 -d data.txt`: lê diretamente o arquivo codificado em Base64 e aplica a descodificação para revelar o texto original
- `cat data.txt | base64 -d`: lê o conteúdo do arquivo com o `cat` e envia o fluxo através de um pipe para o comando `base64 -d` executar a descodificação
