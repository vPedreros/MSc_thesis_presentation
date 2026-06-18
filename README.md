# MSc Thesis Presentation: Cosmological Simulations & Slides

Este repositorio contiene la presentación y las animaciones matemáticas en Python utilizadas para la defensa de la Tesis de Magíster en Ciencias (MSc) con mención en Física, en la Facultad de Ciencias Físicas y Matemáticas (FCFM) de la Universidad de Chile.

El proyecto está estructurado para facilitar el renderizado de animaciones cosmológicas personalizadas mediante la librería **Manim** y su integración en las diapositivas de la presentación.

---

## 📁 Estructura del Proyecto

La organización del repositorio es la siguiente:

```text
├── .gitignore               # Configuración de exclusiones para Git
├── .python-version          # Versión recomendada de Python (>= 3.10)
├── pyproject.toml           # Dependencias de Python gestionadas con uv / pip
├── uv.lock                  # Lockfile de dependencias para reproducibilidad
├── presentation/
│   └── MSc_thesis_slides.key # Diapositivas de la presentación (formato Apple Keynote, ~98 MB)
├── python/
│   ├── manim.cfg            # Configuración por defecto para Manim (Fondo Blanco)
│   ├── main.py              # Plantillas básicas y ejemplos de figuras
│   ├── scene.py             # Plantilla de escena simple (SquareToCircle)
│   # --- Animaciones Principales ---
│   ├── GR_earth_rotating.py # Simulación en 3D de la curvatura del espacio-tiempo
│   ├── receding_galaxies.py # Recesión galáctica en coordenadas físicas
│   ├── comoving_coord.py    # Recesión galáctica en coordenadas comóviles
│   ├── hubble.py            # Ley de Hubble y corrimiento al rojo (Redshift)
│   ├── EB_solver.py         # Flujograma animado de un solver Einstein-Boltzmann (CLASS)
│   ├── coupled.py           # Colapso gravitacional de múltiples especies en el Universo temprano
│   ├── delta.py             # Crecimiento lineal de perturbaciones en 1D (δ)
│   ├── delta2.py            # Crecimiento y colapso no lineal de perturbaciones (1D + partículas 2D)
│   ├── lcdm_vs_fr.py        # Comparativa de colapso de estructuras en ΛCDM vs. Gravedad Modificada f(R)
│   └── regimes.py           # Motivación de métodos numéricos para diferentes escalas físicas
├── imgs/                    # Imágenes de cosmólogos y físicos usadas en la presentación
└── logos/                   # Logotipos de la FCFM y del grupo CosmoUChile
```

---

## 🎬 Detalle de las Animaciones (Manim)

Las animaciones han sido codificadas en Python usando la versión comunitaria de **Manim (Manim Community)**. Todas están diseñadas con un estilo estético de **fondo blanco** para coincidir con el diseño minimalista de la presentación.

