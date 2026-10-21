#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 4: Inferencia Activa (Principio de Energía Libre)
Simulador interactivo de un agente que minimiza VFE (percepción) y EFE (acción).
"""
import numpy as np

def calcular_vfe(creencias, obs, A, prior):
    """Energía Libre Variacional: F = Energía Esperada - Entropía"""
    verosimilitud = A[obs, :]
    expected_energy = -np.sum(creencias * (np.log(verosimilitud + 1e-16) + np.log(prior + 1e-16)))
    entropy = -np.sum(creencias * np.log(creencias + 1e-16))
    return float(expected_energy - entropy)

def calcular_efe(creencias, accion, A, B, C):
    """Energía Libre Esperada: Valor Pragmático (KL) - Valor Epistémico (Entropía)"""
    qs_next = B[accion].T @ creencias
    qo = A.T @ qs_next
    pragmatic = np.sum(qo * np.log(qo / (C + 1e-16) + 1e-16))
    epistemic = -np.sum(qo * np.log(qo + 1e-16))
    return float(pragmatic - epistemic)

def simular_inferencia_activa(A, B, C, D, pasos=5, estado_inicial=0):
    """
    Ejecuta el bucle percepción-acción.
    """
    A = np.array(A); B = np.array(B); C = np.array(C); D = np.array(D)
    
    # Normalizar para evitar errores numéricos
    A = A / np.sum(A, axis=0, keepdims=True)
    B = B / np.sum(B, axis=-1, keepdims=True)
    C = C / np.sum(C); D = D / np.sum(D)
    
    creencias = D.copy()
    estado_verdadero = estado_inicial
    historial = []
    
    for paso in range(pasos):
        creencias_antes = creencias.copy()
        
        # 1. Evaluar acciones (minimizar EFE)
        efe_0 = calcular_efe(creencias, 0, A, B, C)
        efe_1 = calcular_efe(creencias, 1, A, B, C)
        accion = 0 if efe_0 < efe_1 else 1
        
        # 2. El entorno evoluciona (las acciones del agente afectan al estado)
        probs_estado_siguiente = B[accion][estado_verdadero]
        estado_verdadero = int(np.random.choice([0, 1], p=probs_estado_siguiente))
        
        # 3. Generar observación
        probs_obs = A[:, estado_verdadero]
        obs = int(np.random.choice([0, 1], p=probs_obs))
        
        # 4. Inferencia perceptual (minimizar VFE vía Bayes exacto)
        verosimilitud = A[obs, :]
        posterior_no_norm = verosimilitud * creencias
        creencias = posterior_no_norm / np.sum(posterior_no_norm)
        
        # 5. Calcular VFE del paso
        vfe = calcular_vfe(creencias, obs, A, D)
        
        historial.append({
            "paso": paso + 1,
            "estado_verdadero": estado_verdadero,
            "creencias_antes": [round(float(x), 3) for x in creencias_antes],
            "accion": accion,
            "efe_0": round(efe_0, 3),
            "efe_1": round(efe_1, 3),
            "observacion": obs,
            "creencias_despues": [round(float(x), 3) for x in creencias],
            "vfe": round(vfe, 3)
        })
        
    return {
        "parametros": {"A": A.tolist(), "B": B.tolist(), "C": C.tolist(), "D": D.tolist()},
        "historial": historial
    }

# Escenarios predefinidos para la UI
ESCENARIOS = {
    "clasico": {
        "nombre": "Equilibrio Clásico",
        "desc": "El agente prefiere obs=1. La acción 0 mantiene el estado, la acción 1 lo cambia.",
        "A": [[0.9, 0.2], [0.1, 0.8]],
        "B": [[[0.9, 0.1], [0.1, 0.9]], [[0.1, 0.9], [0.9, 0.1]]],
        "C": [0.1, 0.9],
        "D": [0.5, 0.5]
    },
    "ruidoso": {
        "nombre": "Entorno Ruidoso",
        "desc": "Los sentidos son poco confiables (A casi uniforme). El agente duda más.",
        "A": [[0.6, 0.4], [0.4, 0.6]],
        "B": [[[0.9, 0.1], [0.1, 0.9]], [[0.1, 0.9], [0.9, 0.1]]],
        "C": [0.1, 0.9],
        "D": [0.5, 0.5]
    },
    "obsesivo": {
        "nombre": "Preferencia Extrema",
        "desc": "El agente 'necesita' ver la obs=1 (C muy sesgado). Explorará agresivamente.",
        "A": [[0.9, 0.2], [0.1, 0.8]],
        "B": [[[0.9, 0.1], [0.1, 0.9]], [[0.1, 0.9], [0.9, 0.1]]],
        "C": [0.01, 0.99],
        "D": [0.5, 0.5]
    }
}
