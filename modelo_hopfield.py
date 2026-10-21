#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 4: Red de Hopfield (Memoria Asociativa)
Simula una red neuronal recurrente que recupera patrones almacenados
a partir de entradas ruidosas, minimizando una función de energía.
"""
import random
import math


def generar_patrones(n_patrones, n_neuronas):
    """Genera patrones aleatorios de +1 y -1."""
    random.seed(42)
    return [[random.choice([-1, 1]) for _ in range(n_neuronas)] for _ in range(n_patrones)]


def calcular_pesos_hebb(patrones):
    """
    Calcula la matriz de pesos sinápticos usando la regla de Hebb.
    w_ij = (1/N) * sum(mu_i * mu_j) para todos los patrones.
    w_ii = 0 (sin autoconexiones).
    """
    n_patrones = len(patrones)
    n_neuronas = len(patrones[0])
    
    # Inicializar matriz de pesos en 0
    W = [[0.0 for _ in range(n_neuronas)] for _ in range(n_neuronas)]
    
    for i in range(n_neuronas):
        for j in range(n_neuronas):
            if i == j:
                W[i][j] = 0.0
            else:
                suma = sum(patron[i] * patron[j] for patron in patrones)
                W[i][j] = suma / n_neuronas
                
    return W


def agregar_ruido(patron, probabilidad_ruido):
    """Invierte el signo de las neuronas con una probabilidad dada."""
    ruidoso = []
    for s in patron:
        if random.random() < probabilidad_ruido:
            ruidoso.append(-s)
        else:
            ruidoso.append(s)
    return ruidoso


def calcular_energia(estado, W):
    """
    Calcula la energía de la red: E = -1/2 * sum(w_ij * s_i * s_j)
    La red siempre evoluciona hacia estados de menor energía.
    """
    n = len(estado)
    energia = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                energia -= W[i][j] * estado[i] * estado[j]
    return round(energia / 2.0, 4)


def actualizar_estado(estado, W):
    """
    Actualización asíncrona de una neurona aleatoria.
    s_i = sign(sum(w_ij * s_j))
    """
    n = len(estado)
    nuevo_estado = list(estado)
    
    # Elegir una neurona al azar para actualizar
    i = random.randint(0, n - 1)
    
    # Calcular el campo local
    campo_local = sum(W[i][j] * estado[j] for j in range(n) if i != j)
    
    # Regla de activación (signo)
    if campo_local >= 0:
        nuevo_estado[i] = 1
    else:
        nuevo_estado[i] = -1
        
    return nuevo_estado


def simular_hopfield(n_neuronas=100, n_patrones=3, probabilidad_ruido=0.2, 
                     pasos_maximos=500, semilla=42):
    """
    Simula el proceso completo: almacenar, corromper y recuperar.
    """
    random.seed(semilla)
    
    # 1. Generar y almacenar patrones
    patrones_originales = generar_patrones(n_patrones, n_neuronas)
    W = calcular_pesos_hebb(patrones_originales)
    
    # 2. Elegir un patrón objetivo y agregarle ruido
    patron_objetivo_idx = 0
    patron_ruidoso = agregar_ruido(patrones_originales[patron_objetivo_idx], probabilidad_ruido)
    
    # 3. Evolución de la red
    estado_actual = list(patron_ruidoso)
    historial_energia = [calcular_energia(estado_actual, W)]
    historial_estados = [list(estado_actual)]
    
    cambios = 0
    for paso in range(pasos_maximos):
        estado_anterior = list(estado_actual)
        estado_actual = actualizar_estado(estado_actual, W)
        
        # Contar cuántas neuronas cambiaron
        diferencias = sum(1 for i in range(n_neuronas) if estado_actual[i] != estado_anterior[i])
        if diferencias > 0:
            cambios += 1
            
        energia = calcular_energia(estado_actual, W)
        historial_energia.append(energia)
        historial_estados.append(list(estado_actual))
        
        # Criterio de parada: si no hay cambios, la red convergió (atractor)
        if diferencias == 0:
            break
    
    # 4. Evaluar recuperación
    # Calcular similitud (producto punto normalizado) con el patrón original
    similitud = sum(estado_actual[i] * patrones_originales[patron_objetivo_idx][i] for i in range(n_neuronas)) / n_neuronas
    
    # Convertir estados a 0/1 para visualización en canvas (1 -> 1, -1 -> 0)
    grid_inicial = [(s + 1) / 2 for s in patron_ruidoso]
    grid_final = [(s + 1) / 2 for s in estado_actual]
    
    # Calcular dimensiones del grid (asumimos que es cuadrado o cercano)
    lado = int(math.sqrt(n_neuronas))
    if lado * lado != n_neuronas:
        lado = int(math.ceil(math.sqrt(n_neuronas)))
        
    return {
        "parametros": {
            "n_neuronas": n_neuronas,
            "n_patrones": n_patrones,
            "probabilidad_ruido": probabilidad_ruido,
            "pasos_ejecutados": len(historial_energia) - 1
        },
        "resultados": {
            "energia_inicial": historial_energia[0],
            "energia_final": historial_energia[-1],
            "similitud": round(similitud, 4),
            "convergencia": cambios == 0 or historial_energia[-1] == historial_energia[-2],
            "lado_grid": lado
        },
        "visualizacion": {
            "grid_inicial": grid_inicial,
            "grid_final": grid_final
        },
        "historial": {
            "energia": historial_energia
        }
    }
