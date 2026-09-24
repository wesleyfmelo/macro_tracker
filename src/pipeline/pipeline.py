import logging
from typing  import List,Type
import pandas as pd

from src.pipeline.db import DataBaseManager
from src.fetchers.base import BaseFetcher
from src.fetchers.bcb import BCBFetcher
from src.fetchers.ibge import IBGEFetcher

# configuração de logs
logger=logging.getLogger(__name__)

class MacroPipeline:
    """
    Orquestrador do Pipeline de Dados Macroeconômicos.
    Gerencia a execução dos fetchers e a gravação incremental no banco de dados
    """
    def __init__(self,db_manager: DataBaseManager=None):
        """
        :param db_manager: Instância do DataBaseManager. Se None, cria uma nova.
        """
        self.db=db_manager if db_manager else DataBaseManager()
        # adicionaremos futuramente os demais fetchers
        self.fetcher_classes: List[type[BaseFetcher]]=[BCBFetcher,
                                                       IBGEFetcher,
                                                       ]
    
    def _get_start_date_for_fetcher(self, fetcher: BaseFetcher)->str:
        """
        Descrobre a menor data registrada no banco entre os indicadores do fetcher
        para definir a partir de onde fazer a busca incremental.
        """
        #se o Fecther tiver o mapeamento de séries,pega a menor data entre elas
        if hasattr(fetcher,"SERIES_MAP"):
            dates=[]
            for indicador_name in fetcher.SERIES_MAP.keys():
                last_dt=self.db.get_last_date(str(indicador_name))
                if last_dt:
                    dates.append(last_dt)
            
            if dates:
                min_date=min(dates)
                logger.info(f"[{fetcher.name}] Data inicial incremental detectada: {min_date}")
                return min_date
        logger.info(f"[{fetcher.name}] Nenhuma data prévia encontrada. Buscando histórico completo.")
        return None
        
    
    def run(self):
        """
        Executa o pipeline completo:
        1. Instancia cada Fetcher
        2. Verifica a última data no banco (busca incremental)
        3. Puxa novos dados
        4. Executa o Upsert no SQLite
        """
        logger.info("Iniciando execução do Pipeline Macroeconômico...")
        print("\n==========================================")
        print("   INICIANDO EXECUÇÃO DO PIPELINE MACRO   ")
        print("==========================================\n")
        
        total_registros_inseridos=0
        
        for fetcher_class in self.fetcher_classes:
            fetcher=fetcher_class()
            print(f"🔄 Processando coletor: {fetcher.name}...")
            
            try:
                # 1. Determina a data inicial para a carga incremental
                start_date = self._get_start_date_for_fetcher(fetcher)
                # 2. Busca os dados atualizados
                df_new = fetcher.fetch_data(start_date=start_date)
                
                if df_new.empty:
                    print(f"ℹ️  [{fetcher.name}] Nenhum dado novo encontrado.")
                    continue
                # 3. Salva os dados no banco usando Upsert
                self.db.upsert_indicadores(df_new)
                total_registros_inseridos += len(df_new)
                print(f"✅ [{fetcher.name}] Sucesso: {len(df_new)} registros processados.")
            
            except Exception as e:
                logger.error(f"❌ Erro ao executar o fetcher {fetcher.name}: {e}")
                print(f"❌ Erro ao processar {fetcher.name}: {e}")

        print("\n==========================================")
        print(f"   PIPELINE CONCLUÍDO! Total de linhas: {total_registros_inseridos}")
        print("==========================================\n")
        

if __name__ == "__main__":
    # Teste direto do pipeline
    logging.basicConfig(level=logging.INFO)
    pipeline = MacroPipeline()
    pipeline.run()