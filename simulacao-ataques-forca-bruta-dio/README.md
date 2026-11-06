# Simulação de Ataques de Autenticação em Ambiente Controlado

Projeto prático desenvolvido para demonstrar técnicas de teste de autenticação (força bruta, automação web e password spraying) e respectivas medidas defensivas, utilizando um laboratório isolado no VirtualBox.

## 🖥️ Topologia do Laboratório

* **Máquina Atacante:** Kali Linux (Adaptador 1: NAT | Adaptador 2: Host-Only)
* **Máquina Alvo:** Metasploitable 2 (Adaptador: Host-Only - 192.168.56.105)
* **Ferramentas:** Nmap, Medusa, Hydra e Enum4linux.

## 📌 Cenários Executados

### 1. Reconhecimento de Rede
Mapeamento de portas e versões dos serviços com o Nmap para validação dos vetores de ataque:
* FTP (Porta 21)
* HTTP / DVWA (Porta 80)
* SMB (Portas 139 e 445)

### 2. Força Bruta no Serviço FTP
* Utilização da ferramenta **Medusa** com wordlists simples de usuários e senhas.
* Filtro de saída com redirecionamento de descritores e `grep` para identificação de credenciais válidas.

### 3. Automação de Login Web (DVWA)
* Inspeção dos parâmetros de formulário HTTP POST via Developer Tools (F12).
* Execução de teste de credenciais automatizado com **Hydra**, tratando parâmetros de requisição e validação de strings de erro (`Login failed`).

### 4. Enumeração e Password Spraying no SMB
* Enumeração prévia dos usuários locais do alvo utilizando **enum4linux**.
* Aplicação da técnica de **Password Spraying** com o **Medusa** (módulo `smbnt`), testando uma credencial contra múltiplos usuários enumerados.

## 🛡️ Medidas de Defesa
As diretrizes completas de mitigação, proteção contra ataques de dicionário e políticas de segurança estão descritas no arquivo `mitigacao.md`.