#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 2: Dinámica Emocional y Valencia (ADR-016)
Con soporte para simulaciones largas (hasta 10M ciclos) y checkpoints en JSONL.
"""
import math
import os
import json
from datetime import datetime

# Constantes por defecto del ADR-016
TAU_E = 2.0       # Constante de tiempo emocional (segundos/ciclos)
SIGMA_E = 0.3     # Amplitud de activación
SIGMA_P = 0.3     # Ancho del prototipo gaussiano

# Definición de las 7 emociones: (nombre, peso alfa, prototipo [simp, para, cort])
EMOCIONES = [
    {"nombre": "Curiosidad",    "alfa":  0.30, "prototipo": [0.8, 0.2, 0.3]},
    {"nombre": "Placer",        "alfa":  0.25, "prototipo": [0.9, 0.4, 0.1]},
    {"nombre": "Satisfacción",  "alfa":  0.20, "prototipo": [0.7, 0.6, 0.2]},
    {"nombre": "Empatía",       "alfa":  0.15, "prototipo": [0.6, 0.7, 0.3]},
    {"nombre": "Moderación",    "alfa":  0.10, "prototipo": [0.5, 0.5, 0.4]},
    {"nombre": "Prudencia",     "alfa": -0.20, "prototipo": [0.3, 0.4, 0.6]},
    {"nombre": "Frustración",   "alfa": -0.30, "prototipo": [0.2, 0.3, 0.9]},
]

def activacion_gaussiana(S, prototipo, sigma_p):
    """Calcula a_i(S) = exp(-||S - mu_i||^2 / (2 * sigma_p^2))"""
    suma_cuadrados = sum((s - p) ** 2 for s, p in zip(S, prototipo))
    return math.exp(-suma_cuadrados / (2 * sigma_p ** 2))

def paso_emocional(e_actual, S, tau_e, sigma_e, dt=1.0):
    """Integrador con fuga: de_i/dt = -e_i/tau_e + sigma_e * a_i(S)"""
    e_nuevo = []
    for i, emo in enumerate(EMOCIONES):
        a_i = activacion_gaussiana(S, emo["prototipo"], SIGMA_P)
        derivada = -(e_actual[i] / tau_e) + (sigma_e * a_i)
        nuevo_valor = max(0.0, e_actual[i] + dt * derivada)
        e_nuevo.append(round(nuevo_valor, 4))
    return e_nuevo

def calcular_valencia(e):
    """C_v = tanh(sum(alfa_i * e_i))"""
    suma_ponderada = sum(emo["alfa"] * e[i] for i, emo in enumerate(EMOCIONES))
    return round(math.tanh(suma_ponderada), 4)

def calcular_delta_sf(luz_efectiva, C_v):
    """ΔSf = LUZ_efectiva * C_v"""
    return round(luz_efectiva * C_v, 4)


def simular_con_checkpoints(e_inicial, S, luz_efectiva, ciclos, 
                            tau_e=TAU_E, sigma_e=SIGMA_E,
                            intervalo_checkpoint=1000,
                            ruta_archivo=None):
    """
    Simula la evolución emocional con checkpoints periódicos en JSONL.
    
    Args:
        e_inicial: lista de 7 emociones iniciales
        S: vector fisiológico [simp, para, cort]
        luz_efectiva: multiplicador de LUZ
        ciclos: total de ciclos a simular
        tau_e: constante de tiempo emocional
        sigma_e: amplitud de activación
        intervalo_checkpoint: cada cuántos ciclos guardar snapshot
        ruta_archivo: dónde guardar el JSONL (si es None, no guarda)
    
    Returns:
        dict con resultado final, metadata y ruta del archivo
    """
    # Validar límite de checkpoints
    num_checkpoints = ciclos // intervalo_checkpoint
    MAX_CHECKPOINTS = 10000
    if num_checkpoints > MAX_CHECKPOINTS:
        intervalo_checkpoint = max(1, ciclos // MAX_CHECKPOINTS)
        num_checkpoints = ciclos // intervalo_checkpoint
    
    e_actual = list(e_inicial)
    checkpoint_actual = 0
    archivo_abierto = None
    
    if ruta_archivo:
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        archivo_abierto = open(ruta_archivo, 'w', encoding='utf-8')
        # Escribir metadatos como primera línea (comentario JSON)
        metadata = {
            "tipo": "metadata",
            "fecha": datetime.now().isoformat(),
            "parametros": {
                "S": S,
                "luz_efectiva": luz_efectiva,
                "ciclos": ciclos,
                "tau_e": tau_e,
                "sigma_e": sigma_e,
                "intervalo_checkpoint": intervalo_checkpoint
            },
            "emociones_iniciales": dict(zip(
                [emo["nombre"] for emo in EMOCIONES], e_inicial
            ))
        }
        archivo_abierto.write(json.dumps(metadata, ensure_ascii=False) + '\n')
    
    # Simulación por lotes (chunks de 100K para no bloquear)
    TAMANO_LOTE = 100000
    ciclo = 0
    
    while ciclo < ciclos:
        lote_fin = min(ciclo + TAMANO_LOTE, ciclos)
        
        for _ in range(ciclo, lote_fin):
            e_actual = paso_emocional(e_actual, S, tau_e, sigma_e, dt=1.0)
            ciclo += 1
            
            # Guardar checkpoint si corresponde
            if archivo_abierto and ciclo % intervalo_checkpoint == 0:
                C_v = calcular_valencia(e_actual)
                delta_sf = calcular_delta_sf(luz_efectiva, C_v)
                checkpoint = {
                    "tipo": "checkpoint",
                    "ciclo": ciclo,
                    "emociones": dict(zip(
                        [emo["nombre"] for emo in EMOCIONES], e_actual
                    )),
                    "C_v": C_v,
                    "delta_sf": delta_sf
                }
                archivo_abierto.write(json.dumps(checkpoint, ensure_ascii=False) + '\n')
                checkpoint_actual += 1
    
    # Cerrar archivo si estaba abierto
    if archivo_abierto:
        archivo_abierto.close()
    
    # Resultado final
    C_v_final = calcular_valencia(e_actual)
    delta_sf_final = calcular_delta_sf(luz_efectiva, C_v_final)
    
    return {
        "emociones_finales": dict(zip(
            [emo["nombre"] for emo in EMOCIONES], e_actual
        )),
        "C_v": C_v_final,
        "delta_sf": delta_sf_final,
        "ciclos_simulados": ciclo,
        "checkpoints_guardados": checkpoint_actual,
        "intervalo_checkpoint_real": intervalo_checkpoint,
        "ruta_archivo": ruta_archivo
    }
