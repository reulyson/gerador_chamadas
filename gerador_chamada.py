import pandas as pd

df = pd.read_csv('/content/eventos.csv', sep=';')

#Função para converter a coluna DURACAO em segundos
def minutos_para_segundos(tempo):
    partes = tempo.split(':')
    minutos = int(partes[0])
    segundos = int(partes[1])
    return minutos * 60 + segundos

# Exclui as colunas especificadas e reorganiza as colunas restantes
colunas_excluir = ['PROGRAMA', 'SEG', 'ORIGEM', 'INICIO', 'ID', 'CLIENTE', 'Status', 'DAI', 'DAIH', 'AA']
df = df.drop(columns=colunas_excluir)
df = df.reindex(columns=['EVENTO', 'DURACAO', 'MOD'])

# Remove duplicatas na coluna 'EVENTO'
df = df.drop_duplicates(subset=['EVENTO'])

# Apaga as linhas que contêm as informações listadas
df = df[~df['EVENTO'].str.contains('VEM AI|AO VIVO|C/ASS|INTEG|J.|CH EXTRA', na=False, regex=True)]
# Mantém apenas as linhas em que contêm as informações listadas
df = df[df['EVENTO'].str.contains('\(A\)|\(H\)|\(N\)|\(MNT\)', na=False, regex=True)]

# Mantém as linhas em que a coluna 'MOD' contém apenas o valor 'CH'
df = df[df['MOD'] == 'CH']

# Ordena o DataFrame com base na coluna 'DURACAO' do menor para o maior
df = df.sort_values(by='DURACAO')
# Converte os valores na coluna 'DURACAO' de minutos para segundos
df['DURACAO'] = df['DURACAO'].apply(minutos_para_segundos)

# Salva o DataFrame em um arquivo txt
df.to_csv('/content/CH.txt', sep='\t', index=False)

# Lê o arquivo de texto
with open('/content/CH.txt', 'r') as file:
    # Lê todas as linhas do arquivo
    linhas = file.readlines()

# Abre o arquivo novamente, desta vez em modo de escrita, para adicionar 'OKAY' no início de cada linha
with open('/content/CH.txt', 'w') as file:
    # Adiciona 'OKAY' no início de cada linha e escreve de volta no arquivo
    for linha in linhas:
        file.write('OKAY\t' + linha)
df