from typing import NamedTuple

# "struct"
class IVs(NamedTuple):
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int

ivs_filhote = IVs(31, 31, 31, 10, 31, 31)

print(ivs_filhote.attack)

# A implementar: classe Pokémon que contém "struct" IVs, bem como outras classes e atributos de um Pokémon relevantes para breeding.
# classe Ovo/filhote, herança de Pokémon, que são Pokémons mas em "processo de nascimento" (Pokémons em que serão aplicados cálculos e funções nos pais).
