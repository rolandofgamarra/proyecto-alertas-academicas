import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Carga el dataset
archivo_datos = "dataset_notas_22_alumnos.xlsx"
datos_estudiantes = pd.read_excel(archivo_datos)

# convertir fechas
datos_estudiantes["Fecha"] = pd.to_datetime(datos_estudiantes["Fecha"], errors="coerce")

# buscar informacion del alumno
def realizar_busqueda():
    nombre_estudiante = campo_nombre.get().strip()

    if not nombre_estudiante:
        messagebox.showwarning("Atención", "Por favor, escribe el nombre completo del alumno.")
        return

    # Buscar ignorando mayusculas
    registros_estudiante = datos_estudiantes[
        datos_estudiantes["Nombre"].str.lower() == nombre_estudiante.lower()
    ]

    if registros_estudiante.empty:
        tabla_notas.delete(*tabla_notas.get_children())
        etiqueta_estado.config(
            text=f"No se encontró al alumno '{nombre_estudiante}'", 
            bg="pink", fg="red"
        )
        
        # Mostrar sugerencias de nombres disponibles
        todos_los_nombres = datos_estudiantes["Nombre"].unique()
        nombres_parecidos = [n for n in todos_los_nombres 
                            if nombre_estudiante.lower() in n.lower()]
        
        mensaje = f"No se encontró al alumno '{nombre_estudiante}' en el sistema."
        if nombres_parecidos:
            mensaje += f"\n\n¿Quisiste decir alguno de estos?\n" + "\n".join(f"• {n}" for n in nombres_parecidos[:5])
        
        messagebox.showinfo("Sin resultados", mensaje)
        return

    # Limpiar tabla antes de mostrar nuevos datos
    tabla_notas.delete(*tabla_notas.get_children())

    # Variables para calcular estadísticas
    notas_bajas = False
    cantidad_notas = 0
    total_puntos = 0
    contador_bajo_60 = 0

    # Procesar cada registro del estudiante
    for indice, registro in registros_estudiante.iterrows():
        fecha_registro = registro["Fecha"]
        materia_curso = registro["Materia"]
        puntos_obtenidos = registro["Puntaje"]
        tipo_evaluacion = registro["Tipo"]

        # Formatear la fecha
        if pd.isna(fecha_registro):
            texto_fecha = "Sin fecha"
        else:
            texto_fecha = fecha_registro.strftime("%d/%m/%Y")
            
        # Procesar el puntaje
        if pd.isna(puntos_obtenidos):
            mostrar_puntaje = "Pendiente"
            color_fila = "pendiente"
        else:
            mostrar_puntaje = f"{puntos_obtenidos:.1f}"
            cantidad_notas += 1
            total_puntos += puntos_obtenidos
            
            # Determinar el color según el puntaje
            if puntos_obtenidos < 60:
                notas_bajas = True
                contador_bajo_60 += 1
                color_fila = "bajo"
            elif puntos_obtenidos < 70:
                color_fila = "medio"
            else:
                color_fila = "alto"

        # Agregar fila a la tabla
        tabla_notas.insert(
            "", tk.END, 
            values=(texto_fecha, materia_curso, tipo_evaluacion, mostrar_puntaje),
            tags=(color_fila,)
        )

    # Calcular y mostrar el promedio
    if cantidad_notas > 0:
        promedio_general = total_puntos / cantidad_notas
        etiqueta_promedio.config(text=f"Promedio General: {promedio_general:.1f}%")
        
        # Color del promedio según rendimiento
        if promedio_general < 60:
            etiqueta_promedio.config(fg="red")
        elif promedio_general < 70:
            etiqueta_promedio.config(fg="orange")
        else:
            etiqueta_promedio.config(fg="green")
    else:
        etiqueta_promedio.config(text="Promedio General: Sin calificaciones", fg="gray")

    # Mostrar estado general del estudiante
    if notas_bajas:
        etiqueta_estado.config(
            text=f"Alerta Académica: {contador_bajo_60} calificación(es) por debajo del 60%",
            bg="yellow", fg="red"
        )
        messagebox.showwarning(
            "Alerta Académica",
            f"Atención: El estudiante {nombre_estudiante} tiene {contador_bajo_60} "
            f"calificación(es) por debajo del 60%.\n\n"
            f"Promedio general: {promedio_general:.1f}%\n\n"
            f"Se recomienda seguimiento y apoyo académico."
        )
    else:
        etiqueta_estado.config(
            text="✓ Rendimiento satisfactorio - No hay alertas académicas",
            bg="lightgreen", fg="darkgreen"
        )

