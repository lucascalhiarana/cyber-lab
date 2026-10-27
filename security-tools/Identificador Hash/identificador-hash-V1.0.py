# Função para conferir se o texto usa apenas o alfabeto hexadecimal
def eh_hexadecimal(texto):
    """Retorna True se o texto contiver apenas caracteres hexadecimais (0-9, a-f)."""
    if len(texto) == 0:
        return False
    try:
        # A função int(..., 16) tenta converter o texto para número na base 16.
        # Se houver qualquer caractere proibido (como g, z, @), o Python lança um ValueError.
        int(texto, 16)
        return True
    except ValueError:
        # Se caiu no erro, significa que não é hexadecimal puro
        return False


# Função para identificar qual seria o tipo do hash
def identificador_hash(texto):
    """Analisa as características do texto e retorna uma lista de possíveis algoritmos."""
    tamanho = len(texto)
    candidatos = []

    # 1. Confere se é Bcrypt (começa com assinaturas $2a$, $2b$, $2y$ e tem entre 50 e 60 caracteres)
    if texto.startswith(("$2a$", "$2b$", "$2y$")) and (50 <= tamanho <= 60):
        candidatos.append("Bcrypt (algoritmo moderno e seguro para senhas)")
        return candidatos

    # 2. Confere se é JWT (começa com 'ey' e possui 2 pontos separando as 3 partes do token)
    if texto.startswith("ey") and texto.count(".") == 2:
        candidatos.append("Atenção: isso NÃO é um hash! É um JWT (JSON Web Token de autenticação).")
        return candidatos

    # 3. Se for hexadecimal puro, confere o comprimento para deduzir o tipo
    if eh_hexadecimal(texto):
        if tamanho == 32:
            candidatos = ["MD5 (mais comum)", "NTLM", "MD4"]
        elif tamanho == 40:
            candidatos = ["SHA-1"]
        elif tamanho == 64:
            candidatos = ["SHA-256"]
        elif tamanho == 128:
            candidatos = ["SHA-512"]

    return candidatos


# Função principal: cuida da interação com o usuário no terminal
def main():
    # Exibe o cabeçalho inicial do programa
    print("=" * 50)
    print("      IDENTIFICADOR DE HASH - (V1.0)")
    print(" Digite 'sair' para encerrar o programa")
    print("=" * 50)

    # Inicia o loop infinito para que o programa continue rodando até o usuário pedir para sair
    while True:
        try:
            # Recebe o input do usuário e remove espaços acidentais nas pontas (.strip())
            entrada = input("\nDigite ou cole o hash para identificar: ").strip()

            # Se o usuário apenas apertou Enter sem digitar nada, volta para o início do loop
            if not entrada:
                continue

            # Se o usuário digitou 'sair' (maiúsculo ou minúsculo), encerra o programa
            if entrada.lower() == "sair":
                print("\nPrograma finalizado. Até mais!")
                break

            # Chama a função e guarda a lista de algoritmos encontrados na variável possiveis_hashes
            possiveis_hashes = identificador_hash(entrada)

            # Exibe o resumo da análise
            print(f"\n--- RESULTADO ---")
            print(f"Texto: {entrada}")
            print(f"Comprimento: {len(entrada)} caracteres")

            # Se a lista de possíveis hashes não estiver vazia, imprime cada um deles
            if possiveis_hashes:
                print("\nPossíveis algoritmos:")
                for h in possiveis_hashes:
                    print(f" -> {h}")
            # Caso nenhuma regra tenha identificado o texto
            else:
                print("\nNão identificado com as regras atuais.")

        # Permite sair de forma limpa caso o usuário aperte Ctrl + C no terminal
        except KeyboardInterrupt:
            print("\n\nSaindo...")
            break


# Garante que a função main() só seja executada se este arquivo for rodado diretamente no terminal
if __name__ == "__main__":
    main()