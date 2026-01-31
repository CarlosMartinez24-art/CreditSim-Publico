
import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  
  
  //Estado del formulario (Monto, Tasa, Plazo)
  //buscamos datos guardados antes (persistencia)
  const [formulario, setFormulario] = useState(() => {
    const guardado = localStorage.getItem("datosCredito");
    return guardado ? JSON.parse(guardado) : {
      monto: 50000, //datos de muestra 
      tasa_anual: 12,
      plazo_meses: 12
    };
  });

  // guardar la tabla de resultados que viene del backend
  const [tablaResultado, setTablaResultado] = useState(null);
  
  // saber si está cargando
  const [cargando, setCargando] = useState(false);
-
  //recordar valores puestos por ultima vez en el formulario
  useEffect(() => {
    localStorage.setItem("datosCredito", JSON.stringify(formulario));
  }, [formulario]);

  // nuevos cambios 
  const manejarCambioInput = (e) => {
    const { name, value } = e.target;
    
    // valores a numeros
    const valorNumerico = parseFloat(value);

    // si el monto cambia la tabla desaparece
    if (name === "monto") {
      setTablaResultado(null);
    }

    // actualizamos el formulario
    setFormulario({
      ...formulario,
      [name]: valorNumerico
    });
  };

  // le damos los datos al backend
  const calcularCredito = async (e) => {
    e.preventDefault(); // evitamos un refresh de la página
    setCargando(true);
    
    try {
      // Hacemos la petición post a fastAPI
      const respuesta = await axios.post('http://127.0.0.1:8000/simulate', {
        monto: formulario.monto,
        tasa_anual: formulario.tasa_anual,
        plazo_meses: formulario.plazo_meses
      });

      // Guardamos la tabla que nos devolvió el servidor
      setTablaResultado(respuesta.data.tabla_amortizacion);
    
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      alert("Revisar que el servidor backend esté encendido.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="contenedor-principal">
      <h1>Simulador de Crédito (CreditSim)</h1>
      
      
      <form onSubmit={calcularCredito} className="formulario">
        <div className="grupo-input">
          <label>Monto del Préstamo ($)</label>
          <input 
            type="number" 
            name="monto"
            value={formulario.monto}
            onChange={manejarCambioInput}
            required
          />
        </div>

        <div className="grupo-input">
          <label>Tasa Anual (%)</label>
          <input 
            type="number" 
            name="tasa_anual"
            value={formulario.tasa_anual}
            onChange={manejarCambioInput}
            step="0.1"
            required
          />
        </div>

        <div className="grupo-input">
          <label>Plazo (Meses)</label>
          <input 
            type="number" 
            name="plazo_meses"
            value={formulario.plazo_meses}
            onChange={manejarCambioInput}
            required
          />
        </div>

        <button type="submit" disabled={cargando} className="boton-calcular">
          {cargando ? "Calculando..." : "Calcular Tabla"}
        </button>
      </form>

      <hr />

      
      {tablaResultado ? (
        <div className="tabla-contenedor">
          <h3> Tabla de Amortización</h3>
          <table>
            <thead>
              <tr>
                <th>Mes</th>
                <th>Cuota</th>
                <th>Interés</th>
                <th>Capital</th>
                <th>Saldo</th>
              </tr>
            </thead>
            <tbody>
              {tablaResultado.map((fila) => (
                <tr key={fila.mes}>
                  <td>{fila.mes}</td>
                  <td>${fila.cuota}</td>
                  <td>${fila.interes}</td>
                  <td>${fila.capital}</td>
                  <td>${fila.saldo}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="mensaje-vacio">
          {cargando ? "" : "Ingresa los datos y presiona Calcular para ver la tabla."}
        </p>
      )}
    </div>
  );
}

export default App;