# Función para limpiar la búsqueda y empezar de nuevo
def limpiar_todo():
    campo_nombre.delete(0, tk.END)
    tabla_notas.delete(*tabla_notas.get_children())
    etiqueta_estado.config(
        text="Ingresa el nombre completo del alumno para ver sus calificaciones", 
        bg="lightblue", fg="blue"
    )
    etiqueta_promedio.config(text="Promedio General: --", fg="gray")
    campo_nombre.focus_set()

# Crear ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Sistema de Alertas Académicas Q3 2025")
ventana_principal.geometry("950x680")
ventana_principal.configure(bg="lightgray")

# Configurar estilos visuales
estilo_app = ttk.Style()
estilo_app.theme_use("clam")

# Estilos para la tabla de calificaciones
estilo_app.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=28,
                fieldbackground="white",
                font=("Segoe UI", 10))
estilo_app.configure("Treeview.Heading",
                background="blue",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat")
estilo_app.map("Treeview", background=[("selected", "lightblue")])

# Contenedor principal
contenedor_principal = tk.Frame(ventana_principal, bg="lightgray")
contenedor_principal.pack(fill="both", expand=True, padx=20, pady=20)

# Sección de búsqueda (parte superior)
seccion_busqueda = tk.Frame(contenedor_principal, bg="white", relief="solid", bd=1)
seccion_busqueda.pack(fill="x", pady=(0, 15))

# Título principal
titulo_app = tk.Label(
    seccion_busqueda, 
    text="🎓 Sistema de Alertas Académicas - Q3 2025",
    font=("Segoe UI", 16, "bold"),
    bg="white", fg="blue"
)
titulo_app.pack(pady=(15, 10))

# Subtítulo descriptivo
subtitulo_app = tk.Label(
    seccion_busqueda,
    text="Monitoreo de rendimiento estudiantil - Búsqueda por nombre completo",
    font=("Segoe UI", 10),
    bg="white", fg="gray"
)
subtitulo_app.pack(pady=(0, 15))

# Área de entrada de datos
area_entrada = tk.Frame(seccion_busqueda, bg="white")
area_entrada.pack(pady=(0, 15))

etiqueta_nombre = tk.Label(
    area_entrada, 
    text="Nombre completo del alumno:",
    font=("Segoe UI", 11),
    bg="white", fg="black"
)
etiqueta_nombre.pack(side="left", padx=(10, 5))

campo_nombre = tk.Entry(
    area_entrada, 
    width=35,
    font=("Segoe UI", 11),
    relief="solid", bd=1
)
campo_nombre.pack(side="left", padx=5)

# Botones 
boton_buscar = tk.Button(
    area_entrada, 
    text="🔍 Buscar",
    command=realizar_busqueda,
    font=("Segoe UI", 10, "bold"),
    bg="blue", fg="white",
    relief="flat", padx=20, pady=8,
    cursor="hand2"
)
boton_buscar.pack(side="left", padx=5)

boton_limpiar = tk.Button(
    area_entrada, 
    text="Limpiar",
    command=limpiar_todo,
    font=("Segoe UI", 10),
    bg="gray", fg="white",
    relief="flat", padx=15, pady=8,
    cursor="hand2"
)
boton_limpiar.pack(side="left", padx=5)

boton_salir = tk.Button(
    area_entrada, 
    text="✕ Salir",
    command=ventana_principal.destroy,
    font=("Segoe UI", 10),
    bg="red", fg="white",
    relief="flat", padx=15, pady=8,
    cursor="hand2"
)
boton_salir.pack(side="left", padx=5)

# estado y promedio
seccion_informacion = tk.Frame(contenedor_principal, bg="lightgray")
seccion_informacion.pack(fill="x", pady=(0, 10))

etiqueta_estado = tk.Label(
    seccion_informacion,
    text="Ingresa el nombre completo del alumno para ver sus calificaciones",
    font=("Segoe UI", 11, "bold"),
    bg="lightblue", fg="blue",
    relief="solid", bd=1, pady=10
)
etiqueta_estado.pack(fill="x", pady=(0, 5))

etiqueta_promedio = tk.Label(
    seccion_informacion,
    text="Promedio General: --",
    font=("Segoe UI", 12, "bold"),
    bg="white", fg="gray",
    relief="solid", bd=1, pady=8
)
etiqueta_promedio.pack(fill="x")

# Sección de resultados (tabla de calificaciones)
seccion_resultados = tk.Frame(contenedor_principal, bg="white", relief="solid", bd=1)
seccion_resultados.pack(fill="both", expand=True)

titulo_resultados = tk.Label(
    seccion_resultados,
    text="Historial de Calificaciones del Estudiante",
    font=("Segoe UI", 12, "bold"),
    bg="white", fg="black"
)
titulo_resultados.pack(pady=(10, 5))

# Contenedor para la tabla con scroll
contenedor_tabla = tk.Frame(seccion_resultados, bg="white")
contenedor_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))

