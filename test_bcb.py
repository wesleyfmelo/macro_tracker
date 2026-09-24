from src.fetchers.bcb import BCBFetcher
from src.pipeline.db import DataBaseManager

def testar_fetcher_bcb():
    print("--- Testando Coletor do Banco Central ---")
    bcb = BCBFetcher()
    
    # 1. Teste de Busca Completa (todas as séries)
    print("\n1. Buscando dados dos últimos 30 dias...")
    # Podemos usar start_date para não puxar todo o histórico no teste
    df = bcb.fetch_data(start_date="2026-08-01")
    
    print("\nPrimeiras linhas retornadas:")
    print(df.head())
    print(f"\nTotal de registros coletados: {len(df)}")

    # 2. Teste de Integração com o DatabaseManager (Upsert)
    print("\n2. Gravando dados no SQLite via DatabaseManager...")
    db = DataBaseManager()
    db.upsert_indicadores(df)
    
    # 3. Carregando os dados para confirmar o salvamento
    df_banco = db.load_data()
    print("\nDados salvos no Banco de Dados SQLite:")
    print(df_banco.tail(10))

if __name__ == "__main__":
    testar_fetcher_bcb()