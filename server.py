import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from modelo_criticalidad import ejecutar_experimento
from modelo_emocional import simular_con_checkpoints, EMOCIONES

RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
PUERTO = 2529
RUTA_BITACORA = os.path.join(RUTA_PROYECTO, 'bitacora.json')

"""
NeuroMath Salem — Servidor Web del Laboratorio (Puerto 2529)
Salida en consola tipo reporte científico estructurado.
"""
from flask import Flask, render_template, request, jsonify
from modelo_criticalidad import ejecutar_experimento
from datetime import datetime
import json
import os
app = Flask(__name__)
PUERTO = 2529
RUTA_BITACORA = os.path.join(os.path.dirname(__file__), 'bitacora.json')
def imprimir_reporte(parametros, alpha, diagnostico, distribucion, total_nodos):
    """Imprime un reporte estructurado en la consola del servidor."""
    separador_largo = "═" * 60
    separador_corto = "─" * 60
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print()
    print(separador_largo)
    print("  REPORTE DE EXPERIMENTO — NeuroMath Salem")
    print(separador_largo)
    print(f"  Fecha:       {ahora}")
    print(f"  Grid:        {parametros['n_filas']}x{parametros['n_cols']}  |  Agentes: {parametros['n_agentes']}")
    print(f"  Perturbaciones: {parametros['n_perturbaciones']}  |  Magnitud: {parametros['magnitud']}")
    print(f"  γ_som: {parametros['gamma_som']}  |  γ_ef: {parametros['gamma_ef']}  |  σ: {parametros['sigma']}")
    print(separador_corto)
    print(f"  α estimado (MLE): {alpha:.3f}")
    print(f"  Diagnóstico:      {diagnostico}")
    print(f"  Nodos afectados (total): {total_nodos}")
    print(separador_corto)
    print("  Distribución de tamaños (Top 5):")
    for d in distribucion:
        barra = "█" * int(d['porcentaje'])
        print(f"    s={d['tamano']:4d}: {d['cuenta']:4d} ({d['porcentaje']:5.1f}%) {barra}")
    print(separador_largo)
    print()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/ejecutar', methods=['POST'])
