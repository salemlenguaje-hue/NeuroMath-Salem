#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 2: Modelo de Ising (Ferromagnetismo)
Simula una red de espines (+1/-1) con algoritmo de Metropolis.
Muestra la transición de fase entre estado paramagnético (desorden)
y ferromagnético (orden) al variar la temperatura.
"""
import random
import math


def crear_grid(n_filas, n_cols, semilla=None):
    """Crea un grid de espines aleatorios (+1 o -1)."""
    if semilla is not None:
        random.seed(semilla)
    return [[random.choice([-1, 1]) for _ in range(n_cols)] for _ in range(n_filas)]


def energia_espín(grid, i, j, J, h):
    """Calcula la energía de interacción de un espín con sus 4 vecinos."""
    n_filas = len(grid)
    n_cols = len(grid[0])
    s = grid[i][j]
    # Vecinos con condiciones de frontera periódicas (toro)
    vecinos = [
        grid[(i - 1) % n_filas][j],
        grid[(i + 1) % n_filas][j],
        grid[i][(j - 1) % n_cols],
        grid[i][(j + 1) % n_cols]
    ]
    # Energía: -J * s * suma_vecinos - h * s
    return -J * s * sum(vecinos) - h * s


def energia_total(grid, J, h):
    """Calcula la energía total del grid (cada par se cuenta una vez)."""
    n_filas = len(grid)
    n_cols = len(grid[0])
    e = 0.0
    for i in range(n_filas):
        for j in range(n_cols):
            s = grid[i][j]
            vecinos_derecha_abajo = [
                grid[(i + 1) % n_filas][j],
                grid[i][(j + 1) % n_cols]
            ]
            e += -J * s * sum(vecinos_derecha_abajo) - h * s
    return e


def magnetizacion(grid):
    """Calcula la magnetización promedio M = (1/N) Σ s_i."""
    n_filas = len(grid)
    n_cols = len(grid[0])
    suma = sum(grid[i][j] for i in range(n_filas) for j in range(n_cols))
    return suma / (n_filas * n_cols)


def paso_metropolis(grid, J, h, T):
    """Un paso de Monte Carlo: intenta invertir N espines al azar (N = total de espines)."""
    n_filas = len(grid)
    n_cols = len(grid[0])
    N = n_filas * n_cols
    
    for _ in range(N):
        i = random.randint(0, n_filas - 1)
        j = random.randint(0, n_cols - 1)
        
        # Energía actual del espín
        e_actual = energia_espín(grid, i, j, J, h)
        # Energía si se invierte (cambia el signo de s)
        e_nueva = -e_actual
        delta_e = e_nueva - e_actual  # = -2 * e_actual
        
        # Criterio de Metropolis
        if delta_e <= 0:
            grid[i][j] *= -1  # Invertir siempre (baja la energía)
        else:
            probabilidad = math.exp(-delta_e / T) if T > 0 else 0
            if random.random() < probabilidad:
                grid[i][j] *= -1  # Invertir con probabilidad térmica


def simular_ising(n_filas=20, n_cols=20, T=2.0, J=1.0, h=0.0, 
                  pasos=1000, pasos_equilibrio=200, semilla=42):
    """
    Simula el modelo de Ising y devuelve la evolución de M y E.
    
    Args:
        n_filas, n_cols: tamaño del grid
        T: temperatura (en unidades de J/k_B)
        J: constante de acoplamiento (ferromagnético si J > 0)
        h: campo magnético externo
        pasos: pasos de medición
        pasos_equilibrio: pasos de thermalización antes de medir
        semilla: para reproducibilidad
    """
    grid = crear_grid(n_filas, n_cols, semilla)
    
    # Fase de equilibrio (thermalización)
    for _ in range(pasos_equilibrio):
        paso_metropolis(grid, J, h, T)
    
    # Fase de medición
    historial_M = []
    historial_E = []
    historial_M_abs = []  # Magnetización absoluta (para detectar orden)
    
    for paso in range(pasos):
        paso_metropolis(grid, J, h, T)
        M = magnetizacion(grid)
        E = energia_total(grid, J, h)
        historial_M.append(round(M, 4))
        historial_E.append(round(E, 4))
        historial_M_abs.append(round(abs(M), 4))
    
    # Valores finales
    M_final = historial_M[-1]
    E_final = historial_E[-1]
    M_abs_promedio = sum(historial_M_abs) / len(historial_M_abs)
    
    # Temperatura crítica teórica (grid infinito)
    T_c = 2.0 * J / math.log(1 + math.sqrt(2))
    
    # Diagnóstico de fase
    if T < T_c * 0.9:
        fase = "Ferromagnética (ordenada)"
        color_fase = "verde"
    elif T > T_c * 1.1:
        fase = "Paramagnética (desordenada)"
        color_fase = "rojo"
    else:
        fase = "Crítica (transición de fase)"
        color_fase = "amarillo"
    
    # Grid final para visualización (convertir a 0/1 para el canvas)
    grid_visual = [[(grid[i][j] + 1) / 2 for j in range(n_cols)] for i in range(n_filas)]
    
    return {
        "parametros": {
            "n_filas": n_filas, "n_cols": n_cols,
            "T": T, "J": J, "h": h,
            "pasos": pasos, "pasos_equilibrio": pasos_equilibrio
        },
        "resultados": {
            "M_final": round(M_final, 4),
            "E_final": round(E_final, 4),
            "M_abs_promedio": round(M_abs_promedio, 4),
            "T_c_teorica": round(T_c, 4),
            "fase": fase,
            "color_fase": color_fase
        },
        "historial": {
            "M": historial_M,
            "E": historial_E,
            "M_abs": historial_M_abs
        },
        "grid_final": grid_visual
    }


if __name__ == "__main__":
    print("=== Modelo de Ising ===\n")
    print("Simulando a T=1.5 (ferromagnética):")
    r1 = simular_ising(T=1.5, pasos=100, pasos_equilibrio=50)
    print(f"  M_final: {r1['resultados']['M_final']}")
    print(f"  Fase: {r1['resultados']['fase']}")
    
    print("\nSimulando a T=3.0 (paramagnética):")
    r2 = simular_ising(T=3.0, pasos=100, pasos_equilibrio=50)
    print(f"  M_final: {r2['resultados']['M_final']}")
    print(f"  Fase: {r2['resultados']['fase']}")
