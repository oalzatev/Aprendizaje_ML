# Predicción del Precio de Bolsa de Energía en Colombia

Proyecto aplicado de Machine Learning — EAFIT 2026  
**Profesor:** Marco Teran  

## Problema

Predecir el **precio de bolsa ponderado nacional** de energía eléctrica en Colombia para el día siguiente (day-ahead), usando datos históricos del mercado disponibles en la API pública XM/SIMEM.

**Tipo de tarea:** Regresión supervisada  
**Horizonte:** Day-ahead (predicción diaria)  
**Métrica principal:** MAE (COP/kWh)

## Estructura del Repositorio

```
ml-proyecto/
├── data/
│   ├── raw/               # CSVs descargados de XM/SIMEM
│   └── data_card.md       # Descripción del dataset
├── notebooks/
│   └── 01_EDA_baseline.ipynb    # Entrega 1: EDA y baselines
├── figures/               # Figuras generadas por los notebooks
├── report/                # Reportes PDF de cada entrega
├── src/                   # Scripts auxiliares
└── README.md
```

## Datos

Fuente: [API SIMEM — XM](https://www.simem.co)  
Rango: 2023-02-01 a 2026-03-31 (1,125 días)

| Variable | Dataset ID | Descripción |
|---|---|---|
| Precio de Bolsa Ponderado | 96D56E | **Target** |
| Máximo Precio Ofertado | 03ba47 | Señal de oferta |
| Precio de Escasez | 43D616 | Techo regulatorio |
| Demanda Comercial | d55202 | Demanda del sistema |
| Generación Real por Tipo | E17D25 | Mix hidro/térmico |
| Aportes Hídricos | BA1C55 | Lluvias/ríos |
| Reservas Hidráulicas % | 843497 | Nivel de embalses |

## Resultados — Entrega 1 (Baselines)

| Modelo | MAE test | RMSE test |
|---|---|---|
| Persistencia | 27.65 | 39.72 |
| Media Móvil 7d | 43.41 | 57.08 |
| Regresión Lineal | 38.75 | 49.47 |

Media del precio en test: 208.56 COP/kWh

## Reproducibilidad

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
jupyter notebook notebooks/01_EDA_baseline.ipynb
```

## Referencias

1. González & Urbano (2022). *Predicción de corto plazo del precio de bolsa de energía en el mercado colombiano*. U. Andes.
2. Villarreal & Flores (2023). *Modelos de predicción del precio de la energía en bolsa en Colombia*. EAFIT.
