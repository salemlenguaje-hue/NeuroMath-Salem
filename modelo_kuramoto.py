#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 3: Kuramoto (Sincronización de Osciladores)
Simula N osciladores de fase con acoplamiento sinusoidal.
Calcula el parámetro de orden r en función del acoplamiento K.
"""
import math
import random


def generar_frecuencias(n_osciladores, distribucion='lorentz', ancho=1.0, semilla=42):
    """
    Genera frecuencias naturales ω_i desde una distribución.
    
    Args:
        n_osciladores: cantidad de osciladores
        distribucion: 'lorentz' (Cauchy) o 'uniforme'
        ancho: ancho de la distribución (γ en Lorentz)
        semilla: para reproducibilidad
    """
    random.seed(semilla)
    
    if distribucion == 'lorentz':
        # Distribución de Lorentz (Cauchy): g(ω) = γ/(π(ω² + γ²))
        frecuencias = []
        for _ in range(n_osciladores):
            u = random.uniform(-0.99, 0.99)
            omega = ancho * math.tan(math.pi * u / 2)
            frecuencias.append(omega)
    else:
        # Distribución uniforme [-ancho, ancho]
        frecuencias = [random.uniform(-ancho, ancho) for _ in range(n_osciladores)]
    
    return frecuencias


def calcular_parametro_orden(fases):
    """
    Calcula el parámetro de orden r y la fase media ψ.
    
    r * e^(iψ) = (1/N) Σ e^(iθ_j)
    
    r = 0: completamente desincronizado
    r = 1: completamente sincronizado
    """
    n = len(fases)
    suma_cos = sum(math.cos(theta) for theta in fases)
    suma_sin = sum(math.sin(theta) for theta in fases)
    
    r = math.sqrt((suma_cos/n)**2 + (suma_sin/n)**2)
    psi = math.atan2(suma_sin, suma_cos)
    
    return r, psi


def paso_kuramoto(fases, frecuencias, K, dt=0.01):
    """
    Un paso de integración (Euler) de la ecuación de Kuramoto.
    
    dθ_i/dt = ω_i + (K/N) Σ sin(θ_j - θ_i)
    """
    n = len(fases)
    nuevas_fases = []
    
    for i in range(n):
        suma_acoplamiento = sum(math.sin(fases[j] - fases[i]) for j in range(n))
        dtheta = frecuencias[i] + (K / n) * suma_acoplamiento
        nueva_fase = fases[i] + dtheta * dt
        nuevas_fases.append(nueva_fase % (2 * math.pi))  # Normalizar a [0, 2π]
    
    return nuevas_fases


def simular_kuramoto(n_osciladores=50, K=1.0, tiempo_total=10.0, dt=0.01,
                     distribucion='lorentz', ancho=1.0, semilla=42):
    """
    Simula la evolución de N osciladores de Kuramoto.
    
    Args:
        n_osciladores: cantidad de osciladores
        K: fuerza de acoplamiento
        tiempo_total: tiempo de simulación
        dt: paso de integración
        distribucion: tipo de distribución de frecuencias
        ancho: ancho de la distribución
        semilla: para reproducibilidad
    
    Returns:
        Diccionario con historial de r, fases finales, y diagnóstico
    """
    frecuencias = generar_frecuencias(n_osciladores, distribucion, ancho, semilla)
    random.seed(semilla + 1)
    fases = [random.uniform(0, 2 * math.pi) for _ in range(n_osciladores)]
    
    # K_c teórico para distribución de Lorentz: K_c = 2γ
    K_c_teorico = 2.0 * ancho if distribucion == 'lorentz' else None
    
    historial_r = []
    historial_psi = []
    pasos = int(tiempo_total / dt)
    pasos_guardar = max(1, pasos // 100)  # Guardar cada 1% de los pasos
    
    for paso in range(pasos):
        fases = paso_kuramoto(fases, frecuencias, K, dt)
        
        if paso % pasos_guardar == 0:
            r, psi = calcular_parametro_orden(fases)
            historial_r.append(round(r, 4))
            historial_psi.append(round(psi, 4))
    
    # Resultado final
    r_final, psi_final = calcular_parametro_orden(fases)
    
    # Diagnóstico de sincronización
    if r_final < 0.3:
        estado = "Desincronizado (caos)"
        color = "rojo"
    elif r_final < 0.7:
        estado = "Parcialmente sincronizado"
        color = "amarillo"
    else:
        estado = "Sincronizado (orden)"
        color = "verde"
    
    return {
        "parametros": {
            "n_osciladores": n_osciladores,
            "K": K,
            "tiempo_total": tiempo_total,
            "dt": dt,
            "distribucion": distribucion,
            "ancho": ancho
        },
        "resultados": {
            "r_final": round(r_final, 4),
            "psi_final": round(psi_final, 4),
            "K_c_teorico": round(K_c_teorico, 4) if K_c_teorico else None,
            "estado": estado,
            "color": color
        },
        "historial": {
            "r": historial_r,
            "psi": historial_psi
        },
        "fases_finales": [round(f, 4) for f in fases]
    }


def barrido_kuramoto(n_osciladores=50, K_min=0.0, K_max=3.0, K_pasos=20,
                     tiempo_total=10.0, dt=0.01, distribucion='lorentz',
                     ancho=1.0, semilla=42):
    """
    Realiza un barrido de K para encontrar la transición de fase.
    
    Returns:
        Lista de (K, r_final) para graficar la curva de transición
    """
    resultados = []
    
    for i in range(K_pasos):
        K = K_min + (K_max - K_min) * i / (K_pasos - 1)
        sim = simular_kuramoto(n_osciladores, K, tiempo_total, dt,
                               distribucion, ancho, semilla)
        resultados.append({
            "K": round(K, 3),
            "r": sim["resultados"]["r_final"]
        })
    
    return resultados


if __name__ == "__main__":
    print("=== Modelo de Kuramoto ===\n")
    
    print("Simulación con K=0.5 (desincronizado):")
    r1 = simular_kuramoto(K=0.5, tiempo_total=5.0)
    print(f"  r_final: {r1['resultados']['r_final']}")
    print(f"  Estado: {r1['resultados']['estado']}")
    
    print("\nSimulación con K=2.5 (sincronizado):")
    r2 = simular_kuramoto(K=2.5, tiempo_total=5.0)
    print(f"  r_final: {r2['resultados']['r_final']}")
    print(f"  Estado: {r2['resultados']['estado']}")
