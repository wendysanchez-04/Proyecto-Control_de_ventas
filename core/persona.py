from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre: str, correo: str, telefono:str):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @abstractmethod
    def obtener_rol(self) -> str:
        pass
    