barra_scroll = ttk.Scrollbar(contenedor_tabla)
barra_scroll.pack(side="right", fill="y")

tabla_notas = ttk.Treeview(
    contenedor_tabla,
    columns=("Fecha", "Materia", "Tipo", "Puntaje"),
    show="headings",
    yscrollcommand=barra_scroll.set
)
barra_scroll.config(command=tabla_notas.yview)

# Configurar encabezados de columnas
tabla_notas.heading("Fecha", text="Fecha")
tabla_notas.heading("Materia", text="Materia")
tabla_notas.heading("Tipo", text="Tipo de Evaluación")
tabla_notas.heading("Puntaje", text="Puntaje (%)")

# Ajustar ancho de columnas
tabla_notas.column("Fecha", width=120, anchor="center")
tabla_notas.column("Materia", width=180, anchor="w")
tabla_notas.column("Tipo", width=130, anchor="center")
tabla_notas.column("Puntaje", width=110, anchor="center")

# Configurar colores según rendimiento
tabla_notas.tag_configure("bajo", background="pink", foreground="red")
tabla_notas.tag_configure("medio", background="lightyellow", foreground="orange")
tabla_notas.tag_configure("alto", background="lightgreen", foreground="darkgreen")
tabla_notas.tag_configure("pendiente", background="lightgray", foreground="gray")

tabla_notas.pack(fill="both", expand=True)

# Leyenda de colores
seccion_leyenda = tk.Frame(seccion_resultados, bg="white")
seccion_leyenda.pack(pady=(0, 10))

tk.Label(
    seccion_leyenda, 
    text="Leyenda de colores:", 
    font=("Segoe UI", 9, "bold"),
    bg="white", fg="black"
).pack(side="left", padx=5)

tk.Label(seccion_leyenda, text="■", font=("Segoe UI", 14),
        bg="white", fg="red").pack(side="left")
tk.Label(seccion_leyenda, text="Menos de 60%", font=("Segoe UI", 9),
        bg="white", fg="black").pack(side="left", padx=(0, 10))

tk.Label(seccion_leyenda, text="■", font=("Segoe UI", 14),
        bg="white", fg="orange").pack(side="left")
tk.Label(seccion_leyenda, text="60% - 69%", font=("Segoe UI", 9),
        bg="white", fg="black").pack(side="left", padx=(0, 10))

tk.Label(seccion_leyenda, text="■", font=("Segoe UI", 14),
        bg="white", fg="green").pack(side="left")
tk.Label(seccion_leyenda, text="70% o más", font=("Segoe UI", 9),
        bg="white", fg="black").pack(side="left", padx=(0, 10))

tk.Label(seccion_leyenda, text="■", font=("Segoe UI", 14),
        bg="white", fg="gray").pack(side="left")
tk.Label(seccion_leyenda, text="Pendiente", font=("Segoe UI", 9),
        bg="white", fg="black").pack(side="left")

# Establecer foco inicial en el campo de búsqueda
campo_nombre.focus_set()

# Permitir búsqueda presionando Enter
campo_nombre.bind("<Return>", lambda evento: realizar_busqueda())

# Iniciar la aplicación
ventana_principal.mainloop()