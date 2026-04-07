# Resumen de Documentos de Referencia
## Proyecto ML: Predicción del Precio de Bolsa de Energía — Colombia

> Fecha de extracción: 7 de abril de 2026
> Preparado para: Proyecto de predicción day-ahead del precio de bolsa de energía eléctrica en Colombia

---

## DOCUMENTO 1: content.pdf

### Metadatos
| Campo | Detalle |
|-------|---------|
| **Tipo** | Tesis de Maestría (Trabajo de grado) |
| **Título** | Predicción de corto plazo del precio de bolsa de energía en el mercado colombiano |
| **Institución** | Universidad de los Andes, Bogotá |
| **Año** | 2022 |
| **Autores** | Luis Fernando González Pérez, Sara Nathaly Urbano Buriticá |
| **Asesores** | Alejandra Tabares Pozos, PhD; Henry Camilo Torres Valderrama, PhD |
| **Programa** | Maestría en Inteligencia Analítica para la Toma de Decisiones |
| **Páginas** | 40 |

---

### Problema que aborda
- Predicción **day-ahead horaria** (24 horas del día siguiente) del precio de bolsa de energía eléctrica en el mercado colombiano.
- XM recibe ofertas de generadores con un día de anticipación. Los agentes generadores necesitan anticipar el precio de bolsa para optimizar su estrategia de oferta.
- Sin un buen modelo, la incertidumbre del precio equivale a ~$10M COP por GWh/día; para los principales agentes puede representar ~$2.000M COP diarios en riesgo.
- El mercado es imperfectamente competitivo: Enel (~21%), EPM (~18%), ISAGEN (~18%) concentran la generación.
- Matriz energética al momento del estudio: 63.5% hidro, 30.1% termo, 5.1% solar, 0.3% eólica.

---

### Variables utilizadas

**Fuente de datos:** API pública de XM (sinergox.xm.com.co) — datos desde 2020.

| Variable | Tipo | Resolución | Descripción |
|----------|------|-----------|-------------|
| Precio de Bolsa Nacional ($/MWh) | **Dependiente** | Horaria | Variable objetivo — precio de bolsa nacional |
| Demanda (GWh) | Independiente | Diaria | Consumo de energía del sistema |
| Vertimientos (GWh) | Independiente | Diaria | Agua vertida por embalses expresada en energía |
| Aportes (GWh) | Independiente | Diaria | Afluentes hídricos a embalses en energía |
| Reservas (GWh) | Independiente | Diaria | Volumen útil de embalses en energía |
| Generación FNCER en mérito (GWh) | Independiente | Diaria | Energías no convencionales despachadas |
| Generación FNCER fuera de mérito (GWh) | Independiente | Diaria | Energías no convencionales no despachadas |
| Generación Hidro en mérito (GWh) | Independiente | Diaria | Hidroeléctricas despachadas |
| Generación Hidro fuera de mérito (GWh) | Independiente | Diaria | Hidroeléctricas no despachadas |
| Generación Termo en mérito (GWh) | Independiente | Diaria | Termoeléctricas despachadas |
| Generación Termo fuera de mérito (GWh) | Independiente | Diaria | Termoeléctricas no despachadas |
| Mes | Temporal | — | Variable de calendario |
| Día | Temporal | — | Variable de calendario |

**Notas importantes sobre granularidad:**
- **Aportes:** se obtuvieron mejores resultados separando la cuenca de Antioquia del resto de cuencas (dos variables en lugar de una).
- **Reservas:** se obtuvieron mejores resultados desagregando por principales embalses individualmente (Esmeralda, Guavio, El Peñol, etc.).
- **Precio de bolsa:** análisis ACF/PACF muestra autocorrelaciones significativas cada 24 datos (mismo periodo del día anterior) — memoria corta de 1–3 días.

---

### Metodología ML/estadística

#### Preprocesamiento y exploración
- PCA y TSNE para reducción de dimensionalidad (resultado: no fue posible separar grupos de días con estas técnicas).
- Análisis de autocorrelación (ACF, PACF) para identificar lags relevantes.
- Prueba Dickey-Fuller para verificar estacionariedad.

