\## Lista de Compras Interativa



\*\*Objetivo:\*\* Criar um programa em Python que simula uma lista de compras no terminal, permitindo inserir, apagar, listar itens e sair com segurança.



\### O que o programa faz:

\- `\[i]nserir`: Adiciona itens ao final da lista usando `.append()`.

\- `\[a]pagar`: Exibe os itens enumerados e remove pelo índice usando `.pop(indice)`.

\- `\[l]istar`: Percorre a lista exibindo `índice : item` com a função `enumerate()`.

\- `\[s]air`: Interrompe a repetição do programa usando `break`.



\### Dificuldades e pontos de atenção:

\- \*\*Indentação:\*\* no Python, comandos irmãos dentro do `while` precisam estar na mesma coluna de espaços.

\- \*\*`for` na inserção:\*\* tentar rodar um `for` dentro da opção de inserir não funcionava no início porque a lista começava vazia (com tamanho zero).

\- \*\*Entrada de dados:\*\* o `input()` sempre entrega texto (`string`), então para usar como índice numérico foi necessário converter com `int()`.



\### O que aprendi:

\- \*\*`enumerate(lista)`:\*\* permite percorrer uma lista recebendo a posição numérica (`índice`) e o `item` ao mesmo tempo em um laço `for`.

\- \*\*`len(lista)`:\*\* verifica a quantidade de itens na lista (usado para checar se a lista estava vazia antes de tentar apagar).

\- \*\*`try / except`:\*\* atua como rede de proteção para tratar erros esperados (`IndexError` quando o índice não existe e `ValueError` quando o usuário digita letras em vez de números), impedindo o programa de quebrar.
