import logging
from typing import Dict,Optional
import pandas as pd
import requests
from .base import BaseFetcher

logger=logging.getLogger(__name__)

class BCBFetcher(BaseFetcher):
    """
    Coletor para a API do sistema gerenciador de séries temporais (SGS) do banco central do Brasil.
    Documentação da API: https://dadosabertos.bcb.gov.br/
    """
    
    # Mapeamento de códigos das séries no SGS do BCB
    SERIES_MAP={
        "SELIC":432,
        "IPCA":433,
        "CDI":12,
        "CAMBIO_USD":10813
        }
        
    def __init__(self):
        # inicializa a classe pai (BaseFetcher) passando o nome do identificador
        super().__init__(name="BCB_SGS")
    
    def _buld_url(self,code:int,start_date: Optional[str]=None)->str :
        """
        Método privado para construir a URL da API rest do BCB
        Formatos aceitos de data pela API : DD/MM/YYYY
        """
        url=f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json"
        
        if start_date:
            # converter o formato da data
            dt_formatted=pd.to_datetime(start_date).strftime("%d/%m/%Y")
            url+=f"&dataInicial={dt_formatted}"
        return url
    
    def fetch_data(self, start_date: Optional[str] = None) -> pd.DataFrame:
        """
        Implementação OBRIGATÓRIA do método abstrato.
        Busca todas as séries mapeadas e retorna um DataFrame padronizado.
        """
        combined_dfs=[]
        
        for indicator_name,code in self.SERIES_MAP.items():
            url=self._buld_url(code,start_date)
            
            try:
                # requisição HTTP com timeout para segurança
                response=requests.get(url,timeout=10)
                response.raise_for_status()
                
                data=response.json()
                if not data:
                    continue
                
                #Cria o DataFrame com os dados brutos da API
                df=pd.DataFrame(data)
                
                # Trata as colunas e tipos
                df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
                df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
                df["indicador"] = indicator_name
                
                # Seleciona as colunas na ordem padrão
                df = df[["data", "indicador", "valor"]]
                combined_dfs.append(df)
            
            except requests.RequestException as e:
                logger.error(f"[{self.name}] Erro ao buscar série {indicator_name} ({code}): {e}")
                continue
        
        # Se nenhuma série retornou dados, devolve um DataFrame vazio padronizado
        if not combined_dfs:
            return pd.DataFrame(columns=["data", "indicador", "valor"])
        
        # Junta todas as séries em um único DataFrame
        final_df = pd.concat(combined_dfs, ignore_index=True)
        
        # Valida se o DataFrame atende aos requisitos definidos na BaseFetcher
        self._validate_dataframe(final_df)
        
        return final_df