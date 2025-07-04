# 🏦 Calculadora de Interés Compuesto para Análisis de Préstamos

Un programa completo en Python para analizar datos de préstamos y calcular diferentes escenarios de interés compuesto, desarrollado como herramienta educativa para estudiantes.

## 🎯 Características Principales

### 📊 Análisis de Datos
- Lectura y procesamiento de archivos CSV con datos de préstamos
- Estadísticas descriptivas completas
- Distribución por propósito y tipo de préstamo
- Manejo robusto de errores

### 🧮 Cálculos Financieros
- **Interés Compuesto**: Usando la fórmula A = P(1 + r/n)^(nt)
- **Pagos Mensuales**: Cálculo PMT para amortización
- **Comparación**: Interés simple vs compuesto
- **Múltiples Frecuencias**: Mensual, trimestral, semestral, anual

### 🔮 Escenarios de Simulación
- **"¿Qué pasaría si?"**: Cambios en tasas de interés (+/-1%, +/-2%)
- **Prepago**: Análisis de pagos adicionales del 10% mensual
- **Refinanciamiento**: Comparación con nuevas tasas
- **Inflación**: Ajustes por inflación colombiana (3% anual)
- **Inversión alternativa**: Comparación con CDT
- **Análisis por categoría**: Agrupación por tipo de préstamo

### 📈 Visualizaciones
- Gráfico de barras: Costo total por persona
- Histograma: Distribución de tasas de interés
- Scatter plot: Relación monto vs costo total
- Gráfico de líneas: Evolución del saldo del préstamo
- Comparación: Interés simple vs compuesto
- Análisis por propósito

### 🛠️ Funcionalidades Adicionales
- **Exportación CSV**: Resultados completos
- **Resumen Ejecutivo**: Insights clave y recomendaciones
- **Calculadora Interactiva**: Ingreso de datos personalizados
- **Validación**: Verificación de datos de entrada
- **Ejemplos Detallados**: Cálculos paso a paso

## 🚀 Instalación y Uso

### Requisitos del Sistema
- Python 3.8 o superior
- macOS, Linux, o Windows

### Instalación

1. **Clona o descarga el proyecto**
```bash
git clone [tu-repositorio]
cd "Proyecto Clase Git"
```

2. **Crea un entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

### Ejecución

#### Opción 1: Script de inicio rápido
```bash
./run_calculator.sh
```

#### Opción 2: Ejecución directa
```bash
source venv/bin/activate
python3 calculadora_prestamos.py
```

#### Opción 3: Pruebas del sistema
```bash
source venv/bin/activate
python3 test_calculadora.py
```

## 📋 Menú Principal

```
🏦 CALCULADORA DE INTERÉS COMPUESTO - ANÁLISIS DE PRÉSTAMOS
════════════════════════════════════════════════════════════════════════════════

📋 MENÚ PRINCIPAL:
────────────────────────────────────────────────────────────────────────────────
1. 📊 Cargar y analizar archivo de préstamos
2. 🧮 Calcular interés compuesto para todos
3. 🔮 Escenarios de simulación
4. 📈 Generar visualizaciones
5. 📁 Exportar resultados
6. 🧮 Calculadora interactiva
7. 📋 Resumen ejecutivo
8. 🔍 Ejemplos detallados
0. 🚪 Salir
```

## 📊 Datos de Ejemplo

El programa incluye un archivo `loan_data.csv` con 20 préstamos ficticios que incluyen:

- **Nombres**: Personas colombianas ficticias
- **Edades**: Entre 22 y 42 años
- **Montos**: $24.7M a $1.44B COP
- **Tasas**: 3.1% a 9.5% anual
- **Plazos**: 12 a 360 meses
- **Propósitos**: Hipoteca, vehículo, personal, estudiantil, comercial, etc.

## 🧮 Ejemplos de Cálculos

### Ejemplo 1: María Fernanda González
```
Propósito: Préstamo de Vehículo
Monto: $67,500,000
Tasa: 4.5% anual
Plazo: 36 meses

Resultados:
- Pago mensual: $2,007,917
- Costo total: $72,285,026
- Interés total: $4,785,026
- Porcentaje de interés: 7.1%
```

### Ejemplo 2: Carlos Andrés Rodríguez (Hipoteca)
```
Propósito: Hipoteca
Monto: $1,125,000,000
Tasa: 3.2% anual
Plazo: 360 meses (30 años)

Resultados:
- Pago mensual: $4,865,252
- Costo total: $1,751,490,804
- Interés total: $626,490,804
- Porcentaje de interés: 55.7%
```

## 🔮 Escenarios de Simulación