def api_ejecutar():
    datos = request.get_json()
    try:
        alpha, tamanos, estado_final, estados_avalanchas = ejecutar_experimento(
            n_perturbaciones=int(datos.get('n_perturbaciones', 200)),
            magnitud=float(datos.get('magnitud', 1.0)),
            gamma_som=float(datos.get('gamma_som', 0.2)),
            gamma_ef=float(datos.get('gamma_ef', 0.5)),
            sigma=float(datos.get('sigma', 0.2)),
            n_filas=int(datos.get('n_filas', 16)),
            n_cols=int(datos.get('n_cols', 16)),
            n_agentes=int(datos.get('n_agentes', 4)),
            n_ciclos_equilibrio=int(datos.get('n_ciclos_equilibrio', 1000)),
            n_pasos_propagacion=int(datos.get('n_pasos_propagacion', 50)),
            umbral=float(datos.get('umbral', 0.05)),
            semilla=42
        )
        from collections import Counter
        contador = Counter(tamanos)
        distribucion = [
            {"tamano": t, "cuenta": c, "porcentaje": round(c / len(tamanos) * 100, 1)}
            for t, c in sorted(contador.items())[:5]
        ]
        if alpha < 1.0:
            diagnostico = " SUPRA-CRÍTICO (Caótico)"
        elif alpha < 2.0:
            diagnostico = "🟢 CRÍTICO (Ley de potencia)" + (" ✨ α ≈ 1.5 cerebral" if 1.3 <= alpha <= 1.7 else "")
        else:
            diagnostico = "🔵 SUB-CRÍTICO (Rígido)"
        # Imprimir reporte estructurado en consola
        imprimir_reporte(datos, alpha, diagnostico, distribucion, sum(tamanos))
        # Guardar en bitácora
        guardar_en_bitacora(datos, alpha, diagnostico, len(tamanos))
        return jsonify({
            "ok": True,
            "alpha": round(alpha, 3),
            "diagnostico": diagnostico,
            "distribucion": distribucion,
            "estado_final": estado_final,
            "estados_avalanchas": estados_avalanchas,
            "n_filas": int(datos.get('n_filas', 16)),
            "n_cols": int(datos.get('n_cols', 16)),
            "total_nodos_afectados": sum(tamanos),
            "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(f"❌ ERROR en /api/ejecutar: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
def guardar_en_bitacora(parametros, alpha, diagnostico, total_perturbaciones):
    registro = {
        "fecha": datetime.now().isoformat(),
        "parametros": parametros,
        "alpha": round(alpha, 3),
        "diagnostico": diagnostico,
        "total_perturbaciones": total_perturbaciones
    }
    bitacora = []
    if os.path.exists(RUTA_BITACORA):
        try:
            with open(RUTA_BITACORA, 'r', encoding='utf-8') as f:
                bitacora = json.load(f)
        except:
            bitacora = []
    bitacora.append(registro)
    with open(RUTA_BITACORA, 'w', encoding='utf-8') as f:
        json.dump(bitacora, f, ensure_ascii=False, indent=2)
@app.route('/api/historial')
def api_historial():
    if not os.path.exists(RUTA_BITACORA):
        return jsonify([])
    try:
        with open(RUTA_BITACORA, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])
@app.route('/api/emocional/ejecutar', methods=['POST'])
def api_emocional_ejecutar():
    """Calcula la dinámica emocional con checkpoints en JSONL."""
    from modelo_emocional import simular_con_checkpoints, EMOCIONES
    datos = request.get_json()
    S = [
        float(datos.get('simp', 0.5)),
        float(datos.get('para', 0.5)),
        float(datos.get('cort', 0.5))
    ]
    e_inicial = [float(datos.get(f'e_{i}', 0.0)) for i in range(7)]
    luz_efectiva = float(datos.get('luz_efectiva', 1.0))
    ciclos = int(datos.get('ciclos', 10000))
    tau_e = float(datos.get('tau_e', 2.0))
    sigma_e = float(datos.get('sigma_e', 0.3))
    intervalo_checkpoint = int(datos.get('intervalo_checkpoint', 1000))
    # Validar límites
    if ciclos > 10000000:
        return jsonify({"ok": False, "error": "Máximo 10 millones de ciclos"}), 400
    if intervalo_checkpoint < 1:
        return jsonify({"ok": False, "error": "Intervalo de checkpoint debe ser >= 1"}), 400
    # Generar nombre de archivo único
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f"simulacion_{timestamp}.jsonl"
    ruta_archivo = os.path.join(RUTA_PROYECTO, 'data', nombre_archivo)
    try:
        resultado = simular_con_checkpoints(
            e_inicial, S, luz_efectiva, ciclos,
            tau_e, sigma_e, intervalo_checkpoint, ruta_archivo
        )
        # Preparar respuesta con las 7 emociones finales
        emociones_resp = [
            {"nombre": emo["nombre"], 
             "valor": resultado["emociones_finales"][emo["nombre"]], 
             "alfa": emo["alfa"]}
            for emo in EMOCIONES
        ]
        return jsonify({
            "ok": True,
            "C_v": resultado["C_v"],
            "delta_sf": resultado["delta_sf"],
            "emociones": emociones_resp,
            "ciclos_simulados": resultado["ciclos_simulados"],
            "checkpoints_guardados": resultado["checkpoints_guardados"],
            "intervalo_checkpoint_real": resultado["intervalo_checkpoint_real"],
            "ruta_archivo": nombre_archivo
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
@app.route('/api/emocional/simulaciones')
def api_emocional_simulaciones():
    """Lista todas las simulaciones guardadas."""
    carpeta_data = os.path.join(RUTA_PROYECTO, 'data')
    if not os.path.exists(carpeta_data):
        return jsonify([])
    simulaciones = []
    for archivo in sorted(os.listdir(carpeta_data)):
        if archivo.endswith('.jsonl'):
            ruta = os.path.join(carpeta_data, archivo)
            tamano = os.path.getsize(ruta)
            # Leer primera línea para obtener metadata
            with open(ruta, 'r', encoding='utf-8') as f:
                primera_linea = f.readline()
                try:
                    metadata = json.loads(primera_linea)
                    simulaciones.append({
                        "nombre": archivo,
                        "fecha": metadata.get('fecha', 'desconocida'),
                        "parametros": metadata.get('parametros', {}),
                        "tamano_kb": round(tamano / 1024, 2)
                    })
                except:
                    simulaciones.append({
                        "nombre": archivo,
                        "fecha": 'desconocida',
                        "parametros": {},
                        "tamano_kb": round(tamano / 1024, 2)
                    })
    return jsonify(simulaciones)
@app.route('/api/emocional/checkpoints/<nombre_archivo>')
def api_emocional_checkpoints(nombre_archivo):
    """Devuelve los checkpoints de una simulación específica."""
    ruta = os.path.join(RUTA_PROYECTO, 'data', nombre_archivo)
    if not os.path.exists(ruta):
        return jsonify({"ok": False, "error": "Archivo no encontrado"}), 404
    checkpoints = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            try:
                dato = json.loads(linea)
                if dato.get('tipo') == 'checkpoint':
                    checkpoints.append(dato)
            except:
                continue
    return jsonify({"ok": True, "checkpoints": checkpoints})

@app.route('/api/bayes/actualizar', methods=['POST'])
def api_bayes_actualizar():
    """Actualiza probabilidades usando el teorema de Bayes."""
    from modelo_bayesiano import actualizar_bayes
    
    datos = request.get_json()
    previas = datos.get('probabilidades_previas', [])
    verosimilitudes = datos.get('verosimilitudes', [])
    
    # Validar
    if not previas or not verosimilitudes:
        return jsonify({"ok": False, "error": "Se requieren probabilidades_previas y verosimilitudes"}), 400
    
    if len(previas) != len(verosimilitudes):
        return jsonify({"ok": False, "error": "Las listas deben tener la misma longitud"}), 400
    
    if len(previas) > 20:
        return jsonify({"ok": False, "error": "Máximo 20 hipótesis"}), 400
    
    try:
        resultado = actualizar_bayes(previas, verosimilitudes)
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/bayes/ejemplo')
def api_bayes_ejemplo():
    """Devuelve el ejemplo clínico pre-cargado."""
    return jsonify({
        "ok": True,
        "ejemplo": {
            "nombre": "Diagnóstico médico con síntoma",
            "hipotesis": ["Enfermedad A (1%)", "Enfermedad B (0.5%)", "Sin enfermedad grave (98.5%)"],
            "probabilidades_previas": [0.01, 0.005, 0.985],
            "verosimilitudes": [0.9, 0.8, 0.1],
            "descripcion": "Paciente presenta síntoma X. ¿Cuál es la probabilidad de cada enfermedad?"
        }
    })


@app.route('/api/inferencia_activa/simular', methods=['POST'])
def api_inferencia_activa_simular():
    from modelo_inferencia_activa import simular_inferencia_activa, ESCENARIOS
    
    datos = request.get_json()
    escenario_key = datos.get('escenario', 'clasico')
    
    if escenario_key in ESCENARIOS:
        config = ESCENARIOS[escenario_key]
        A, B, C, D = config['A'], config['B'], config['C'], config['D']
    else:
        # Permitir matrices personalizadas si se envían
        A = datos.get('A', [[0.9, 0.2], [0.1, 0.8]])
        B = datos.get('B', [[[0.9, 0.1], [0.1, 0.9]], [[0.1, 0.9], [0.9, 0.1]]])
        C = datos.get('C', [0.1, 0.9])
        D = datos.get('D', [0.5, 0.5])
        
    pasos = int(datos.get('pasos', 5))
    estado_inicial = int(datos.get('estado_inicial', 0))
    
    try:
        resultado = simular_inferencia_activa(A, B, C, D, pasos, estado_inicial)
        return jsonify({"ok": True, "resultado": resultado, "escenario": ESCENARIOS.get(escenario_key, {}).get('nombre', 'Personalizado')})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/inferencia_activa/escenarios')
def api_inferencia_activa_escenarios():
    from modelo_inferencia_activa import ESCENARIOS
    # Devolvemos solo nombres y descripciones para la UI
    lista = [{"key": k, "nombre": v["nombre"], "desc": v["desc"]} for k, v in ESCENARIOS.items()]
    return jsonify({"ok": True, "escenarios": lista})


@app.route('/api/entropia/calcular', methods=['POST'])
def api_entropia_calcular():
    """Calcula entropía de Shannon o información mutua."""
    from modelo_entropia import entropia_shannon, informacion_mutua
    
    datos = request.get_json()
    tipo = datos.get('tipo', 'entropia')  # 'entropia' o 'mutua'
    base = int(datos.get('base', 2))
    
    try:
        if tipo == 'entropia':
            distribucion = datos.get('distribucion', [])
            if not distribucion:
                return jsonify({"ok": False, "error": "Se requiere una distribución"}), 400
            
            h = entropia_shannon(distribucion, base)
            h_max = entropia_shannon([1.0/len(distribucion)] * len(distribucion), base)
            
            return jsonify({
                "ok": True,
                "entropia": h,
                "entropia_maxima": h_max,
                "eficiencia": round(h / h_max * 100, 2) if h_max > 0 else 0
            })
        
        elif tipo == 'mutua':
            matriz = datos.get('matriz', [])
            if not matriz or not matriz[0]:
                return jsonify({"ok": False, "error": "Se requiere una matriz conjunta"}), 400
            
            resultado = informacion_mutua(matriz, base)
            
            if "error" in resultado:
                return jsonify({"ok": False, "error": resultado["error"]}), 400
            
            return jsonify({"ok": True, "resultado": resultado})
        
        else:
            return jsonify({"ok": False, "error": "Tipo no válido"}), 400
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/entropia/ejemplo')
def api_entropia_ejemplo():
    """Devuelve el ejemplo clima-paraguas."""
    return jsonify({
        "ok": True,
        "ejemplo": {
            "nombre": "Clima y Paraguas",
            "descripcion": "Relación entre el clima y la decisión de llevar paraguas",
            "matriz": [
                [0.5, 0.05],
                [0.15, 0.1],
                [0.05, 0.15]
            ],
            "filas": ["Soleado", "Nublado", "Lluvioso"],
            "columnas": ["No llevo", "Llevo"]
        }
    })


@app.route('/api/ising/simular', methods=['POST'])
def api_ising_simular():
    """Simula el modelo de Ising con parámetros configurables."""
    from modelo_ising import simular_ising
    
    datos = request.get_json()
    
    try:
        resultado = simular_ising(
            n_filas=int(datos.get('n_filas', 20)),
            n_cols=int(datos.get('n_cols', 20)),
            T=float(datos.get('T', 2.0)),
            J=float(datos.get('J', 1.0)),
            h=float(datos.get('h', 0.0)),
            pasos=int(datos.get('pasos', 500)),
            pasos_equilibrio=int(datos.get('pasos_equilibrio', 200)),
            semilla=int(datos.get('semilla', 42))
        )
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/kuramoto/simular', methods=['POST'])
def api_kuramoto_simular():
    """Simula el modelo de Kuramoto con parámetros configurables."""
    from modelo_kuramoto import simular_kuramoto
    
    datos = request.get_json()
    
    try:
        resultado = simular_kuramoto(
            n_osciladores=int(datos.get('n_osciladores', 50)),
            K=float(datos.get('K', 1.0)),
            tiempo_total=float(datos.get('tiempo_total', 10.0)),
            dt=float(datos.get('dt', 0.01)),
            distribucion=datos.get('distribucion', 'lorentz'),
            ancho=float(datos.get('ancho', 1.0)),
            semilla=int(datos.get('semilla', 42))
        )
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/kuramoto/barrido', methods=['POST'])
def api_kuramoto_barrido():
    """Realiza un barrido de K para mostrar la transición de fase."""
    from modelo_kuramoto import barrido_kuramoto
    
    datos = request.get_json()
    
    try:
        resultados = barrido_kuramoto(
            n_osciladores=int(datos.get('n_osciladores', 50)),
            K_min=float(datos.get('K_min', 0.0)),
            K_max=float(datos.get('K_max', 3.0)),
            K_pasos=int(datos.get('K_pasos', 20)),
            tiempo_total=float(datos.get('tiempo_total', 5.0)),
            dt=float(datos.get('dt', 0.01)),
            distribucion=datos.get('distribucion', 'lorentz'),
            ancho=float(datos.get('ancho', 1.0)),
            semilla=int(datos.get('semilla', 42))
        )
        return jsonify({"ok": True, "resultados": resultados})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/hopfield/simular', methods=['POST'])
def api_hopfield_simular():
    """Simula la Red de Hopfield con parámetros configurables."""
    from modelo_hopfield import simular_hopfield
    
    datos = request.get_json()
    
    try:
        resultado = simular_hopfield(
            n_neuronas=int(datos.get('n_neuronas', 100)),
            n_patrones=int(datos.get('n_patrones', 3)),
            probabilidad_ruido=float(datos.get('probabilidad_ruido', 0.2)),
            pasos_maximos=int(datos.get('pasos_maximos', 500)),
            semilla=int(datos.get('semilla', 42))
        )
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/potencial_accion/simular', methods=['POST'])
def api_potencial_accion_simular():
    """Simula el potencial de acción (FitzHugh-Nagumo)."""
    from modelo_potencial_accion import simular_potencial_accion
    
    datos = request.get_json()
    
    try:
        resultado = simular_potencial_accion(
            I_ext=float(datos.get('I_ext', 1.0)),
            tiempo_total=float(datos.get('tiempo_total', 50.0)),
            dt=0.1,
            epsilon=float(datos.get('epsilon', 0.08)),
            a=float(datos.get('a', 0.7)),
            b=float(datos.get('b', 0.8)),
            V0=float(datos.get('V0', -1.0)),
            W0=float(datos.get('W0', -1.0))
        )
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/landau/calcular', methods=['POST'])
def api_landau_calcular():
    """Calcula el potencial de Landau-Ginzburg."""
    from modelo_landau import calcular_potencial_landau
    
    datos = request.get_json()
    try:
        a = float(datos.get('a', 1.0))
        b = float(datos.get('b', 1.0))
        resultado = calcular_potencial_landau(a, b)
        return jsonify({
            "ok": True, 
            "resultado": resultado, 
            "parametros": {"a": a, "b": b}
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
if __name__ == '__main__':
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   🧠 NeuroMath Salem — Laboratorio de Criticalidad   ║")
    print("║   Puerto: 2529                                       ║")
    print("║   http://localhost:2529                              ║")
    print("══════════════════════════════════════════════════════╝")
    print()
    app.run(host='0.0.0.0', port=PUERTO, debug=False)
