# Medidas de Mitigação e Prevenção

Para proteger os ambientes contra ataques de força bruta, dicionário e password spraying, recomendam-se as seguintes práticas:

## 1. Políticas de Senhas e Bloqueio de Contas
* **Complexidade e Comprimento:** Exigir senhas longas (mínimo de 12 a 16 caracteres) e evitar termos comuns de dicionário.
* **Bloqueio Temporário (Account Lockout):** Bloquear temporariamente contas após um número pré-determinado de tentativas incorretas (ex: 5 tentativas = 15 minutos de bloqueio).
* **Defesa contra Password Spraying:** Monitorar falhas de login distribuídas por múltiplos usuários vindas da mesma origem ou em janelas curtas de tempo.

## 2. Autenticação Multifator (MFA)
* Implementar MFA (2FA) em todos os serviços de acesso externo ou administrativo, inviabilizando o acesso mesmo que a senha seja descoberta.

## 3. Proteção no Nível de Rede e Aplicação
* **Rate Limiting / Throttling:** Limitar a taxa de requisições por endereço IP em formulários web e serviços de login.
* **WAF e Ferramentas Anti-Bruteforce:** Utilizar ferramentas como Fail2ban ou CrowdSec para identificar e banir automaticamente IPs maliciosos no firewall.
* **Desativação de Serviços Legados:** Desativar serviços inseguros como FTP puro e versões antigas de SMB (SMBv1), migrando para SFTP/SSH e SMBv3 assinado.