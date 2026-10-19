\- `ssh usuario@servidor -p PORTA`: conecta a uma máquina remota (a porta só é necessária se não for a 22)

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
- `find . -type f -size 1033c ! -executable -exec file {} +`: busca arquivos com 1033 bytes, não executáveis, e verifica o tipo de cada um[cite: 8]
- `cat ./maybehere07/.file2`: mostra o conteúdo do arquivo correto de texto ASCII[cite: 8]