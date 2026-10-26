import Pokebreed as pb

if __name__ == "__main__":
    ditto = pb.new_pokemon("ditto", ivs=pb.IVs(32,32,32,32,32,32), item=pb.BreedingItem.POWER_ANKLET)
    raichu = pb.new_pokemon("raichu", gender=pb.Gender.FEMALE, ivs=pb.IVs(67,67,67,67,67,67), item=pb.BreedingItem.DESTINY_KNOT)
    print(ditto)
    print(raichu)

    son = pb.gerar_ovo(ditto, raichu)
    print(son)