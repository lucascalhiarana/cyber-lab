# DIO Agent — Mentor de Segurança

> Uma especialização do DIO Agent para aprender análise defensiva de vulnerabilidades com contexto, avaliação de risco e recomendações de correção.

O DIO Agent é um mentor de estudos orientado por arquivos. Este projeto amplia o agente original com uma skill de análise de vulnerabilidades, uma base de conhecimento de Segurança da Informação e instruções para que o agente conduza a conversa de forma didática e responsável. Nenhum modelo foi treinado: o comportamento é orientado pelo conteúdo do repositório.

## O que foi acrescentado

- **Análise de vulnerabilidades:** a skill `vulnerability-analysis` orienta o agente a entender o cenário antes de avaliar uma falha, explicar o conceito, estimar impacto e probabilidade, justificar a severidade, sugerir investigação defensiva e recomendar melhorias.
- **Fundamentos de segurança:** `agent/knowledge/security-basics.md` reúne os conceitos de vulnerabilidade, ameaça e risco, a tríade confidencialidade, integridade e disponibilidade (CID) e boas práticas.
- **Persona de segurança:** `agent/persona.md` reforça o papel de mentor que explica, pergunta antes de orientar e prioriza práticas defensivas.
- **Descoberta da skill:** `AGENTS.md` registra quando o agente deve aplicar `vulnerability-analysis`.

A skill não é uma resposta pronta nem uma ferramenta de varredura. É um roteiro para ajudar o estudante a raciocinar sobre o contexto e aprender o processo.

## Arquivos envolvidos

```text
agent/
├── app.py                              Exemplo de login com consulta parametrizada
├── persona.md                          Identidade, tom e especialização do agente
└── knowledge/
    └── security-basics.md               Conceitos e boas práticas de segurança
skills/
└── vulnerability-analysis/
    ├── SKILL.md                         Processo que o agente segue
    └── README.md                        Explicação da skill para pessoas
AGENTS.md                                Instruções e registro das skills
README.md                                Visão geral e instruções deste projeto
```

## Como executar no Hermes

O Hermes precisa ser iniciado com a pasta do projeto como diretório atual, para que consiga ler `AGENTS.md`, a persona e as skills.

1. Instale o [Hermes](https://hermes-agent.nousresearch.com/docs), seguindo a documentação oficial.
2. Baixe ou clone este repositório e abra a pasta que contém `AGENTS.md` no VS Code.
3. Abra o terminal integrado do VS Code nessa pasta. Confira o caminho com `pwd` no PowerShell (`Get-Location` também funciona).
4. Inicie o Hermes:

   ```powershell
   hermes
   ```

   Se o comando não estiver no PATH, use o caminho do executável da sua instalação. Por exemplo:

   ```powershell
   & "$env:LOCALAPPDATA\hermes\bin\hermes.exe"
   ```

5. Faça uma pergunta sobre segurança e forneça o contexto que você conhece. O agente deve aplicar a skill quando o assunto for análise de vulnerabilidades.

## Exemplo de conversa

Use um ambiente próprio ou de laboratório e comece com contexto suficiente para uma avaliação responsável:

```text
Estou estudando segurança em uma máquina Ubuntu de laboratório que eu administro.
Quero avaliar uma configuração que pode estar insegura. Antes de sugerir comandos,
me pergunte quais informações faltam. Depois, ajude a avaliar impacto, probabilidade,
severidade e formas de corrigir.
```

A skill orienta o agente a esclarecer o sistema, o ambiente, as versões, o comportamento observado e a autorização antes de propor investigação. Com os dados disponíveis, a análise deve separar fatos de hipóteses e explicar as recomendações.

## Exemplo de código: login com SQLite

`agent/app.py` mostra um exemplo de autenticação que usa parâmetros na consulta SQL. O código valida os tipos recebidos, fecha a conexão e falha de forma controlada quando ocorre um erro do SQLite. A parametrização impede que os valores fornecidos sejam interpretados como parte da instrução SQL.

Para praticar, compare esse padrão com uma versão de laboratório que concatene entradas na consulta. Analise somente código e sistemas seus ou para os quais você tenha autorização. Depois, peça ao agente para explicar a falha, avaliar o risco e revisar a correção. A consulta parametrizada reduz o risco de SQL Injection; ela não substitui outras medidas, como armazenamento seguro de senhas.

## Skills do agente

| Skill | Finalidade |
|---|---|
| [Análise de vulnerabilidades](skills/vulnerability-analysis/README.md) | Conduz uma análise defensiva, contextualiza o risco e orienta melhorias. |
| [Plano de estudos](skills/study-plan/SKILL.md) | Organiza objetivos e rotina de aprendizagem. |
| [Destravar desafio](skills/unblock-challenge/SKILL.md) | Ajuda o estudante a avançar sem entregar a solução pronta. |
| [Explicar conceito](skills/explain-concept/SKILL.md) | Explica conceitos de tecnologia de forma didática. |
| [Pesquisa na web](skills/web-search/SKILL.md) | Ajuda a responder dúvidas que dependem de informações atuais. |
| [Revisão de portfólio](skills/portfolio-review/SKILL.md) | Orienta a revisão de portfólio e GitHub. |
| [Caminho AI Builder](skills/ai-builder-path/SKILL.md) | Ajuda a escolher próximos passos na carreira AI Builder. |

## Limites e uso responsável

Use os exemplos em laboratório e faça avaliações somente em sistemas próprios ou com autorização explícita. A análise do agente é educativa e depende das informações fornecidas; confirme descobertas e correções com documentação, evidências e validação apropriada ao ambiente.

## Sobre o projeto base

Este projeto parte do [DIO Agent](https://github.com/digitalinnovationone/dio-agent), um mentor de estudos para quem aprende tecnologia na DIO. Consulte o [README original](https://github.com/digitalinnovationone/dio-agent) e a [documentação do Hermes](https://hermes-agent.nousresearch.com/docs) para obter informações atualizadas sobre o harness.

Bons estudos! 🔐
