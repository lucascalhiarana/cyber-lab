# 🔍 Identificador de Hash (Hash Identifier)

Uma ferramenta de linha de comando desenvolvida em Python para analisar cadeias de caracteres criptográficas e identificar quais algoritmos de hash provavelmente as produziram.

Construído com base em fundamentos de segurança da informação, inspeção de charset e formatos padrão de strings criptográficas (PHC string formats).

---

## 🚀 Funcionalidades

- **Reconhecimento por Assinatura / Prefixo (Alta Confiança):**
  - Argon2 (`$argon2id$`, `$argon2i$`, `$argon2d$`)
  - Bcrypt (`$2a$`, `$2b$`, `$2y$`)
  - Unix Crypt (`$6$` SHA-512, `$5$` SHA-256, `$1$` MD5)
  - Apache htpasswd (`$apr1$`)
  - Django PBKDF2 (`pbkdf2_sha256$`)
- **Reconhecimento por Comprimento Hexadecimal:**
  - 16 caracteres: MySQL323
  - 32 caracteres: MD5, NTLM, MD4, RIPEMD-128
  - 40 caracteres: SHA-1, RIPEMD-160
  - 56 caracteres: SHA-224, SHA3-224
  - 64 caracteres: SHA-256, BLAKE2s-256
  - 96 caracteres: SHA-384
  - 128 caracteres: SHA-512, Whirlpool
- **Detecção de Falsos-Positivos:**
  - Identifica e alerta sobre tokens **JWT** (`eyJ...`)
  - Identifica blobs genéricos codificados em **Base64** (`+`, `/`, `=`)
- **Interface Interativa:** Loop contínuo com saída formatada em tabela e níveis de confiança (`ALTA`, `MÉDIA`, `BAIXA`).

---

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Nenhuma dependência externa necessária (feito em Python puro com a biblioteca padrão).

### Executando o projeto

No terminal (PowerShell, Bash ou CMD), navegue até a pasta do projeto e execute:

```bash
python identificador-hash.py
```

---

## 🧪 Exemplos de Uso

### 1. Hash MD5 (32 caracteres hex):
```text
Digite ou cole o hash para identificar: 5f4dcc3b5aa765d61d8327deb882cf99

--- RESULTADO DA ANÁLISE ---
ALGORITMO                 | CONFIANÇA  | MOTIVO
-----------------------------------------------------------------
MD5                       | MÉDIA      | Comprimento exato de 32 caracteres hexadecimais
NTLM (Windows)            | BAIXA      | Comprimento exato de 32 caracteres hexadecimais
MD4                       | BAIXA      | Comprimento exato de 32 caracteres hexadecimais
```

### 2. Bcrypt (Prefixo explícito):
```text
Digite ou cole o hash para identificar: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQNQy.uk4Of2T7G

--- RESULTADO DA ANÁLISE ---
ALGORITMO                 | CONFIANÇA  | MOTIVO
-----------------------------------------------------------------
Bcrypt                    | ALTA       | Bcrypt padrão atual (variante 2b)
```

---

## 👨‍💻 Autor

Desenvolvido para estudo e prática de segurança ofensiva/defensiva e programação em Python.