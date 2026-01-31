
import time
import random

# Amortización francesa
def calcular_tabla_amortizacion(monto, tasa_anual, meses):
    
    tabla = []
    saldo = monto
    # Convertimos tasa anual a mensual 
    tasa_mensual = (tasa_anual / 100) / 12

    # Si la tasa es 0 es una división simple
    if tasa_mensual == 0:
        cuota = monto / meses
    else:
        #sistema francés
        numerador = saldo * tasa_mensual * ((1 + tasa_mensual) ** meses)
        denominador = ((1 + tasa_mensual) ** meses) - 1
        cuota = numerador / denominador if denominador != 0 else 0

    for mes in range(1, meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo -= capital
        
        # Guardamos la fila del mes
        tabla.append({
            "mes": mes,
            "cuota": round(cuota, 2),
            "interes": round(interes, 2),
            "capital": round(capital, 2),
            "saldo": round(saldo, 2) if saldo > 0 else 0
        })
    
    return tabla

# Auditoria de riesgo simulada
def auditoria_riesgo_background():

    print("Auditoria de riesgo en segundo plano iniciada")
    
    # Simular tiempo de espera aleatorio 
    tiempo_espera = random.uniform(1, 3)
    time.sleep(tiempo_espera)

    # Simular probabilidad de fallo del 10%
    if random.random() < 0.1:
        print(f"La simulacion de la auditoria fallo en: {tiempo_espera:.2f}segundos")
        # Aquí normalmente registraríamos el error en un log real
        raise Exception("Error simulado en el servicio de scoring")
    
    print(f"auditoria completada en: {tiempo_espera:.2f}segundos")