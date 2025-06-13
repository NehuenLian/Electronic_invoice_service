from pydantic import BaseModel


class AlicIva(BaseModel):
    Id: int
    BaseImp: float
    Importe: float

class Iva(BaseModel):
    AlicIva: AlicIva

class FECAEDetRequest(BaseModel):
    Concepto: int
    DocTipo: int
    DocNro: int
    CbteDesde: int
    CbteHasta: int
    CbteFch: str
    ImpTotal: float
    ImpTotConc: float
    ImpNeto: float
    ImpOpEx: float
    ImpTrib: float
    ImpIVA: float
    MonId: str
    MonCotiz: float
    CondicionIVAReceptorId: int
    Iva: Iva

class FeDetReq(BaseModel):
    FECAEDetRequest: FECAEDetRequest

class FeCabReq(BaseModel):
    CantReg: int
    PtoVta: int
    CbteTipo: int

class FeCAEReq(BaseModel):
    FeCabReq: FeCabReq
    FeDetReq: FeDetReq

class Auth(BaseModel):
    Cuit: int

class RootModel(BaseModel):
    Auth: Auth
    FeCAEReq: FeCAEReq
