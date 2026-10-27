# =============================================================================
# 1. TABELAS DE REGRAS E CONHECIMENTO CRIPTOGRÁFICO
# =============================================================================

# Lista de tuplas com prefixos conhecidos (Self-describing hashes / PHC strings).
# Formato: (Prefixo, Nome do Algoritmo, Nível de Confiança, Motivo explicativo)
PREFIX_RULES = [
    # Argon2: Vencedor da competição de hashing de senhas de 2015 (padrão moderno da indústria)
    ("$argon2id$", "Argon2id", "ALTA", "Padrão moderno PHC string (alta segurança)"),
    ("$argon2i$",  "Argon2i",  "ALTA", "Variante do Argon2 resistente a ataques side-channel"),
    ("$argon2d$",  "Argon2d",  "ALTA", "Variante do Argon2 com foco contra GPUs"),

    # Família Bcrypt: amplamente utilizado em sistemas web nos últimos 15 anos
    ("$2b$",       "Bcrypt",   "ALTA", "Bcrypt padrão atual (variante 2b)"),
    ("$2a$",       "Bcrypt",   "ALTA", "Bcrypt legado (variante 2a)"),
    ("$2y$",       "Bcrypt",   "ALTA", "Bcrypt clássico gerado pelo PHP"),

    # Unix Crypt: formatos clássicos encontrados no arquivo /etc/shadow do Linux
    ("$6$",        "SHA-512 crypt", "ALTA", "Unix crypt com SHA-512 (padrão no Linux moderno)"),
    ("$5$",        "SHA-256 crypt", "ALTA", "Unix crypt com SHA-256"),
    ("$1$",        "MD5 crypt",     "ALTA", "Unix crypt com MD5 (legado e vulnerável)"),

    # Servidores Apache: hashes de autenticação básica (.htpasswd)
    ("$apr1$",     "Apache MD5",    "ALTA", "Formato gerado pelo comando 'htpasswd -m'"),

    # Frameworks Web
    ("pbkdf2_sha256$", "Django PBKDF2", "ALTA", "Formato padrão do framework web Django"),
]

# Dicionário de regras para hashes hexadecimais puros.
# A chave é o comprimento em caracteres (len) e o valor é a lista de algoritmos possíveis.
# O primeiro item da lista é sempre o mais comum no mundo real!
HEX_RULES = {
    16:  ["MySQL323 (legado)", "CRC-64"],
    32:  ["MD5", "NTLM (Windows)", "MD4", "RIPEMD-128"],
    40:  ["SHA-1", "RIPEMD-160"],
    56:  ["SHA-224", "SHA3-224"],
    64:  ["SHA-256", "SHA3-256", "BLAKE2s-256"],
    96:  ["SHA-384"],
    128: ["SHA-512", "Whirlpool", "BLAKE2b-512"],
}


# =============================================================================
# 2. FUNÇÃO AUXILIAR: VALIDAÇÃO DE HEXADECIMAL
# =============================================================================

def eh_hexadecimal(texto):
    """
    Verifica se o texto contém exclusivamente caracteres hexadecimais válidos.
    O alfabeto hexadecimal aceita apenas dígitos de 0 a 9 e letras de 'a' até 'f'.
    """
    # String vazia não pode ser considerada hexadecimal
    if not texto:
        return False
    
    try:
        # A função int(..., 16) tenta interpretar o texto na base 16.
        # Se houver caracteres fora da base 16 (ex: g, z, @, espaços), o Python lança um ValueError.
        int(texto, 16)
        return True
    except ValueError:
        return False


# =============================================================================
# 3. MOTOR DE IDENTIFICAÇÃO (CLASSIFICADOR)
# =============================================================================

