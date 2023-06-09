from __future__ import annotations

import csv

from usuario import Usuario
from viaje import Viaje


class DatasetViajes:
    def __init__(self, usuarios_filename: str, viajes_filename: str):
        self.usuarios: Dict[int, Usuario] = {}
        self.viajes_por_usuario: Dict[int, List[Viaje]] = {}

        # Importamos los usuarios primero
        file_usuarios: TextIO = open(usuarios_filename, 'r', encoding='utf-8')
        linea: Dict[str, str]
        for linea in csv.DictReader(file_usuarios):
            # Tomo los datos y los convierto a int
            id_usuario: int = int(linea['id_usuario'])
            edad: int = int(linea['edad_usuario'])

            # Creo el usuario y lo almaceno
            usuario: Usuario = Usuario(id_usuario, edad)
            self.usuarios[usuario.id_usuario] = usuario
            self.viajes_por_usuario[usuario.id_usuario] = []

        # Luego completamos con los datos de los viajes
        file_viajes = open(viajes_filename, 'r', encoding='utf-8')
        linea: Dict[str, str]
        for linea in csv.DictReader(file_viajes):
            # Tomo los datos y los convierto a int
            id_usuario: int = int(linea['id_usuario'])
            duracion: int = int(linea['duracion_recorrido'])
            estacion_origen: str = linea['nombre_estacion_origen']
            estacion_destino: str = linea['nombre_estacion_destino']

            # Creo el viaje y lo almaceno
            viaje: Viaje = Viaje(duracion, estacion_origen, estacion_destino)
            self.viajes_por_usuario[id_usuario].append(viaje)

        # Cierro ambos archivos
        file_usuarios.close()
        file_viajes.close()

    def minutos_pedaleando(self, id_usuario: int) -> float:
        """Devuelve la cantidad de minutos acumulados en los viajes del usuario
        Pre: id_usuario in self.usuarios
        Post: Devuelve la suma de la duración de todos los viajes del usuario
              con id_usuario en minutos
        """
        duracion_total_segs: int = 0
        for viaje in self.viajes_por_usuario[id_usuario]:
            duracion_total_segs = duracion_total_segs + viaje.duracion

        return duracion_total_segs / 60

    def minutos_promedio_para_edad(self, edad: int) -> float:
        """Devuelve el promedio de minutos pedaleados para los usuarios con cierta edad
        Pre: ninguna
        Post: Devuelve el promedio de los minutos pedaleados por todos los usuarios
              cuya edad es igual a la edad pasada por parámetro
        """
        duracion_total_min: float = 0
        usuarios_con_edad: int = 0

        for usuario in self.usuarios.values():
            if usuario.edad == edad:
                duracion_total_min += self.minutos_pedaleando(usuario.id_usuario)
                usuarios_con_edad += 1

        if usuarios_con_edad == 0:
            return 0

        return duracion_total_min / usuarios_con_edad
