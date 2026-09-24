import sqlite3
import pandas as pd
from typing import List,Optional

class DataBaseManager:
    """
    Gerenciador do banco de dados SQLite para o Macro Tracker.
    Encapsula todas as operações de leitura, escrita e criação de tabelas.
    """
    def __init__(self, db_path: str="data/macro_database.db"):
        """
        Inicializa o gerenciador e garante que as tabelas necessárias existam.
        :param db_path: Caminho relativo ou absoluto do arquivo .db
        """
        self.db_path=db_path
        self._create_tables()
    
    def _get_connection(self)->sqlite3.Connection:
        """ Método privado para abrir a conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self)->None:
        """
        Cria a tabela de indicadores caso não exista.
        A chave primária é a combinação de (data, indicador) para evitar duplicatas.
        """ 
        query=""" 
            CREATE TABLE IF NOT EXISTS indicadores(
                data TEXT NOT NULL,
                indicador TEXT NOT NULL,
                valor Real,
                PRIMARY KEY(data, indicador)
                );"""
        with self._get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute(query)
            conn.commit()
            
    def upsert_indicadores(self,df: pd.DataFrame)->None:
        """
        Insere novos registros ou atualiza valores de registros existentes (Upsert).
        Espera um DataFrame com as colunas: ['data','indicador','valor']
        """
        if df.empty:
            print("DataFrame vazio. Nenhuma inserção realizada.")
            return
        # garante que temos as colunas necessárias
        required_cols={"data","indicador","valor"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"O DataFrame  precisa conter as colunas {required_cols}")
            
        # Prepara uma copia padronizando a data para texto formato ISO (YYYY-MM-DD)
        df_to_insert=df.copy()
        df_to_insert['data']=pd.to_datetime(df_to_insert["data"]).dt.strftime("%Y-%m-%d")
        
        # Query com clausula ON CONFLICT para fazer o Upsert
        query="""
        INSERT INTO indicadores(data,indicador,valor)
        VALUES (?,?,?)
        ON CONFLICT (data,indicador) DO UPDATE SET
        valor=excluded.valor;
        """
        records=df_to_insert[["data","indicador","valor"]].to_records(index=False).tolist()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, records)
            conn.commit()
            print(f"{len(records)} registro(s) inserido(s)/atualizado(s) com sucesso!")
                
                
    def load_data(self,indicadores: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Lê os dados do SQLite e retorna um DataFrame formatado.
        
        :param indicadores: Lista opcional de nomes de indicadores para filtrar. Ex: ['IPCA', 'SELIC']
        """
        query="SELECT data,indicador,valor FROM indicadores "
        params=[]
        
        if indicadores:
            placeholders=",".join(["?"]*len(indicadores))
            query+=f"WHERE indicador IN ({placeholders})"
            params=indicadores
            
        query+="ORDER BY data ASC"
        
        with self._get_connection() as conn:
            df=pd.read_sql_query(query,conn,params=params)
            
        if not df.empty:
            df["data"]=pd.to_datetime(df["data"])
        
        return df
        
        
    def get_last_date(self,indicador: str)->Optional[str]:
        """
        Retorna a ultima data para um indicador específico (util para atualizações incrementais)
        """
        # Se o indicador veio como uma tupla por engano, extrai o primeiro valor
        if isinstance(indicador,tuple):
            indicador=indicador[0]
            
        query="SELECT MAX(data) FROM indicadores WHERE indicador=?"
        with self._get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute(query,(indicador,))
            result=cursor.fetchone()
            return result[0] if result and result[0] else None
            
    
        
        
        