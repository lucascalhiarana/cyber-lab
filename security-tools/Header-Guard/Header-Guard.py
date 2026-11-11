# Bibliotecas que já vêm com o Python.
import sys

# Biblioteca usada para enviar a requisição ao site.
import requests

# Componentes do Rich usados para formatar a saída no terminal.
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


# Cria o objeto que exibirá painéis, tabelas e mensagens coloridas.
console = Console()


# Lista os valores reconhecidos pela especificação de Referrer-Policy.
POLITICAS_REFERRER_VALIDAS = (
    "no-referrer",
    "no-referrer-when-downgrade",
    "same-origin",
    "origin",
    "strict-origin",
    "origin-when-cross-origin",
    "strict-origin-when-cross-origin",
    "unsafe-url",
)

# Define os valores que nossa regra considera mais restritivos.
POLITICAS_REFERRER_SEGURAS = (
    "no-referrer",
    "same-origin",
    "strict-origin",
    "strict-origin-when-cross-origin",
)


def pontuar(status, peso):
    """Converte o status de um cabeçalho em pontos."""
    if status == "ok":
        return peso
    elif status == "weak":
        # Um cabeçalho fraco recebe metade do peso.
        return peso / 2
    else:
        # Um cabeçalho ausente recebe zero.
        return 0


def colorir_status(status):
    """Devolve um status com a cor correspondente para o Rich."""
    cores = {
        "ok": "green",
        "weak": "yellow",
        "missing": "red",
    }

    # Procura a cor associada ao status.
    cor = cores[status]

    # A marcação entre colchetes é interpretada pelo Rich.
    return f"[{cor}]{status}[/{cor}]"


def extrair_max_age(valor_hsts):
    """Extrai o valor de max-age do cabeçalho Strict-Transport-Security."""
    if valor_hsts is None:
        return None

    # As diretivas do HSTS são separadas por ponto e vírgula.
    for diretiva in valor_hsts.split(";"):
        # Separa o nome da diretiva e seu valor no primeiro sinal de igual.
        nome, separador, valor = diretiva.partition("=")

        # Compara o nome ignorando espaços e letras maiúsculas/minúsculas.
        if nome.strip().lower() == "max-age" and separador:
            return valor.strip()

    # Retorna None quando não encontra a diretiva.
    return None


def obter_politica_referrer_efetiva(valor_referrer):
    """Retorna o último valor reconhecido em Referrer-Policy."""
    if valor_referrer is None:
        return None

    politica_efetiva = None

    # O cabeçalho pode conter vários valores separados por vírgulas.
    for politica in valor_referrer.split(","):
        politica = politica.strip().lower()

        # Cada valor reconhecido substitui o anterior.
        if politica in POLITICAS_REFERRER_VALIDAS:
            politica_efetiva = politica

    return politica_efetiva


