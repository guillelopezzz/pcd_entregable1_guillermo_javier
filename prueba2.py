from enum import Enum

class ErrorSexo(Exception):
    pass

class Sexo(Enum):
    VARON = 0
    MUJER = 1

class Persona:
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        if sexo not in [Sexo.VARON, Sexo.MUJER]:
            print("El sexo debe ser 0:Varón o 1:Mujer.")
            raise ErrorSexo
        self.sexo = sexo

    def recuperar_nombre(self):
        return self.nombre

    def recuperar_dni(self):
        return self.dni

    def recuperar_direccion(self):
        return self.direccion

    def recuperar_sexo(self):
        return self.sexo

    def recuperar_datos_personales(self):
        return [self.recuperar_nombre(), self.recuperar_dni(), self.recuperar_direccion(), self.recuperar_sexo()]

class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = []

    def añadir_asignatura(self, asignatura):
        if asignatura in self.asignaturas:
            print("Asignatura ya existente")
            pass # aquí va el raise
        self.asignaturas.append(asignatura)
        return "Asignatura añadida correctamente"

    def eliminar_asignatura(self, asignatura):
        if asignatura not in self.asignaturas:
            print("Asignatura no existente")
            pass # aquí va el raise
        self.asignaturas.remove(asignatura)
        return "Asignatura eliminada correctamente"

    def recuperar_matricula(self):
        return self.asignaturas

class Tipo(Enum):
    TITULAR = 0
    ASOCIADO = 1