#### Modelos entrenados

| Familia | Modelos específicos | Transformaciones probadas |
|---------|---------------------|--------------------------|
| Series de tiempo univariadas | ARMA, ARIMA | Sin transformación, BoxCox, LOG |
| Series de tiempo con variables exógenas | ARMA(variables exógenas), SARIMAX | Con/sin diferenciación; con/sin exógenas |
| Modelos de descomposición | Prophet (Facebook) | Sin transformación, BoxCox, LOG |
| Redes neuronales | MLP (Perceptrón Multicapa), ARNN (autorregresiva) | — |
| Redes recurrentes | **LSTM (Long Short-Term Memory)** | Función activación ReLU, capas ocultas |

**Estrategia de segmentación (importante):**
- Segmentación por **tipo de día**: lunes–viernes / sábado / domingo+festivos.
- Segmentación por **periodo horario**: 24 modelos independientes (uno por hora del día).
- El mejor esquema encontrado fue **filtro solo por periodo horario** (sin filtro de tipo de día).

---

### Métricas de evaluación
| Métrica | Descripción |
|---------|-------------|
| **MSE** | Error Cuadrático Medio |
| **MAPE** | Mean Absolute Percentage Error (%) |
| **MaxError** | Error máximo puntual |
| **Varianza Explicada (%)** | Capacidad explicativa del modelo |

---

### Resultados cuantitativos

#### Modelos de series de tiempo (Tablas 3 y 4 del documento)

| Modelo | Transformación | MAPE PPB [%] | MaxError | MSE |
|--------|---------------|:------------:|:--------:|:---:|
| ARMA(1,0,1) | Sin transformación | 26.96 | 33.54 | 5,202.0 |
| ARMA(1,0,1) | BOXCOX | 29.58 | 58.54 | 7,567.4 |
| ARMA(1,0,1) | LOG | 28.11 | 48.60 | 6,462.6 |
| ARMA(1,0,1) | **Variables exógenas** | **18.46** | 32.30 | **4,862.6** |
| SARIMAX(1,0,1)(1,1,0)24 | Sin transformación | **12.28** | 15.35 | **235.67** |
| SARIMAX(1,1,1)(1,1,0)24 | Diferenciación | 30.52 | 12.33 | 3,169.8 |
| **SARIMAX(1,0,1)(1,1,0)24** | **Variables exógenas** | **11.58** | **2.82** | 634.20 |
| Prophet | Sin transformación | 59.33 | 112.05 | 19,654.9 |
| Prophet | BOXCOX | 38.43 | 81.72 | 13,215.2 |
| Prophet | LOG | 27.61 | 36.34 | 1,652.7 |

#### Modelos LSTM (Tabla 6 del documento)

| Modelo | Lags usados | Filtro por periodo horario | MSE | MaxError | Varianza Explicada |
|--------|:-----------:|:--------------------------:|:---:|:--------:|:------------------:|
| **Lag 1.2** | 1 | Sí | **31.406** | 139.267 | 81.634% |
| Lag 2.2 | 2 | Sí | 32.715 | 138.040 | **82.482%** |
| Lag 3.2 | 3 | Sí | 33.457 | **137.451** | 82.090% |

**Modelo ganador global:** LSTM "Lag 1.2" — 1 lag anterior, 24 modelos (uno por hora), sin filtro por tipo de día.
- MSE = 31.406
- MaxError = 139.267 $/kWh
- Varianza Explicada = 81.634%
- MAPE ≈ 13.89%

---

