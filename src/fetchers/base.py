from abc import ABC,abstractmethod
import pandas as pd
from typing import Optional



class BaseFetcher(ABC):
    """
    Classe abstrata para todos os coletores (fetchers) de dados macroeconômicos
    Garante que qualquer novo coletor implemente a interface padrão
    """
    
    def __init__(self,name:str):
        """
        :param name: Nome identificador do coletor (ex: 'BCB_SGS','IBGE_SIDRA')
        """
        self.name=name
    
    @abstractmethod
    def fetch_data(self,start_date: Optional[str]=None)->pd.DataFrame:
        """
        Método abstrato obrigatório para buscar dados.
        
        Cada Classe filha DEVE implementar sua própria lógica de coleta.
        Deve retornar um padas DataFrame padronizado com as colunas:
        ['data','indicador','valor']
        
        :param start_date: Data inicial opcional no formato 'YYYY-MM-DD' para buscas incrementais
        """
        pass
    def _validate_dataframe(self,df:pd.DataFrame)-> bool:
        """
        Método auxiliar para validar se o DataFrame coletado possui formato exigido pelo banco.
        """
        if df.empty:
            return True
        
        required_cols={'data','indicador','valor'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"[{self.name}] O DataFrame retornado não possui as colunas obrigatórias: {required_cols}")
            
        return True