from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('mysql+mariadb://root:root@localhost:3306/recetario', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    ingredientes = Column(String(500), nullable=False)
    pasos = Column(String(1000), nullable=False)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)


def agregar_receta(nombre, ingredientes, pasos):
    with Session() as session:
        nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
        session.add(nueva_receta)
        try:
            session.commit()
            print("Receta agregada con éxito.")
        except Exception as e:
            session.rollback()
            print(f"Error al agregar la receta: {e}")

def actualizar_receta(nombre, nuevos_ingredientes, nuevos_pasos):
    with Session() as session:
        receta = session.query(Receta).filter_by(nombre=nombre).first()
        if receta:
            receta.ingredientes = nuevos_ingredientes
            receta.pasos = nuevos_pasos
            session.commit()
            print("Receta actualizada con éxito.")
        else:
            print("Error: No se encontró una receta con ese nombre.")

def eliminar_receta(nombre):
    with Session() as session:
        receta = session.query(Receta).filter_by(nombre=nombre).first()
        if receta:
            session.delete(receta)
            session.commit()
            print("Receta eliminada con éxito.")
        else:
            print("Error: No se encontró una receta con ese nombre.")

def ver_recetas():
    with Session() as session:
        recetas = session.query(Receta).all()
        if recetas:
            print("Listado de recetas:")
            for receta in recetas:
                print(f"- {receta.nombre}")
        else:
            print("No hay recetas disponibles.")

def buscar_receta(nombre):
    with Session() as session:
        receta = session.query(Receta).filter_by(nombre=nombre).first()
        if receta:
            print(f"\nIngredientes:\n{receta.ingredientes}\n")
            print(f"Pasos:\n{receta.pasos}\n")
        else:
            print("Error: No se encontró una receta con ese nombre.")


def menu():
    while True:
        print("\n--- Libro de Recetas ---")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre de la receta: ")
            ingredientes = input("Ingredientes (separados por comas): ")
            pasos = input("Pasos: ")
            agregar_receta(nombre, ingredientes, pasos)
        elif opcion == '2':
            nombre = input("Nombre de la receta a actualizar: ")
            nuevos_ingredientes = input("Nuevos ingredientes (separados por comas): ")
            nuevos_pasos = input("Nuevos pasos: ")
            actualizar_receta(nombre, nuevos_ingredientes, nuevos_pasos)
        elif opcion == '3':
            nombre = input("Nombre de la receta a eliminar: ")
            eliminar_receta(nombre)
        elif opcion == '4':
            ver_recetas()
        elif opcion == '5':
            nombre = input("Nombre de la receta a buscar: ")
            buscar_receta(nombre)
        elif opcion == '6':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == '__main__':
    menu()