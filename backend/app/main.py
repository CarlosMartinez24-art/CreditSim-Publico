from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List           
from datetime import datetime      

from .base_datos import motor, Base, obtener_db
from .modelos import Simulacion
from .logica import calcular_tabla_amortizacion, auditoria_riesgo_background

Base.metadata.create_all(bind=motor)

app = FastAPI(title="CreditSim API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# recibimos lo que el usuario envia
class DatosSimulacion(BaseModel):
    monto: float
    tasa_anual: float
    plazo_meses: int

# mostrar los datos
class SimulacionGuardada(BaseModel):
    id: int
    monto_prestamo: float
    tasa_interes_anual: float
    plazo_meses: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True # Esto permite leer directo de la Base de Datos

# endpoint

@app.post("/simulate")
async def simular_credito(
    datos: DatosSimulacion, 
    tareas_fondo: BackgroundTasks, 
    db: Session = Depends(obtener_db)
):
    
    tareas_fondo.add_task(auditoria_riesgo_background)

    tabla_resultado = calcular_tabla_amortizacion(
        datos.monto, 
        datos.tasa_anual, 
        datos.plazo_meses
    )

    nueva_simulacion = Simulacion(
        monto_prestamo=datos.monto,
        tasa_interes_anual=datos.tasa_anual,
        plazo_meses=datos.plazo_meses
    )
    db.add(nueva_simulacion)
    db.commit()
    db.refresh(nueva_simulacion)

    return {
        "id_simulacion": nueva_simulacion.id,
        "tabla_amortizacion": tabla_resultado
    }

# un endpoint para ver la base de datos
@app.get("/simulaciones", response_model=List[SimulacionGuardada])
def ver_historial(db: Session = Depends(obtener_db)):
    """
    Obtiene todas las simulaciones guardadas en la base de datos.
    """
    # Consulta la tabla Simulacion y trae todos los registros
    historial = db.query(Simulacion).all()
    return historial