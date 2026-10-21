from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum, auto
import random

# Bibliografia: https://pokemondb.net/mechanics/breeding

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

class Gender(Enum):
    """Valores do ENUM escolhidos para facilitar a verificação de gêneros válidos/opostos entre dois Pokémons.
    * soma = 1 => gêneros opostos (macho e fêmea).
    * soma = 0 ou 2 => gêneros iguais (duas fêmeas ou dois machos).
    * soma >= 3 => pelo menos um Pokémon sem gênero."""

    GENDERLESS = 3
    MALE = 1
    FEMALE = 0

# Classe dos Pokémons
@dataclass(slots=True)
class Pokemon:
    """Todos os atributos de um Pokémon que são relevantes para a mecânica de breeding.
    
    .. Note:: Para a declaração desta classe, é necessário apenas espécie e gênero (se não for Ditto), pois são os atributos que são necessários
        em todas as funcionalidades. Os demais devem ser atribuídos conforme a necessidade.
        
    .. Attention:: Ainda falta implementar atributos de natureza, habilidade e outras coisas que são relevantes no cruzamento."""
    
    especie: str
    genero: Gender = None
    ivs: IVs = None
    item: BreedingItem = None # NONE POR ENQUANTO SÓ
    egg_groups: tuple[EggGroup, ...] = None # Um pkm pode ter até dois grupos

    def __post_init__(self):
        if self.especie == "Ditto":
            self.genero = Gender.GENDERLESS
            self.egg_groups = None
    # A IMPLEMENTAR: nature, ability, etc.

# GRAFO DAS CONEXÕES DE GRUPOS DE OVOS
conexoes_egg_groups = {
    EggGroup.AMORPHOUS: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.GRASS, 
        EggGroup.HUMAN_LIKE, EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.BUG: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.GRASS, 
        EggGroup.HUMAN_LIKE, EggGroup.MINERAL, EggGroup.WATER_1, EggGroup.WATER_3
    },
    EggGroup.DRAGON: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.FIELD, EggGroup.FLYING, 
        EggGroup.GRASS, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1, EggGroup.WATER_2
    },
    EggGroup.FAIRY: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.FIELD, EggGroup.FLYING, 
        EggGroup.GRASS, EggGroup.HUMAN_LIKE, EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.FIELD: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.FLYING, EggGroup.GRASS, 
        EggGroup.HUMAN_LIKE, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1, EggGroup.WATER_2
    },
    EggGroup.FLYING: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.FIELD, 
        EggGroup.HUMAN_LIKE, EggGroup.WATER_1, EggGroup.WATER_3
    },
    EggGroup.GRASS: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.FIELD, EggGroup.HUMAN_LIKE, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1
    },
    EggGroup.HUMAN_LIKE: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.FAIRY, EggGroup.FIELD, 
        EggGroup.FLYING, EggGroup.GRASS, EggGroup.WATER_1
    },
    EggGroup.MINERAL: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.FIELD, EggGroup.GRASS, EggGroup.MONSTER
    },
    EggGroup.MONSTER: {
        EggGroup.DRAGON, EggGroup.FIELD, EggGroup.GRASS, 
        EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.WATER_1: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.FIELD, EggGroup.FLYING, EggGroup.GRASS, EggGroup.HUMAN_LIKE, 
        EggGroup.MONSTER, EggGroup.WATER_2, EggGroup.WATER_3
    },
    EggGroup.WATER_2: {
        EggGroup.DRAGON, EggGroup.FIELD, EggGroup.WATER_1
    },
    EggGroup.WATER_3: {
        EggGroup.BUG, EggGroup.FLYING, EggGroup.WATER_1
    }
}

def compatible(p1: Pokemon, p2: Pokemon) -> bool:
    """Verifica se dois Pokémons podem cruzar com base no gênero, grupos de ovos e no fato de serem ou não Ditto."""

    # 2 Dittos não podem se cruzar
    if p1.especie == "Ditto" and p2.especie == "Ditto":
        return False
        
    # Se não forem 2, 1 DItto pode se cruzar com qualquer genero (até genderless)
    if p1.especie == "Ditto" or p2.especie == "Ditto":
        return True
        
    # Se não tiver nenhum Ditto, devem ser de gêneros opostos e não pode ter nenhum genderless
    if (p1.genero.value + p2.genero.value) != 1:
        return False
        
    # Se as questões de gêneros e Ditto estiverem okay, precisam ser de grupos de ovos compatíveis.
    if p1.egg_groups and p2.egg_groups:
        grupos_em_comum = set(p1.egg_groups) & set(p2.egg_groups)
        if not grupos_em_comum:
            return False
    else:
        # Se as variáveis não estiverem setadas, não cruza
        return False
        
    return True

def __get_especie_filho(p1: Pokemon, p2: Pokemon) -> str:
    """A espécie do filhote é definida pela fêmea, a menos que cruze com Ditto.
    
    .. note:: Função auxiliar. Os Pokémons passados de parâmetro devem ser obrigatoriamente válidos.
        Isso significa que se há um Ditto, será apenas um."""
    
    # Se tiver um Ditto, espécie do fiho será obrigatoriamente igual ao parente não-Ditto.
    if p1.especie == "Ditto":
        return p2.especie
    if p2.especie == "Ditto":
        return p1.especie
        
    # Se não, é igual à mãe.
    return p1.especie if p1.especie == Gender.FEMALE else p2.especie

# IMPLEMENTAR: LÓGICA PARA DESTINY KNOT
# IMPLEMENTAR: transmissão de habilidades e naturezas também
def gerar_ovo(parent1: Pokemon, parent2: Pokemon) -> Pokemon:
    """Gera o ovo de um Pokémon, fruto do cruzamento de outros dois Pokémons compatíveis, calculando os atributos.
    A função também verifica compatibilidade.
    
    .. Attention:: Apenas herança de IVs, por enquanto (Ainda falta implementar lógica para itens e trasmissão de habilidades e naturezas).
    
        Cálculo de probabilidade de gênero ainda deve ser implementado (Há probabilidades específicas para algumas espécies).
        Por enquanto, é só 50%/50%."""

    if not compatible(parent1, parent2):
        raise ValueError(f"Cruzamento inválido: {parent1.especie} e {parent2.especie} não são compatíveis.", "compatibilidade")
    
    atributos = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
    
    # Escolhe três dentre os atributos acima para serem herdados dos pais (sem o Destiny Knot)
    atributos_herdados = random.sample(atributos, 3)
    
    # Formação dos IVs do pkm filho
    novos_ivs = {}
    for atributo in atributos:
        # Se é um atributo que vai ser herdado, tem 50% de ser do pai e 50% de ser da mãe
        # Se não, é gerado aleatoriamente de 0 a 31
        if atributo in atributos_herdados:
            valor_herdado = getattr(parent1.ivs, atributo) if random.choice([True, False]) else getattr(parent2.ivs, atributo)
            novos_ivs[atributo] = valor_herdado
        else:
            novos_ivs[atributo] = random.randint(0, 31)
            
    ivs_filhote = IVs(**novos_ivs)
    especie_filho = __get_especie_filho(parent1, parent2)
    # IMPLEMENTAR CÁLCULO DE PROBABILIDADE DE GÊNERO FUTURAMENTE
    genero_filho = Gender.MALE if random.random() < 0.5 else Gender.FEMALE
    return Pokemon(especie=especie_filho, genero=genero_filho, ivs=ivs_filhote)