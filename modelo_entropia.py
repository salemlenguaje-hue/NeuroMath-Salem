#!/usr/bin/env python3
"""
NeuroMath Salem — Modelo 6: Entropía de Shannon e Información Mutua
Calcula la entropía de distribuciones de probabilidad y la información mutua entre variables.
"""
import math
from typing import List, Dict, Tuple


def entropia_shannon(distribucion: List[float], base: int = 2) -> float:
    """
    Calcula la entropía de Shannon: H(X) = -Σ p(x) * log(p(x))
    
    Args:
        distribucion: lista de probabilidades (deben sumar 1)
        base: base del logaritmo (2 para bits, e para nats, 10 para dits)
    
    Returns:
        Entropía en la unidad correspondiente a la base
    """
    # Normalizar por si acaso
    suma = sum(distribucion)
    if suma == 0:
        return 0.0
    distribucion = [p / suma for p in distribucion]
    
    entropia = 0.0
    for p in distribucion:
        if p > 0:  # Evitar log(0)
            entropia -= p * math.log(p, base)
    
    return round(entropia, 6)


def entropia_maxima(n_eventos: int, base: int = 2) -> float:
    """
    Calcula la entropía máxima posible para n eventos equiprobables.
    H_max = log(n)
    """
    if n_eventos <= 0:
        return 0.0
    return round(math.log(n_eventos, base), 6)


def informacion_mutua(
    distribucion_conjunta: List[List[float]],
    base: int = 2
) -> Dict:
    """
    Calcula la información mutua I(X;Y) entre dos variables discretas.
    
    I(X;Y) = Σ Σ p(x,y) * log(p(x,y) / (p(x) * p(y)))
    
    Args:
        distribucion_conjunta: matriz 2D de probabilidades conjuntas p(x,y)
        base: base del logaritmo
    
    Returns:
        Diccionario con información mutua, entropías marginales y condicional
    """
    # Validar que sea una matriz
    if not distribucion_conjunta or not distribucion_conjunta[0]:
        return {"error": "Matriz vacía"}
    
    n_filas = len(distribucion_conjunta)
    n_cols = len(distribucion_conjunta[0])
    
    # Normalizar la matriz conjunta
    suma_total = sum(sum(fila) for fila in distribucion_conjunta)
    if suma_total == 0:
        return {"error": "Suma de probabilidades es cero"}
    
    p_xy = [[p / suma_total for p in fila] for fila in distribucion_conjunta]
    
    # Calcular marginales
    p_x = [sum(fila) for fila in p_xy]  # P(X)
    p_y = [sum(p_xy[i][j] for i in range(n_filas)) for j in range(n_cols)]  # P(Y)
    
    # Calcular información mutua
    i_mutua = 0.0
    for i in range(n_filas):
        for j in range(n_cols):
            if p_xy[i][j] > 0 and p_x[i] > 0 and p_y[j] > 0:
                i_mutua += p_xy[i][j] * math.log(p_xy[i][j] / (p_x[i] * p_y[j]), base)
    
    # Calcular entropías
    h_x = entropia_shannon(p_x, base)
    h_y = entropia_shannon(p_y, base)
    h_xy = entropia_shannon([p for fila in p_xy for p in fila], base)
    
    # Entropía condicional: H(X|Y) = H(X) - I(X;Y)
    h_x_dado_y = h_x - i_mutua
    h_y_dado_x = h_y - i_mutua
    
    return {
        "informacion_mutua": round(i_mutua, 6),
        "entropia_x": h_x,
        "entropia_y": h_y,
        "entropia_conjunta": h_xy,
        "entropia_condicional_x_dado_y": round(h_x_dado_y, 6),
        "entropia_condicional_y_dado_x": round(h_y_dado_x, 6),
        "marginal_x": [round(p, 4) for p in p_x],
        "marginal_y": [round(p, 4) for p in p_y]
    }


def ejemplo_clima_y_paraguas():
    """Ejemplo didáctico: relación entre clima y llevar paraguas."""
    # Matriz conjunta P(clima, paraguas)
    # Filas: clima (soleado, nublado, lluvioso)
    # Columnas: paraguas (no llevo, llevo)
    distribucion = [
        [0.5, 0.05],   # Soleado: 50% no llevo, 5% llevo
        [0.15, 0.1],   # Nublado: 15% no llevo, 10% llevo
        [0.05, 0.15]   # Lluvioso: 5% no llevo, 15% llevo
    ]
    
    resultado = informacion_mutua(distribucion, base=2)
    
    print("\n" + "="*60)
    print("EJEMPLO: Clima y decisión de llevar paraguas")
    print("="*60)
    print("\nMatriz conjunta P(clima, paraguas):")
    print("              | No llevo | Llevo")
    print("Soleado       |   0.50   |  0.05")
    print("Nublado       |   0.15   |  0.10")
    print("Lluvioso      |   0.05   |  0.15")
    print("\n" + "-"*60)
    print("RESULTADOS:")
    print("-"*60)
    print(f"Entropía del clima H(Clima): {resultado['entropia_x']:.4f} bits")
    print(f"Entropía de la decisión H(Paraguas): {resultado['entropia_y']:.4f} bits")
    print(f"Entropía conjunta H(Clima, Paraguas): {resultado['entropia_conjunta']:.4f} bits")
    print(f"\nInformación Mutua I(Clima; Paraguas): {resultado['informacion_mutua']:.4f} bits")
    print(f"\nInterpretación:")
    print(f"  El clima reduce la incertidumbre sobre llevar paraguas en {resultado['informacion_mutua']:.4f} bits")
    print(f"  (de {resultado['entropia_y']:.4f} a {resultado['entropia_condicional_y_dado_x']:.4f} bits)")
    print("="*60 + "\n")
    
    return resultado


if __name__ == "__main__":
    ejemplo_clima_y_paraguas()
