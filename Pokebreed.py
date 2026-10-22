from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum, auto
import random
import json

# Bibliografia: https://pokemondb.net/mechanics/breeding

__DATABASE_FILENAME = "pokemon_data.json"
try:
    with open(__DATABASE_FILENAME, "r", encoding="utf-8") as f:
        POKEDEX_DB = json.load(f)
except FileNotFoundError:
    print(f"Aviso: {__DATABASE_FILENAME} não encontrado.")
    POKEDEX_DB = {}

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
    DITTO = auto()
    UNDISCOVERED = auto()

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
    
    .. Note:: Para a declaração desta classe, é necessário apenas espécie e gênero (se não for Ditto) e o grupo de ovos, pois são os atributos que são necessários
        em todas as funcionalidades. Os demais devem ser atribuídos conforme a necessidade.
        
    .. Attention:: Ainda falta implementar atributos de natureza, habilidade e outras coisas que são relevantes no cruzamento."""
    
    especie: str
    egg_groups: tuple[EggGroup, ...] # Um pkm pode ter até dois grupos (NECESSÁRIO PARA INICIALIZAÇÃO DO POKEMON)
    genero: Gender = None
    ivs: IVs = None
    item: BreedingItem = None # NONE POR ENQUANTO SÓ

    def __post_init__(self):
        if self.especie == "Ditto":
            self.genero = Gender.GENDERLESS
            self.egg_groups = EggGroup.DITTO
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

# -----------------------------------------------
# ------------------- FUNCOES -------------------
# -----------------------------------------------

def make_pokemon(nome_especie: str, item: BreedingItem = None, ivs_customizados: IVs = None) -> Pokemon:
    """Cria um Pokémon buscando automaticamente seus Egg Groups e sorteando seu gênero."""
    
    nome = nome_especie.lower()
    if nome not in POKEDEX_DB:
        raise ValueError(f"Espécie '{nome}' não existe no banco de dados.")
        
    dados = POKEDEX_DB[nome]
    
    # 1. Converter Strings do JSON para o Enum EggGroup
    # Nota: A PokéAPI usa 'plant' ao invés de 'grass' e 'humanshape' ao invés de 'human-like'.
    # Você precisará alinhar os nomes do seu Enum com os nomes da API.
    tupla_grupos = tuple(EggGroup[nome_grupo] for nome_grupo in dados['egg_groups'])
    
    # 2. Calcular o Gênero
    taxa = dados['gender_rate']
    if taxa == -1:
        genero_sorteado = Gender.GENDERLESS
    elif taxa == 0:
        genero_sorteado = Gender.MALE
    elif taxa == 8:
        genero_sorteado = Gender.FEMALE
    else:
        # random.randint(1, 8) gera um número de 1 a 8. 
        # Se cair dentro da "taxa", é fêmea.
        genero_sorteado = Gender.FEMALE if random.randint(1, 8) <= taxa else Gender.MALE
        
    # 3. Retorna a dataclass preenchida
    return Pokemon(
        especie=nome_especie.capitalize(),
        egg_groups=tupla_grupos,
        genero=genero_sorteado,
        item=item,
        ivs=ivs_customizados
    )

def compatible(p1: Pokemon, p2: Pokemon) -> bool:
    """Verifica se dois Pokémons podem cruzar e gerar um ovo, com base no gênero, grupos de ovos e no fato de serem ou não Ditto."""

    # 2 Dittos não podem se cruzar
    if p1.egg_groups == EggGroup.DITTO and p2.egg_groups == EggGroup.DITTO:
        return False
        
    # Se não forem 2, 1 DItto pode se cruzar com qualquer genero (até genderless)
    if p1.egg_groups == EggGroup.DITTO or p2.egg_groups == EggGroup.DITTO:
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

def __get_parent_base(p1: Pokemon, p2: Pokemon) -> Pokemon:
    """Identifica o Pokémon matriz do cruzamento (a maioria das vezes é a fêmea). 
    fornecerá espécie, grupos de ovo e (futuramente) a pokeboll"""
    
    # se há um Ditto, 
    if p1.egg_groups == EggGroup.DITTO:
        return p2
    if p2.egg_groups == EggGroup.DITTO:
        return p1
        
    # Em cruzamentos comuns, a fêmea é sempre a matriz
    return p1 if p1.genero == Gender.FEMALE else p2

# IMPLEMENTAR: LÓGICA PARA DESTINY KNOT
# IMPLEMENTAR: transmissão de habilidades e naturezas também
def gerar_ovo(parent1: Pokemon, parent2: Pokemon) -> Pokemon:
    """Gera o ovo de um Pokémon, fruto do cruzamento de outros dois Pokémons compatíveis, calculando os atributos.
    A função também verifica compatibilidade.
    
    .. Attention:: Apenas herança de IVs, por enquanto (Ainda falta implementar lógica para itens e trasmissão de habilidades e naturezas).
    
        Cálculo de probabilidade de gênero ainda deve ser implementado (Há probabilidades específicas para algumas espécies).
        Por enquanto, é só 50%/50%."""

    # ---------- VERIFICAÇÃO DE COMPATIBILIDADE ------------------
    if not compatible(parent1, parent2):
        raise ValueError(f"Cruzamento inválido: {parent1.especie} e {parent2.especie} não são compatíveis.", "compatibilidade")
    
    atributos = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
    
    # Pré randomiza os 6 atributos para depois mudarmos 3 (com repetição permitida)
    novos_ivs = {attr: random.randint(0, 31) for attr in atributos}

    # para facilitar a checagem dos itens de poder
    mapa_power_items = {
        BreedingItem.POWER_WEIGHT: 'hp',
        BreedingItem.POWER_BRACER: 'attack',
        BreedingItem.POWER_BELT: 'defense',
        BreedingItem.POWER_LENS: 'sp_atk',
        BreedingItem.POWER_BAND: 'sp_def',
        BreedingItem.POWER_ANKLET: 'speed'
    }

    poder_p1 = mapa_power_items.get(parent1.item)
    poder_p2 = mapa_power_items.get(parent2.item)
    
    atributo_forcado = None
    pai_do_atributo_forcado = None
    
    # -------------- TRATAMENTO DE CASOS (POWER ITEMS) ------------------
    # Se os dois seguram Power Items, escolhe um aleatoriamente para prevalecer
    if poder_p1 and poder_p2:
        if random.choice([True, False]):
            atributo_forcado, pai_do_atributo_forcado = poder_p1, parent1
        else:
            atributo_forcado, pai_do_atributo_forcado = poder_p2, parent2
    elif poder_p1:
        atributo_forcado, pai_do_atributo_forcado = poder_p1, parent1
    elif poder_p2:
        atributo_forcado, pai_do_atributo_forcado = poder_p2, parent2

    # -------------------- CHECAGEM DESTINY KNOT -------------------------
    has_destiny_knot = (parent1.item == BreedingItem.DESTINY_KNOT) or (parent2.item == BreedingItem.DESTINY_KNOT)
    qtd_herdar = 5 if has_destiny_knot else 3
    atributos_disponiveis = atributos.copy()

    # ---------------- APLICA POWER ITEM (SE HOUVER) -----------------------------
    if atributo_forcado:
        novos_ivs[atributo_forcado] = getattr(pai_do_atributo_forcado.ivs, atributo_forcado)
        atributos_disponiveis.remove(atributo_forcado)
        qtd_herdar -= 1

    # ---------------- RESTANTE DA HERANÇA -----------------------------
    if has_destiny_knot or atributo_forcado:
        # Se usou item, o sorteio é sem repetição e isola os atributos
        atributos_sorteados = random.sample(atributos_disponiveis, qtd_herdar)
        for attr in atributos_sorteados:
            pai_escolhido = parent1 if random.choice([True, False]) else parent2
            novos_ivs[attr] = getattr(pai_escolhido.ivs, attr)
    else:
        # Se não tem itens, sorteio normal 
        for _ in range(qtd_herdar):
            atributo_sorteado = random.choice(atributos)
            pai_escolhido = parent1 if random.choice([True, False]) else parent2 
            novos_ivs[atributo_sorteado] = getattr(pai_escolhido.ivs, atributo_sorteado)
            
    ivs_filhote = IVs(**novos_ivs)
    pai_base = __get_parent_base(parent1, parent2)
    especie_filho = pai_base.especie
    grupos_filho = pai_base.egg_groups
    
    # IMPLEMENTAR CÁLCULO DE PROBABILIDADE DE GÊNERO FUTURAMENTE
    genero_filho = Gender.MALE if random.random() < 0.5 else Gender.FEMALE
    
    return Pokemon(
        especie=especie_filho, 
        egg_groups=grupos_filho, 
        genero=genero_filho, 
        ivs=ivs_filhote
    )