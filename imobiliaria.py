import csv
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

imoveis = {
    'Casa': {
        'base': 900,
        'extra_quarto': 250,   # a partir do 2º quarto
        'garagem': 300,        # por vaga
    },
    'Apartamento': {
        'base': 700,
        'extra_quarto': 200,   # a partir do 2º quarto
        'garagem': 300,        # por vaga
        'sem_crianca': 0.05,
    },
    'Studio': {
        'base': 1200,
        'garagem_2vagas': 250, # pacote com 2 vagas
        'garagem_extra': 60,   # cada vaga adicional além das 2
    },
}

contrato_total = 2000.00
contrato_parcelas = 5

def calcular_aluguel(imovel, quartos, vagas, crianca):
    dados = imoveis.get(imovel)
    if dados is None:
        raise ValueError(f"Tipo de imóvel '{imovel}' não reconhecido.")
    valor = dados['base']

    if imovel in ['Casa', 'Apartamento'] and quartos > 1:
        valor += (quartos - 1) * dados['extra_quarto']

    if vagas > 0:
        if imovel in ['Casa', 'Apartamento']:
            valor += vagas * dados['garagem']
        else:
            if imovel == 'Studio':
                if vagas < 2:
                    raise ValueError("Studio requer mínimo de 2 vagas no pacote.")
                valor += dados['garagem_2vagas']
                if vagas > 2:
                    valor += (vagas - 2) * dados['garagem_extra']
    if imovel == 'Apartamento' and not crianca:
        valor *= (1 - dados['sem_crianca'])
    return valor

def gerar_csv(nome_cliente, imovel, aluguel_mensal, parcela_contrato, parcelas):
    nome_arquivo = f'contrato_{nome_cliente.replace(" ", "_")}_{datetime.now().strftime("%d%m%Y%H%M%S")}.csv'
    hoje = date.today()

    with open(nome_arquivo, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Parcela', 'Vencimento', 'Aluguel R$', 'Parcela Contrato R$', 'Total R$'])

        for i in range(1,13):
            vencimento = hoje + relativedelta(months=i)
            contrato = parcela_contrato if i <= parcelas else 0.00
            total = aluguel_mensal + contrato
            writer.writerow ([
                f'{i:02d} de 12',
                vencimento.strftime('%d/%m/%Y'),
                f'{aluguel_mensal:.2f}',
                f'{contrato:.2f}',
                f'{total:.2f}', 
             ])

    return nome_arquivo
    
def input_nome(mensagem):
    while True:
        nome = input(mensagem).strip()
        if nome:
            return nome
        else:
            print('Nome não pode ser vazio. Por favor, digite o nome do cliente.')
            
def input_int(mensagem, minimo = 0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:
                print(f' Digite um valor igual ou maior que {minimo}')
            else:
                return valor
        except ValueError:
            print('Digite um número inteiro válido.')
def input_resposta(mensagem,opcoes):
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in opcoes:
            return resposta
        else:
            print(f'Opção inválida. Digite uma das opções válidas: {opcoes}')
def input_imovel():
    opcoes = list(imoveis.keys())
    while True:
        imovel = input(f'Tipo de imóvel: (Casa, Apartamento, Studio): ').strip().title()
        if imovel in imoveis:
            return imovel
        else:
            print('Tipo de imóvel inválido. Por favor, escolha entre Casa, Apartamento ou Studio.')
while True:
    print('\n' + '=' * 55)
    print('   🏠  IMOBILIÁRIA R.M  —  Gerador de Orçamento')
    print('=' * 55)    

    nome_cliente = input_nome('Nome do cliente: ').strip()

    imovel = input_imovel()

    quartos = 1
    if imovel != 'Studio':
        quartos = input_int('Número de quartos:', minimo = 1)

    vagas = 0
    quer_vaga = input_resposta('Deseja incluir vaga de garagem? (S/N): ', ['S','N'])
    if quer_vaga == 'S':
        if imovel == 'Studio':
            vagas = input_int('Número de vagas de garagem( mínimo 2 para pacote): ', minimo =2)
        else:
            vagas = input_int('Número de vagas de garagem:', minimo = 1)
        
    crianca = False
    if imovel == 'Apartamento':
        resposta_crianca = input_resposta('Há crianças no imóvel? (S/N): ', ['S','N'])
        crianca = resposta_crianca == 'S'
    
    parcelas = input_int('Em quantas vezes deseja parcelar o contrato? (máximo 5): ', minimo = 1)
    parcelas = min(parcelas, contrato_parcelas)

    aluguel_mensal = calcular_aluguel(imovel, quartos, vagas, crianca)
    parcela_contrato = contrato_total / parcelas
    total_mensal = aluguel_mensal + parcela_contrato

    print('\n' + '-' * 55)
    print(f'  ORÇAMENTO — {nome_cliente.upper()}')
    print('-' * 55)
    print(f'  Imóvel          : {imovel}')
    if imovel != 'Studio':
        print(f'  Quartos         : {quartos}')
    if vagas > 0:
        print(f'  Vagas de garagem: {vagas}')
    if imovel == 'Apartamento':
        print(f'  Crianças        : {"Sim" if crianca else "Não"}')
        if not crianca:
            print(f'  Desconto (5%)   : aplicado')
    print(f'  Aluguel mensal  : R$ {aluguel_mensal:,.2f}')
    print(f'  Contrato total  : R$ {contrato_total:,.2f} em {parcelas}x de R$ {parcela_contrato:,.2f}')
    print(f'  Total 1º mês    : R$ {total_mensal:,.2f}')
    print('-' * 55)

    if input_resposta('Deseja gerar o contrato em CSV? (S/N):', ['S','N']) == 'S':
        try:
            arquivo = gerar_csv(nome_cliente, imovel, aluguel_mensal, parcela_contrato, parcelas)
            print(f'Contrato gerado: {arquivo}')
        except Exception as e:
            print(f'Erro ao gerar o contrato em CSV: {e}')
    if input_resposta('Deseja realizar um novo orçamento? (S/N):', ['S','N']) == 'N':
        print('\n  Obrigado por usar a Imobiliária R.M! Até logo. 👋\n')
        break