### Hallazgos principales
1. **SARIMAX con variables exógenas** obtuvo el mejor MAPE entre todos los modelos de series de tiempo (11.58%).
2. **LSTM fue el mejor modelo global**, alcanzando la mayor varianza explicada (81.6%) con el menor MSE.
3. El precio de bolsa es un **commodity de memoria corta (1–3 días)**; usar más de 2–3 lags empeora sistemáticamente la predicción.
4. La **diferenciación** en ARIMA/SARIMAX no mejora los resultados para este caso.
5. Añadir **variables exógenas** (Demanda, Generación Termo) mejora significativamente los modelos de series de tiempo.
6. **Prophet no es adecuado** para esta serie: fue el peor modelo en todas las configuraciones.
7. La **volatilidad del precio** aumenta en periodos de alta demanda (franjas de mañana y tarde), degradando el desempeño de los modelos en esas horas.
8. Los modelos con **filtro solo por periodo horario** (sin filtro adicional por tipo de día) son superiores.
9. PCA y TSNE no lograron identificar clusters de días en el espacio de variables del mercado.

---

### Conclusiones relevantes para predicción day-ahead del precio de bolsa en Colombia
- Usar datos disponibles hasta **D-2** (la información del mercado tiene un retraso de al menos un día hábil).
- Segmentar en **24 modelos independientes** (uno por hora del día).
- El precio tiene **memoria de 1–2 días**: usar 1 o 2 lags anteriores como máximo.
- **LSTM supera** a redes MLP y ARNN para esta tarea.
- Las **variables exógenas del mercado** (Demanda, Generación, Reservas) mejoran notablemente los modelos de series de tiempo.
- Para trabajo futuro: incorporar **precios de combustibles térmicos** (variables macroeconómicas) y **pronósticos de aportes e hidrología** disponibles en XM.
- Revisar literatura de mercados energéticos similares como el de **Brasil** para adaptar enfoques.

---
---

## DOCUMENTO 2: Tesis_Precio_de_Bolsa.pdf

### Metadatos
| Campo | Detalle |
|-------|---------|
| **Tipo** | Tesis de Maestría |
| **Título** | Modelos de predicción del precio de la energía en bolsa en Colombia |
| **Institución** | Universidad EAFIT, Medellín |
| **Año** | 2023 |
| **Autores** | Yeison José Villarreal Marimon, Luis Armando Flores San Martín |
| **Directora** | Paula María Almonacid Hurtado, PhD |
| **Programa** | Maestría en Administración Financiera (MAF) |
| **Páginas** | 86 |

---

### Problema que aborda
- Estimar el **precio spot del kWh** en la bolsa de energía colombiana como **insumo financiero** para modelar ingresos en proyectos de generación renovable (horizonte de planificación hasta 3 años).
- La mayor capacidad instalada es hidráulica (~86.66% a 2022 según Corficolombiana, 2023) → el clima (especialmente el fenómeno ENSO/El Niño) impacta directamente los precios.
- El Mercado Energético Mayorista (MEM) opera desde 1995 mediante subasta de sobre cerrado (precio de bolsa = precio marginal del sistema).

---

### Variables utilizadas

**Fuentes de datos:**
- XM Sinergox (sinergox.xm.com.co) — variables hidrológicas del mercado eléctrico colombiano.
- NOAA (National Oceanic and Atmospheric Administration) — índice ONI para ENSO.
- **Periodo:** enero 2000 – julio 2023 (n = 8,613 datos diarios).

**Variable dependiente:**
- Valor kW (COP/kWh): media = 146.29, desv. estándar = 143.08, mín = 28.84, **máx = 1,942.69** (durante El Niño 2015–2016).

**Variables independientes evaluadas:**

| Variable | Correlación con precio (Pearson) |
|----------|:--------------------------------:|
| Aportes hídricos (%) | -0.045 |
| Aportes en Energía (kWh) | -0.094 |
| Aportes en Caudal (m³/s) | -0.019 |
| Volumen Útil Diario (Mm³) | -0.14 |
| Volumen Útil Diario Energía (kWh) | **-0.14** ← seleccionada |
| Volumen Útil Diario (%) | -0.050 |
| Volumen total (Mm³) | -0.23 |
| Volumen total Energía (kWh) | -0.074 |
| Volumen total (%) | -0.016 |
| **Fenómeno ENSO (ONI index)** | **+0.31** ← correlación más fuerte |