def identificar_hash(texto):
    """
    Analisa a estrutura do texto e retorna uma lista de tuplas com os candidatos:
    [(Nome do Algoritmo, Grau de Confiança, Motivo)]
    """
    tamanho = len(texto)
    candidatos = []

    # ETAPA 1: Hashes que anunciam a própria identidade através de prefixos (PHC strings)
    # Como o prefixo é uma assinatura explícita, a confiança é sempre ALTA.
    for prefixo, algo, confianca, motivo in PREFIX_RULES:
        if texto.startswith(prefixo):
            candidatos.append((algo, confianca, motivo))
            return candidatos  # Encontrou o prefixo exato, já podemos retornar

    # ETAPA 2: Detecção de formatos comuns que NÃO são hashes (Falsos-positivos comuns)
    
    # Caso A: JSON Web Token (JWT)
    # Começa com 'eyJ' (base64 de '{"') e tem 2 pontos que dividem header.payload.signature
    if texto.startswith("eyJ") and texto.count(".") == 2:
        candidatos.append((
            "JWT (Token de Autenticação)", 
            "BAIXA", 
            "Inicia com 'eyJ' e possui 3 partes separadas por pontos. Não é um hash!"
        ))
        return candidatos

    # Caso B: Base64 genérico
    # Hashes hexadecimais nunca têm '+', '/' ou '='. A presença deles indica dado em Base64.
    if any(c in texto for c in "+/=") and tamanho > 8:
        candidatos.append((
            "Blob em Base64", 
            "BAIXA", 
            "Contém caracteres exclusivos de Base64 (+, /, =). Não parece ser um hash puro."
        ))
        return candidatos

    # ETAPA 3: Hashes hexadecimais tradicionais analisados pelo comprimento
    if eh_hexadecimal(texto):
        # Se o tamanho existir no nosso dicionário de tamanhos conhecidos:
        if tamanho in HEX_RULES:
            algoritmos = HEX_RULES[tamanho]
            for indice, algo in enumerate(algoritmos):
                # O primeiro item é o mais popular (confiança MÉDIA, pois não há prefixo garantindo)
                # Os demais candidatos menos comuns recebem confiança BAIXA
                confianca = "MÉDIA" if indice == 0 else "BAIXA"
                motivo = f"Comprimento exato de {tamanho} caracteres hexadecimais"
                candidatos.append((algo, confianca, motivo))

    return candidatos


# =============================================================================
# 4. INTERFACE DE TERMINAL (LOOP INTERATIVO)
# =============================================================================

def main():
    # Cabeçalho visual
    print("=" * 65)
    print("        IDENTIFICADOR DE HASH PROFISSIONAL - (v2.0)")
    print("           Digite 'sair' para encerrar o programa")
    print("=" * 65)

    # Mantém o programa aberto para o usuário testar vários hashes em sequência
    while True:
        try:
            # Entrada do usuário: .strip() remove espaços acidentais nas pontas
            entrada = input("\nDigite ou cole o hash para identificar: ").strip()

            # Se o usuário apertar Enter em branco, volta para o início do loop
            if not entrada:
                continue

            # Se digitar 'sair', quebra o loop e encerra a execução
            if entrada.lower() == "sair":
                print("\nPrograma finalizado com sucesso. Até mais!")
                break

            # Executa a identificação
            resultados = identificar_hash(entrada)

            # Exibição do resumo
            print("\n--- RESULTADO DA ANÁLISE ---")
            print(f"Texto fornecido: {entrada}")
            print(f"Comprimento:     {len(entrada)} caracteres\n")

            # Se encontrou candidatos, imprime em formato de tabela elegante
            if resultados:
                # O operador :<25 garante largura fixa de 25 caracteres para alinhar as colunas
                print(f"{'ALGORITMO':<25} | {'CONFIANÇA':<10} | MOTIVO")
                print("-" * 65)
                for algo, conf, mot in resultados:
                    print(f"{algo:<25} | {conf:<10} | {mot}")
            else:
                print("Não identificado com as regras atuais (formato desconhecido ou não suportado).")

        # Permite ao usuário sair a qualquer momento teclando Ctrl + C
        except KeyboardInterrupt:
            print("\n\nEncerrando o programa...")
            break


# Garante que o script só rode a função main() quando executado diretamente
if __name__ == "__main__":
    main()