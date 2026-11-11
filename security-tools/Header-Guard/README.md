# HeaderGuard

Ferramenta de linha de comando em Python que consulta cabeçalhos HTTP de segurança e apresenta uma pontuação, uma classificação e recomendações.

## Funcionalidades

- Recebe endereços HTTPS em sequência. Digite sair para encerrar.
- Faz uma requisição GET com limite de espera de 10 segundos.
- Segue redirecionamentos e mostra o endereço final analisado.
- Avalia seis cabeçalhos de segurança.
- Exibe status, pontuação e explicações em uma tabela colorida.
- Recomenda ajustes para cabeçalhos ausentes ou fracos.
- Retorna códigos de saída úteis para automações.

## Cabeçalhos avaliados

| Cabeçalho | Peso | Verificação inicial |
|---|---:|---|
| Strict-Transport-Security | 30 | Verifica se max-age existe, é numérico e maior que zero. |
| Content-Security-Policy | 30 | Sinaliza unsafe-inline e unsafe-eval. |
| X-Content-Type-Options | 15 | Considera nosniff o valor esperado. |
| X-Frame-Options | 15 | Considera DENY e SAMEORIGIN os valores aceitos. |
| Referrer-Policy | 5 | Considera políticas mais restritivas da lista definida no código. |
| Permissions-Policy | 5 | Sinaliza o uso do wildcard *. |

## Pontuação e classificação

- ok: recebe o peso completo do cabeçalho.
- weak: recebe metade do peso.
- missing: recebe zero.
- A: 90 pontos ou mais.
- B: de 80 a 89 pontos.
- C: de 70 a 79 pontos.
- D: de 60 a 69 pontos.
- F: menos de 60 pontos.

## Códigos de saída

| Código | Resultado |
|---:|---|
| 0 | Nota A ou B |
| 1 | Nota C ou D |
| 2 | Nota F ou erro de rede |

## Requisitos

- Python instalado.
- Dependências listadas em requirements.txt.

## Instalação no PowerShell

Abra o terminal na pasta do projeto e execute:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Como executar

Na pasta do projeto, com o ambiente virtual ativo:

    python Header-Guard.py

Informe um endereço HTTPS quando solicitado. O programa continuará pedindo outros endereços até você digitar sair.

## Limites das verificações

As verificações de Content-Security-Policy e Permissions-Policy são heurísticas iniciais. Um resultado ok significa que os marcadores definidos no código não foram encontrados; isso não garante que toda a política esteja segura. Use os resultados como uma triagem e revise as políticas conforme os recursos e as origens realmente necessários pelo site.

## Uso responsável

Use o HeaderGuard em sites que você administra ou tem autorização para avaliar.