**Variables seleccionadas para los modelos:**
1. **Volumen Útil Diario en Energía (kWh)** — correlación negativa más fuerte con el precio.
2. **Fenómeno ENSO (índice ONI de NOAA)** — correlación positiva más fuerte con el precio.
3. **Variable dummy**: período El Niño fuerte (15 sep 2015 – 14 abr 2016).

---

### Metodología ML/estadística

| Técnica | Configuraciones probadas |
|---------|--------------------------|
| Regresión Lineal Simple | 5 modelos individuales (una variable cada uno) |
| Regresión Múltiple | Volumen Útil Diario Energía + ENSO; con y sin dummy El Niño |
| **VAR** (Vector Autorregresivo) | — |
| ARIMA | (1,1,1) |
| ARIMAX | (1,1,1), (2,1,1), (0,1,0) — con variables exógenas: Volumen Útil + ENSO |
| **SARIMAX** | (1,1,1)×(1,1,1,12); (0,1,0)×(0,0,0,0) |
| Prueba Dickey-Fuller | Verificación de estacionariedad |
| Correlación de Pearson | Selección de variables |

**Optimización:** backtesting + grid search para selección de hiperparámetros.
**Implementación:** Python.

---

### Métricas de evaluación
| Métrica | Descripción |
|---------|-------------|
| **RMSE** | Raíz del Error Cuadrático Medio — castiga outliers con mayor fuerza |
| **MAE** | Error Medio Absoluto — trata todos los errores igual |
| **R²** | Coeficiente de determinación (en regresión) |
| **Error porcentual** | RMSE% y MAE% sobre el valor medio observado |

> Nota metodológica: dado que los datos incluyen valores extremos (hasta 13.5 desviaciones estándar de la media, por El Niño 2015–2016), el RMSE arroja errores sistemáticamente mayores que el MAE en todos los modelos.

---

### Resultados cuantitativos

#### Comparación de modelos (Tabla 15 del documento)

| Modelo | RMSE (COP/kWh) | Error RMSE% | MAE (COP/kWh) | Error MAE% |
|--------|:--------------:|:-----------:|:-------------:|:----------:|
| Regresión Múltiple (sin dummy) | — | — | — | — |
| Regresión Múltiple (con dummy El Niño) | 105.93 | 72.41% | 69.37 | 47.42% |
| **VAR** | **85.01** | **17.75%** | **78.16** | **16.32%** |
| ARIMA (1,1,1) | 168.68 | 35.22% | 153.27 | 32.01% |
| ARIMAX (1,1,1) | 168.68 | 35.22% | 153.27 | 32.01% |
| ARIMAX (2,1,1) | 160.00 | 33.41% | 144.12 | 30.10% |
| ARIMAX (0,1,0) | 171.50 | 35.81% | 158.31 | 33.06% |
| **SARIMAX (1,1,1)×(1,1,1,12)** | — | — | **82.46** | **28.22%** |
| SARIMAX (0,1,0)×(0,0,0,0) | — | — | 111.96 | 26.42% |

#### Regresión múltiple — R²
| Configuración | R² |
|--------------|:--:|
| Sin dummy El Niño | 0.119 |
| **Con dummy El Niño fuerte** | **0.452** |

---

### Hallazgos principales
1. El **Fenómeno de El Niño 2015–2016** llevó el precio hasta $1,942.69/kWh (precio de escasez), el evento más extremo en los últimos 23 años de la serie. Los precios en ese período se alejaron hasta 13.5 desviaciones estándar de la media.
2. El índice **ENSO tiene la correlación positiva más fuerte** con el precio (+0.31): a mayor intensidad del fenómeno, mayor precio de bolsa.
3. El **Volumen Útil Diario en Energía** tiene la correlación negativa más fuerte: más agua almacenada → menor precio.
4. Ninguna variable por sí sola explica bien la variabilidad del precio (R² bajos en regresiones simples). La inclusión de la dummy de El Niño fuerte eleva el R² de 0.119 a **0.452**, lo que subraya la importancia de tratar este evento como un régimen especial.
5. **VAR es el mejor modelo para corto plazo** (días), con error RMSE del 17.75%.
6. **SARIMAX es el mejor modelo para mediano plazo** (meses), con error MAE del 28.22%.
7. **Regresión Múltiple con dummy** es el mejor enfoque para **largo plazo** (>1 año), útil para planificación financiera de proyectos.
8. Todos los modelos principales (Regresión Múltiple, VAR, SARIMAX) se ubican dentro de una desviación estándar de los datos, lo que equivale a una probabilidad de ocurrencia correcta del ~68%.
9. Los modelos siguen las tendencias históricas con razonable fidelidad, pero **no capturan exactamente los picos extremos**.

