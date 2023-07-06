from enum import Enum


class Tipo(Enum):
    PIX = 'Pix'
    CC = 'CC'
    BOLETO = 'Boleto'
    TRIB_ESTADUAL_S_BARRA = 'Tributo_Estadual'
    TRIB_ESTADUAL_C_BARRA = 'Tributo_Estadual'
    TRIB_MUNICIPAL = 'Tributo_Municipal'
    VIVO = 'Vivo'
    GRRF = 'Grrf'
    DARF = 'Darf'
    TED = "Ted"
    GPS = 'Gps'
    SABESP = 'Sabesp'
    ALGAR = 'Algar'
    GRF = 'Grf'
    GARE = 'Gare'
    SEFAZ_DARE = 'Sefaz_Dare'
    CLARO = 'Claro'
    ELETROPAULO = 'Eletropaulo'
    NAO_MAPEADO = 'Documento_não_mapeado'
