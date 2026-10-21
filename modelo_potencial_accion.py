#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 5: Potencial de Acción (FitzHugh-Nagumo)
Simplificación didáctica del modelo Hodgkin-Huxley.
Simula el voltaje de membrana (V) y la variable de recuperación (W) 
ante una corriente externa (I_ext).
"""
import math


def paso_fhn(V, W, I_ext, epsilon=0.08, a=0.7, b=0.8, dt=0.1):
    """
    Un paso de integración (Euler) de las ecuaciones de FitzHugh-Nagumo.
    
    dV/dt = V - V^3/3 - W + I_ext
    dW/dt = epsilon * (V + a - b*W)
    """
    # Ecuación del voltaje (rápida)
    dV = (V - (V**3) / 3.0 - W + I_ext) * dt
    
    # Ecuación de recuperación (lenta, representa canales de potasio)
    dW = epsilon * (V + a - b * W) * dt
    
    return V + dV, W + dW


def simular_potencial_accion(I_ext=1.0, tiempo_total=50.0, dt=0.1, 
                             epsilon=0.08, a=0.7, b=0.8, V0=-1.0, W0=-1.0):
    """
    Simula la evolución del potencial de membrana.
    
    Args:
        I_ext: Corriente externa aplicada (el estímulo)
        tiempo_total: Duración de la simulación
        dt: Paso de tiempo
        epsilon, a, b: Parámetros del modelo
        V0, W0: Condiciones iniciales (estado de reposo típico: V≈-1, W≈-1)
    
    Returns:
        Diccionario con historial de V, W y análisis del spike
    """
    V = V0
    W = W0
    
    historial_t = []
    historial_V = []
    historial_W = []
    
    pasos = int(tiempo_total / dt)
    
    # Para detectar si hubo un spike (umbral típico V > 0)
    max_V = V
    hubo_spike = False
    
    for i in range(pasos):
        t = i * dt
        historial_t.append(round(t, 2))
        historial_V.append(round(V, 4))
        historial_W.append(round(W, 4))
        
        if V > max_V:
            max_V = V
            
        if V > 0.5:  # Umbral de spike
            hubo_spike = True
            
        V, W = paso_fhn(V, W, I_ext, epsilon, a, b, dt)
    
    # Diagnóstico
    if hubo_spike and max_V > 1.0:
        estado = "Disparo de Potencial de Acción (Spike)"
        color = "verde"
    elif max_V > -0.5:
        estado = "Subumbral (Respuesta pasiva)"
        color = "amarillo"
    else:
        estado = "Reposo / Hiperpolarización"
        color = "azul"
        
    return {
        "parametros": {
            "I_ext": I_ext,
            "tiempo_total": tiempo_total,
            "epsilon": epsilon,
            "a": a,
            "b": b
        },
        "resultados": {
            "max_V": round(max_V, 4),
            "estado": estado,
            "color": color
        },
        "historial": {
            "t": historial_t,
            "V": historial_V,
            "W": historial_W
        }
    }
