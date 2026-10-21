#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 6: Landau-Ginzburg (Transiciones de Fase)
Calcula el potencial de energía libre F(ψ) = aψ² + bψ⁴.
Herramienta de estudio teórico para entender la ruptura espontánea de simetría.
"""
import numpy as np


def calcular_potencial_landau(a, b, psi_min=-2.0, psi_max=2.0, puntos=200):
    """
    Calcula el potencial de Landau para un rango del parámetro de orden ψ.
    
    Args:
        a: Parámetro de control (proporcional a T - T_c).
        b: Coeficiente positivo que estabiliza el potencial.
        psi_min, psi_max: Rango del parámetro de orden.
        puntos: Resolución del gráfico.
    
    Returns:
        Diccionario con los datos para graficar y el análisis del estado.
    """
    psi = np.linspace(psi_min, psi_max, puntos)
    F = a * (psi**2) + b * (psi**4)
    
    # Análisis del estado de equilibrio
    if a < 0:
        # Fase ordenada: mínimo en ψ ≠ 0 (doble pozo)
        psi_eq = np.sqrt(-a / (2 * b))
        F_min = a * (psi_eq**2) + b * (psi_eq**4)
        fase = "Ordenada (Ruptura de simetría)"
        color = "verde"
        descripcion = "El sistema elige espontáneamente un estado (ψ > 0 o ψ < 0)."
    elif a > 0:
        # Fase desordenada: mínimo único en ψ = 0
        psi_eq = 0.0
        F_min = 0.0
        fase = "Desordenada (Simetría conservada)"
        color = "rojo"
        descripcion = "El único estado estable es el desorden (ψ = 0)."
    else:
        # Punto crítico
        psi_eq = 0.0
        F_min = 0.0
        fase = "Punto Crítico"
        color = "amarillo"
        descripcion = "El pozo se aplana. El sistema es altamente susceptible a fluctuaciones."
        
    return {
        "psi": np.round(psi, 4).tolist(),
        "F": np.round(F, 4).tolist(),
        "psi_eq": round(float(psi_eq), 4),
        "F_min": round(float(F_min), 4),
        "fase": fase,
        "color": color,
        "descripcion": descripcion
    }