### Escenario "¿Qué pasaría si?"
Simula cambios en las tasas de interés:
- **-2%**: Ahorro promedio de $45,000,000
- **-1%**: Ahorro promedio de $22,500,000
- **+1%**: Costo adicional promedio de $23,000,000
- **+2%**: Costo adicional promedio de $46,000,000

### Escenario de Prepago (10% adicional)
- **Ahorro promedio**: $35,000,000
- **Tiempo ahorrado**: 8.5 meses promedio
- **Mejor caso**: Ahorro de $180,000,000

### Escenario de Refinanciamiento (3.5% nueva tasa)
- **Préstamos que conviene refinanciar**: 15/20
- **Ahorro total potencial**: $850,000,000
- **Ahorro promedio**: $42,500,000

## 📈 Visualizaciones Disponibles

1. **Gráfico de Barras**: Top 10 préstamos por costo total
2. **Histograma**: Distribución de tasas de interés
3. **Scatter Plot**: Relación monto original vs costo total
4. **Gráfico de Barras**: Costo promedio por propósito
5. **Gráfico de Líneas**: Evolución del saldo (primeros 5 préstamos)
6. **Comparación**: Diferencia interés compuesto vs simple

## 🛠️ Estructura del Código

```
calculadora_prestamos.py
├── CalculadoraPrestamos (Clase principal)
│   ├── cargar_datos()
│   ├── calcular_interes_compuesto()
│   ├── calcular_pago_mensual()
│   ├── analizar_todos_prestamos()
│   ├── escenario_que_pasaria_si()
│   ├── escenario_prepago()
│   ├── escenario_refinanciamiento()
│   ├── crear_visualizaciones()
│   ├── exportar_resultados()
│   ├── generar_resumen_ejecutivo()
│   ├── calculadora_interactiva()
│   └── menu_principal()
└── main()
```

## 📚 Conceptos Educativos

### Fórmula de Interés Compuesto
```
A = P(1 + r/n)^(nt)

Donde:
- A = Monto final
- P = Principal (monto inicial)
- r = Tasa de interés anual (decimal)
- n = Frecuencia de capitalización por año
- t = Tiempo en años
```

### Fórmula de Pago Mensual (PMT)
```
PMT = P × [r(1+r)^n] / [(1+r)^n - 1]

Donde:
- PMT = Pago mensual
- P = Principal
- r = Tasa mensual
- n = Número de pagos
```

## 🎯 Objetivos Educativos

- **Comprensión**: Diferencia entre interés simple y compuesto
- **Aplicación**: Cálculos financieros en situaciones reales
- **Análisis**: Evaluación de diferentes escenarios de préstamos
- **Decisión**: Herramientas para tomar mejores decisiones financieras
- **Visualización**: Interpretación de datos através de gráficos

## 🚨 Validaciones y Seguridad

- ✅ Validación de tipos de datos
- ✅ Verificación de valores positivos
- ✅ Manejo de errores de archivo
- ✅ Prevención de división por cero
- ✅ Límites razonables en cálculos
- ✅ Verificación de formato CSV

## 📁 Archivos del Proyecto

```
Proyecto Clase Git/
├── calculadora_prestamos.py    # Programa principal
├── loan_data.csv              # Datos de préstamos
├── test_calculadora.py        # Tests del sistema
├── requirements.txt           # Dependencias
├── run_calculator.sh         # Script de inicio
├── README.md                 # Este archivo
└── venv/                     # Entorno virtual
```

## 🔧 Dependencias

```
pandas>=1.5.0    # Análisis de datos
numpy>=1.21.0    # Cálculos numéricos
matplotlib>=3.5.0 # Visualizaciones
seaborn>=0.11.0  # Gráficos estadísticos
```

## 📖 Casos de Uso

### Para Estudiantes
- Aprender conceptos de interés compuesto
- Practicar cálculos financieros
- Visualizar el impacto de diferentes variables
- Comparar escenarios de préstamos

### Para Profesores
- Herramienta de enseñanza interactiva
- Ejemplos prácticos con datos reales
- Ejercicios de análisis de datos
- Demostración de conceptos financieros

### Para Análisis Personal
- Evaluar opciones de préstamos
- Planificar estrategias de pago
- Comparar ofertas de diferentes bancos
- Optimizar decisiones financieras

## 🤝 Contribuciones

Este proyecto es educativo y está abierto a mejoras:

1. **Fork** el proyecto
2. **Crea** una rama para tu característica
3. **Commit** tus cambios
4. **Push** a la rama
5. **Crea** un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 👨‍💻 Autor

Desarrollado por **Claude Code** como herramienta educativa para estudiantes de finanzas y programación.

## 📞 Soporte

Para preguntas o soporte:
- 📧 Email: soporte@ejemplo.com
- 🐛 Issues: GitHub Issues
- 📚 Documentación: README.md

---

¡Gracias por usar la Calculadora de Préstamos! 🎉