
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# La URL de la base de datos en SQLite
URL_BASE_DATOS = "sqlite:///./creditsim.db"


motor = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False}) #evitamos errores con FastAPI

# Clase sessionlocal para que se haga una nueva sesion cada que interactue la base de datos.
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# clase que heredarán nuestros modelos o las tablas.
Base = declarative_base()

# Función para obtener la sesión de la base de datos en cada petición
def obtener_db():
    db = SesionLocal()
    try:
        yield db # Entrega la sesión
    finally:
        db.close() # Se asegura de cerrarla al terminar, pase lo que pase