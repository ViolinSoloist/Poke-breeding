class InvalidBreedingAttempt(Exception):
    def __init__(self, especie1:str, especie2:str, motivo:str):
        self.pk1 = especie1
        self.pk2 = especie2
        self.motivo = motivo
        mensagem = f"Falha no breeding entre {self.pk1} e {self.pk2}: {motivo}"
        super().__init__(mensagem)