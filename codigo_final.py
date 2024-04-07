from enum import Enum

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
            raise ValueError("Sexo incorrecto")
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

class Tipo(Enum):
    TITULAR = 0
    ASOCIADO = 1

class ProfesorAsociado(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)

class ProfesorTitular(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)

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

    def __init__(self, nombre, dni, direccion, sexo, departamento):
        if not isinstance(departamento, Departamento):
            print("Introduzca un departamento válido")
            raise ValueError("Departamento inexistente")
        self.nombre, self.dni, self.direccion, self.sexo = nombre, dni, direccion, sexo
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
        self.investigadores = {} # dni: instancia
        self.matriculas = {} # dni del estudiante: lista con sus asignaturas
        self.docencia = {} # dni del profesor: lista con sus asignaturas

    def recuperar_departamento(self, departamento):
        if not isinstance(departamento, Departamento):
            print("Introduzca un departamento válido")
            raise ValueError("Departamento inexistente")
        return [self.departamentos[departamento][dni].recuperar_nombre() for dni in self.departamentos[departamento]]
        # Devuelve los nombres de las personas de un determinado departamento
    def recuperar_matricula(self, dni):
        if dni not in self.personas["estudiantes"]:
            print("El DNI introducido no corresponde con ningún estudiante")
            raise ValueError("Estudiante inexistente")
        return self.matriculas[dni] # Devuelve las asignaturas que cursa actualmente el estudiante introducido
    
    def recuperar_docencia(self, dni):
        if dni not in self.personas["profesores_titulares"] and dni not in self.personas["profesores_asociados"]:
            print("Introduzca un DNI válido")
            raise ValueError("Profesor inexistente")
        return self.docencia[dni] # Devuelve tanto las asignaturas impartidas por un profesor como los grados donde se imparten

    def recuperar_informacion_persona(self, dni):
        if dni in self.personas["estudiantes"]:
            datos = self.personas["estudiantes"][dni].recuperar_datos_personales()
            return f"Estudiante. Nombre: {datos[0]}. Dirección: {datos[2]}. Sexo: {datos[3]}"
        elif dni in self.personas["profesores_titulares"]:
            datos = self.personas["profesores_titulares"][dni].recuperar_datos_personales()
            return f"Profesor titular. Nombre: {datos[0]}. Dirección: {datos[2]}. Sexo: {datos[3]}"
        elif dni in self.personas["profesores_asociados"]:
            datos = self.personas["profesores_asociados"][dni].recuperar_datos_personales()
            return f"Profesor asociado. Nombre: {datos[0]}. Dirección: {datos[2]}. Sexo: {datos[3]}"
        print("Intruduce un dni válido")
        raise ValueError("Persona inexistente")

    def crear_estudiante(self, nombre, dni, direccion, sexo):
        estudiante = Estudiante(nombre, dni, direccion, sexo)
        self.personas["estudiantes"][dni] = estudiante
        self.matriculas[dni] = []
        return "Estudiante creado exitosamente"

    def eliminar_estudiante(self, dni):
        if dni not in self.personas["estudiantes"]:
            print("El DNI introducido no corresponde con ningún estudiante")
            raise ValueError("Estudiante inexistente")
        nombre = self.personas["estudiantes"][dni].recuperar_nombre()
        del self.personas["estudiantes"][dni]
        del self.matriculas[dni] # Eliminamos también su matrícula
        return nombre

    def crear_miembro_departamento(self, nombre, dni, direccion, sexo, departamento):
        if dni not in self.personas["profesores_asociados"] and dni not in self.personas["profesores_titulares"]:
            print("La persona debe ser profesor (asociado o titular)")
            raise ValueError("Profesor inexistente")
        miembro = MiembroDepartamento(nombre, dni, direccion, sexo, departamento)
        self.departamentos[departamento][dni] = miembro
        return "Miembro añadido"

    def eliminar_miembro_departamento(self, dni, departamento):
        if dni not in self.departamentos[departamento]:
            print("Introduzca el DNI del miembro correctamente")
            raise ValueError("Miembro inexistente")
        nombre = self.departamentos[departamento][dni].recuperar_nombre()
        del self.departamentos[departamento][dni]
        return nombre

    def crear_profesor(self, nombre, dni, direccion, sexo, tipo):
        if tipo.lower() not in ['asociado', 'titular']:
            print("El profesor debe ser *asociado* o *titular*")
            raise ValueError("Tipo de profesor no válido")
        if tipo.lower() == "asociado":
            profesor = ProfesorAsociado(nombre, dni, direccion, sexo)
            self.personas["profesores_asociados"][dni] = profesor
        else:
            area = str(input("Introduce el área de investigación del profesor titular: "))
            profesor = ProfesorTitular(nombre, dni, direccion, sexo)
            self.personas["profesores_titulares"][dni] = profesor
            investigador = Investigador(profesor.nombre, profesor.dni, profesor.direccion, profesor.sexo, area)
            self.investigadores[dni] = investigador
        self.docencia[dni] = []
        return "Profesor creado exitosamente"

    def eliminar_profesor(self, dni):
        if dni in self.personas["profesores_asociados"]:
            nombre = self.personas["profesores_asociados"][dni].recuperar_nombre()
            del self.personas["profesores_asociados"][dni]
            del self.docencia[dni] # Eliminamos también su docencia
            return nombre
        elif dni in self.personas["profesores_titulares"]:
            nombre = self.personas["profesores_titulares"][dni].recuperar_nombre()
            # También tenemos que eliminar el investigador asociado
            del self.personas["profesores_titulares"][dni]
            del self.investigadores[dni] # También lo eliminamos de investigador
            del self.docencia[dni]
            return nombre
        print("Introduzca un DNI válido")
        raise ValueError("El profesor no existe")

    def ampliar_matricula(self, dni, asignatura):
        if dni not in self.matriculas:
            print("Introduzca un DNI válido")
            raise ValueError("Este estudiante no está matriculado")
        self.matriculas[dni].append(asignatura)

    def asignatura_aprobada(self, dni, asignatura):
        if dni not in self.personas["estudiantes"]:
            print("Introduzca un DNI válido")
            raise ValueError("Este estudiante no está matriculado")
        if asignatura not in self.matriculas[dni]:
            print("Introduzca una asignatura válida")
            raise ValueError("Esta asignatura no está en la lista de matrículas del estudiante")
        self.matriculas[dni].remove(asignatura)

    def ampliar_docencia(self, dni, asignatura, grado):
        if dni not in self.docencia:
            print("Introduzca un DNI válido")
            raise ValueError("Esta persona no forma parte del profesorado")
        self.docencia[dni].append([asignatura, grado])

    def reducir_docencia(self, dni, asignatura, grado):
        if dni not in self.docencia:
            print("Introduzca un DNI válido")
            raise ValueError("Esta persona no forma parte del profesorado")
        if [asignatura, grado] not in self.docencia[dni]:
            print("Introduzca una asignatura impartida por este profesor")
            raise ValueError("Asignatura inexistente en la docencia de este profesor")

    def cambiar_area(self, dni, nueva_area):
        if dni not in self.investigadores:
            print("Introduzca un DNI válido")
            raise ValueError("No existe el investigador")
        if self.investigadores[dni].recuperar_area() == nueva_area:
            print("Introduzca un área diferente")
            raise ValueError("El investigador ya pertenece a ese área")
        self.investigadores[dni].area = nueva_area

    def cambiar_departamento(self, dni, nuevo_departamento):
        if not isinstance(nuevo_departamento, Departamento):
            print("Introduzca un departamento válido")
            raise ValueError("Departamento inexistente")
        for departamento, miembros in self.departamentos.items():
            if dni in miembros:
                self.departamentos[departamento][dni].departamento = nuevo_departamento
                miembro = miembros[dni]
                del miembros[dni]
                self.departamentos[nuevo_departamento][dni] = miembro
                return "Departamento cambiado exitosamente"
        print("Introduzca un miembro válido")
        raise ValueError("Miembro no encontrado en ningún departamento")



if __name__ == "__main__":
    # Crear una instancia de Admin
    admin = Admin(id_cuenta="admin_1")

    # Crear un estudiante
    print(admin.crear_estudiante(nombre="Estudiante 1", dni="12345678A", direccion="Calle Principal 123", sexo=Sexo.VARON))
    print(admin.personas)
    # Crear un profesor asociado
    '''print(admin.crear_profesor(nombre="Profesor Asociado 1", dni="87654321B", direccion="Calle Secundaria 456", sexo=Sexo.MUJER, tipo="asociado"))

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
    print("Profesor eliminado:", nombre_profesor_eliminado)'''

