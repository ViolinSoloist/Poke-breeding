import Pokebreed as pb

if __name__ == "__main__":
    ditto = pb.new_pokemon("ditto", gender=pb.Gender.GENDERLESS, ivs=pb.IVs(31,31,31,31,31,31))
    raichu = pb.new_pokemon("raichu", gender=pb.Gender.FEMALE, ivs=pb.IVs(0,0,0,0,0,0))
    print(ditto)
    print(raichu)

    son = pb.gerar_ovo(ditto, raichu)
    print(son)