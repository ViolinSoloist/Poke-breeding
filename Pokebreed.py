from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum, auto
import errors as err
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
    GROUND = auto()
    FLYING = auto()
    PLANT = auto()
    HUMANSHAPE = auto()
    MINERAL = auto()
    MONSTER = auto()
    WATER_1 = auto()
    WATER_2 = auto()
    WATER_3 = auto()
    DITTO = auto()
    NOEGGS = auto()

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
class Pkm:
    """Todos os atributos de um Pokémon que são relevantes para a mecânica de breeding.
    
    .. Note:: Para a declaração desta classe, é necessário apenas espécie, pois a API offline (database) é usada para preencher as outras informações.
        
    .. Attention:: Ainda falta implementar atributos de natureza, habilidade e outras coisas que são relevantes no cruzamento."""
    
    especie: str        # Único atributo necessário para instanciar esta classe, pois outras são preenchidas com com API
    egg_groups: tuple[EggGroup, ...] = None
    gender_rate: int = None
    genero: Gender = None
    ivs: IVs = None
    item: BreedingItem = None

    def __str__(self):
        grupos_str = self.egg_groups[0].name if len(self.egg_groups) == 1 else f"{self.egg_groups[0].name}, {self.egg_groups[1].name}"
        item_str = "Not holding any item." if self.item is None else self.item.name
        
        if self.ivs is None:
            ivs_str = "Unknown IVs."
        else:
            ivs_str = (
                f"{self.ivs.hp:02} HP\n"
                f"{self.ivs.attack:02} Attack\n"
                f"{self.ivs.defense:02} Defense\n"
                f"{self.ivs.sp_atk:02} Sp. Attack\n"
                f"{self.ivs.sp_def:02} Sp. Defense\n"
                f"{self.ivs.speed:02} Speed"
            )    
        return f"- {self.especie} -\n{self.genero.name}\n{grupos_str}\n{ivs_str}\n{item_str}\n"
    
    # A IMPLEMENTAR: nature, ability, etc.

# GRAFO DAS CONEXÕES DE GRUPOS DE OVOS
conexoes_egg_groups = {
    EggGroup.AMORPHOUS: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.PLANT, 
        EggGroup.HUMANSHAPE, EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.BUG: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.PLANT, 
        EggGroup.HUMANSHAPE, EggGroup.MINERAL, EggGroup.WATER_1, EggGroup.WATER_3
    },
    EggGroup.DRAGON: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.GROUND, EggGroup.FLYING, 
        EggGroup.PLANT, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1, EggGroup.WATER_2
    },
    EggGroup.FAIRY: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.GROUND, EggGroup.FLYING, 
        EggGroup.PLANT, EggGroup.HUMANSHAPE, EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.GROUND: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.FLYING, EggGroup.PLANT, 
        EggGroup.HUMANSHAPE, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1, EggGroup.WATER_2
    },
    EggGroup.FLYING: {
        EggGroup.DRAGON, EggGroup.FAIRY, EggGroup.GROUND, 
        EggGroup.HUMANSHAPE, EggGroup.WATER_1, EggGroup.WATER_3
    },
    EggGroup.PLANT: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.GROUND, EggGroup.HUMANSHAPE, EggGroup.MINERAL, EggGroup.MONSTER, EggGroup.WATER_1
    },
    EggGroup.HUMANSHAPE: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.FAIRY, EggGroup.GROUND, 
        EggGroup.FLYING, EggGroup.PLANT, EggGroup.WATER_1
    },
    EggGroup.MINERAL: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.GROUND, EggGroup.PLANT, EggGroup.MONSTER
    },
    EggGroup.MONSTER: {
        EggGroup.DRAGON, EggGroup.GROUND, EggGroup.PLANT, 
        EggGroup.MINERAL, EggGroup.WATER_1
    },
    EggGroup.WATER_1: {
        EggGroup.AMORPHOUS, EggGroup.BUG, EggGroup.DRAGON, EggGroup.FAIRY, 
        EggGroup.GROUND, EggGroup.FLYING, EggGroup.PLANT, EggGroup.HUMANSHAPE, 
        EggGroup.MONSTER, EggGroup.WATER_2, EggGroup.WATER_3
    },
    EggGroup.WATER_2: {
        EggGroup.DRAGON, EggGroup.GROUND, EggGroup.WATER_1
    },
    EggGroup.WATER_3: {
        EggGroup.BUG, EggGroup.FLYING, EggGroup.WATER_1
    }
}

# -----------------------------------------------
# ------------------- FUNCOES -------------------
# -----------------------------------------------

