# Sistema de Alertas Académicas – Q3 2025

Este proyecto es una aplicación desarrollada en **Python** utilizando **Tkinter** y **Pandas**.  
Su objetivo es ayudar a docentes a monitorear rápidamente el rendimiento académico de sus estudiantes mediante la búsqueda por nombre, la visualización de calificaciones y la generación de alertas automáticas.

---

##  Objetivo del Proyecto

Facilitar el trabajo docente permitiendo:
- Buscar estudiantes por nombre.
- Ver sus calificaciones por **fecha**, **materia** y **tipo de evaluación**.
- Identificar notas por debajo del **60%**.
- Mostrar alertas automáticas cuando el estudiante presenta riesgo académico.
- Calcular el promedio general del alumno.
- Marcar visualmente cada registro según su rendimiento.

---

##  Descripción del Dataset

El archivo `dataset_notas_22_alumnos.xlsx` contiene:
- **22 estudiantes** del 6° grado.
- Materias: ELA, Science, Math, Social Studies, Technology, World History.
- Campos incluidos:
  - `Nombre`
  - `Grado`
  - `Materia`
  - `Periodo`
  - `Fecha`
  - `Tipo` (Tarea, Proceso, Examen)
  - `Puntaje`
  - `Estado` (Calificado / Pendiente)

El dataset se utiliza directamente en la aplicación para generar resultados en tiempo real.

---

## Estructura y Funcionamiento

1. El docente escribe el **nombre completo del alumno**.
2. La aplicación filtra y muestra:
   - Fecha de la evaluación  
   - Materia  
   - Tipo  
   - Puntaje  
3. Los puntajes se colorean según rendimiento:
   - Rojo **Menos de 60%**  
   - Amarillo **Entre 60% y 69%**  
   - Verde **70% o más**  
   - Blanco **Pendiente**  
4. Se calcula automáticamente el **promedio del estudiante**.
5. Si el alumno tiene notas debajo del 60% → aparece una **Alerta Académica**.

---

## Alertas Generadas por la App

La aplicación detecta automáticamente:
- Cantidad de calificaciones < 60%.
- Evaluaciones pendientes.
- Promedio general menor a 60%.

Ejemplo de mensaje emergente:

> “Atención: El estudiante presenta calificaciones menores al 60%. Se recomienda intervención docente.”

---

## Tecnologías Utilizadas

- **Python 3**
- **Tkinter** (Interfaz gráfica)
- **Pandas** (Procesamiento del archivo Excel)
- **ttk.Treeview** (Tabla para mostrar resultados)
- **GitHub/Git** (Control de versiones)

---

## ¿Cómo ejecutar el proyecto?

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/rolandofgamarra/proyecto-alertas-academicas.git
