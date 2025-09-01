from enum import Enum

class GetTypeOffer(Enum):
    ORICARE = "0"
    OFERTA_CONCURENTIALA = "1"
    OFERTA_UNIVERSALA = "2"

class GetTypeProduct(Enum):
    ORICARE = "0"
    PRET_FIX = "1"
    PRET_VARIABIL = "2"