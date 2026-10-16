from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum, auto
import random

# NamedTuple => "Struct" imutável
class IVs(NamedTuple):
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int

class EggGroup(Enum):
    AMORPHOUS = auto()
    BUG = auto()
    DRAGON = auto()
    FAIRY = auto()
    FIELD = auto()
    FLYING = auto()
    GRASS = auto()
    HUMAN_LIKE = auto()
    MINERAL = auto()
    MONSTER = auto()
    WATER_1 = auto()
    WATER_2 = auto()
    WATER_3 = auto()

class BreedingItem(Enum):
    NONE = auto()           # Quando um pkm não está segurando nenhum item
    DESTINY_KNOT = auto()
    EVERSTONE = auto()
    POWER_WEIGHT = auto()
    POWER_BRACER = auto()
    POWER_BELT = auto()
    POWER_LENS = auto()
    POWER_BAND = auto()
    POWER_ANKLET = auto()

# Classe dos Pokémons
@dataclass(slots=True)
class Pokemon:
    especie: str
    ivs: IVs
    item: BreedingItem = None # NONE POR ENQUANTO SÓ
    egg_groups: tuple[EggGroup, ...] = None # Um pkm pode ter até dois grupos
    # A IMPLEMENTAR: nature, ability, etc.

# IMPLEMENTAR: LÓGICA PARA DESTINY KNOT, CASO UM (OU AMBOS??) DOS POKEMONS SEJA O DITTO
def gerar_ovo(pai: Pokemon, mae: Pokemon) -> Pokemon:
    """Função que gera IVs aleatórios para o Pokémon filho (sem itens, herda 3 IVs e randomiza 3)"""
    
    atributos = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
    
    # Escolhe três dentre os atributos acima para serem herdados dos pais (sem o Destiny Knot)
    atributos_herdados = random.sample(atributos, 3)
    
    # Formação dos IVs do pkm filho
    novos_ivs = {}
    for atributo in atributos:
        # Se é um atributo que vai ser herdado, tem 50% de ser do pai e 50% de ser da mãe
        # Se não, é gerado aleatoriamente de 0 a 31
        if atributo in atributos_herdados:
            valor_herdado = getattr(pai.ivs, atributo) if random.choice([True, False]) else getattr(mae.ivs, atributo)
            novos_ivs[atributo] = valor_herdado
        else:
            novos_ivs[atributo] = random.randint(0, 31)
            
    ivs_filhote = IVs(**novos_ivs)
    # pkm filho sempre será da espécie mãe, a não ser se for male + ditto (implementar exceção!!!)
    return Pokemon(especie=mae.especie, ivs=ivs_filhote)

# --- Testando a Estrutura ---
if __name__ == "__main__":
    pai_ivs = IVs(hp=31, attack=31, defense=31, sp_atk=31, sp_def=31, speed=31)
    pai = Pokemon(especie="Ditto", ivs=pai_ivs)

    mae_ivs = IVs(hp=0, attack=0, defense=0, sp_atk=0, sp_def=0, speed=0)
    mae = Pokemon(especie="Pikachu", ivs=mae_ivs)

    filhote = gerar_ovo(pai, mae)
    
    print(f"Pai: {pai.ivs}")
    print(f"Mãe: {mae.ivs}")
    print(f"Filhote: {filhote.ivs}")