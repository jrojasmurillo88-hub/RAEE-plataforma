from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PuntoRecoleccion:
    sistema: str
    nombre: str
    direccion: str
    ciudad: str
    tipos_raee: list[str] = field(default_factory=list)
    horario: str | None = None
    lat: float | None = None
    lng: float | None = None
    fuente_url: str = ""
    ultima_verificacion: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "sistema": self.sistema,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "tipos_raee": self.tipos_raee,
            "horario": self.horario,
            "lat": self.lat,
            "lng": self.lng,
            "fuente_url": self.fuente_url,
            "ultima_verificacion": self.ultima_verificacion,
        }
