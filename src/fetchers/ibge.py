import logging
from typing import Optional
import pandas as pd
import requests

from .base import BaseFetcher

logger=logging.getLogger(__name__)

class IBGEFetcher(BaseFetcher):
    """
    Coletor para a API  do SIDRA/IBGE
    Documentação da API: https://apisidra.ibge.gov.br/
    """
    # Mapeamento dos indicadores do IBGE
    # Chave: Nome no nosso BD | Valor: Dicionário com tabela, variável e período
    SERIES_MAP = {
        "IPCA_MENSAL_IBGE": {
            "table": 6691,      # Tabela IPCA - Série histórica numero indice 
            "variable": 2266,     # Variável: IPCA - Variação mensal (%)
        }, # a adicionar outras séries
        }
    
    def __init__(self):
        super().__init__(name="IBGE_SIDRA")
    
    def _build_url(self,table:int,variable:int,start_date: Optional[str]=None)->str:
        """
        Constrói a URL da API do SIDRA. 
        Formato de período no SIDRA: AAAAMM (ex: 202401)
        Documentação : https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-bq
        """
        period="-12" 
        if start_date:
            dt=pd.to_datetime(start_date)
            period = f"{dt.strftime('%Y%m')}-"        
        url=f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}/periodos/{period}/variaveis/{variable}?localidades=N1[all]"
        return url
        
    def fetch_data(self, start_date: Optional[str] = None) -> pd.DataFrame:
        """
        Busca os indicadores mapeados do IBGE e retorna um DataFrame padronizado.
        """
        combined_dfs = []

        for indicator_name, config in self.SERIES_MAP.items():
            url = self._build_url(config["table"], config["variable"], start_date)

            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()

                data = response.json()
                
                if not data or not isinstance(data, list):
                    continue

                # Navega na estrutura JSON aninhada da API v3 de Agregados
                # Estrutura: data[0]['resultados'][0]['series'][0]['serie'] -> {'202401': '102.5', ...}
                resultados = data[0].get("resultados", [])
                if not resultados:
                    continue

                series = resultados[0].get("series", [])
                if not series:
                    continue

                # Dicionário com chave="AAAAMM" e valor="123.45"
                serie_dict = series[0].get("serie", {})
                if not serie_dict:
                    continue

                # Converte o dicionário {'AAAAMM': 'valor'} em DataFrame
                df = pd.DataFrame(list(serie_dict.items()), columns=["periodo_id", "valor"])

                # 1. Filtra apenas códigos de período válidos (AAAAMM de 6 dígitos)
                df = df[df["periodo_id"].str.isdigit() & (df["periodo_id"].str.len() == 6)]

                # 2. Converte valores para numérico (trata vírgula se houver e ignora "...", "-", etc.)
                df["valor_clean"] = df["valor"].astype(str).str.replace(",", ".", regex=False)
                df["valor"] = pd.to_numeric(df["valor_clean"], errors="coerce")
                
                # Remove registros nulos ou não numéricos
                df = df.dropna(subset=["valor"])

                # 3. Formata a data: AAAAMM -> YYYY-MM-01
                df["data"] = pd.to_datetime(df["periodo_id"], format="%Y%m").dt.strftime("%Y-%m-%d")
                df["indicador"] = indicator_name

                # Mantém o contrato padrão do nosso banco de dados
                df = df[["data", "indicador", "valor"]]
                combined_dfs.append(df)

            except (requests.RequestException, KeyError, IndexError, ValueError) as e:
                logger.error(f"[{self.name}] Erro ao buscar {indicator_name}: {e}")
                continue

        if not combined_dfs:
            return pd.DataFrame(columns=["data", "indicador", "valor"])

        final_df = pd.concat(combined_dfs, ignore_index=True)
        self._validate_dataframe(final_df)

        return final_df
        