def new_pokemon(specie: str, gender: Gender = None, item: BreedingItem = None, ivs: IVs = None) -> Pkm:
    """Instancia um Pokémon pela sua espécie, preenchendo informações importantes através da base de dados."""
    
    nome = specie.lower()
    if nome not in POKEDEX_DB:
        raise ValueError(f"Espécie '{nome}' não existe no banco de dados.")
        
    dados = POKEDEX_DB[nome]
    tupla_grupos = tuple(EggGroup[nome_grupo] if nome_grupo != "NO-EGGS" else EggGroup["NOEGGS"] for nome_grupo in dados['egg_groups'])

    return Pkm(
        especie=specie.capitalize(),
        egg_groups=tupla_grupos,
        genero=gender if nome != "ditto" else Gender.GENDERLESS,
        gender_rate=dados['gender_rate'],
        item=item,
        ivs=ivs
    )

def randomGender(nome_especie: str) -> Gender:
    """Determina aleatoriamente o gênero do pokémon dependendo da espécie.
    (Cada espécie tem uma probabilidade diferente para fêmea/macho)."""
    nome = nome_especie.lower()
    if nome not in POKEDEX_DB:
        raise ValueError(f"Espécie '{nome}' não existe no banco de dados.")
        
    dados = POKEDEX_DB[nome]
    female_rate = dados['gender_rate']
    if female_rate == -1:
        return Gender.GENDERLESS
    return Gender.FEMALE if random.randint(1, 8) <= female_rate else Gender.MALE

def compatible(p1: Pkm, p2: Pkm):
    """Verifica se dois Pokémons podem cruzar e gerar um ovo, com base no gênero, grupos de ovos e no fato de serem ou não Ditto."""
    # Pokémons que são baby, lendários, etc não cruzam
    if EggGroup.NOEGGS in p1.egg_groups or EggGroup.NOEGGS in p2.egg_groups:
        raise err.InvalidBreedingAttempt(p1.especie, p2.especie, "Não é possível cruzar Pokémons lendários, baby, Unown, Nidorina e Nidoqueen.")

    # 2 Dittos não podem se cruzar
    if EggGroup.DITTO in p1.egg_groups and EggGroup.DITTO in p2.egg_groups:
        raise err.InvalidBreedingAttempt("ditto", "ditto", "Não é possível cruzar dois Dittos.")
        
    # Se não forem 2, 1 Ditto pode se cruzar com qualquer genero (até genderless)
    if EggGroup.DITTO in p1.egg_groups or EggGroup.DITTO in p2.egg_groups:
        return True
        
    # Se não tiver nenhum Ditto, devem ser de gêneros opostos e não pode ter nenhum genderless
    if (p1.genero.value + p2.genero.value) != 1:
        raise err.InvalidBreedingAttempt(p1.especie, p2.especie, "Não é possível cruzar dois Pokémons de mesmo sexo ou sem sexo (apenas com Ditto).")
        
    # Se as questões de gêneros e Ditto estiverem okay, precisam ser de grupos de ovos compatíveis.
    if p1.egg_groups and p2.egg_groups:
        grupos_em_comum = set(p1.egg_groups) & set(p2.egg_groups)
        if not grupos_em_comum:
            raise err.InvalidBreedingAttempt(p1.especie, p2.especie, "Grupos de ovos imcompatíveis entre os Pokémons genitores.")
    else:
        # Se as variáveis não estiverem setadas, não cruza
        raise err.InvalidBreedingAttempt("indeterminado", "indeterminado", "Pokémons ou grupos de ovos não determinados.")
        
    return True

def __get_parent_base(p1: Pkm, p2: Pkm) -> Pkm:
    """Identifica o Pokémon matriz do cruzamento (a maioria das vezes é a fêmea). 
    fornecerá espécie, grupos de ovo e (futuramente) a pokeboll"""
    
    # se há um Ditto, 
    if p1.egg_groups == EggGroup.DITTO:
        return p2
    if p2.egg_groups == EggGroup.DITTO:
        return p1
        
    # Em cruzamentos comuns, a fêmea é sempre a matriz
    return p1 if p1.genero == Gender.FEMALE else p2

# IMPLEMENTAR: transmissão de habilidades e naturezas também
def gerar_ovo(parent1: Pkm, parent2: Pkm) -> Pkm:
    """Gera o ovo de um Pokémon, fruto do cruzamento de outros dois Pokémons compatíveis, calculando os atributos.
    A função também verifica compatibilidade.
    
    .. Attention:: Apenas herança de IVs, por enquanto (Ainda falta implementar lógica para itens e trasmissão de habilidades e naturezas).
    
        Cálculo de probabilidade de gênero ainda deve ser implementado (Há probabilidades específicas para algumas espécies).
        Por enquanto, é só 50%/50%."""

    # ---------- VERIFICAÇÃO DE COMPATIBILIDADE ------------------
    compatible(parent1, parent2)
    
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
    genero_filho = randomGender(especie_filho)

    return new_pokemon(
        specie=especie_filho,
        gender=genero_filho,
        item=None,
        ivs=ivs_filhote)