def analisar_site(url):
    """Analisa um site e devolve o código de saída correspondente."""
    try:
        # Faz uma requisição GET com limite de espera.
        # O Requests segue redirecionamentos de GET por padrão.
        resposta = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as erro:
        # Erros de conexão, DNS, timeout e URL são tratados aqui.
        console.print(
            Panel(
                f"Não foi possível acessar o site.\nDetalhe: {erro}",
                title="Erro de conexão",
                border_style="red",
            )
        )

        # Retorna 2; o loop principal poderá pedir outra URL.
        return 2

    # Mostra o destino final depois de eventuais redirecionamentos.
    console.print(f"[bold]URL final:[/bold] {resposta.url}")
    console.print(f"[bold]Status HTTP:[/bold] {resposta.status_code}")

    # Lê os seis cabeçalhos que serão classificados.
    hsts = resposta.headers.get("Strict-Transport-Security")
    csp = resposta.headers.get("Content-Security-Policy")
    content_type_options = resposta.headers.get("X-Content-Type-Options")
    frame_options = resposta.headers.get("X-Frame-Options")
    referrer_policy = resposta.headers.get("Referrer-Policy")
    permissions_policy = resposta.headers.get("Permissions-Policy")

    # Extrai max-age para avaliar a configuração do HSTS.
    max_age = extrair_max_age(hsts)

    # Determina a política Referrer-Policy efetiva.
    politica_referrer_efetiva = obter_politica_referrer_efetiva(
        referrer_policy
    )

    # Classifica o HSTS: ausente, fraco ou aprovado pela regra inicial.
    if hsts is None:
        hsts_status = "missing"
    elif (
        max_age is None
        or not max_age.isdigit()
        or int(max_age) <= 0
    ):
        hsts_status = "weak"
    else:
        hsts_status = "ok"

    # Verifica se a CSP está ausente ou contém marcadores fracos.
    # Esta é uma checagem inicial, não uma análise completa da política.
    if csp is None:
        csp_status = "missing"
    elif (
        "unsafe-inline" in csp.lower()
        or "unsafe-eval" in csp.lower()
    ):
        csp_status = "weak"
    else:
        csp_status = "ok"

    # X-Content-Type-Options deve ter exatamente o valor nosniff.
    if content_type_options is None:
        content_type_options_status = "missing"
    elif content_type_options.strip().lower() == "nosniff":
        content_type_options_status = "ok"
    else:
        content_type_options_status = "weak"

    # Para X-Frame-Options, aceita DENY ou SAMEORIGIN.
    if frame_options is None:
        frame_options_status = "missing"
    elif frame_options.strip().upper() in ("DENY", "SAMEORIGIN"):
        frame_options_status = "ok"
    else:
        frame_options_status = "weak"

    # Considera ok apenas as políticas Referrer mais restritivas da lista.
    if referrer_policy is None:
        referrer_policy_status = "missing"
    elif politica_referrer_efetiva in POLITICAS_REFERRER_SEGURAS:
        referrer_policy_status = "ok"
    else:
        referrer_policy_status = "weak"

    # Regra inicial para Permissions-Policy:
    # o wildcard * é considerado amplo demais.
    if permissions_policy is None:
        permissions_policy_status = "missing"
    elif "*" in permissions_policy:
        permissions_policy_status = "weak"
    else:
        permissions_policy_status = "ok"

    # Calcula pontos com o peso definido para cada cabeçalho.
    pontos_hsts = pontuar(hsts_status, 30)
    pontos_csp = pontuar(csp_status, 30)
    pontos_content_type_options = pontuar(
        content_type_options_status, 15
    )
    pontos_frame_options = pontuar(frame_options_status, 15)
    pontos_referrer_policy = pontuar(referrer_policy_status, 5)
    pontos_permissions_policy = pontuar(permissions_policy_status, 5)

    # Soma os pontos. Os pesos dos seis cabeçalhos totalizam 100.
    pontuacao = (
        pontos_hsts
        + pontos_csp
        + pontos_content_type_options
        + pontos_frame_options
        + pontos_referrer_policy
        + pontos_permissions_policy
    )

    # Converte a pontuação em uma nota.
    if pontuacao >= 90:
        nota = "A"
    elif pontuacao >= 80:
        nota = "B"
    elif pontuacao >= 70:
        nota = "C"
    elif pontuacao >= 60:
        nota = "D"
    else:
        nota = "F"

    # Converte a nota em código de saída para automações.
    if nota in ("A", "B"):
        codigo_saida = 0
    elif nota in ("C", "D"):
        codigo_saida = 1
    else:
        codigo_saida = 2

    # Cria a tabela formatada.
    tabela = Table(title="Cabeçalhos de segurança")
    tabela.add_column("Cabeçalho", style="cyan", overflow="fold")
    tabela.add_column("Gravidade")
    tabela.add_column("Status")
    tabela.add_column("Pontos", justify="right")
    tabela.add_column("Explicação", overflow="fold")

    # Guarda a explicação adequada para cada status do HSTS.
    explicacoes_hsts = {
        "missing": "O servidor não enviou o cabeçalho.",
        "weak": "max-age está ausente, zerado ou inválido.",
        "ok": "max-age é numérico e maior que zero.",
    }

    # Guarda a explicação adequada para cada status da CSP.
    explicacoes_csp = {
        "missing": "O servidor não enviou uma política de segurança de conteúdo.",
        "weak": "A política contém unsafe-inline ou unsafe-eval.",
        "ok": "Não encontramos esses marcadores nas verificações iniciais.",
    }

    # Guarda a explicação adequada para X-Content-Type-Options.
    explicacoes_content_type = {
        "missing": "O servidor não enviou X-Content-Type-Options.",
        "weak": "O valor enviado não é nosniff.",
        "ok": "nosniff está configurado.",
    }

    # Guarda a explicação adequada para X-Frame-Options.
    explicacoes_frame_options = {
        "missing": "O servidor não enviou X-Frame-Options.",
        "weak": "O valor não é DENY nem SAMEORIGIN.",
        "ok": "O valor restringe a exibição da página em frames.",
    }

    # Guarda a explicação adequada para Referrer-Policy.
    explicacoes_referrer = {
        "missing": "O servidor não definiu uma política explícita para o Referer.",
        "weak": "A política efetiva não está entre os valores aceitos.",
        "ok": "A política está entre os valores aceitos pela nossa regra.",
    }

    # Guarda a explicação adequada para Permissions-Policy.
    explicacoes_permissions = {
        "missing": "O servidor não enviou Permissions-Policy.",
        "weak": "A política contém * e permite qualquer origem nessa diretiva.",
        "ok": "A checagem inicial não encontrou o wildcard *.",
    }

    # Adiciona cada cabeçalho, gravidade, status, pontos e explicação à tabela.
    tabela.add_row(
        "Strict-Transport-Security",
        "Alta",
        colorir_status(hsts_status),
        str(pontos_hsts),
        explicacoes_hsts[hsts_status],
    )
    tabela.add_row(
        "Content-Security-Policy",
        "Alta",
        colorir_status(csp_status),
        str(pontos_csp),
        explicacoes_csp[csp_status],
    )
    tabela.add_row(
        "X-Content-Type-Options",
        "Média",
        colorir_status(content_type_options_status),
        str(pontos_content_type_options),
        explicacoes_content_type[content_type_options_status],
    )
    tabela.add_row(
        "X-Frame-Options",
        "Média",
        colorir_status(frame_options_status),
        str(pontos_frame_options),
        explicacoes_frame_options[frame_options_status],
    )
    tabela.add_row(
        "Referrer-Policy",
        "Baixa",
        colorir_status(referrer_policy_status),
        str(pontos_referrer_policy),
        explicacoes_referrer[referrer_policy_status],
    )
    tabela.add_row(
        "Permissions-Policy",
        "Baixa",
        colorir_status(permissions_policy_status),
        str(pontos_permissions_policy),
        explicacoes_permissions[permissions_policy_status],
    )

    # Exibe a tabela completa.
    console.print(tabela)

    # Escolhe a cor do painel conforme a nota final.
    if nota in ("A", "B"):
        cor_nota = "green"
    elif nota in ("C", "D"):
        cor_nota = "yellow"
    else:
        cor_nota = "red"

    # Exibe pontuação e nota em um painel.
    console.print(
        Panel(
            f"Pontuação: {pontuacao}/100\nNota: {nota}",
            title="Classificação final",
            border_style=cor_nota,
        )
    )

    # Monta recomendações para cabeçalhos ausentes ou fracos.
    recomendacoes = []

    # Verifica se o site terminou em HTTP após redirecionar.
    if not resposta.url.lower().startswith("https://"):
        recomendacoes.append(
            f"O destino final não usa HTTPS: {resposta.url}. "
            "Revise o redirecionamento."
        )

    if hsts_status != "ok":
        recomendacoes.append(
            "HSTS: configure max-age com um valor numérico positivo."
        )

    if csp_status != "ok":
        recomendacoes.append(
            "CSP: restrinja as fontes permitidas e evite "
            "unsafe-inline e unsafe-eval."
        )

    if content_type_options_status != "ok":
        recomendacoes.append(
            "X-Content-Type-Options: configure o valor nosniff."
        )

    if frame_options_status != "ok":
        recomendacoes.append(
            "X-Frame-Options: configure DENY ou SAMEORIGIN; "
            "avalie também frame-ancestors na CSP."
        )

    if referrer_policy_status != "ok":
        recomendacoes.append(
            "Referrer-Policy: considere "
            "strict-origin-when-cross-origin ou no-referrer."
        )

    if permissions_policy_status != "ok":
        recomendacoes.append(
            "Permissions-Policy: restrinja recursos às origens "
            "necessárias e evite *."
        )

    # Mostra as recomendações ou informa que nenhuma foi encontrada.
    if recomendacoes:
        console.print(
            Panel(
                "\n".join(recomendacoes),
                title="Recomendações",
                border_style="yellow",
            )
        )
    else:
        console.print(
            Panel(
                "Nenhum ajuste recomendado pelas regras iniciais.",
                title="Recomendações",
                border_style="green",
            )
        )

    # Devolve o código desta análise ao loop principal.
    return codigo_saida


