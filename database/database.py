import sqlalchemy
import psycopg2


DB_USER = "postgres"
DB_PASS = "vini1234"       
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "minerva_motors"

def get_engine():
    """Retorna a engine do SQLAlchemy para uso com Pandas"""
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = sqlalchemy.create_engine(url)
    return engine

def get_connection():
    """Retorna uma conexão crua (raw) para inserts simples se necessário"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

