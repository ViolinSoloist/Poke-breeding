import Pokebreed as pb

if __name__ == "__main__":
    pai_ivs = pb.IVs(hp=31, attack=31, defense=31, sp_atk=31, sp_def=31, speed=31)
    pai = pb.Pokemon(especie="Ditto", ivs=pai_ivs, egg_groups=pb.EggGroup.DITTO)

    mae_ivs = pb.IVs(hp=0, attack=0, defense=0, sp_atk=0, sp_def=0, speed=0)
    mae = pb.Pokemon(especie="Raichu", genero=pb.Gender.FEMALE, ivs=mae_ivs, egg_groups=[pb.EggGroup.FAIRY, pb.EggGroup.FIELD])

    filhote = pb.gerar_ovo(pai, mae)
    
    print(f"Info pai:\n{pai}\n")
    print(f"Info Mãe:\n{mae}\n")
    print(f"Filhote:\n{filhote}")