---

### Conclusiones relevantes para predicción day-ahead del precio de bolsa en Colombia
- Para horizonte de **días (day-ahead): VAR es el mejor modelo**, con RMSE = 85.01 COP/kWh y error del 17.75%.
- **ENSO y el volumen de reservas** son las dos variables más significativas y se deben incluir en cualquier modelo colombiano.
- Incluir una **variable dummy para períodos de El Niño fuerte** mejora sustancialmente todos los modelos, especialmente para horizontes largos.
- La **hidrología (aportes y volúmenes de embalses)** es el predictor fundamental del precio en Colombia, por la dominancia hídrica en la matriz de generación.
- Las series temporales econométricas como **VAR y SARIMAX son robustas** para este mercado sin necesidad de Deep Learning, especialmente para horizontes medios y largos.
- Para trabajos futuros: añadir **más variables exógenas del mercado** (precios de gas, carbón, demanda) y probar técnicas de **redes neuronales, SVM o regresión ridge** para mejorar el desempeño en horizontes largos.
- La selección del modelo debe hacerse en función del **horizonte de tiempo** de la predicción requerida.

---
---

## ESTADO DEL ARTE RELEVANTE (extraído de Tesis EAFIT, páginas 16–23)

### Estudios internacionales

| Autores | Año | Mercado | Metodología | Resultado clave |
|---------|-----|---------|-------------|-----------------|
| Tehrani et al. | 2022 | Europeo | ARIMA + GARCH (24h ahead) | GARCH supera a ARIMA puro |
| Shah et al. | 2021 | — | VAR con ventana móvil (MFP) + tratamiento outliers | Menores MAPE y MAE que VAR estándar |
| Zhang et al. | 2019 | — | HFS + SSA + SVM (Cuckoo Search) | Supera SARIMA, ARMA, SVM, ANN |
| Monteiro et al. | 2018 | Ibérico | PPFM (Nadaraya-Watson KDE) | MAE = 5.55 €/MWh |
| Mirakyan et al. | 2017 | — | SVR + ANN + Ridge (pronóstico compuesto) | Mejora ~22% vs. modelo individual |

### Estudios colombianos

| Autores | Año | Metodología | Resultado clave |
|---------|-----|-------------|-----------------|
| Urbano & González (= content.pdf) | 2022 | ARIMA, Prophet, SARIMAX, LSTM | **LSTM mejor modelo** (MAPE ~13.89%) |
| Villa et al. | 2023 | Análisis ondículas (CWT) — ENSO + precio + IGBX | Correlación fuerte entre ENSO y precio durante El Niño 2015–2016 |
| Muñoz et al. | 2017 | ARIMA + IGARCH | ~4% error para horizonte de 1 mes |
| Galindo | 2017 | ARIMA con 3 escenarios ENSO | Segmentación por escenario climático |
| Barrientos & Toro | 2016 | ARDL + VAR | Hidrología es predictor efectivo del precio colombiano |

---
---

## SÍNTESIS COMPARATIVA Y RECOMENDACIONES PARA EL PROYECTO

### Comparación de enfoques entre documentos

