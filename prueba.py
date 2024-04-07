from enum import Enum

class ErrorSexo(Exception):
    pass

class Sexo:
    VARON = 0
    MUJER = 1

class Persona(Enum):
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
            pass # aqui va el raise
        self.asignaturas.append(asignatura)
        return f"Asignatura añadida correctamente"
    
    def eliminar_asignatura(self, asignatura):
        if asignatura not in self.asignaturas:
            print("Asignatura no existente")
            pass # aqui va el raise
        self.asignaturas.remove(asignatura)
        return f"Asignatura eliminada correctamente"
    
    def recuperar_matricula(self):
        return self.asignaturas

class ProfesorAsociado(Persona):
    def __init__(self, nombre, dni, direccion, sexo, formacion):
        super().__init__(nombre, dni, direccion, sexo)
        self.formacion = formacion
        self.docencia = []

    def añadir_asignatura(self, asignatura):
        if asignatura in self.docencia:
            print("Asignatura ya existente")
            pass # aqui va el raise
        self.docencia.append(asignatura)
        return f"Asignatura añadida correctamente"
    
    def eliminar_asignatura(self, asignatura):
        if asignatura not in self.docencia:
            print("Asignatura no existente")
            pass # aqui va el raise
        self.docencia.remove(asignatura)
        return f"Asignatura eliminada correctamente"
    
    def recuperar_docencia(self):
        return self.docencia
    
class ProfesorTitular(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)

class Investigador(Persona):
    def __init__(self, nombre, dni, direccion, sexo, area):
        super().__init__(nombre, dni, direccion, sexo)
        if not isinstance(Persona, ProfesorTitular):
            print("El investigador debe ser profesor titular")
            # raise
        self.area = area
    
    def recuperar_area(self):
        return self.area

    def cambiar_area(self, nueva_area):
        if self.area == nueva_area:
            print("El investigador ya pertenece a ese área")
            # raise
    

class Departamento:
    DIIC = 0
    DITEC = 1
    DIS = 2

class Miembro_departamento:
    def __init__(self, persona, departamento):
        if not (isinstance(persona, ProfesorAsociado) or isinstance(persona, ProfesorTitular) or isinstance(persona, Investigador)):
            print("Esta persona no puede ser miembro de departamento.")
            # raise
        if not isinstance(departamento, Departamento):
            print("Departamento inexistente")
            # raise
        self.departamento = departamento
        
    def eliminar_miembro(self):
        self.departamento.eliminar_miembro(self.persona)
        self.departamento = None

    def __del__(self):
        pass