class ProfesorAsociado(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
        self.docencia = []

    def añadir_asignatura(self, asignatura):
        if asignatura in self.docencia:
            print("Asignatura ya existente")
            pass # aquí va el raise
        self.docencia.append(asignatura)
        return "Asignatura añadida correctamente"

    def eliminar_asignatura(self, asignatura):
        if asignatura not in self.docencia:
            print("Asignatura no existente")
            pass # aquí va el raise
        self.docencia.remove(asignatura)
        return "Asignatura eliminada correctamente"

    def recuperar_docencia(self):
        return self.docencia

class ProfesorTitular(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
        self.docencia = []

    def añadir_asignatura(self, asignatura):
        if asignatura in self.docencia:
            print("Asignatura ya existente")
            pass # aquí va el raise
        self.docencia.append(asignatura)
        return "Asignatura añadida correctamente"

    def eliminar_asignatura(self, asignatura):
        if asignatura not in self.docencia:
            print("Asignatura no existente")
            pass # aquí va el raise
        self.docencia.remove(asignatura)
        return "Asignatura eliminada correctamente"

    def recuperar_docencia(self):
        return self.docencia

class Investigador(ProfesorTitular):
    def __init__(self, nombre, dni, direccion, sexo, area):
        super().__init__(nombre, dni, direccion, sexo)
        self.area = area

    def recuperar_area(self):
        return self.area

class Departamento(Enum):
    DIIC = 0
    DITEC = 1
    DIS = 2

class MiembroDepartamento:

    def __init__(self, persona, departamento):
        if not (isinstance(persona, ProfesorAsociado) or isinstance(persona, ProfesorTitular) or isinstance(persona, Investigador)):
            print("Esta persona no puede ser miembro de departamento.")
            # raise
        if not isinstance(departamento, Departamento):
            print("Departamento inexistente")
            # raise
        self.nombre = persona.recuperar_nombre()
        self.departamento = departamento

    def recuperar_nombre(self):
        return self.nombre

    def recuperar_departamento(self):
        return self.departamento

class Admin:
    def __init__(self, id_cuenta):
        self.id_cuenta = id_cuenta
        self.personas = {"estudiantes": {}, "profesores_titulares": {}, "profesores_asociados": {}}
        self.departamentos = {Departamento.DIIC: {}, Departamento.DITEC: {}, Departamento.DIS: {}}
        self.asignaturas = []

    def crear_estudiante(self, nombre, dni, direccion, sexo):
        estudiante = Estudiante(nombre, dni, direccion, sexo)
        self.personas["estudiantes"][dni] = estudiante
        return "Estudiante creado exitosamente"

    def eliminar_estudiante(self, dni):
        if dni not in self.personas["estudiantes"]:
            print("Estudiante inexistente")
            # raise
        nombre = self.personas["estudiantes"][dni].recuperar_nombre()
        del self.personas["estudiantes"][dni]
        return nombre

    def crear_miembro_departamento(self, nombre, dni, direccion, sexo, departamento):
        persona = Persona(nombre, dni, direccion, sexo)
        miembro = MiembroDepartamento(persona, departamento)
        self.departamentos[departamento][dni] = miembro
        return "Miembro añadido"

    def eliminar_miembro_departamento(self, dni, departamento):
        if dni not in self.departamentos[departamento]:
            print("Miembro inexistente")
            # raise
        nombre = self.departamentos[departamento][dni].recuperar_nombre()
        del self.departamentos[departamento][dni]
        return nombre

    def crear_profesor(self, nombre, dni, direccion, sexo, tipo):
        if tipo.lower() not in ['asociado', 'titular']:
          print("Tipo de profesor no válido.")
          # raise
        if tipo.lower() == "asociado":
            profesor = ProfesorAsociado(nombre, dni, direccion, sexo)
            self.personas["profesores_asociados"][dni] = profesor
        else:
            profesor = ProfesorTitular(nombre, dni, direccion, sexo)
            self.personas["profesores_titulares"][dni] = profesor
        return "Profesor creado exitosamente"

    def eliminar_profesor(self, dni):
        if dni in self.personas["profesores_asociados"]:
            nombre = self.personas["profesores_asociados"][dni].recuperar_nombre()
            del self.personas["profesores_asociados"][dni]
            return nombre
        elif dni in self.personas["profesores_titulares"]:
            nombre = self.personas["profesores_titulares"][dni].recuperar_nombre()
            del self.personas["profesores_titulares"][dni]
            return nombre
        else:
            print("El profesor no existe.")


    '''def cambiar_area(self, dni, nueva_area):
        if  == nueva_area:
            print("El investigador ya pertenece a ese área")
            # raise
        self.area = nueva_area'''

    def cambiar_departamento(self, dni, nuevo_departamento):
        if not isinstance(nuevo_departamento, Departamento):
            print("Departamento inexistente")
            # raise
        for departamento, miembros in self.departamentos.items():  # Iterar sobre las claves y los valores del diccionario
            if dni in miembros:
                miembro = miembros[dni]
                del miembros[dni]  # Eliminar el miembro del departamento actual
                self.departamentos[nuevo_departamento][dni] = miembro  # Asignar el miembro al nuevo departamento
                return "Departamento cambiado exitosamente"
        print("Miembro no encontrado en ningún departamento")

if __name__ == "__main__":
    # Crear una instancia de Admin
    admin = Admin(id_cuenta="admin_1")

    # Crear un estudiante
    print(admin.crear_estudiante(nombre="Estudiante 1", dni="12345678A", direccion="Calle Principal 123", sexo=Sexo.VARON))

    # Crear un profesor asociado
    print(admin.crear_profesor(nombre="Profesor Asociado 1", dni="87654321B", direccion="Calle Secundaria 456", sexo=Sexo.MUJER, tipo="asociado"))

    # Crear un profesor titular
    admin.crear_profesor(nombre="Profesor Titular 1", dni="65432178C", direccion="Avenida Principal 789", sexo=Sexo.MUJER, tipo="titular")

    # Crear un miembro de departamento para un estudiante
    admin.crear_miembro_departamento(nombre="Miembro Estudiante 1", dni="12345678A", direccion="Calle del Departamento 1", sexo=Sexo.VARON, departamento=Departamento.DIIC)

    # Crear un miembro de departamento para un profesor
    admin.crear_miembro_departamento(nombre="Miembro Profesor Asociado 1", dni="87654321B", direccion="Calle del Departamento 2", sexo=Sexo.MUJER, departamento=Departamento.DITEC)

    # Cambiar departamento de un estudiante
    admin.cambiar_departamento(dni="12345678A", nuevo_departamento=Departamento.DIS)

    # Eliminar un estudiante
    nombre_estudiante_eliminado = admin.eliminar_estudiante(dni="12345678A")
    print("Estudiante eliminado:", nombre_estudiante_eliminado)

    # Eliminar un miembro de departamento
    nombre_miembro_eliminado = admin.eliminar_miembro_departamento(dni="87654321B", departamento=Departamento.DITEC)
    print("Miembro de departamento eliminado:", nombre_miembro_eliminado)

    # Eliminar un profesor
    nombre_profesor_eliminado = admin.eliminar_profesor(dni="65432178C")
    print("Profesor eliminado:", nombre_profesor_eliminado)