| Dimensión | content.pdf (U. Andes, 2022) | Tesis_Precio_de_Bolsa.pdf (EAFIT, 2023) |
|-----------|-----------------------------|-----------------------------------------|
| Horizonte | Day-ahead horario (24h) | Day-ahead a largo plazo (días → años) |
| Resolución objetivo | Horaria | Diaria |
| Mejor modelo | **LSTM (1 lag, por hora)** | **VAR** (corto plazo) / SARIMAX (mediano) |
| MAPE/Error mejor | ~13.89% (LSTM) | ~17.75% RMSE error (VAR) |
| Variables clave | Demanda, Gx Hidro/Termo, Reservas, Aportes | Volumen Útil Diario Energía, ENSO (ONI) |
| Variable climática | No incluida | ENSO es la más importante (+0.31) |
| Fuente datos | API XM (2020 en adelante) | Sinergox XM + NOAA (2000–2023) |
| Dummy El Niño | No usada | Mejora R² de 0.12 → 0.45 |
| Segmentación | 24 modelos por hora | Modelo único con componente estacional |

---

### Variables recomendadas para el proyecto (lista consolidada)

#### Variables de mercado (fuente: XM Sinergox)
- Precio de bolsa nacional $/MWh — variable dependiente (resolución horaria)
- Demanda del sistema (GWh)
- Vertimientos (GWh)
- Aportes hídricos (GWh) — separar cuenca Antioquia vs. resto
- Reservas/Volumen útil de embalses (GWh o kWh) — separar principales embalses
- Generación hidro en mérito y fuera de mérito (GWh)
- Generación térmica en mérito y fuera de mérito (GWh)
- Generación FNCER en mérito y fuera de mérito (GWh)

#### Variables climáticas (fuente: NOAA)
- **Índice ONI (ENSO)** — variable de alta importancia para Colombia

#### Variables de ingeniería de características
- **Dummy El Niño fuerte** (umbral históricamente: ONI ≥ 1.5 sostenido)
- Variables de calendario: mes, día, hora, día de semana, festivo
- Lags del precio de bolsa (1 y 2 datos anteriores en la misma hora)

#### Variables para trabajo futuro
- Precios de combustibles térmicos (gas natural, carbón, fuel oil)
- Pronósticos de aportes e hidrología publicados por XM/IDEAM
- Precio de bolsa de mercados similares (Brasil — CCEE)

---

### Metodología recomendada para predicción day-ahead horaria

1. **Baseline:** SARIMAX(1,0,1)(1,1,0)24 con variables exógenas (MAPE ~11.6% en U. Andes)
2. **Modelo principal:** LSTM con 1 lag anterior, 24 modelos independientes por hora
3. **Arquitectura segmentada:** entrenar un modelo por hora del día (24 modelos)
4. **Alternativa robusta corto plazo:** VAR con ventana móvil (MFP) — ver Shah et al., 2021
5. **Ensemble (trabajo futuro):** combinar SARIMAX + LSTM + SVR (mejoras de ~22% en Mirakyan et al., 2017)

### Consideraciones de diseño críticas
- El precio de bolsa colombiano tiene **memoria corta** (1–3 días): no usar más de 2–3 lags.
- Usar datos hasta **D-2** por disponibilidad operativa de la información XM.
- El **Fenómeno El Niño** es el principal disruptor del mercado: debe modelarse explícitamente (dummy, variable de régimen, o dataset separado).
- Los **periodos de alta demanda** (franja mañana y tarde) presentan mayor volatilidad y degradan los modelos; considerar pesos o pérdidas asimétricas.
- La desviación estándar del precio es casi igual a la media (muy alta volatilidad): el RMSE será sistemáticamente mayor que el MAE; **reportar ambas métricas**.
- **Prophet no es recomendable** para esta tarea.

---

## FUENTES

1. González Pérez, L.F. & Urbano Buriticá, S.N. (2022). *Predicción de corto plazo del precio de bolsa de energía en el mercado colombiano*. Tesis de Maestría, Universidad de los Andes. Archivo: `content.pdf`.

2. Villarreal Marimon, Y.J. & Flores San Martín, L.A. (2023). *Modelos de predicción del precio de la energía en bolsa en Colombia*. Tesis de Maestría, Universidad EAFIT. Archivo: `Tesis_Precio_de_Bolsa.pdf`.

3. XM S.A. E.S.P. — Base de datos Sinergox: https://sinergox.xm.com.co

4. NOAA — Índice ONI (Oceanic Niño Index): https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php
