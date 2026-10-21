#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 1: Criticalidad y Avalanchas (ADR-017)
Simulador del grid CCD con parámetros configurables y visualización del estado.
"""
import numpy as np
import math
from collections import Counter


class GridCCD:
    """Simulación del grid CCD de Sofía para experimentos de criticalidad."""
    
    def __init__(self, n_filas=16, n_cols=16, gamma_som=0.2, gamma_ef=0.5, 
                 sigma=0.2, z_objetivo=1.0, semilla=42):
        self.n_filas = int(n_filas)
        self.n_cols = int(n_cols)
        self.gamma_som = float(gamma_som)
        self.gamma_ef = float(gamma_ef)
        self.sigma = float(sigma)
        self.z_objetivo = float(z_objetivo)
        self.rng = np.random.default_rng(int(semilla))
        
        # Inicializar grid como array numpy (garantizado)
        self.z = np.array(self.rng.normal(self.z_objetivo, 0.1, (self.n_filas, self.n_cols)))

    def paso(self):
        """Un paso discreto de la dinámica del grid (Ecuación maestra ADR-016 §3.1)."""
        # Asegurar que z sea array numpy
        self.z = np.asarray(self.z, dtype=float)
        z_nuevo = np.copy(self.z)
        
        # Término homeostático: empuja hacia el objetivo
        z_nuevo += self.gamma_som * (self.z_objetivo - self.z)
        
        # Término efáptico: interacción con vecinos inmediatos (kernel 3x3)
        for i in range(self.n_filas):
            for j in range(self.n_cols):
                vecinos = [
                    self.z[i, j],
                    self.z[(i-1) % self.n_filas, j],
                    self.z[(i+1) % self.n_filas, j],
                    self.z[i, (j-1) % self.n_cols],
                    self.z[i, (j+1) % self.n_cols]
                ]
                suma_vecinos = sum(vecinos)
                z_nuevo[i, j] += self.gamma_ef * np.tanh(suma_vecinos)
        
        # Ruido gaussiano
        z_nuevo += self.sigma * self.rng.normal(0, 1, (self.n_filas, self.n_cols))
        
        # Clamp fisiológico [-3, 3]
        self.z = np.clip(z_nuevo, -3.0, 3.0)

    def copiar_estado(self):
        """Devuelve una copia profunda del estado actual."""
        return np.array(self.z, dtype=float)

    def restaurar_estado(self, estado):
        """Restaura el grid a un estado anterior."""
        self.z = np.array(estado, dtype=float)

    def perturbar_nodo(self, indice, magnitud):
        """Inyecta una perturbación en un nodo específico."""
        indice = int(indice)
        magnitud = float(magnitud)
        fila = indice // self.n_cols
        col = indice % self.n_cols
        self.z[fila, col] += magnitud

    def medir_cambio(self, estado_previo, umbral=0.05):
        """Cuenta cuántos nodos cambiaron más que el umbral."""
        estado_previo = np.asarray(estado_previo, dtype=float)
        delta = np.abs(self.z - estado_previo)
        afectados = np.where(delta > umbral)
        return len(afectados[0]), afectados

    def obtener_estado_normalizado(self):
        """Devuelve el estado z normalizado a [0, 1] para visualización."""
        z_min, z_max = -3.0, 3.0
        return ((self.z - z_min) / (z_max - z_min)).clip(0, 1).tolist()


def estimar_alpha(tamanos):
    """Estima el exponente α de la ley de potencia P(s) ∝ s^(-α) usando MLE."""
    tamanos_validos = [s for s in tamanos if s >= 2]
    if len(tamanos_validos) < 10:
        return -1.0
    
    s_min = 2
    suma_logs = sum(math.log(s / s_min) for s in tamanos_validos)
    
    if suma_logs == 0:
        return -1.0
    
    n = len(tamanos_validos)
    alpha = 1.0 + n / suma_logs
    return alpha


def ejecutar_experimento(n_perturbaciones=200, magnitud=1.0, 
                         gamma_som=0.2, gamma_ef=0.5, sigma=0.2,
                         n_filas=16, n_cols=16, n_agentes=4,
                         n_ciclos_equilibrio=1000, n_pasos_propagacion=50,
                         umbral=0.05, semilla=42):
    """Ejecuta el experimento de avalanchas con parámetros configurables."""
    print(f"🔬 Experimento: Grid {n_filas}x{n_cols}, {n_agentes} agentes, N={n_perturbaciones}")
    
    # Crear grid con los parámetros personalizados
    grid = GridCCD(
        n_filas=n_filas, n_cols=n_cols,
        gamma_som=gamma_som, gamma_ef=gamma_ef, sigma=sigma,
        semilla=semilla
    )
    
    # 1. Fase de equilibrio
    print(f"  → Equilibrando ({n_ciclos_equilibrio} pasos)...")
    for _ in range(int(n_ciclos_equilibrio)):
        grid.paso()
    
    # 2. Medición de avalanchas
    tamanos = []
    estados_avalanchas = []
    rng_exp = np.random.default_rng(int(semilla) + 1000)
    total_nodos = int(n_filas) * int(n_cols)
    
    # Seleccionar nodos "agentes"
    nodos_agentes = rng_exp.choice(total_nodos, size=min(int(n_agentes), total_nodos), replace=False)
    
    for i in range(int(n_perturbaciones)):
        estado_previo = grid.copiar_estado()
        
        nodo = int(rng_exp.choice(nodos_agentes))
        grid.perturbar_nodo(nodo, float(magnitud))
        
        for _ in range(int(n_pasos_propagacion)):
            grid.paso()
        
        tamano, _ = grid.medir_cambio(estado_previo, float(umbral))
        tamanos.append(tamano)
        
        if i < 10:
            estados_avalanchas.append(grid.obtener_estado_normalizado())
        
        grid.restaurar_estado(estado_previo)
        
        if (i + 1) % 50 == 0:
            print(f"    Progreso: {i + 1}/{n_perturbaciones}")

    # 3. Análisis
    alpha = estimar_alpha(tamanos)
    
    print(f"\n📊 α estimado: {alpha:.3f}")
    if alpha > 0:
        if alpha < 1.0:
            print("🔴 SUPRA-CRÍTICO")
        elif alpha < 2.0:
            print("🟢 CRÍTICO (ley de potencia)")
        else:
            print("🔵 SUB-CRÍTICO")
    
    estado_final = grid.obtener_estado_normalizado()
    
    return alpha, tamanos, estado_final, estados_avalanchas


if __name__ == "__main__":
    ejecutar_experimento(n_perturbaciones=200, magnitud=1.0)
