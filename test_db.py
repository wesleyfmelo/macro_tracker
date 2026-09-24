# test_db.py (arquivo temporário de teste na raiz)
import pandas as pd
from src.pipeline import DataBaseManager

# 1. Instancia o gerenciador (deve criar a pasta data/ e o arquivo .db se não existirem)
db = DataBaseManager()

# 2. Cria dados simulados de teste
dados_teste = pd.DataFrame({
    'data': ['2026-01-01', '2026-02-01', '2026-01-01'],
    'indicador': ['IPCA', 'IPCA', 'SELIC'],
    'valor': [0.42, 0.35, 11.25]
})

# 3. Testa o Upsert
print("Inserindo dados de teste...")
db.upsert_indicadores(dados_teste)

# 4. Lê os dados salvos
df_resultado = db.load_data()
print("\n--- Dados gravados no banco ---")
print(df_resultado)

# 5. Testa a leitura da última data
ultima_data = db.get_last_date('IPCA')
print(f"\nÚltima data gravada do IPCA: {ultima_data}")

# 6 inclui nova info de IPCA

dados_teste_2 = pd.DataFrame({
    'data': ['2026-01-01','2026-03-01'],
    'indicador': ['IPCA','IPCA'],
    'valor': [1.45,0.99]})

# 7 inserindo os dados "novos"
 
db.upsert_indicadores(dados_teste_2)

# 8 Lendo dados novos
df_resultado = db.load_data()
print("\n--- Dados gravados no banco ---")
print(df_resultado) 


# 8. Testa a leitura da última data apos novo dado
ultima_data = db.get_last_date('IPCA')
print(f"\nÚltima data gravada do IPCA: {ultima_data}")