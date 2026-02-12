from services.cotacao_service import CotacaoService

def testar():
    print("🚀 Iniciando Teste do Backend...")
    service = CotacaoService()

    marcas = service.listar_marcas()
    print(f"✅ Marcas encontradas: {marcas}")
    
    if not marcas:
        print("❌ Erro: Nenhuma marca encontrada. O seed.py rodou?")
        return

    marca_teste = marcas[0] 
    
    modelos = service.listar_modelos(marca_teste)
    print(f"✅ Modelos da {marca_teste}: {modelos}")
    
    modelo_teste = modelos[0] 
    print(f"🔎 Buscando ofertas para: {marca_teste} {modelo_teste}...")
    df = service.buscar_ofertas(marca_teste, modelo_teste)
    
    if not df.empty:
        print("\n📊 Resultados encontrados:")
        print(df[["Loja", "Preço", "Ano"]].head())
        
        kpis = service.calcular_kpis(df)
        print(f"\n💰 Preço Médio: R$ {kpis['media']:.2f}")
        print(f"📉 Menor Preço: R$ {kpis['min']:.2f} ({kpis['loja_mais_barata']})")
        
        service.registrar_log({"teste": "backend_dia_03"})
        print("\n📝 Log de auditoria gravado.")
        
    else:
        print("⚠️ Nenhuma oferta encontrada. Verifique se o seed gerou dados para esse modelo.")

if __name__ == "__main__":
    testar()