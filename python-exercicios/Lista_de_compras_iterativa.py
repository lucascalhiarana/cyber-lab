"""
Faça uma lista de compras com listas
O usuário deve ter a possibilidade de 
inserir, apagar e listar valores da sua lista
Não permita que o programa quebre com
erros de índices inexistentes na lista.
"""

lista_de_compras = []

print("Bem vindo a sua lista de compras!")

while True:
    opcao = input('Você quer [i]serir, [a]pagar, [l]istar [s]air:  \n')
    if opcao == 'i':
        item = input('Qual item gostaria de adicionar?  \n')
        lista_de_compras.append(item)
        # for indice, item in enumerate(lista_de_compras):
        print(f"'{item}' foi adicionado com sucesso!\n")
            # print(f"'{indice}:{lista_de_compras}'")

    elif opcao == 'a':
        if len(lista_de_compras) == 0:
            print('A lista está vazia! Não há nada para apagar.\n')
        else:
            for indice, item in enumerate(lista_de_compras):
                print(f"{indice} : {item}")
            try:    
                indice = int(input("Digite o índice que deseja apagar:  \m"))
                item_apagado = lista_de_compras.pop(indice)
                print(f"O item '{item_apagado}' foi apagado com sucesso!\n")
            except IndexError:
                 print("Erro: esse índice não existe na lista!\n")
            except ValueError:
                 print("Erro: Digite apenas números inteiros válidos!\n")
    elif opcao == 'l':
        if len(lista_de_compras) == 0:
                    print('A lista está vazia! Não há nada para apagar.\n')
        else:
             for indice, item in enumerate(lista_de_compras):
                  print(f"{indice} : {item}")
    
    elif opcao == 's':
         print('Saindo do programa... Até mais')
         break        


        

        