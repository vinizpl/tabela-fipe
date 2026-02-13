import pandas as pd
import json
from sqlalchemy import text
from database.database import get_engine

class CotacaoService:
    def __init__(self):
        self.engine = get_engine()

    def listar_marcas(self):
        """Retorna todas as marcas disponíveis para o filtro."""
        try:
            query = "SELECT nome FROM marcas ORDER BY nome ASC"
            df = pd.read_sql(query, self.engine)
            return df['nome'].tolist()
        except Exception as e:
            print(f"Erro ao listar marcas: {e}")
            return []

    def listar_modelos(self, marca_selecionada):
        """Retorna os modelos baseados na marca escolhida."""
        try:
            query = text("""
                SELECT m.nome 
                FROM modelos m
                JOIN marcas ma ON m.marca_id = ma.id
                WHERE ma.nome = :marca
                ORDER BY m.nome ASC
            """)
            df = pd.read_sql(query, self.engine, params={"marca": marca_selecionada})
            return df['nome'].tolist()
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
            return []

    def buscar_ofertas(self, marca, modelo, ano=None):
        """
        A Query Principal! Busca as cotações aplicando os filtros.
        Retorna um DataFrame Pandas formatado.
        """
        sql = text("""
            SELECT 
                l.nome_fantasia AS "Loja",
                r.nome AS "Região",
                m.nome AS "Modelo",
                cv.ano_modelo AS "Ano",
                cv.preco_coletado AS "Preço",
                cv.data_coleta AS "Data Coleta",
                cv.opcionais
            FROM coletas_veiculos cv
            JOIN modelos m ON cv.modelo_id = m.id
            JOIN marcas ma ON m.marca_id = ma.id
            JOIN alocacoes_pesquisa ap ON cv.alocacao_id = ap.id
            JOIN lojas l ON ap.loja_id = l.id
            JOIN regioes r ON l.regiao_id = r.id
            WHERE 
                ma.nome = :marca
                AND m.nome = :modelo
                AND (:ano IS NULL OR cv.ano_modelo = :ano)
            ORDER BY cv.preco_coletado ASC
        """)
        
        try:
            params = {"marca": marca, "modelo": modelo, "ano": ano}
            df = pd.read_sql(sql, self.engine, params=params)
            
            if df.empty:
                return pd.DataFrame()

            return df
        except Exception as e:
            print(f"Erro na busca: {e}")
            return pd.DataFrame()

    def calcular_kpis(self, df):
        """Calcula as métricas de negócio (Cards) a partir dos dados."""
        if df.empty:
            return None
            
        return {
            "media": df["Preço"].mean(),
            "min": df["Preço"].min(),
            "max": df["Preço"].max(),
            "loja_mais_barata": df.loc[df["Preço"].idxmin()]["Loja"],
            "loja_mais_cara": df.loc[df["Preço"].idxmax()]["Loja"],
            "total_ofertas": len(df),
            "regiao_predominante": df["Região"].mode()[0] if not df["Região"].empty else "N/A"
        }

    def obter_historico_precos(self, modelo):
        """
        Gera dados para o gráfico de evolução.
        Agrupa as coletas por mês para mostrar tendência.
        """
        sql = text("""
            SELECT 
                DATE_TRUNC('month', cv.data_coleta) AS "Mês",
                AVG(cv.preco_coletado) AS "Preço Médio",
                MIN(cv.preco_coletado) AS "Preço Mínimo",
                MAX(cv.preco_coletado) AS "Preço Máximo"
            FROM coletas_veiculos cv
            JOIN modelos m ON cv.modelo_id = m.id
            WHERE m.nome = :modelo
            GROUP BY 1
            ORDER BY 1
        """)
        try:
            df = pd.read_sql(sql, self.engine, params={"modelo": modelo})
            return df
        except Exception as e:
            print(f"Erro no histórico: {e}")
            return pd.DataFrame()

    def registrar_log(self, filtros, ip_origem="127.0.0.1"):
        """
        Requisito de Auditoria: Salva o que o usuário pesquisou.
        """
        sql = text("""
            INSERT INTO logs_consultas_usuario (filtros_aplicados, ip_origem)
            VALUES (:filtros, :ip)
        """)
        try:
            filtros_json = json.dumps(filtros, ensure_ascii=False)
            
            with self.engine.connect() as conn:
                conn.execute(sql, {"filtros": filtros_json, "ip": ip_origem})
                conn.commit()
        except Exception as e:
            print(f"Erro ao gravar log: {e}")