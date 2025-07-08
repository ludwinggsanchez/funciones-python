from flask import jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


def function_three():
    """
    Esta función crea una instancia de la clase CalculadoraPrestamos y ejecuta su menú principal.
    """
    calculadora = CalculadoraPrestamos()
    calculadora.menu_principal()

class CalculadoraPrestamos:
    """
    Clase principal para análisis de préstamos con cálculos de interés compuesto.
    
    Esta clase maneja la lectura, procesamiento y análisis de datos de préstamos,
    incluyendo cálculos de interés compuesto, escenarios de simulación y
    visualizaciones.
    """
    
    def __init__(self, archivo_csv: str = "loan_data.csv"):
        """
        Inicializa la calculadora de préstamos.
        
        Args:
            archivo_csv (str): Ruta al archivo CSV con datos de préstamos
        """
        self.archivo_csv = archivo_csv
        self.datos = None
        self.resultados = None
        self.inflacion_anual = 0.03  # 3% inflación anual Colombia
        
    def cargar_datos(self) -> bool:
        """
        Carga los datos del archivo CSV y muestra información básica.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        """
        try:
            self.datos = pd.read_csv(self.archivo_csv)
            print("=" * 60)
            print("📊 DATOS DE PRÉSTAMOS CARGADOS EXITOSAMENTE")
            print("=" * 60)
            print(f"Número total de préstamos: {len(self.datos)}")
            print(f"Columnas disponibles: {list(self.datos.columns)}")
            print("\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
            print("-" * 40)
            
            # Estadísticas del monto del préstamo
            monto_stats = self.datos['Monto_Prestamo'].describe()
            print(f"Monto promedio: ${monto_stats['mean']:,.0f}")
            print(f"Monto mediano: ${monto_stats['50%']:,.0f}")
            print(f"Monto mínimo: ${monto_stats['min']:,.0f}")
            print(f"Monto máximo: ${monto_stats['max']:,.0f}")
            
            # Estadísticas de tasa de interés
            tasa_stats = self.datos['Tasa_Interes_Anual'].describe()
            print(f"\nTasa promedio: {tasa_stats['mean']:.2f}%")
            print(f"Tasa mediana: {tasa_stats['50%']:.2f}%")
            print(f"Tasa mínima: {tasa_stats['min']:.2f}%")
            print(f"Tasa máxima: {tasa_stats['max']:.2f}%")
            
            # Estadísticas de tiempo
            tiempo_stats = self.datos['Tiempo_Meses'].describe()
            print(f"\nTiempo promedio: {tiempo_stats['mean']:.0f} meses")
            print(f"Tiempo mediano: {tiempo_stats['50%']:.0f} meses")
            print(f"Tiempo mínimo: {tiempo_stats['min']:.0f} meses")
            print(f"Tiempo máximo: {tiempo_stats['max']:.0f} meses")
            
            # Distribución por propósito
            print(f"\n📋 DISTRIBUCIÓN POR PROPÓSITO:")
            print("-" * 40)
            proposito_count = self.datos['Proposito'].value_counts()
            for proposito, count in proposito_count.items():
                print(f"{proposito}: {count} préstamos")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: No se pudo encontrar el archivo '{self.archivo_csv}'")
            return False
        except Exception as e:
            print(f"❌ Error al cargar los datos: {str(e)}")
            return False
    
    def calcular_interes_compuesto(self, principal: float, tasa_anual: float, 
                                 tiempo_meses: int, frecuencia: int = 12) -> Dict:
        """
        Calcula el interés compuesto usando la fórmula A = P(1 + r/n)^(nt)
        
        Args:
            principal (float): Monto inicial del préstamo
            tasa_anual (float): Tasa de interés anual (en porcentaje)
            tiempo_meses (int): Tiempo en meses
            frecuencia (int): Frecuencia de capitalización por año (12=mensual, 4=trimestral, etc.)
            
        Returns:
            Dict: Diccionario con los resultados del cálculo
        """
        # Convertir tasa de porcentaje a decimal
        r = tasa_anual / 100
        
        # Convertir tiempo a años
        t = tiempo_meses / 12
        
        # Calcular monto final con interés compuesto
        monto_final = principal * (1 + r/frecuencia) ** (frecuencia * t)
        
        # Calcular interés total
        interes_total = monto_final - principal
        
        # Calcular interés simple para comparación
        interes_simple = principal * r * t
        monto_simple = principal + interes_simple
        
        # Diferencia entre compuesto y simple
        diferencia = interes_total - interes_simple
        
        return {
            'principal': principal,
            'tasa_anual': tasa_anual,
            'tiempo_meses': tiempo_meses,
            'tiempo_años': t,
            'frecuencia': frecuencia,
            'monto_final': monto_final,
            'interes_total': interes_total,
            'interes_simple': interes_simple,
            'monto_simple': monto_simple,
            'diferencia_compuesto_simple': diferencia,
            'frecuencia_nombre': self._obtener_nombre_frecuencia(frecuencia)
        }
    
    def _obtener_nombre_frecuencia(self, frecuencia: int) -> str:
        """Convierte la frecuencia numérica a nombre descriptivo."""
        nombres = {1: 'Anual', 2: 'Semestral', 4: 'Trimestral', 12: 'Mensual', 52: 'Semanal', 365: 'Diario'}
        return nombres.get(frecuencia, f'{frecuencia} veces por año')
    
    def calcular_pago_mensual(self, principal: float, tasa_anual: float, tiempo_meses: int) -> float:
        """
        Calcula el pago mensual usando la fórmula PMT.
        
        Args:
            principal (float): Monto del préstamo
            tasa_anual (float): Tasa de interés anual
            tiempo_meses (int): Tiempo en meses
            
        Returns:
            float: Pago mensual
        """
        if tasa_anual == 0:
            return principal / tiempo_meses
        
        tasa_mensual = tasa_anual / 100 / 12
        pago_mensual = principal * (tasa_mensual * (1 + tasa_mensual) ** tiempo_meses) / \
                      ((1 + tasa_mensual) ** tiempo_meses - 1)
        
        return pago_mensual
    
    def analizar_todos_prestamos(self) -> pd.DataFrame:
        """
        Analiza todos los préstamos del dataset y calcula métricas clave.
        
        Returns:
            pd.DataFrame: DataFrame con análisis completo de todos los préstamos
        """
        if self.datos is None:
            print("❌ Primero debe cargar los datos")
            return None
        
        resultados = []
        
        for index, row in self.datos.iterrows():
            # Calcular interés compuesto
            calculo = self.calcular_interes_compuesto(
                row['Monto_Prestamo'], 
                row['Tasa_Interes_Anual'], 
                row['Tiempo_Meses']
            )
            
            # Calcular pago mensual
            pago_mensual = self.calcular_pago_mensual(
                row['Monto_Prestamo'], 
                row['Tasa_Interes_Anual'], 
                row['Tiempo_Meses']
            )
            
            # Calcular costo total
            costo_total = pago_mensual * row['Tiempo_Meses']
            
            # Crear registro de resultados
            resultado = {
                'Nombre': row['Nombre'],
                'Edad': row['Edad'],
                'Proposito': row['Proposito'],
                'Monto_Original': row['Monto_Prestamo'],
                'Tasa_Interes': row['Tasa_Interes_Anual'],
                'Tiempo_Meses': row['Tiempo_Meses'],
                'Pago_Mensual': pago_mensual,
                'Costo_Total': costo_total,
                'Interes_Total': costo_total - row['Monto_Prestamo'],
                'Monto_Final_Compuesto': calculo['monto_final'],
                'Diferencia_Simple_Compuesto': calculo['diferencia_compuesto_simple'],
                'Porcentaje_Interes': (costo_total - row['Monto_Prestamo']) / row['Monto_Prestamo'] * 100
            }
            
            resultados.append(resultado)
        
        self.resultados = pd.DataFrame(resultados)
        return self.resultados
    
    def mostrar_ejemplos_detallados(self, n_ejemplos: int = 3):
        """
        Muestra cálculos paso a paso para los primeros n préstamos.
        
        Args:
            n_ejemplos (int): Número de ejemplos a mostrar
        """
        if self.datos is None:
            print("❌ Primero debe cargar los datos")
            return
        
        print("=" * 80)
        print("🔍 EJEMPLOS DE CÁLCULOS PASO A PASO")
        print("=" * 80)
        
        for i in range(min(n_ejemplos, len(self.datos))):
            row = self.datos.iloc[i]
            print(f"\n📋 EJEMPLO {i+1}: {row['Nombre']}")
            print("-" * 60)
            
            # Datos del préstamo
            print(f"Propósito: {row['Proposito']}")
            print(f"Monto del préstamo: ${row['Monto_Prestamo']:,.0f}")
            print(f"Tasa de interés anual: {row['Tasa_Interes_Anual']}%")
            print(f"Tiempo: {row['Tiempo_Meses']} meses ({row['Tiempo_Meses']/12:.1f} años)")
            
            # Cálculos paso a paso
            calculo = self.calcular_interes_compuesto(
                row['Monto_Prestamo'], 
                row['Tasa_Interes_Anual'], 
                row['Tiempo_Meses']
            )
            
            print("\n🧮 CÁLCULOS:")
            print(f"Fórmula: A = P(1 + r/n)^(nt)")
            print(f"Donde:")
            print(f"  P = ${calculo['principal']:,.0f} (principal)")
            print(f"  r = {calculo['tasa_anual']/100:.4f} (tasa decimal)")
            print(f"  n = {calculo['frecuencia']} (capitalización mensual)")
            print(f"  t = {calculo['tiempo_años']:.2f} años")
            
            print(f"\nResultado:")
            print(f"  A = ${calculo['principal']:,.0f} × (1 + {calculo['tasa_anual']/100:.4f}/12)^(12 × {calculo['tiempo_años']:.2f})")
            print(f"  A = ${calculo['monto_final']:,.0f}")
            
            # Pago mensual
            pago_mensual = self.calcular_pago_mensual(
                row['Monto_Prestamo'], 
                row['Tasa_Interes_Anual'], 
                row['Tiempo_Meses']
            )
            
            print(f"\n💰 RESULTADOS FINANCIEROS:")
            print(f"  Pago mensual: ${pago_mensual:,.0f}")
            print(f"  Costo total: ${pago_mensual * row['Tiempo_Meses']:,.0f}")
            print(f"  Interés total: ${(pago_mensual * row['Tiempo_Meses']) - row['Monto_Prestamo']:,.0f}")
            print(f"  Porcentaje de interés: {((pago_mensual * row['Tiempo_Meses']) - row['Monto_Prestamo']) / row['Monto_Prestamo'] * 100:.1f}%")
            
            # Comparación con interés simple
            print(f"\n📊 COMPARACIÓN CON INTERÉS SIMPLE:")
            print(f"  Interés simple: ${calculo['interes_simple']:,.0f}")
            print(f"  Interés compuesto: ${calculo['interes_total']:,.0f}")
            print(f"  Diferencia: ${calculo['diferencia_compuesto_simple']:,.0f}")
    
    def escenario_que_pasaria_si(self, cambios_tasa: List[float] = [-2, -1, 1, 2]):
        """
        Simula cambios en las tasas de interés para todos los préstamos.
        
        Args:
            cambios_tasa (List[float]): Lista de cambios en puntos porcentuales
        """
        if self.datos is None:
            print("❌ Primero debe cargar los datos")
            return
        
        print("=" * 80)
        print("🔮 ANÁLISIS DE ESCENARIOS: '¿QUÉ PASARÍA SI?'")
        print("=" * 80)
        
        resultados_escenarios = []
        
        for index, row in self.datos.iterrows():
            tasa_original = row['Tasa_Interes_Anual']
            pago_original = self.calcular_pago_mensual(
                row['Monto_Prestamo'], tasa_original, row['Tiempo_Meses']
            )
            costo_original = pago_original * row['Tiempo_Meses']
            
            escenario = {
                'Nombre': row['Nombre'],
                'Tasa_Original': tasa_original,
                'Costo_Original': costo_original
            }
            
            for cambio in cambios_tasa:
                nueva_tasa = max(0.1, tasa_original + cambio)  # Mínimo 0.1%
                nuevo_pago = self.calcular_pago_mensual(
                    row['Monto_Prestamo'], nueva_tasa, row['Tiempo_Meses']
                )
                nuevo_costo = nuevo_pago * row['Tiempo_Meses']
                diferencia = nuevo_costo - costo_original
                
                escenario[f'Tasa_{cambio:+.0f}%'] = nueva_tasa
                escenario[f'Costo_{cambio:+.0f}%'] = nuevo_costo
                escenario[f'Diferencia_{cambio:+.0f}%'] = diferencia
            
            resultados_escenarios.append(escenario)
        
        df_escenarios = pd.DataFrame(resultados_escenarios)
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE IMPACTO PROMEDIO:")
        print("-" * 50)
        for cambio in cambios_tasa:
            impacto_promedio = df_escenarios[f'Diferencia_{cambio:+.0f}%'].mean()
            print(f"Cambio de {cambio:+.0f}%: ${impacto_promedio:+,.0f} promedio")
        
        # Mostrar los 5 préstamos más afectados
        print(f"\n🎯 TOP 5 PRÉSTAMOS MÁS AFECTADOS POR AUMENTO DE +2%:")
        print("-" * 60)
        top_afectados = df_escenarios.nlargest(5, 'Diferencia_+2%')
        for _, row in top_afectados.iterrows():
            print(f"{row['Nombre']}: ${row['Diferencia_+2%']:+,.0f}")
        
        return df_escenarios
    
    def escenario_prepago(self, porcentaje_prepago: float = 0.10):
        """
        Calcula el ahorro si se hacen pagos adicionales.
        
        Args:
            porcentaje_prepago (float): Porcentaje adicional a pagar mensualmente
        """
        if self.datos is None:
            print("❌ Primero debe cargar los datos")
            return
        
        print("=" * 80)
        print(f"💰 ESCENARIO DE PREPAGO ({porcentaje_prepago*100:.0f}% ADICIONAL MENSUAL)")
        print("=" * 80)
        
        resultados_prepago = []
        
        for index, row in self.datos.iterrows():
            # Pago normal
            pago_normal = self.calcular_pago_mensual(
                row['Monto_Prestamo'], row['Tasa_Interes_Anual'], row['Tiempo_Meses']
            )
            costo_normal = pago_normal * row['Tiempo_Meses']
            
            # Pago con prepago
            pago_con_prepago = pago_normal * (1 + porcentaje_prepago)
            
            # Calcular nuevo tiempo y costo con prepago
            principal = row['Monto_Prestamo']
            tasa_mensual = row['Tasa_Interes_Anual'] / 100 / 12
            
            # Simular pagos con prepago
            saldo = principal
            mes = 0
            while saldo > 0 and mes < row['Tiempo_Meses']:
                interes_mes = saldo * tasa_mensual
                principal_mes = min(pago_con_prepago - interes_mes, saldo)
                saldo -= principal_mes
                mes += 1
            
            costo_con_prepago = pago_con_prepago * mes
            ahorro = costo_normal - costo_con_prepago
            ahorro_tiempo = row['Tiempo_Meses'] - mes
            
            resultado = {
                'Nombre': row['Nombre'],
                'Pago_Normal': pago_normal,
                'Pago_Con_Prepago': pago_con_prepago,
                'Tiempo_Normal': row['Tiempo_Meses'],
                'Tiempo_Con_Prepago': mes,
                'Costo_Normal': costo_normal,
                'Costo_Con_Prepago': costo_con_prepago,
                'Ahorro_Dinero': ahorro,
                'Ahorro_Tiempo_Meses': ahorro_tiempo
            }
            
            resultados_prepago.append(resultado)
        
        df_prepago = pd.DataFrame(resultados_prepago)
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DE AHORROS:")
        print("-" * 40)
        ahorro_promedio = df_prepago['Ahorro_Dinero'].mean()
        tiempo_promedio = df_prepago['Ahorro_Tiempo_Meses'].mean()
        print(f"Ahorro promedio: ${ahorro_promedio:,.0f}")
        print(f"Tiempo ahorrado promedio: {tiempo_promedio:.1f} meses")
        
        # Top 5 ahorros
        print(f"\n🎯 TOP 5 MAYORES AHORROS:")
        print("-" * 40)
        top_ahorros = df_prepago.nlargest(5, 'Ahorro_Dinero')
        for _, row in top_ahorros.iterrows():
            print(f"{row['Nombre']}: ${row['Ahorro_Dinero']:,.0f} ({row['Ahorro_Tiempo_Meses']:.0f} meses)")
        
        return df_prepago
    
    def escenario_refinanciamiento(self, nueva_tasa: float = 3.5):
        """
        Compara el préstamo actual vs refinanciamiento con nueva tasa.
        
        Args:
            nueva_tasa (float): Nueva tasa de interés para refinanciamiento
        """
        if self.datos is None:
            print("❌ Primero debe cargar los datos")
            return
        
        print("=" * 80)
        print(f"🔄 ANÁLISIS DE REFINANCIAMIENTO (Nueva tasa: {nueva_tasa}%)")
        print("=" * 80)
        
        resultados_refi = []
        
        for index, row in self.datos.iterrows():
            # Costo actual
            pago_actual = self.calcular_pago_mensual(
                row['Monto_Prestamo'], row['Tasa_Interes_Anual'], row['Tiempo_Meses']
            )
            costo_actual = pago_actual * row['Tiempo_Meses']
            
            # Costo con refinanciamiento
            pago_nuevo = self.calcular_pago_mensual(
                row['Monto_Prestamo'], nueva_tasa, row['Tiempo_Meses']
            )
            costo_nuevo = pago_nuevo * row['Tiempo_Meses']
            
            ahorro = costo_actual - costo_nuevo
            porcentaje_ahorro = (ahorro / costo_actual) * 100
            
            resultado = {
                'Nombre': row['Nombre'],
                'Tasa_Actual': row['Tasa_Interes_Anual'],
                'Tasa_Nueva': nueva_tasa,
                'Pago_Actual': pago_actual,
                'Pago_Nuevo': pago_nuevo,
                'Costo_Actual': costo_actual,
                'Costo_Nuevo': costo_nuevo,
                'Ahorro': ahorro,
                'Porcentaje_Ahorro': porcentaje_ahorro,
                'Conviene_Refinanciar': ahorro > 0
            }
            
            resultados_refi.append(resultado)
        
        df_refi = pd.DataFrame(resultados_refi)
        
        # Mostrar resumen
        conviene_count = df_refi['Conviene_Refinanciar'].sum()
        total_count = len(df_refi)
        
        print(f"\n📊 RESUMEN DE REFINANCIAMIENTO:")
        print("-" * 45)
        print(f"Préstamos que conviene refinanciar: {conviene_count}/{total_count}")
        print(f"Ahorro total potencial: ${df_refi['Ahorro'].sum():,.0f}")
        print(f"Ahorro promedio: ${df_refi['Ahorro'].mean():,.0f}")
        
        # Mejores oportunidades
        if conviene_count > 0:
            print(f"\n🎯 MEJORES OPORTUNIDADES DE REFINANCIAMIENTO:")
            print("-" * 50)
            mejores = df_refi[df_refi['Conviene_Refinanciar']].nlargest(5, 'Ahorro')
            for _, row in mejores.iterrows():
                print(f"{row['Nombre']}: ${row['Ahorro']:,.0f} ({row['Porcentaje_Ahorro']:.1f}%)")
        
        return df_refi
    
    def crear_visualizaciones(self):
        """Crea todas las visualizaciones solicitadas."""
        if self.resultados is None:
            print("❌ Primero debe analizar los préstamos")
            return
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Gráfico de barras: Costo total por persona
        plt.subplot(2, 3, 1)
        top_10 = self.resultados.nlargest(10, 'Costo_Total')
        plt.barh(range(len(top_10)), top_10['Costo_Total'])
        plt.yticks(range(len(top_10)), [name.split()[0] for name in top_10['Nombre']])
        plt.xlabel('Costo Total ($)')
        plt.title('Top 10 Préstamos por Costo Total')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 2. Histograma: Distribución de tasas de interés
        plt.subplot(2, 3, 2)
        plt.hist(self.datos['Tasa_Interes_Anual'], bins=15, alpha=0.7, color='skyblue')
        plt.xlabel('Tasa de Interés Anual (%)')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de Tasas de Interés')
        
        # 3. Scatter plot: Monto vs Costo Total
        plt.subplot(2, 3, 3)
        plt.scatter(self.resultados['Monto_Original'], self.resultados['Costo_Total'], 
                   alpha=0.7, s=50)
        plt.xlabel('Monto Original ($)')
        plt.ylabel('Costo Total ($)')
        plt.title('Relación Monto Original vs Costo Total')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 4. Gráfico de barras: Costo por propósito
        plt.subplot(2, 3, 4)
        costo_por_proposito = self.resultados.groupby('Proposito')['Costo_Total'].mean()
        plt.bar(range(len(costo_por_proposito)), costo_por_proposito.values)
        plt.xticks(range(len(costo_por_proposito)), 
                  [prop.replace(' ', '\n') for prop in costo_por_proposito.index], 
                  rotation=45, ha='right')
        plt.ylabel('Costo Promedio ($)')
        plt.title('Costo Promedio por Propósito')
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 5. Evolución del saldo para los primeros 5 préstamos
        plt.subplot(2, 3, 5)
        for i in range(min(5, len(self.datos))):
            row = self.datos.iloc[i]
            saldo = row['Monto_Prestamo']
            pago_mensual = self.calcular_pago_mensual(
                row['Monto_Prestamo'], row['Tasa_Interes_Anual'], row['Tiempo_Meses']
            )
            tasa_mensual = row['Tasa_Interes_Anual'] / 100 / 12
            
            saldos = [saldo]
            for mes in range(row['Tiempo_Meses']):
                interes = saldo * tasa_mensual
                principal = pago_mensual - interes
                saldo = max(0, saldo - principal)
                saldos.append(saldo)
            
            plt.plot(saldos, label=row['Nombre'].split()[0], linewidth=2)
        
        plt.xlabel('Mes')
        plt.ylabel('Saldo Pendiente ($)')
        plt.title('Evolución del Saldo - Primeros 5 Préstamos')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 6. Comparación Interés Simple vs Compuesto
        plt.subplot(2, 3, 6)
        diferencias = []
        nombres = []
        for index, row in self.datos.iterrows():
            calculo = self.calcular_interes_compuesto(
                row['Monto_Prestamo'], row['Tasa_Interes_Anual'], row['Tiempo_Meses']
            )
            diferencias.append(calculo['diferencia_compuesto_simple'])
            nombres.append(row['Nombre'].split()[0])
        
        plt.barh(range(len(diferencias)), diferencias)
        plt.yticks(range(len(diferencias)), nombres)
        plt.xlabel('Diferencia Compuesto - Simple ($)')
        plt.title('Diferencia: Interés Compuesto vs Simple')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        
        plt.tight_layout()
        plt.show()
        
        print("📊 Visualizaciones generadas exitosamente")
    
    def exportar_resultados(self, archivo_salida: str = "resultados_analisis.csv"):
        """
        Exporta todos los resultados a un archivo CSV.
        
        Args:
            archivo_salida (str): Nombre del archivo de salida
        """
        if self.resultados is None:
            print("❌ Primero debe analizar los préstamos")
            return
        
        try:
            self.resultados.to_csv(archivo_salida, index=False)
            print(f"✅ Resultados exportados exitosamente a '{archivo_salida}'")
            print(f"📁 Archivo contiene {len(self.resultados)} registros con {len(self.resultados.columns)} columnas")
        except Exception as e:
            print(f"❌ Error al exportar: {str(e)}")
    
    def generar_resumen_ejecutivo(self):
        """Genera un resumen ejecutivo con insights clave."""
        if self.resultados is None:
            print("❌ Primero debe analizar los préstamos")
            return
        
        print("=" * 80)
        print("📋 RESUMEN EJECUTIVO - ANÁLISIS DE PRÉSTAMOS")
        print("=" * 80)
        
        # Estadísticas generales
        total_prestamos = len(self.resultados)
        monto_total = self.resultados['Monto_Original'].sum()
        costo_total = self.resultados['Costo_Total'].sum()
        interes_total = self.resultados['Interes_Total'].sum()
        
        print(f"\n📊 ESTADÍSTICAS GENERALES:")
        print("-" * 40)
        print(f"Total de préstamos analizados: {total_prestamos}")
        print(f"Monto total prestado: ${monto_total:,.0f}")
        print(f"Costo total de todos los préstamos: ${costo_total:,.0f}")
        print(f"Interés total a pagar: ${interes_total:,.0f}")
        print(f"Tasa de interés promedio: {self.datos['Tasa_Interes_Anual'].mean():.2f}%")
        
        # Análisis por propósito
        print(f"\n🎯 ANÁLISIS POR PROPÓSITO:")
        print("-" * 40)
        analisis_proposito = self.resultados.groupby('Proposito').agg({
            'Monto_Original': ['count', 'sum', 'mean'],
            'Tasa_Interes': 'mean',
            'Costo_Total': 'sum'
        }).round(2)
        
        for proposito in analisis_proposito.index:
            count = analisis_proposito.loc[proposito, ('Monto_Original', 'count')]
            suma = analisis_proposito.loc[proposito, ('Monto_Original', 'sum')]
            tasa = analisis_proposito.loc[proposito, ('Tasa_Interes', 'mean')]
            print(f"{proposito}: {count} préstamos, ${suma:,.0f} total, {tasa:.1f}% tasa promedio")
        
        # Préstamos más costosos
        print(f"\n💰 PRÉSTAMOS MÁS COSTOSOS:")
        print("-" * 40)
        top_costosos = self.resultados.nlargest(3, 'Costo_Total')
        for _, row in top_costosos.iterrows():
            print(f"{row['Nombre']}: ${row['Costo_Total']:,.0f} ({row['Proposito']})")
        
        # Oportunidades de ahorro
        print(f"\n💡 OPORTUNIDADES DE AHORRO:")
        print("-" * 40)
        tasas_altas = self.resultados[self.resultados['Tasa_Interes'] > 7.0]
        if len(tasas_altas) > 0:
            print(f"• {len(tasas_altas)} préstamos con tasas > 7% podrían beneficiarse de refinanciamiento")
            ahorro_potencial = tasas_altas['Costo_Total'].sum() * 0.15  # Estimación 15% ahorro
            print(f"• Ahorro potencial estimado: ${ahorro_potencial:,.0f}")
        
        tiempos_largos = self.resultados[self.resultados['Tiempo_Meses'] > 60]
        if len(tiempos_largos) > 0:
            print(f"• {len(tiempos_largos)} préstamos a largo plazo podrían beneficiarse de prepagos")
        
        print(f"\n🎯 RECOMENDACIONES:")
        print("-" * 40)
        print("• Considerar refinanciamiento para préstamos con tasas > 7%")
        print("• Evaluar prepagos para préstamos a largo plazo")
        print("• Revisar opciones de consolidación para múltiples préstamos")
        print("• Monitorear cambios en tasas de interés del mercado")
    
    def calculadora_interactiva(self):
        """Calculadora interactiva para que el usuario ingrese sus propios valores."""
        print("=" * 80)
        print("🧮 CALCULADORA INTERACTIVA DE PRÉSTAMOS")
        print("=" * 80)
        
        try:
            # Solicitar datos al usuario
            print("\n📝 Ingrese los datos del préstamo:")
            monto = float(input("Monto del préstamo ($): "))
            tasa = float(input("Tasa de interés anual (%): "))
            tiempo = int(input("Tiempo en meses: "))
            
            # Validar datos
            if monto <= 0 or tasa < 0 or tiempo <= 0:
                print("❌ Error: Todos los valores deben ser positivos")
                return
            
            # Calcular resultados
            calculo = self.calcular_interes_compuesto(monto, tasa, tiempo)
            pago_mensual = self.calcular_pago_mensual(monto, tasa, tiempo)
            costo_total = pago_mensual * tiempo
            
            # Mostrar resultados
            print("\n" + "=" * 60)
            print("📊 RESULTADOS DE SU PRÉSTAMO")
            print("=" * 60)
            
            print(f"\n💰 INFORMACIÓN DEL PRÉSTAMO:")
            print(f"Monto solicitado: ${monto:,.0f}")
            print(f"Tasa de interés: {tasa}% anual")
            print(f"Plazo: {tiempo} meses ({tiempo/12:.1f} años)")
            
            print(f"\n📈 CÁLCULOS FINANCIEROS:")
            print(f"Pago mensual: ${pago_mensual:,.0f}")
            print(f"Costo total: ${costo_total:,.0f}")
            print(f"Interés total: ${costo_total - monto:,.0f}")
            print(f"Porcentaje de interés: {((costo_total - monto) / monto) * 100:.1f}%")
            
            print(f"\n🔍 ANÁLISIS DETALLADO:")
            print(f"Monto con interés compuesto: ${calculo['monto_final']:,.0f}")
            print(f"Diferencia vs interés simple: ${calculo['diferencia_compuesto_simple']:,.0f}")
            
            # Comparar con diferentes frecuencias
            print(f"\n📊 COMPARACIÓN POR FRECUENCIA DE CAPITALIZACIÓN:")
            frecuencias = [1, 2, 4, 12]
            for freq in frecuencias:
                calc_freq = self.calcular_interes_compuesto(monto, tasa, tiempo, freq)
                print(f"{calc_freq['frecuencia_nombre']}: ${calc_freq['monto_final']:,.0f}")
            
        except ValueError:
            print("❌ Error: Por favor ingrese valores numéricos válidos")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def menu_principal(self):
        """Menú principal interactivo."""
        print("=" * 80)
        print("🏦 CALCULADORA DE INTERÉS COMPUESTO - ANÁLISIS DE PRÉSTAMOS")
        print("=" * 80)
        
        while True:
            print("\n📋 MENÚ PRINCIPAL:")
            print("-" * 40)
            print("1. 📊 Cargar y analizar archivo de préstamos")
            print("2. 🧮 Calcular interés compuesto para todos")
            print("3. 🔮 Escenarios de simulación")
            print("4. 📈 Generar visualizaciones")
            print("5. 📁 Exportar resultados")
            print("6. 🧮 Calculadora interactiva")
            print("7. 📋 Resumen ejecutivo")
            print("8. 🔍 Ejemplos detallados")
            print("0. 🚪 Salir")
            
            try:
                opcion = input("\nSeleccione una opción: ")
                
                if opcion == "1":
                    if self.cargar_datos():
                        self.analizar_todos_prestamos()
                
                elif opcion == "2":
                    if self.datos is not None:
                        self.analizar_todos_prestamos()
                        print("✅ Análisis completado")
                    else:
                        print("❌ Primero debe cargar los datos (opción 1)")
                
                elif opcion == "3":
                    if self.datos is not None:
                        print("\n🔮 ESCENARIOS DISPONIBLES:")
                        print("1. ¿Qué pasaría si cambian las tasas?")
                        print("2. Escenario de prepago")
                        print("3. Análisis de refinanciamiento")
                        
                        sub_opcion = input("\nSeleccione un escenario: ")
                        if sub_opcion == "1":
                            self.escenario_que_pasaria_si()
                        elif sub_opcion == "2":
                            self.escenario_prepago()
                        elif sub_opcion == "3":
                            self.escenario_refinanciamiento()
                    else:
                        print("❌ Primero debe cargar los datos (opción 1)")
                
                elif opcion == "4":
                    if self.resultados is not None:
                        self.crear_visualizaciones()
                    else:
                        print("❌ Primero debe analizar los préstamos (opción 2)")
                
                elif opcion == "5":
                    if self.resultados is not None:
                        archivo = input("Nombre del archivo (o Enter para 'resultados_analisis.csv'): ")
                        if not archivo:
                            archivo = "resultados_analisis.csv"
                        self.exportar_resultados(archivo)
                    else:
                        print("❌ Primero debe analizar los préstamos (opción 2)")
                
                elif opcion == "6":
                    self.calculadora_interactiva()
                
                elif opcion == "7":
                    self.generar_resumen_ejecutivo()
                
                elif opcion == "8":
                    self.mostrar_ejemplos_detallados()
                
                elif opcion == "0":
                    print("\n👋 ¡Gracias por usar la Calculadora de Préstamos!")
                    print("🎓 Esperamos que esta herramienta haya sido educativa")
                    break
                
                else:
                    print("❌ Opción no válida. Por favor seleccione una opción del menú.")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def main():
    """Función principal del programa."""
    calculadora = CalculadoraPrestamos()
    calculadora.menu_principal()

    if __name__ == "__main__":
        main()

        return jsonify({'message': 'This is function three.'})
