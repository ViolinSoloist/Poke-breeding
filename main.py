import breeding_mech as bm

if __name__ == "__main__":
    pai_ivs = bm.IVs(hp=31, attack=31, defense=31, sp_atk=31, sp_def=31, speed=31)
    pai = bm.Pokemon(especie="Ditto", ivs=pai_ivs)

    mae_ivs = bm.IVs(hp=0, attack=0, defense=0, sp_atk=0, sp_def=0, speed=0)
    mae = bm.Pokemon(especie="Pikachu", genero=bm.Gender.FEMALE, ivs=mae_ivs)

    filhote = bm.gerar_ovo(pai, mae)
    
    print(f"Info pai:\n{pai}\n")
    print(f"Info Mãe:\n{mae}\n")
    print(f"Filhote:\n{filhote}")