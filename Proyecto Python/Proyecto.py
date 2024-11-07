import random
import json
import os

# Funciones de Utilidad
def generar_ids_unicos(cantidad):
    ids = set()
    while len(ids) < cantidad:
        id_4_digitos = random.randint(1000, 9999)
        ids.add(id_4_digitos)
    return ids

def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            return json.load(f)
    return []

def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=4)

# Funciones para Profesores y Materias
def cargar_profesores():
    return cargar_datos("profesores.json")

def guardar_profesores(profesores):
    guardar_datos("profesores.json", profesores)

def cargar_materias():
    return cargar_datos("materias.json")

def guardar_materias(materias):
    guardar_datos("materias.json", materias)

def cargar_horarios():
    return cargar_datos("horarios.json")

def guardar_horarios(horarios):
    guardar_datos("horarios.json", horarios)

# Variables estáticas
USUARIOCORRECTO = "admin"
CLAVECORRECTA = "280122"

# Ingreso de usuario
usuario = input("Dame tu usuario: ")
clave = input("Dame tu clave: ")

if usuario == USUARIOCORRECTO and clave == CLAVECORRECTA:
    print("Bienvenido")

    # Cargar datos
    profesores = cargar_profesores()
    materias = cargar_materias()
    horarios = cargar_horarios()

    # Menú Principal
    while True:
        print("\nSeleccione una opción:")
        print("1. Profesores")
        print("2. Materias")
        print("3. Asignación de Materias")
        print("4. Ver Horarios")
        print("5. Salir")
        opcionMenuPrincipal = int(input("Opción: "))

        # Opciones para Profesores
        if opcionMenuPrincipal == 1:
            while True:
                print("\nSección de PROFESORES")
                print("1. Ingresar nuevo profesor")
                print("2. Eliminar profesor")
                print("3. Mostrar todos los profesores")
                print("4. Volver al menú principal")
                menuProfesor = int(input("Opción: "))

                if menuProfesor == 1:
                    id_profesor = list(generar_ids_unicos(1))[0]
                    print(f"ID profesor: {id_profesor}")
                    nombre = input("Nombre del profesor: ")
                    apellido = input("Apellido del profesor: ")
                    telefono = input("Teléfono del profesor: ")
                    direccion = input("Dirección del profesor: ")
                    
                    nuevo_profesor = {"id": id_profesor, "nombre": nombre, "apellidos": apellido, "telefono": telefono, "direccion": direccion}
                    profesores.append(nuevo_profesor)
                    guardar_profesores(profesores)
                    print("Profesor guardado correctamente.")

                elif menuProfesor == 2:
                    id_profesor = int(input("ID del profesor a eliminar: "))
                    profesores = [p for p in profesores if p['id'] != id_profesor]
                    guardar_profesores(profesores)
                    print("Profesor eliminado correctamente.")
                
                elif menuProfesor == 3:
                    print("\nLista de Profesores:")
                    for profesor in profesores:
                        print(f"ID: {profesor['id']}, Nombre: {profesor['nombre']} {profesor['apellidos']}")
                
                elif menuProfesor == 4:
                    break

                else:
                    print("Opción no válida.")

        # Opciones para Materias
        elif opcionMenuPrincipal == 2:
            while True:
                print("\nSección de MATERIAS")
                print("1. Ingresar nueva materia")
                print("2. Eliminar materia")
                print("3. Mostrar todas las materias")
                print("4. Volver al menú principal")
                menuMateria = int(input("Opción: "))

                if menuMateria == 1:
                    id_materia = list(generar_ids_unicos(1))[0]
                    print(f"ID materia: {id_materia}")
                    nombre = input("Nombre de la materia: ")
                    horaInicio = input("Hora de inicio: ")
                    horaFinal = input("Hora final: ")
                    
                    nueva_materia = {"id": id_materia, "nombre": nombre, "horaInicio": horaInicio, "horaFinal": horaFinal}
                    materias.append(nueva_materia)
                    guardar_materias(materias)
                    print("Materia guardada correctamente.")

                elif menuMateria == 2:
                    id_materia = int(input("ID de la materia a eliminar: "))
                    materias = [m for m in materias if m['id'] != id_materia]
                    guardar_materias(materias)
                    print("Materia eliminada correctamente.")
                
                elif menuMateria == 3:
                    print("\nLista de Materias:")
                    for materia in materias:
                        print(f"ID: {materia['id']}, Nombre: {materia['nombre']}, Hora Inicio: {materia['horaInicio']}, Hora Final: {materia['horaFinal']}")
                
                elif menuMateria == 4:
                    break

                else:
                    print("Opción no válida.")

        # Opciones para Asignación de Materias
        elif opcionMenuPrincipal == 3:
            print("\nAsignación de Materias")
            
            # Mostrar Profesores
            print("\nLista de Profesores:")
            for profesor in profesores:
                print(f"ID: {profesor['id']}, Nombre: {profesor['nombre']} {profesor['apellidos']}")
            
            id_profesor = int(input("Ingrese el ID del profesor: "))

            # Mostrar Materias y Verificar Disponibilidad
            print("\nLista de Materias:")
            for materia in materias:
                asignada = any(h['materia_id'] == materia['id'] for h in horarios)
                estado = "Asignada" if asignada else "Disponible"
                print(f"ID: {materia['id']}, Nombre: {materia['nombre']} ({estado})")
            
            id_materia = int(input("Ingrese el ID de la materia: "))
            
            # Validación de asignación previa
            if any(h['materia_id'] == id_materia for h in horarios):
                print("Esta materia ya tiene un profesor asignado.")
            else:
                horario = {"profesor_id": id_profesor, "materia_id": id_materia}
                horarios.append(horario)
                guardar_horarios(horarios)
                print("Asignación realizada correctamente.")

        # Ver Horarios
        elif opcionMenuPrincipal == 4:
            print("\nHorarios de Materias Asignadas:")
            for horario in horarios:
                profesor = next((p for p in profesores if p['id'] == horario['profesor_id']), None)
                materia = next((m for m in materias if m['id'] == horario['materia_id']), None)
                
                if profesor and materia:
                    print(f"Materia: {materia['nombre']} (ID: {materia['id']}), Hora: {materia['horaInicio']} - {materia['horaFinal']}, Profesor: {profesor['nombre']} {profesor['apellidos']}")

        # Salir
        elif opcionMenuPrincipal == 5:
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida. Regresando al menú principal...")

else:
    print("Usuario o clave incorrectos, adiós")
