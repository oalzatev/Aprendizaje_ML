# Data Card — Predicción del Precio de Bolsa de Energía en Colombia

## Información General

| Campo | Detalle |
|---|---|
| **Proyecto** | Predicción day-ahead del precio de bolsa de energía eléctrica en Colombia |
| **Tipo de tarea** | Regresión supervisada |
| **Variable objetivo** | Precio de Bolsa Ponderado Nacional (COP/kWh) |
| **Rango temporal** | 2023-02-01 a 2026-03-31 |
| **Granularidad** | Diaria |
| **Total de observaciones** | 1,125 días (después de feature engineering) |
| **Fuente principal** | API pública XM/SIMEM — simem.co |

---

## Variables del Dataset

### Variable Objetivo

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `precio_bolsa` | float | COP/kWh | Precio de bolsa ponderado nacional (PPBO). Es el precio oficial de liquidación del mercado spot colombiano. Dataset ID: 96D56E |

### Variables de Precio y Mercado

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `mpo_promedio` | float | COP/kWh | Máximo Precio Ofertado Nacional — promedio diario. Señal de estrategia de oferta de generadores. Dataset ID: 03ba47 |
| `mpo_maximo` | float | COP/kWh | Máximo Precio Ofertado Nacional — valor máximo del día. Señal de presión alcista. |
| `precio_escasez` | float | COP/kWh | Precio de escasez ponderado — techo regulatorio del mercado. Dataset ID: 43D616 |

### Variables de Demanda

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `demanda_promedio` | float | kWh | Demanda comercial total del sistema — promedio horario diario (suma de todos los agentes). Dataset ID: d55202 |
| `demanda_max` | float | kWh | Demanda máxima horaria del día |
| `demanda_pico` | float | kWh | Demanda promedio en horas pico (18:00-21:00) |

### Variables de Generación

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `gen_hidro` | float | kWh | Generación hidráulica total diaria. Dataset ID: E17D25 |
| `gen_termica` | float | kWh | Generación térmica total diaria (incluye cogeneración) |
| `gen_solar` | float | kWh | Generación solar total diaria |
| `gen_eolica` | float | kWh | Generación eólica total diaria |
| `ratio_hidro` | float | % | Porcentaje de generación hidráulica sobre total. Driver fundamental del precio. |

### Variables Hidrológicas

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `aportes_hidricos` | float | kWh | Aportes hídricos total nacional en energía equivalente. Dataset ID: BA1C55 |
| `reservas_pct` | float | fracción (0-1) | Nivel de embalses como fracción de capacidad útil total del sistema. Dataset ID: 843497 |

### Features de Ingeniería

| Variable | Tipo | Descripción |
|---|---|---|
| `precio_lag1` | float | Precio de bolsa del día anterior |
| `precio_lag2` | float | Precio de bolsa de hace 2 días |
| `precio_lag7` | float | Precio de bolsa de hace 7 días |
| `precio_ma7` | float | Media móvil del precio — 7 días |
| `precio_ma30` | float | Media móvil del precio — 30 días |
| `demanda_lag1` | float | Demanda del día anterior |
| `aportes_ma7` | float | Media móvil de aportes — 7 días |
| `ratio_reserva` | float | Ratio reservas vs. aportes normalizado |
| `mes` | int | Mes del año (1-12) |
| `dia_semana` | int | Día de la semana (0=lunes, 6=domingo) |
| `es_fin_semana` | int | Indicador fin de semana (0/1) |
| `es_festivo` | int | Indicador festivo colombiano (0/1) |
| `temporada_hidro` | int | Temporada hidrológica (1=seco, 2=trans.húmeda, 3=húmedo, 4=trans.seca) |

---

## Estadísticas de la Variable Objetivo

| Estadística | Valor |
|---|---|
| Media | ~471 COP/kWh |
| Mediana | ~350 COP/kWh |
| Desv. Estándar | ~400 COP/kWh |
| Mínimo | ~102 COP/kWh |
| Máximo | ~3,683 COP/kWh |
| Coef. Variación | >100% (alta volatilidad) |

---

## Partición de Datos

| Conjunto | Período | Filas | Proporción |
|---|---|---|---|
| Entrenamiento | 2023-03-03 a 2024-12-31 | 670 | 59.6% |
| Validación | 2025-01-01 a 2025-06-30 | 181 | 16.1% |
| Test | 2025-07-01 a 2026-03-31 | 274 | 24.4% |

**Estrategia:** split temporal estricto (cronológico). No se usa split aleatorio para evitar data leakage.

---

## Calidad de Datos

| Aspecto | Estado |
|---|---|
| Valores faltantes | Presentes en periodos sin publicación de XM. Tratados con interpolación lineal. |
| Duplicados | Ninguno |
| Outliers | Sí — picos de precio en periodos de sequía. Se mantienen (son información real del mercado). |
| Cobertura temporal | Aportes Hídricos disponibles desde feb-2023; demás variables desde ene-2023. |

---

## Limitaciones y Riesgos

1. **Alta volatilidad:** el precio tiene coeficiente de variación >100%. Los modelos pueden fallar en días de eventos extremos.
2. **Datos con rezago:** en producción, XM publica los datos con 1-2 días de rezago. Los lags del modelo respetan esto.
3. **Ausencia del índice ENSO:** el fenómeno El Niño/La Niña afecta significativamente el precio (correlación +0.31 según literatura). No se incluyó por decisión de simplicidad (las variables hidrológicas lo capturan indirectamente).
4. **Dataset con 3 años:** no incluye El Niño fuerte 2015-2016 (picos de hasta 1,942 COP/kWh). El modelo puede subestimar eventos extremos futuros.
5. **Resolución diaria:** no captura la dinámica horaria del precio. Para predicción horaria se requeriría un enfoque diferente.

---

## Fuente y Acceso

- **API SIMEM:** https://www.simem.co/backend-files/api/PublicData?datasetId={ID}&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
- **Documentación XM:** https://sinergox.xm.com.co
- **Descarga:** reproducible via app SIMEM Explorer (proyecto paralelo)
- **Licencia de datos:** datos públicos del Operador del Sistema Interconectado Nacional (XM S.A. E.S.P.)
