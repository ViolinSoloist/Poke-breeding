import requests
import json
import time

def baixar_e_atualizar_banco(max_tries:int, timeout_limit_seconds:int, exception_waiting_time_seconds:int):
    print("Iniciando o download de dados da PokéAPI...")
    
    session = requests.Session()
    
    url_base = "https://pokeapi.co/api/v2/pokemon-species?limit=1500"
    try:
        resposta = session.get(url_base)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro crítico ao acessar a API: {e}")
        return
        
    especies = resposta.json()['results']
    banco_local = {}
    total = len(especies)
    
    print(f"Encontradas {total} espécies. Processando (isso pode levar alguns minutos)...")
    
    # main loop (para cada pokémon)
    for i, especie in enumerate(especies):
        nome = especie['name']
        url_detalhe = especie['url']
        
        sucesso = False
        tentativas = 0
        
        while not sucesso and tentativas < max_tries:
            try:
                # O timeout caso internet seja ruim
                detalhe_resp = session.get(url_detalhe, timeout=timeout_limit_seconds).json()
                
                grupos = [grupo['name'].upper() for grupo in detalhe_resp['egg_groups']]
                evolves_from = detalhe_resp['evolves_from_species']
                
                banco_local[nome] = {
                    "egg_groups": grupos,
                    "gender_rate": detalhe_resp['gender_rate'],
                    "is_baby": detalhe_resp['is_baby'],
                    # "is_legendary": detalhe_resp['is_legendary'],
                    # "is_mythical": detalhe_resp['is_mythical'],
                    "evolui_de": evolves_from['name'] if evolves_from else None
                }
                sucesso = True
                
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                tentativas += 1
                print(f"\nQueda de conexão no {nome} (Tentativa {tentativas}/{max_tries}). Aguardando {exception_waiting_time_seconds}s...")
                time.sleep(exception_waiting_time_seconds) 
        
        if not sucesso:
            print(f"\nFalha definitiva ao baixar {nome}. Pulando para o próximo...")
            
        # Progresso
        if (i + 1) % 50 == 0:
            print(f"Progresso: {i + 1}/{total} Pokémons processados...")
            
        time.sleep(0.05)

    print("\n! Download concluído. Iterando novamente pela base para determinar espécie de forma base...")
    
    # primeira re-iteração (calcular a forma base de todas as espécies)
    for nome, dados in banco_local.items():
        especie_atual = nome

        # recursão enquanto Pokémon tiver "evolui_de"
        while banco_local.get(especie_atual, {}).get("evolui_de") is not None:
            especie_atual = banco_local[especie_atual]["evolui_de"]
            
        dados["forma_base"] = especie_atual

    # segunda re-iteração (apagar chaves temporárias)
    for dados in banco_local.values():
        if "evolui_de" in dados:
            del dados["evolui_de"]

    with open("pokemon_data.json", "w", encoding="utf-8") as arquivo:
        json.dump(banco_local, arquivo, indent=4)
        
    print("pokemon_data.json foi atualizado/criado.")

if __name__ == "__main__":
    baixar_e_atualizar_banco(max_tries=3, timeout_limit_seconds=10, exception_waiting_time_seconds=3)