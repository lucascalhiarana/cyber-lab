import random
# 1. Gera os 9 primeiros dígitos aleatórios
nove_digitos = ''
for i in range(9):
    nove_digitos += str(random.randint(0, 9))
# --- CÁLCULO DO 1º DÍGITO ---
# Multiplica cada dígito de 'nove_digitos' por pesos de 10 até 2
soma_1 = 0
contador_regressivo_1 = 10
for digito in nove_digitos:
    soma_1 += int(digito) * contador_regressivo_1
    contador_regressivo_1 -= 1
digito_1 = (soma_1 * 10) % 11
digito_1 = digito_1 if digito_1 <= 9 else 0
# --- CÁLCULO DO 2º DÍGITO ---
# Agora consideramos os 10 dígitos (9 iniciais + 1º dígito) com pesos de 11 até 2
dez_digitos = nove_digitos + str(digito_1)
soma_2 = 0
contador_regressivo_2 = 11
for digito in dez_digitos:
    soma_2 += int(digito) * contador_regressivo_2
    contador_regressivo_2 -= 1
digito_2 = (soma_2 * 10) % 11
digito_2 = digito_2 if digito_2 <= 9 else 0
# --- RESULTADO FINAL ---
cpf_gerado = f'{nove_digitos}{digito_1}{digito_2}'
print(f'CPF Gerado: {cpf_gerado}')