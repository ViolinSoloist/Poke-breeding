import Pokebreed as Pb

if __name__ == "__main__":
    ditto = Pb.newPokemon("ditto", ivs=Pb.IVs(32,32,32,32,32,32), item=Pb.BreedingItem.POWER_ANKLET)
    raichu = Pb.newPokemon("raichu", gender=Pb.Gender.FEMALE, ivs=Pb.IVs(67,67,67,67,67,67), item=Pb.BreedingItem.DESTINY_KNOT)
    print(ditto)
    print(raichu)

    son = Pb.gerar_ovo(ditto, raichu)
    print(son)