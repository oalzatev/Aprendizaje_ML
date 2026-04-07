# Esquema de Variables para Predicción Day-Ahead del Precio de Bolsa de Energía en Colombia

## Fundamentación

### ¿Cómo se forma el precio de bolsa en Colombia?

El precio de bolsa se determina por un **despacho por mérito de precios**: XM ordena las ofertas de los generadores de menor a mayor precio y despacha hasta cubrir la demanda. El precio de bolsa es el precio de la última planta despachada (precio marginal).

**Drivers fundamentales del precio:**

1. **Hidrología** (70% de la generación es hidro): cuando hay menos agua → entra más térmica cara → sube el precio
2. **Demanda**: más demanda → se necesitan más plantas → entran plantas más caras → sube el precio  
3. **Disponibilidad de plantas**: mantenimientos o fallas reducen oferta → sube el precio
4. **Comportamiento estratégico de ofertas**: generadores pueden ofertar por encima de costos en periodos críticos
5. **Fenómeno ENSO**: El Niño reduce lluvias → menos hidro → más térmica → precios 3-5x más altos

### Metodología ML Propuesta

**Tipo de problema:** Regresión (predicción de valor continuo)
**Horizonte:** Day-ahead (predecir el precio promedio del día siguiente)
**Framework:** CRISP-DM

**Modelos a comparar (3 familias):**
1. **Baseline:** Persistencia (precio_hoy = precio_mañana) + Regresión Lineal
2. **Ensambles basados en árboles:** Random Forest, XGBoost, LightGBM
3. **Modelos de series de tiempo:** ARIMA con features exógenas, o ElasticNet con lags

**Validación:** 
- Split temporal (NO aleatorio): train 2023-2024, validation 2025 H1, test 2025 H2-2026
- Walk-forward validation con ventana deslizante
- Métricas: MAE, RMSE, MAPE, R²

**Pipeline (scikit-learn):**
```
Split temporal → Imputer → Scaler → Feature Engineering → Modelo → Evaluación
```

---

## Variables Seleccionadas

### GRUPO 1: Variable Objetivo (Target)

| Variable | Dataset ID | Campo | Agregación | Justificación |
|---|---|---|---|---|
| **Precio de Bolsa Ponderado** | 96D56E | PPBO | Promedio diario | Es el precio oficial de liquidación del mercado spot. Usar PPBO (no PPBOGReal). |

### GRUPO 2: Variables de Oferta de Generación (Supply-side)

| Variable | Dataset ID | Campo | Agregación | Justificación |
|---|---|---|---|---|
| **Generación Real por Tipo** | E17D25 | TipoGeneracion + GeneracionRealEstimada | Suma diaria por tipo | Permite calcular: gen_hidro, gen_termica, gen_solar, gen_eolica, gen_total, ratio_hidro. El ratio hidro/térmico es el driver #1 del precio. |
| **Disponibilidad Comercial** | 24F4EC | DispCom | Suma total diaria | Capacidad total disponible del sistema. Cuando baja (mantenimientos, fallas), hay presión alcista. |
| **Capacidad Efectiva Neta** | FADED0 | CapEfectivaNeta | Suma total diaria | Capacidad instalada del sistema. Junto con disponibilidad, permite calcular el % de disponibilidad. |

### GRUPO 3: Variables de Demanda (Demand-side)

| Variable | Dataset ID | Campo | Agregación | Justificación |
|---|---|---|---|---|
| **Demanda Comercial** | d55202 | DdaCom (todos los agentes) | Por día: total, max horaria, min horaria, promedio, pico (18-21h) | La demanda total y especialmente la demanda pico determina cuántas plantas caras se necesitan. |

### GRUPO 4: Variables Hidrológicas (El driver principal)

| Variable | Dataset ID | Campo | Agregación | Justificación |
|---|---|---|---|---|
| **Aportes Hídricos en Energía** | BA1C55 | Colombia (total nacional) | Suma diaria | Cuánta agua llega a los embalses. Baja → menos hidro → más térmica → precio sube. |
| **Aportes Hídricos en %** | 34FFDA | Colombia (total nacional) | Promedio diario | Aportes como % de la media histórica. <100% = sequía relativa. Mejor señal que el valor absoluto para capturar El Niño/La Niña. |
| **Reservas Hidráulicas en %** | 843497 | VolumenUtilPorcentaje | Promedio ponderado nacional | Nivel de embalses como % de capacidad útil. Es la variable de "reserva" que indica riesgo de escasez a mediano plazo. |
| **Nivel de Embalse Declarado** | BD26DC | NEM | Suma total | Volumen absoluto en kWh del sistema. Complementa el porcentaje. |
| **Vertimientos Hídricos** | AECA28 | VertimientosEnergia | Suma total diaria | Agua que se bota (embalses llenos). Señal de abundancia hídrica → precios bajos. |

