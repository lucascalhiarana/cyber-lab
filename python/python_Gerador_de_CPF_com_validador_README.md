# 🪪 Gerador de CPF Válido em Python

Um script simples e direto desenvolvido em Python para gerar números de CPF válidos com base no algoritmo oficial da Receita Federal.

---

## 📌 Sobre o Projeto

O objetivo deste projeto foi aplicar lógica de programação e pensamento computacional para entender como funciona o cálculo dos dígitos verificadores do CPF, criando uma ferramenta capaz de gerar números matematicamente válidos para fins de teste e desenvolvimento.

---

## ⚙️ Como Funciona o Algoritmo

1. **9 Primeiros Dígitos:** Gerados aleatoriamente utilizando o módulo nativo `random`.
2. **Cálculo do 1º Dígito:**
   - Multiplicação de cada um dos 9 primeiros dígitos por uma contagem regressiva de pesos de **10 a 2**.
   - Soma de todas as multiplicações, multiplicada por 10 e calculada com o resto da divisão por 11 (`% 11`).
   - Se o resultado for maior que 9, o dígito passa a ser `0`.
3. **Cálculo do 2º Dígito:**
   - Considera os 9 dígitos iniciais somados ao 1º dígito recém-calculado (totalizando 10 dígitos).
   - Multiplicação por uma contagem regressiva de pesos de **11 a 2**.
   - Aplica-se a mesma fórmula matemática para encontrar o segundo dígito.
4. **Resultado:** Junção de todos os dígitos para compor o CPF final no formato de 11 números.

---

## 🚀 Como Executar

### Pré-requisitos
- Ter o [Python 3.x](https://www.python.org/) instalado na máquina.

### Executando o script
No terminal, na pasta do projeto, execute:

```bash
python gerador_cpf.py