def main():
    """Mostra a introdução e analisa sites até a pessoa digitar sair."""
    # Exibe a introdução uma vez no início do programa.
    console.print(
        Panel(
            "Analisa cabeçalhos HTTP de segurança e gera uma pontuação.\n"
            "Informe uma URL HTTPS para começar.\n"
            "Digite 'sair' quando quiser encerrar.",
            title="HeaderGuard",
            border_style="cyan",
        )
    )

    # Guarda o pior código de saída entre os sites analisados.
    # 0 = A/B; 1 = C/D; 2 = F ou erro de rede.
    codigo_saida_final = 0

    # Repete o pedido de URL até receber o comando sair.
    while True:
        url = input(
            "\nDigite uma URL HTTPS ou 'sair' para encerrar: "
        ).strip()

        # Permite encerrar sem diferenciar maiúsculas e minúsculas.
        if url.lower() == "sair":
            console.print("[cyan]HeaderGuard encerrado.[/cyan]")
            return codigo_saida_final

        # Uma entrada sem HTTPS é inválida, então pede outra URL.
        if not url.lower().startswith("https://"):
            console.print(
                "[red]URL inválida. Digite um endereço começando com "
                "https://[/red]"
            )
            continue

        # Analisa o site. Se houver erro de rede, a função mostra a
        # mensagem e devolve 2; o loop continua pedindo outra URL.
        codigo_saida = analisar_site(url)

        # Mantém o resultado mais grave entre todas as análises.
        codigo_saida_final = max(codigo_saida_final, codigo_saida)


# Executa main somente quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    sys.exit(main())