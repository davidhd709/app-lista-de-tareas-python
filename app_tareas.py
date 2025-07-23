# Todas las importaciones al principio del archivo
import datetime
import json

class Tarea:
    """Representa una sola tarea en nuestra lista de quehaceres."""
    def __init__(self, descripcion, completada=False, fecha_creacion=None):
        self.descripcion = descripcion
        self.completada = completada
        
        if fecha_creacion is None:
            self.fecha_creacion = datetime.datetime.now()
        else:
            self.fecha_creacion = datetime.datetime.fromisoformat(fecha_creacion)

    def marcar_como_completada(self):
        """Cambia el estado de la tarea a completada."""
        self.completada = True

    def __str__(self):
        """Devuelve una representación en texto de la tarea."""
        estado = "✅" if self.completada else "❌"
        fecha_formateada = self.fecha_creacion.strftime("%Y-%m-%d %H:%M")
        return f"[{estado}] {self.descripcion} (Creada: {fecha_formateada})"

class GestorTareas:
    """Gestiona una colección de tareas, incluyendo guardado y carga."""
    def __init__(self, nombre_archivo):
        self.tareas = []
        self.nombre_archivo = nombre_archivo

    def agregar_tarea(self, descripcion):
        nueva_tarea = Tarea(descripcion)
        self.tareas.append(nueva_tarea)
        print(f"Tarea '{descripcion}' agregada.")

    def mostrar_tareas(self, mostrar_solo_pendientes=False):
        print("\n--- LISTA DE TAREAS ---")
        
        tareas_a_mostrar = self.tareas
        if mostrar_solo_pendientes:
            tareas_a_mostrar = [t for t in self.tareas if not t.completada]

        if not tareas_a_mostrar:
            if mostrar_solo_pendientes:
                print("¡Felicidades! No hay tareas pendientes.")
            else:
                print("No hay tareas en la lista.")
            return

        for i, tarea in enumerate(tareas_a_mostrar, start=1):
            print(f"{i}. {tarea}")

    def marcar_completada(self):
        if not self.tareas:
            print("No hay tareas para marcar. ¡Agrega una primero!")
            return

        # Para evitar confusión, siempre mostramos la lista completa antes de modificarla
        self.mostrar_tareas(mostrar_solo_pendientes=False) 
        try:
            num = int(input("Ingresa el número de la tarea a marcar como completada: "))
            if 1 <= num <= len(self.tareas):
                self.tareas[num - 1].marcar_como_completada()
                print("¡Tarea marcada como completada!")
            else:
                print("Número de tarea no válido.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")

    def eliminar_tarea(self):
        if not self.tareas:
            print("No hay tareas para eliminar.")
            return

        # Siempre mostramos la lista completa para la eliminación
        self.mostrar_tareas(mostrar_solo_pendientes=False) 
        try:
            num = int(input("Ingresa el número de la tarea a eliminar: "))
            if 1 <= num <= len(self.tareas):
                tarea_eliminada = self.tareas.pop(num - 1)
                print(f"Tarea '{tarea_eliminada.descripcion}' eliminada.")
            else:
                print("Número de tarea no válido.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")
            
    # --- MÉTODOS DE PERSISTENCIA ---

    def guardar_en_archivo(self):
        """Convierte las tareas a un formato simple (diccionario) y las guarda en JSON."""
        lista_para_json = []
        for tarea in self.tareas:
            lista_para_json.append({
                "descripcion": tarea.descripcion,
                "completada": tarea.completada,
                "fecha_creacion": tarea.fecha_creacion.isoformat()
            })
        
        try:
            with open(self.nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(lista_para_json, f, indent=4, ensure_ascii=False)
            print("Tareas guardadas con éxito.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    def cargar_desde_archivo(self):
        """Carga las tareas desde un archivo JSON y las convierte en objetos Tarea."""
        try:
            with open(self.nombre_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.tareas = [Tarea(**dato) for dato in datos]
            print("Tareas cargadas con éxito.")
        except FileNotFoundError:
            print("Archivo de tareas no encontrado. Empezando con una lista vacía.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar o leer el archivo: {e}")

# --- FUNCIÓN PRINCIPAL DEL PROGRAMA ---
# Nota: Esta función ya no está indentada dentro de la clase
def main():
    nombre_archivo = "mis_tareas.json"
    gestor = GestorTareas(nombre_archivo)
    
    gestor.cargar_desde_archivo()

    while True:
        print("\n===== APP DE LISTA DE TAREAS =====")
        print("1. Mostrar todas las tareas")
        print("2. Mostrar solo tareas pendientes")
        print("3. Agregar nueva tarea")
        print("4. Marcar tarea como completada")
        print("5. Eliminar tarea")
        print("6. Guardar y Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            gestor.mostrar_tareas()
        elif opcion == "2":
            gestor.mostrar_tareas(mostrar_solo_pendientes=True)
        elif opcion == "3":
            descripcion = input("Escribe la descripción de la nueva tarea: ")
            gestor.agregar_tarea(descripcion)
        elif opcion == "4":
            gestor.marcar_completada()
        elif opcion == "5":
            gestor.eliminar_tarea()
        elif opcion == "6":
            gestor.guardar_en_archivo()
            break
        else:
            print("Opción no válida.")

# Este bloque asegura que el programa solo se ejecute cuando corres este archivo directamente
if __name__ == "__main__":
    main()