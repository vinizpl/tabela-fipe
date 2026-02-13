import pytest
import pandas as pd
from services.cotacao_service import CotacaoService
from unittest.mock import MagicMock

def test_calculo_kpis_deve_retornar_media_correta():
    # 1. Setup: Criar um DataFrame Pandas (formato que o Service espera)
    dados_mock = pd.DataFrame({
        "Preço": [100.00, 200.00, 300.00],
        "Loja": ["Loja A", "Loja B", "Loja C"],     # Necessário para logica de 'loja_mais_barata'
        "Região": ["Norte", "Norte", "Sul"]         # Necessário para 'regiao_predominante'
    })
    
    # Mock do Service para não tentar conectar no Banco de Dados real
    service = CotacaoService()
    service.engine = MagicMock() # Ignora a conexão SQL
    
    # 2. Execução
    resultado = service.calcular_kpis(dados_mock)
    
    # 3. Asserção (Validação)
    assert resultado['media'] == 200.00
    assert resultado['min'] == 100.00
    assert resultado['max'] == 300.00
    assert resultado['total_ofertas'] == 3  # Nome correto da chave na implementação
    assert resultado['loja_mais_barata'] == "Loja A"