| Script Python | Clase de Escena | Descripción Física / Conceptual |
| :--- | :--- | :--- |
| `GR_earth_rotating.py` | `SpacetimeCurvature` | **Curvatura en Relatividad General**: Representación 3D del pozo gravitacional del Sol usando una métrica deformada y la órbita de la Tierra regida por la ecuación de campo $G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$. |
| `receding_galaxies.py` | `GalacticRecession` | **Expansión del Universo (Física)**: Dos galaxias separándose debido a la tasa de expansión de la métrica (factor de escala $a(t)$), mientras su red física espacial subyacente se estira. |
| `comoving_coord.py` | `GalacticRecessionComovingCoord` | **Coordenadas Comóviles**: Muestra la misma expansión del universo, pero manteniendo la cuadrícula de coordenadas comóviles fija para ilustrar el concepto físico de comovilidad. |
| `hubble.py` | `HubblesLawRedshift` | **Ley de Hubble y Redshift**: Onda de luz propagándose entre un emisor y un receptor que se estira (corrimiento al rojo cosmológico) debido a la expansión del espacio durante su viaje. |
| `EB_solver.py` | `EBSolverFlow` | **Solver de Einstein-Boltzmann**: Diagrama de bloques dinámico del flujo de cómputo en códigos numéricos como `CLASS` (parámetros cosmológicos de entrada $\rightarrow$ ecuaciones lineales acopladas de fluidos y Einstein $\rightarrow$ espectro de potencia de materia y CMB). |
| `coupled.py` | `MultiSpeciesFormation` | **Especies Múltiples**: Visualización del comportamiento acoplado de bariones (rojo), materia oscura fría (azul) y neutrinos (gris) en el Universo temprano, mostrando cómo la materia oscura guía el colapso gravitacional. |
| `delta.py` | `StructureFormation` | **Contraste de Densidad ($\delta$)**: Crecimiento de una perturbación esférica de densidad $\delta(x, t)$ a medida que la gravedad atrae masa hacia el centro de la fluctuación. |
| `delta2.py` | `StructureFormation` | **Colapso Esférico**: Pantalla dividida que muestra de forma simultánea el colapso físico de un gas de partículas en 2D y el crecimiento correspondiente del pico de densidad en 1D. |
| `lcdm_vs_fr.py` | `LCDMvsFRComparison` | **ΛCDM vs Gravedad Modificada $f(R)$**: Comparación lado a lado de la velocidad de colapso y aglomeración de materia oscura en el modelo estándar ($\Lambda$CDM) frente a teorías de gravedad modificada $f(R)$ (como el modelo Hu-Sawicki). |
| `regimes.py` | `NumericalMotivation` | **La Muralla Matemática**: Demostración visual de la necesidad de solvers numéricos al pasar del régimen lineal (ondulatorio y resoluble analíticamente) al no-lineal (caótico y con cruzamiento de órbitas). |

---

## 🛠️ Requisitos e Instalación

Para ejecutar y renderizar estas animaciones en tu máquina local, necesitarás tener instalado tanto el motor de renderizado del sistema como las librerías de Python.

### 1. Dependencias del Sistema

Manim requiere de ciertas herramientas externas para procesar videos y fórmulas matemáticas en LaTeX.

- **FFmpeg**: Motor de procesamiento de audio y video.
- **Pango** y **Cairo**: Librerías de renderizado vectorial de texto y gráficos.
- **LaTeX** (opcional pero altamente recomendado para las ecuaciones matemáticas): Se recomienda una distribución completa como MacTeX (macOS) o TeX Live (Linux/Windows).

#### Instalación en macOS (usando Homebrew):
```bash
brew install pyenv
brew install ffmpeg pango scipy
# Si deseas ecuaciones matemáticas renderizadas en alta calidad:
brew install --cask mactex-no-gui
```

### 2. Dependencias de Python (Usando `uv`)

Este proyecto está configurado con **`uv`**, un gestor de proyectos de Python sumamente rápido escrito en Rust. Si no tienes instalado `uv`, puedes instalarlo con:

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Una vez que tengas `uv`, simplemente ubícate en la raíz del repositorio y sincroniza el entorno virtual:

```bash
uv sync
```

Esto creará automáticamente una carpeta `.venv/` con la versión correcta de Python e instalará `manim` y todas sus dependencias.

---

## 🚀 Cómo Renderizar las Animaciones

Para renderizar cualquier escena de los scripts de Python, utiliza el entorno virtual configurado. Por ejemplo, para renderizar la animación de curvatura 3D en baja calidad y abrirla inmediatamente tras terminar:

```bash
# Renderizar en baja resolución (480p, rápido para pruebas)
uv run manim -pql python/GR_earth_rotating.py SpacetimeCurvature

# Renderizar en alta resolución (1080p, calidad final de presentación)
uv run manim -pqh python/GR_earth_rotating.py SpacetimeCurvature
```

### Explicación de los Parámetros de Manim:
* `-p` (**p**lay): Reproduce o abre el video generado automáticamente al terminar el renderizado.
* `-q` (**q**uality): Define la calidad del renderizado.
  * `l` (**l**ow): 480p, 15 fps (ideal para previsualizaciones rápidas).
  * `m` (**m**edium): 720p, 30 fps.
  * `h` (**h**igh): 1080p, 60 fps (calidad óptima para diapositivas).
  * `k` (**k**4): 1440p / 4K, 60 fps.

Los videos e imágenes resultantes se guardarán por defecto en el directorio `media/videos/` y `media/images/` respectivamente (este directorio está configurado en `.gitignore` para no subir archivos binarios pesados al repositorio de GitHub).

---
