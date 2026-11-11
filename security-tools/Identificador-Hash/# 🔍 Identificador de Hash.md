# 🔍 Identificador de Hash em Python

Um script simples e eficiente desenvolvido em Python puro para analisar sequências criptográficas e deduzir quais algoritmos de hash provavelmente as geraram.

---

## 📌 Sobre o Projeto

Em cibersegurança e testes de invasão, quando encontramos senhas armazenadas ou hashes vazados, o primeiro desafio é saber qual algoritmo os gerou antes de qualquer tentativa de auditoria ou quebra.

O objetivo deste projeto foi aplicar lógica de programação e fundamentos de criptografia para construir um identificador do zero, sem dependências externas, analisando padrões estruturais, prefixos e tamanhos de saída.

---

## ⚙️ Como Funciona o Algoritmo

O programa atua como um sistema de regras e dedução dividido em três etapas:

1. **Assinaturas e Prefixos (PHC Strings - Confiança Alta):**
   - Muitos algoritmos modernos anunciam sua própria identidade no início da string.
   - O script verifica prefixos conhecidos como `$2b$` (Bcrypt), `$argon2id$` (Argon2), `$6$` (SHA-512 Unix Crypt do Linux) e `$apr1$` (Apache).
   - Por ser uma assinatura explícita, o resultado é classificado com **confiança ALTA**.

2. **Detecção de Falsos-Positivos (Tokens e Codificações):**
   - **JWT:** Identifica tokens de autenticação Web que começam com `eyJ` e possuem 3 partes separadas por pontos (`.`).
   - **Base64:** Identifica dados codificados que contenham caracteres exclusivos como `+`, `/` ou `=`.
   - Em ambos os casos, alerta o usuário que a entrada **não é um hash puro**.

3. **Comprimento e Base Hexadecimal (Confiança Média/Baixa):**
   - Verifica se o texto é composto exclusivamente pelo alfabeto hexadecimal (`0-9` e `a-f`).
   - Se for hexadecimal puro, analisa a quantidade de caracteres para mapear os algoritmos clássicos correspondentes:
     - **32 caracteres:** MD5 (mais provável), NTLM (Windows), MD4.
     - **40 caracteres:** SHA-1, RIPEMD-160.
     - **64 caracteres:** SHA-256, BLAKE2s.
     - **128 caracteres:** SHA-512, Whirlpool.
   - O algoritmo mais comum no mercado recebe **confiança MÉDIA**, e alternativas secundárias recebem **confiança BAIXA**.

4. **Interface e Usabilidade:**
   - Loop contínuo que permite testar múltiplos hashes em sequência.
   - Saída formatada em colunas (Algoritmo | Confiança | Motivo).
   - Saída limpa ao digitar `sair` ou pressionar `Ctrl + C`.

---

## 🚀 Como Executar

### Pré-requisitos
- Ter o [Python 3.x](https://www.python.org/) instalado na máquina.
- Nenhuma biblioteca adicional necessária (utiliza apenas recursos nativos do Python).

### Executando o script
No terminal, na pasta do projeto, execute:

```bash
python identificador-hash.py