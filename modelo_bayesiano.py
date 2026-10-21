#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 3: Actualizador Bayesiano Escalable
Calcula cómo se actualizan las creencias (probabilidades) ante nueva evidencia.
Acepta múltiples hipótesis y muestra el proceso paso a paso.
"""
import json
from typing import List, Dict, Tuple


def normalizar_vector(vector: List[float]) -> List[float]:
    """Normaliza un vector de probabilidades para que sumen 1."""
    suma = sum(vector)
    if suma == 0:
        # Si todas las probabilidades son 0, distribuir uniformemente
        n = len(vector)
        return [1.0 / n] * n
    return [p / suma for p in vector]


def actualizar_bayes(
    probabilidades_previas: List[float],
    verosimilitudes: List[float]
) -> Dict:
    """
    Aplica el teorema de Bayes para actualizar probabilidades.
    
    Fórmula: P(H_i|E) = P(E|H_i) * P(H_i) / P(E)
    donde P(E) = Σ P(E|H_j) * P(H_j) para todas las hipótesis j
    
    Args:
        probabilidades_previas: P(H_i) - probabilidad a priori de cada hipótesis
        verosimilitudes: P(E|H_i) - probabilidad de la evidencia dado cada hipótesis
    
    Returns:
        Diccionario con:
        - probabilidades_posteriores: P(H_i|E) normalizadas
        - factor_de_actualizacion: P(E|H_i) para cada hipótesis
        - evidencia_marginal: P(E) - probabilidad total de la evidencia
        - pasos_intermedios: lista de cálculos intermedios para didáctica
    """
    n = len(probabilidades_previas)
    if n != len(verosimilitudes):
        raise ValueError("Las listas de probabilidades previas y verosimilitudes deben tener la misma longitud")
    
    if n == 0:
        raise ValueError("Debe haber al menos una hipótesis")
    
    # Paso 1: Calcular numeradores (P(E|H_i) * P(H_i))
    numeradores = []
    pasos = []
    
    for i in range(n):
        previo = probabilidades_previas[i]
        verosimilitud = verosimilitudes[i]
        numerador = previo * verosimilitud
        numeradores.append(numerador)
        
        pasos.append({
            "hipotesis": f"H_{i+1}",
            "previa": previo,
            "verosimilitud": verosimilitud,
            "numerador": numerador,
            "formula": f"P(E|H_{i+1}) × P(H_{i+1}) = {verosimilitud} × {previo} = {numerador}"
        })
    
    # Paso 2: Calcular evidencia marginal P(E) = Σ numeradores
    evidencia_marginal = sum(numeradores)
    
    # Paso 3: Calcular posteriores P(H_i|E) = numerador / P(E)
    posteriores = []
    for i in range(n):
        if evidencia_marginal == 0:
            posterior = 0
        else:
            posterior = numeradores[i] / evidencia_marginal
        posteriores.append(posterior)
        
        if i < len(pasos):
            pasos[i]["posterior"] = posterior
            if evidencia_marginal > 0:
                pasos[i]["formula_posterior"] = f"{numeradores[i]} / {evidencia_marginal} = {posterior}"
            else:
                pasos[i]["formula_posterior"] = "Indeterminado (evidencia = 0)"
    
    # Paso 4: Calcular factor de actualización (cuánto cambió cada probabilidad)
    factores = []
    for i in range(n):
        if probabilidades_previas[i] > 0:
            factor = posteriores[i] / probabilidades_previas[i]
        else:
            factor = 0 if posteriores[i] == 0 else float('inf')
        factores.append(factor)
    
    return {
        "probabilidades_posteriores": posteriores,
        "evidencia_marginal": evidencia_marginal,
        "factores_actualizacion": factores,
        "pasos_intermedios": pasos,
        "resumen": {
            "hipotesis_analizadas": n,
            "hipotesis_mas_probable": f"H_{posteriores.index(max(posteriores)) + 1}",
            "probabilidad_maxima": max(posteriores),
            "cambio_promedio": sum(factores) / n if n > 0 else 0
        }
    }


def ejemplo_clinico():
    """Ejemplo didáctico: diagnóstico médico con 3 enfermedades."""
    # Hipótesis: Enfermedad A, B, C
    previas = [0.01, 0.005, 0.985]  # Prevalencias en la población
    
    # Verosimilitud: probabilidad de tener el síntoma dado cada enfermedad
    verosimilitudes = [0.9, 0.8, 0.1]  # El síntoma es muy común en A y B, raro en C
    
    resultado = actualizar_bayes(previas, verosimilitudes)
    
    print("\n" + "="*60)
    print("EJEMPLO CLÍNICO: Diagnóstico con síntoma observado")
    print("="*60)
    print("\nHipótesis:")
    print("  H_1: Enfermedad A (prevalencia 1%)")
    print("  H_2: Enfermedad B (prevalencia 0.5%)")
    print("  H_3: Sin enfermedad grave (98.5%)")
    print("\nEvidencia: Paciente presenta el síntoma X")
    print("\nVerosimilitudes P(síntoma|enfermedad):")
    print("  P(síntoma|A) = 0.9")
    print("  P(síntoma|B) = 0.8")
    print("  P(síntoma|C) = 0.1")
    print("\n" + "-"*60)
    print("CÁLCULOS INTERMEDIOS:")
    print("-"*60)
    for paso in resultado["pasos_intermedios"]:
        print(f"\n{paso['hipotesis']}:")
        print(f"  {paso['formula']}")
        print(f"  Posterior: {paso['formula_posterior']}")
    
    print("\n" + "="*60)
    print("RESULTADO FINAL:")
    print("="*60)
    print(f"Evidencia marginal P(E): {resultado['evidencia_marginal']:.6f}")
    print(f"\nProbabilidades posteriores:")
    for i, post in enumerate(resultado["probabilidades_posteriores"]):
        factor = resultado["factores_actualizacion"][i]
        print(f"  P(H_{i+1}|síntoma) = {post:.4f} (factor de actualización: {factor:.2f}x)")
    
    print(f"\nHipótesis más probable: {resultado['resumen']['hipotesis_mas_probable']}")
    print(f"Probabilidad máxima: {resultado['resumen']['probabilidad_maxima']:.4f}")
    print("="*60 + "\n")
    
    return resultado


if __name__ == "__main__":
    ejemplo_clinico()
