# seed.py
import random
from faker import Faker
from database import get_engine
from sqlalchemy import text

fake = Faker('pt_BR')
engine = get_engine()

def seed_database():
    print("🌱 Iniciando o semeio do banco de dados...")
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE coletas_veiculos, alocacoes_pesquisa, lojas, regioes, modelos, marcas, usuarios RESTART IDENTITY CASCADE;"))
        
        print("👤 Criando Usuários...")
        conn.execute(text("""
            INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES 
            ('Admin Minerva', 'admin@minerva.com', 'hash123', 'ADMIN'),
            ('João Pesquisador', 'joao@minerva.com', 'hash123', 'PESQUISADOR');
        """))

        print("🚗 Criando Veículos...")
        marcas = {
            'Fiat': ['Palio 1.0', 'Mobi Like', 'Toro Freedom', 'Cronos'],
            'Volkswagen': ['Gol MPI', 'Polo Track', 'Nivus Highline', 'T-Cross'],
            'Toyota': ['Corolla XEi', 'Yaris XS', 'Hilux SRV'],
            'Honda': ['Civic Touring', 'HR-V EXL', 'City Hatch']
        }
        
        for marca, modelos in marcas.items():
            result = conn.execute(text("INSERT INTO marcas (nome) VALUES (:nome) RETURNING id"), {"nome": marca})
            marca_id = result.scalar()
            
            for modelo in modelos:
                conn.execute(text("""
                    INSERT INTO modelos (marca_id, nome, categoria, ano_inicio_fabricacao) 
                    VALUES (:mid, :nome, 'Passeio', 2020)
                """), {"mid": marca_id, "nome": modelo})

        print("🏢 Criando Lojas...")
        regioes = ['Fortaleza - Centro', 'Fortaleza - Sul', 'Russas', 'Sobral', 'Juazeiro']
        
        for reg in regioes:
            res_reg = conn.execute(text("INSERT INTO regioes (nome, coordenador_id) VALUES (:nome, 1) RETURNING id"), {"nome": reg})
            reg_id = res_reg.scalar()
            
            for _ in range(3):
                conn.execute(text("""
                    INSERT INTO lojas (nome_fantasia, endereco, regiao_id, status) 
                    VALUES (:nome, :end, :rid, 'APROVADO')
                """), {
                    "nome": f"{fake.company()} Veículos",
                    "end": fake.address(),
                    "rid": reg_id
                })

        print("💰 Gerando 500 cotações de preço...")
        
        lojas_ids = [row[0] for row in conn.execute(text("SELECT id FROM lojas")).fetchall()]
        modelos_ids = [row[0] for row in conn.execute(text("SELECT id FROM modelos")).fetchall()]
        pesquisador_id = 2
        
        for _ in range(500):
            
            res_aloc = conn.execute(text("""
                INSERT INTO alocacoes_pesquisa (coordenador_id, pesquisador_id, loja_id, data_inicio_semana, status)
                VALUES (1, :pid, :lid, '2026-02-01', 'CONCLUIDA') RETURNING id
            """), {"pid": pesquisador_id, "lid": random.choice(lojas_ids)})
            aloc_id = res_aloc.scalar()
            
            preco_base = random.randint(40000, 120000)
            
            conn.execute(text("""
                INSERT INTO coletas_veiculos (alocacao_id, modelo_id, preco_coletado, ano_modelo, ano_fabricacao, opcionais, data_coleta)
                VALUES (:aid, :mid, :preco, :ano, :ano, '{"ar": true, "trava": true}', NOW() - (random() * interval '60 days'))
            """), {
                "aid": aloc_id,
                "mid": random.choice(modelos_ids),
                "preco": preco_base,
                "ano": random.choice([2024, 2025, 2026])
            })
        
        conn.commit()
        print("✅ Banco de dados populado com sucesso!")

if __name__ == "__main__":
    seed_database()