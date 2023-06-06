from enum import Enum


class Tipo(Enum):
    PIX = 'Pix'
    CC = 'CC'
    BOLETO = 'Boleto'
    TRIBUTOS = 'Tributos'
    VIVO = 'Vivo'
    GRRF = 'Grrf'
    DARF = 'Darf'
    TED = "Ted"

    # def equals(self, string):
    #     return self.name == string

    # def __str__(self) -> str:
    #     return self.value
