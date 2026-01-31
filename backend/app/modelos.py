
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .base_datos import Base

# las tabla simuladas de guardan aqui en la clase Simulacion
class Simulacion(Base):
    __tablename__ = "simulaciones"

    
    id = Column(Integer, primary_key=True, index=True) # ID 
    monto_prestamo = Column(Float, nullable=False)     # Monto solicitado
    tasa_interes_anual = Column(Float, nullable=False) # Tasa anual
    plazo_meses = Column(Integer, nullable=False)      # Plazo
    # Guardamos la fecha y hora en que se hizo la simulación
    fecha_creacion = Column(DateTime, default=datetime.utcnow)