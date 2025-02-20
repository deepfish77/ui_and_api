from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel

class Voto(BaseModel):
    codProvincia: Optional[int] = None
    codDignidad: Optional[int] = None
    nomPartido: Optional[str] = None
    lisPartido: Optional[str] = None
    nomCandidato: Optional[str] = None
    votos: Optional[int] = None
    votosM: Optional[int] = None
    votosF: Optional[int] = None
    porcentajeF: Optional[float] = None
    porcentajeM: Optional[float] = None
    porcentaje: Optional[float] = None
    iconCandidato: Optional[str] = None

class Acta(BaseModel):
    codDignidad: Optional[int] = None
    novedades: Optional[int] = None
    totalActas: Optional[int] = None
    totalNovedades: Optional[int] = None
    totalValidas: Optional[int] = None
    validas: Optional[float] = None
    codQrUuId: Optional[Any] = None
    huella: Optional[Any] = None

class Sufragante(BaseModel):
    codDignidad: Optional[int] = None
    sufragantes: Optional[int] = None
    sufragantesM: Optional[int] = None
    sufragantesF: Optional[int] = None
    sufMPorc: Optional[float] = None
    sufFPorc: Optional[float] = None
    ausentismo: Optional[int] = None
    ausentismoM: Optional[int] = None
    ausentismoF: Optional[int] = None
    ausMPorc: Optional[float] = None
    ausFPorc: Optional[float] = None
    sufPorc: Optional[float] = None
    ausPorc: Optional[float] = None

class Blanco(BaseModel):
    codDignidad: Optional[int] = None
    blancos: Optional[int] = None
    votosBlancosM: Optional[int] = None
    votosBlancosF: Optional[int] = None
    blancosMPorc: Optional[float] = None
    blancosFPorc: Optional[float] = None
    nulos: Optional[int] = None
    votosNulosM: Optional[int] = None
    votosNulosF: Optional[int] = None
    nulosMPorc: Optional[float] = None
    nulosFPorc: Optional[float] = None
    blancosPorc: Optional[float] = None
    nulosPorc: Optional[float] = None

class Electore(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeHombres: Optional[float] = None
    porcentajeMujeres: Optional[float] = None
    totalJuntas: Optional[int] = None
    juntasHombres: Optional[int] = None
    juntasMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[int] = None
    porcentajeJuntas: Optional[int] = None

class ElectoresPplItem(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[int] = None
    porcentajeJuntas: Optional[int] = None

class Totale(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeHombres: Optional[float] = None
    porcentajeMujeres: Optional[float] = None
    totalJuntas: Optional[int] = None
    juntasHombres: Optional[int] = None
    juntasMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[int] = None
    porcentajeJuntas: Optional[int] = None

class ElectoresJunta(BaseModel):
    electores: Optional[List[Electore]] = None
    electoresPpl: Optional[List[ElectoresPplItem]] = None
    totales: Optional[List[Totale]] = None

class Electore1(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeHombres: Optional[float] = None
    porcentajeMujeres: Optional[float] = None
    totalJuntas: Optional[int] = None
    juntasHombres: Optional[int] = None
    juntasMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[float] = None
    porcentajeJuntas: Optional[float] = None

class ElectoresPplItem1(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[int] = None
    porcentajeJuntas: Optional[int] = None

class Totale1(BaseModel):
    codDignidad: Optional[int] = None
    codZona: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeHombres: Optional[float] = None
    porcentajeMujeres: Optional[float] = None
    totalJuntas: Optional[int] = None
    juntasHombres: Optional[int] = None
    juntasMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[float] = None
    porcentajeJuntasMujeres: Optional[float] = None
    porcentaje: Optional[float] = None
    porcentajeJuntas: Optional[float] = None

class ElectoresJuntaComputada(BaseModel):
    electores: Optional[List[Electore1]] = None
    electoresPpl: Optional[List[ElectoresPplItem1]] = None
    totales: Optional[List[Totale1]] = None

class ElectoresJuntasAnuladas(BaseModel):
    codDignidad: Optional[int] = None
    total: Optional[int] = None
    totalHombres: Optional[int] = None
    totalMujeres: Optional[int] = None
    porcentajeHombres: Optional[float] = None
    porcentajeMujeres: Optional[float] = None
    totalJuntas: Optional[int] = None
    juntasHombres: Optional[int] = None
    juntasMujeres: Optional[int] = None
    porcentajeJuntasHombres: Optional[int] = None
    porcentajeJuntasMujeres: Optional[int] = None
    percentage: Optional[float] = None
    percentageJuntas: Optional[float] = None

class Model(BaseModel):
    votos: Optional[List[Voto]] = None
    actas: Optional[List[Acta]] = None
    sufragantes: Optional[List[Sufragante]] = None
    blancos: Optional[List[Blanco]] = None
    corte: Optional[str] = None
    electoresJunta: Optional[ElectoresJunta] = None
    electoresJuntaComputada: Optional[ElectoresJuntaComputada] = None
    electoresJuntasAnuladas: Optional[ElectoresJuntasAnuladas] = None
