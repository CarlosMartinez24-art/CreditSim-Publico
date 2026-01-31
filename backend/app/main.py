
from fastapi import FastAPI, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .base_datos import motor, Base, obtener_db
from .modelos import Simulacion
from .logica import calcular_tabla_amortizacion, auditoria_riesgo_background


Base.metadata.create_all(bind=motor)

# Inicializar  FastAPI
app = FastAPI(title="CreditSim API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexiones desde cualquier origen 
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos 
    allow_headers=["*"],
)


class DatosSimulacion(BaseModel):
    monto: float
    tasa_anual: float
    plazo_meses: int

#endpoints

@app.post("/simulate")
async def simular_credito(
    datos: DatosSimulacion, 
    tareas_fondo: BackgroundTasks, # Tareas en segundo plano
    db: Session = Depends(obtener_db)
):
   
    
    # la auditoria empieza despues de responder la tabla
    tareas_fondo.add_task(auditoria_riesgo_background)

    
    tabla_resultado = calcular_tabla_amortizacion(
        datos.monto, 
        datos.tasa_anual, 
        datos.plazo_meses
    )

    # persistencia, guardamos en la base de datos
    nueva_simulacion = Simulacion(
        monto_prestamo=datos.monto,
        tasa_interes_anual=datos.tasa_anual,
        plazo_meses=datos.plazo_meses
    )
    db.add(nueva_simulacion)
    db.commit() 
    db.refresh(nueva_simulacion) #ID generado

    
    return {
        "id_simulacion": nueva_simulacion.id,
        "tabla_amortizacion": tabla_resultado
    }