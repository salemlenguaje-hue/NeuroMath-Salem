# 🧠 NeuroMath Salem

![Salem Logo](salem-logo.png)

> **Laboratorio de Modelos Matemáticos para el Estudio del Desarrollo Cognitivo Artificial y Computacional**

---

## 📖 ¿Qué es NeuroMath Salem?

**NeuroMath Salem** es un laboratorio web interactivo de código abierto, diseñado y ejecutado completamente desde un dispositivo Android (vía Termux), que reúne los modelos matemáticos fundamentales de la neurociencia computacional, la física estadística y la teoría de la información.

Su propósito es **facilitar el estudio, la experimentación y la investigación** en el campo del desarrollo cognitivo artificial, permitiendo a cualquier persona —estudiante, investigador o entusiasta— manipular parámetros, visualizar resultados en tiempo real y generar reportes científicos sin necesidad de hardware especializado ni licencias costosas.

---

## 🎯 Objetivo

El objetivo central de NeuroMath Salem es **democratizar el acceso a las herramientas matemáticas** que sustentan la investigación en:

- **Neurociencia computacional**: modelos de neuronas, redes y dinámicas cerebrales.
- **Física estadística aplicada**: transiciones de fase, criticalidad y sincronización.
- **Teoría de la información**: entropía, información mutua y codificación predictiva.
- **Inteligencia artificial bioinspirada**: agentes con inferencia activa, memoria asociativa y dinámicas emocionales.

