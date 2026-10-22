import requests
import json
import time

def baixar_e_atualizar_banco():
    print("Fetch PokéAPI (starting...)")
    
    url_base = "https://pokeapi.co/api/v2/pokemon-species?limit=1500"
    resposta = requests.get(url_base)
    if resposta.status_code != 200:
        print("Erro ao acessar a API.")
        return
        
    especies = resposta.json()['results']
    banco_local = {}
    
    total = len(especies)
    print(f"Encontradas {total} espécies. Processando (isso pode levar alguns minutos)...")
    
    for i, especie in enumerate(especies):
        nome = especie['name']
        url_detalhe = especie['url']    
        detalhe_resp = requests.get(url_detalhe).json()
        grupos = [grupo['name'].upper() for grupo in detalhe_resp['egg_groups']]
        gender_rate = detalhe_resp['gender_rate'] # retorna de -1 a 8, chance de ser fêmea
        
        # Salva no dicionário local
        banco_local[nome] = {
            "egg_groups": grupos,
            "gender_rate": gender_rate
        }
        
        # Feedback visual no console
        if (i + 1) % 50 == 0:
            print(f"Progresso: {i + 1}/{total} Pokémons processados...")
            
    # 3. Salva o dicionário final em um arquivo JSON
    with open("pokemon_data.json", "w", encoding="utf-8") as arquivo:
        json.dump(banco_local, arquivo, indent=4)
        
    print("Sucesso! pokemon_data.json foi atualizado/criado na sua pasta.")

if __name__ == "__main__":
    baixar_e_atualizar_banco()