### GRUPO 5: Variables de Precio y Mercado

| Variable | Dataset ID | Campo | Agregación | Justificación |
|---|---|---|---|---|
| **Máximo Precio Ofertado** | 03ba47 | MPO_Nal | Promedio diario + Máximo diario | Señal de la estrategia de oferta de generadores. Un MPO alto indica expectativa de precios altos. |
| **Precio de Escasez** | 43D616 | PrecioEscasezPonderado | Promedio diario | Techo regulatorio. Cuando el precio de bolsa se acerca al precio de escasez, se activan OEF y cambia la dinámica. |

### GRUPO 6: Features Temporales (a construir en el notebook)

| Feature | Cómo se calcula | Justificación |
|---|---|---|
| día_semana | 0=lunes...6=domingo | Demanda y precio varían por día (fines de semana más bajo) |
| mes | 1-12 | Estacionalidad anual (temporada seca dic-mar, lluvias abr-jun, sep-nov) |
| es_festivo | 0/1 | Demanda cae en festivos → precio baja |
| trimestre_hidrologico | categoría | Seco(dic-mar), trans1(abr-jun), húmedo(jul-sep), trans2(oct-nov) |
| precio_lag_1 | precio de bolsa t-1 | Autocorrelación del precio (el mejor predictor es el día anterior) |
| precio_lag_7 | precio de bolsa t-7 | Captura patrón semanal |
| precio_lag_30 | precio de bolsa t-30 | Captura tendencia mensual |
| precio_rolling_7 | media móvil 7 días | Suaviza volatilidad, captura tendencia corta |
| precio_rolling_30 | media móvil 30 días | Tendencia mensual |
| demanda_lag_1 | demanda total t-1 | La demanda del día anterior predice la de mañana |
| aportes_rolling_7 | media móvil 7 días aportes | Tendencia hidrológica reciente |
| ratio_reserva_aportes | reserva% / aportes% | Combina nivel actual + tendencia. Bajo = riesgo |

---

## Variables Descartadas (y por qué)

| Variable | Por qué no |
|---|---|
| PPBOGReal (Precio Bolsa Gen Real) | Es un cálculo posterior, no el precio de liquidación real |
| MPO_Tie, MPO_Int | Son derivados del MPO_Nal, agregan ruido sin información nueva |
| Generación por planta individual | Demasiado granular, se agrega por tipo |
| Demanda por agente individual | Se necesita el total del sistema, no por comercializador |
| Aportes por región individual | El total nacional es suficiente para precio nacional |
| IPC, TRC, PIB | Según la literatura colombiana, no afectan significativamente en el corto plazo (day-ahead) |
| Precio internacional de combustibles | Efecto de segundo orden en Colombia (la mayoría es hidro) |

---

## Resumen: 12 Variables de SIMEM + 12 Features Engineered

**De la API (12 datasets):**
1. Precio de Bolsa Ponderado (target)
2. Generación Real por Tipo (E17D25) → 6 sub-features
3. Disponibilidad Comercial (24F4EC)
4. Demanda Comercial (d55202) → 5 sub-features
5. Aportes Hídricos en Energía (BA1C55)
6. Aportes Hídricos en % (34FFDA)
7. Reservas Hidráulicas en % (843497)
8. Nivel de Embalse Declarado (BD26DC)
9. Vertimientos Hídricos (AECA28)
10. Máximo Precio Ofertado (03ba47) → 2 sub-features
11. Precio de Escasez (43D616)
12. Capacidad Efectiva Neta (FADED0)

**Features temporales (12, construidas en notebook):**
- día_semana, mes, es_festivo, trimestre_hidrologico
- 3 lags de precio (1, 7, 30)
- 2 rolling means de precio (7, 30)
- demanda_lag_1, aportes_rolling_7, ratio_reserva_aportes

**Total: ~30 features para el modelo final**