Este laboratorio nace como **herramienta de estudio complementaria** al proyecto [Sofía Salem](https://github.com/salemlenguaje-hue/sofia_salem), un agente cognitivo artificial cuyo modelo matemático está documentado en el [ADR-016](https://github.com/salemlenguaje-hue/sofia_salem/blob/main/docs/ADR-016.md). Mientras Sofía *implementa* estos modelos en producción, NeuroMath Salem los *desagrega, visualiza y explica* para su estudio independiente.

---

##  Modelos Implementados

El laboratorio cuenta con **10 modelos matemáticos** organizados en pestañas interactivas:

### 🌊 1. Criticalidad y Avalanchas (ADR-017)
Simula el grid CCD (Campo de Correlación Dinámica) de Sofía. Inyecta perturbaciones y mide el tamaño de las avalanchas para estimar el exponente **α** de la ley de potencia. Permite verificar si el sistema opera en régimen crítico (α ≈ 1.5, como un cerebro real), sub-crítico (rígido) o supra-crítico (caótico).

**Parámetros ajustables:** tamaño del grid, agentes, γ_som, γ_ef, σ, magnitud de perturbación.

### ❤️ 2. Dinámica Emocional y Valencia (ADR-016)
Calcula la evolución de las 7 emociones del modelo Sofía (Curiosidad, Placer, Satisfacción, Empatía, Moderación, Prudencia, Frustración) mediante un integrador con fuga (*leaky integrator*). Calcula el **Coeficiente de Valencia (C_v)** y el **ΔSf** (delta de evolución) a partir del vector fisiológico observable S = (simpático, parasimpático, cortisol).

**Característica especial:** soporte para simulaciones de hasta 10 millones de ciclos con checkpoints en JSONL.

### 🎯 3. Actualizador Bayesiano
Implementa el Teorema de Bayes escalable a múltiples hipótesis. Acepta vectores de probabilidades a priori y verosimilitudes, y devuelve las probabilidades posteriori normalizadas con el factor de actualización de cada hipótesis.

**Ejemplo incluido:** diagnóstico clínico con 3 enfermedades.

### 🧠 4. Inferencia Activa (Principio de Energía Libre — Friston)
Simula un agente que minimiza la **Energía Libre Variacional (VFE)** para percibir y la **Energía Libre Esperada (EFE)** para actuar. Muestra paso a paso cómo el agente actualiza sus creencias y elige acciones en un entorno con 2 estados ocultos.

**Escenarios predefinidos:** Equilibrio Clásico, Entorno Ruidoso, Preferencia Extrema.

###  5. Entropía de Shannon e Información Mutua
Calcula la entropía H(X) de distribuciones de probabilidad y la información mutua I(X;Y) entre variables discretas. Soporta bases 2 (bits), e (nats) y 10 (dits).

**Ejemplo incluido:** relación entre clima y decisión de llevar paraguas.

### 🧲 6. Modelo de Ising (Ferromagnetismo)
Simula una red de espines (+1/-1) con algoritmo de Metropolis. Muestra la transición de fase entre estado paramagnético (desorden) y ferromagnético (orden) al variar la temperatura. Calcula magnetización M, energía E y compara con la T_c teórica.

**Presets:** T=1.0 (frío), T≈2.269 (crítico), T=4.0 (caliente).

### 🌊 7. Modelo de Kuramoto (Sincronización)
Simula N osciladores de fase con acoplamiento sinusoidal. Calcula el **parámetro de orden r** (0 = caos, 1 = sincronía) y permite realizar barridos de K para visualizar la curva de transición de fase.

**Distribuciones:** Lorentz (Cauchy) y Uniforme.

###  8. Red de Hopfield (Memoria Asociativa)
Implementa una red neuronal recurrente que almacena patrones mediante la regla de Hebb y los recupera a partir de entradas ruidosas. Muestra el descenso de la función de energía y la similitud con el patrón original.

**Experimento clave:** variar el nivel de ruido (0-50%) para observar los límites de la memoria asociativa.

### ⚡ 9. Potencial de Acción (FitzHugh-Nagumo)
Simplificación didáctica del modelo Hodgkin-Huxley (Nobel 1963). Simula el voltaje de membrana V y la variable de recuperación W ante una corriente externa I_ext. Muestra el "spike" neuronal, el umbral de disparo y el periodo refractario.

**Presets:** I=0.5 (subumbral), I=1.0 (spike), I=1.5 (spike rápido).

###  10. Teoría de Landau-Ginzburg (Transiciones de Fase)
Modelo teórico fundacional que describe el potencial de energía libre F(ψ) = aψ² + bψ⁴. Visualiza la ruptura espontánea de simetría y la aparición del "doble pozo" (sombrero mexicano) cuando el parámetro de control `a` cruza cero.

**Nota:** este modelo es de estudio teórico y no se implementa operativamente en Sofía (ver ADR-016 §6.4).

---

##  Instalación y Uso

### Requisitos
- Dispositivo Android con **Termux** instalado.
- Python 3.10+ (disponible en Termux).
- Conexión WiFi (para acceder desde el navegador del celu o de otra PC en la misma red).

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/salemlenguaje-hue/NeuroMath-Salem.git
cd NeuroMath-Salem

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar el servidor
python server.py
```

El servidor se inicia en el **puerto 2529**. Abrí el navegador en:
- `http://localhost:2529` (desde el mismo celular)
- `http://<IP-del-celular>:2529` (desde otra PC en la misma red WiFi)

### Uso básico
1. Seleccioná una pestaña del modelo que querés explorar.
2. Ajustá los parámetros según el experimento deseado.
3. Tocá **"Ejecutar"** o **"Calcular"**.
4. Visualizá los resultados en los gráficos de canvas.
5. Usá los botones **📋 Copiar reporte** (Markdown) o **🖨️ Imprimir** (PDF) para archivar.

---

## 🏗️ Arquitectura Técnica
NeuroMath-Salem/
├── server.py                      # Servidor Flask (puerto 2529)
├── requirements.txt               # Dependencias Python
├── modelo_criticalidad.py         # Modelo 1: Avalanchas
├── modelo_emocional.py            # Modelo 2: Emociones + Valencia
├── modelo_bayesiano.py            # Modelo 3: Bayes escalable
├── modelo_inferencia_activa.py    # Modelo 4: Friston / VFE-EFE
├── modelo_entropia.py             # Modelo 5: Shannon + Info. Mutua
├── modelo_ising.py                # Modelo 6: Ising / Metropolis
├── modelo_kuramoto.py             # Modelo 7: Kuramoto / Sincronía
├── modelo_hopfield.py             # Modelo 8: Hopfield / Memoria
├── modelo_potencial_accion.py     # Modelo 9: FitzHugh-Nagumo
── modelo_landau.py               # Modelo 10: Landau-Ginzburg
├── templates/
│   └── index.html                 # Interfaz web (pestañas + canvas)
├── static/
│   ── style.css                  # Estilos (tema oscuro, responsive)
├── data/                          # Checkpoints JSONL de simulaciones largas
├── bitacora.json                  # Historial de experimentos
└── salem-logo.png                 # Logotipo del proyecto
### Stack tecnológico
- **Backend:** Python 3 + Flask
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla (sin frameworks)
- **Visualización:** Canvas 2D API (mapas de calor, gráficos de evolución, histogramas)
- **Matemática:** `numpy`, `scipy`, `math` estándar
- **Persistencia:** JSONL para checkpoints, JSON para bitácora

---

## 📚 Conexión con el Proyecto Sofía Salem

NeuroMath Salem es el **laboratorio de estudio** del ecosistema Sofía Salem, que incluye:

| Proyecto | Puerto | Propósito |
|----------|--------|-----------|
| [Sofía Salem](https://github.com/salemlenguaje-hue/sofia_salem) | — | Agente cognitivo en producción |
| [Diario Salem](https://github.com/salemlenguaje-hue/diario-salem) | 2527 | Registro de estudio y reflexión |
| [Conector Salem](https://github.com/salemlenguaje-hue/conector-salem) | 2528 | Integración y auditoría |
| **NeuroMath Salem** | **2529** | **Laboratorio de modelos matemáticos** |

Cada modelo de NeuroMath corresponde a una capa del ADR-016 de Sofía:
- **Capa de Campo (Grid CCD)** → Modelo de Criticalidad, Ising
- **Capa Biosintética (Emociones)** → Modelo Emocional
- **Capa de Evolución (LUZ/Sf)** → Modelo Emocional (C_v, ΔSf)
- **Capa de Cristalización** → Modelo de Ising, Landau-Ginzburg
- **Capa Social** → Actualizador Bayesiano
- **Capa de Skills** → Red de Hopfield

---

## 🧪 Ejemplos de Experimentos

### 1. Verificar criticalidad en el grid de Sofía
- Pestaña: **Criticalidad**
- Parámetros: Grid 16x16, γ_som=0.2, γ_ef=0.3, σ=0.2
- Resultado esperado: α ≈ 1.2 (régimen crítico)

### 2. Explorar la transición de fase ferromagnética
- Pestaña: **Ising**
- Presets: T=1.0 → T=2.269 → T=4.0
- Observar: cómo cambia M y el mapa de espines

### 3. Simular un potencial de acción neuronal
- Pestaña: **Potencial de Acción**
- I_ext=1.0, tiempo=50
- Observar: el spike y el periodo refractario

### 4. Probar los límites de la memoria asociativa
- Pestaña: **Hopfield**
- 100 neuronas, 5 patrones, ruido 10% → 40%
- Observar: cómo cae la similitud recuperada

---

## 📄 Licencia y Créditos

**Autor:** Martín José Dalberto  
**Año:** 2026  
**Organización:** Salem Lenguaje Hue  

Este proyecto es de código abierto y se distribuye con fines educativos y de investigación. Los modelos matemáticos implementados se basan en literatura científica pública:

- **Teorema de Bayes:** Thomas Bayes (1763)
- **Modelo de Ising:** Ernst Ising (1925)
- **Modelo de Kuramoto:** Yoshiki Kuramoto (1975)
- **Red de Hopfield:** John Hopfield (1982)
- **Modelo Hodgkin-Huxley:** Hodgkin & Huxley (1952, Nobel 1963)
- **FitzHugh-Nagumo:** FitzHugh (1961), Nagumo et al. (1962)
- **Teoría de Landau:** Lev Landau (1937, Nobel 1962)
- **Principio de Energía Libre:** Karl Friston (2010)
- **Criticalidad neuronal:** Beggs & Plenz (2003)

---

##  Contribuciones

Este proyecto nació como herramienta de estudio personal y se comparte con la comunidad. Las contribuciones, sugerencias y reportes de bugs son bienvenidos a través de Issues en GitHub.

---

*Generado con ❤️ desde un celular Android, en Termux, demostrando que la investigación científica de alto nivel no necesita hardware costoso.*
