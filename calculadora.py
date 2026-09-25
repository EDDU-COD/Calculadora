"""
Calculadora moderna con CustomTkinter
======================================
Aplicación de escritorio que implementa una calculadora básica
(suma, resta, multiplicación, división, porcentaje, cambio de signo)
con una interfaz gráfica moderna y oscura.
 
Requisitos:
    pip install customtkinter
 
Ejecución:
    python calculadora.py
"""
 
import customtkinter as ctk
 
# ---------------------------------------------------------------------------
# Configuración global de apariencia
# ---------------------------------------------------------------------------
ctk.set_appearance_mode("dark")          # Tema oscuro
ctk.set_default_color_theme("blue")      # Paleta de acentos azules
 
 
class Calculadora(ctk.CTk):
    """
    Clase principal de la aplicación.
    Hereda de CTk (la ventana raíz) y contiene tanto la lógica de cálculo
    como la construcción de la interfaz gráfica.
    """
 
    # Operadores permitidos y su función matemática asociada
    OPERACIONES = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "×": lambda a, b: a * b,
        "÷": lambda a, b: a / b,  # La división por cero se controla aparte
    }
 
    def __init__(self):
        super().__init__()
 
        # ---------------- Configuración de la ventana ----------------
        self.title("Calculadora")
        ancho, alto = 350, 500
        self.minsize(320, 460)            # Evita que la ventana sea demasiado pequeña
        self._centrar_ventana(ancho, alto)
        self.configure(fg_color="#070706")  # Fondo morado de la calculadora
 
        # ---------------- Estado interno de la calculadora ----------------
        self.entrada_actual = "0"   # Texto que se está escribiendo/mostrando
        self.operando_previo = None  # Primer número guardado (float)
        self.operador_pendiente = None  # Operador seleccionado ("+", "-", "×", "÷")
        self.reiniciar_entrada = False  # Indica si el próximo dígito debe iniciar un número nuevo
        self.hubo_error = False     # Marca si la pantalla muestra un mensaje de error
 
        # ---------------- Construcción de la interfaz ----------------
        self._crear_pantalla()
        self._crear_botones()
 
    # ------------------------------------------------------------------
    # Utilidades de ventana
    # ------------------------------------------------------------------
    def _centrar_ventana(self, ancho, alto):
        """Calcula la posición para que la ventana aparezca centrada en pantalla."""
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
 
    # ------------------------------------------------------------------
    # Construcción de widgets
    # ------------------------------------------------------------------
    def _crear_pantalla(self):
        """Crea el área superior donde se muestra la expresión y el resultado."""
        frame_pantalla = ctk.CTkFrame(self, fg_color="transparent")
        frame_pantalla.pack(fill="x", padx=15, pady=(20, 10))
 
        # Pequeña etiqueta que muestra la operación en curso (ej: "10 +")
        self.label_expresion = ctk.CTkLabel(
            frame_pantalla,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="gray70",
            anchor="e",
            justify="right",
        )
        self.label_expresion.pack(fill="x")
 
        # Etiqueta principal con el número/resultado actual
        self.label_resultado = ctk.CTkLabel(
            frame_pantalla,
            text=self.entrada_actual,
            font=ctk.CTkFont(family="Segoe UI", size=42, weight="bold"),
            anchor="e",
            justify="right",
        )
        self.label_resultado.pack(fill="x")
 
    def _crear_botones(self):
        """Crea la cuadrícula de botones (números, operadores y funciones)."""
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(fill="both", expand=True, padx=15, pady=(0, 15))
 
        # 4 columnas y 5 filas con el mismo peso -> botones uniformes y responsivos
        for col in range(4):
            frame_botones.grid_columnconfigure(col, weight=1, uniform="col")
        for fila in range(5):
            frame_botones.grid_rowconfigure(fila, weight=1)
 
        # Definición de la distribución: (texto, fila, columna, tipo, columnspan)
        # tipo -> "numero", "operador", "funcion", "igual"
        botones = [
            ("⌫", 0, 0, "funcion", 1),
            ("AC", 0, 1, "funcion", 1),
            ("%", 0, 2, "funcion", 1),
            ("÷", 0, 3, "operador", 1),
 
            ("7", 1, 0, "numero", 1),
            ("8", 1, 1, "numero", 1),
            ("9", 1, 2, "numero", 1),
            ("×", 1, 3, "operador", 1),
 
            ("4", 2, 0, "numero", 1),
            ("5", 2, 1, "numero", 1),
            ("6", 2, 2, "numero", 1),
            ("-", 2, 3, "operador", 1),
 
            ("1", 3, 0, "numero", 1),
            ("2", 3, 1, "numero", 1),
            ("3", 3, 2, "numero", 1),
            ("+", 3, 3, "operador", 1),
 
            ("+/-", 4, 0, "funcion", 1),
            ("0", 4, 1, "numero", 1),
            (".", 4, 2, "numero", 1),
            ("=", 4, 3, "igual", 1),
        ]
 
        # Colores para diferenciar visualmente cada tipo de botón
        estilos = {
            "numero": {"fg_color": "#585A59", "hover_color": "#080808", "text_color": "white"},     # Verde
            "operador": {"fg_color": "#850073", "hover_color": "#A396A3", "text_color": "black"},   # Café claro
            "funcion": {"fg_color": "#092C55", "hover_color": "#8C8E91", "text_color": "white"},    # Azul
            "igual": {"fg_color": "#492A0D", "hover_color": "#B4B3B1", "text_color": "white"},      # Café oscuro
        }
 
        for texto, fila, col, tipo, span in botones:
            estilo = estilos[tipo]
            boton = ctk.CTkButton(
                frame_botones,
                text=texto,
                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
                corner_radius=15,
                height=60,
                command=lambda t=texto: self._al_presionar(t),
                **estilo,
            )
            boton.grid(row=fila, column=col, columnspan=span, sticky="nsew", padx=6, pady=6)
 
    # ------------------------------------------------------------------
    # Enrutador de eventos: decide qué hacer según el botón pulsado
    # ------------------------------------------------------------------
    def _al_presionar(self, texto):
        """Recibe el texto del botón presionado y llama a la acción correspondiente."""
        # Si la pantalla muestra un error, cualquier tecla (excepto AC) reinicia
        if self.hubo_error and texto != "AC":
            self._limpiar_todo()
 
        if texto.isdigit():
            self._agregar_digito(texto)
        elif texto == ".":
            self._agregar_punto_decimal()
        elif texto == "AC":
            self._limpiar_todo()
        elif texto == "⌫":
            self._borrar_ultimo()
        elif texto == "+/-":
            self._cambiar_signo()
        elif texto == "%":
            self._aplicar_porcentaje()
        elif texto in self.OPERACIONES:
            self._seleccionar_operador(texto)
        elif texto == "=":
            self._calcular_resultado()
 
        self._actualizar_pantalla()
 
    # ------------------------------------------------------------------
    # Lógica de entrada de números
    # ------------------------------------------------------------------
    def _agregar_digito(self, digito):
        """Añade un dígito a la entrada actual, controlando ceros iniciales."""
        if self.reiniciar_entrada or self.entrada_actual == "0":
            self.entrada_actual = digito
            self.reiniciar_entrada = False
        else:
            # Limita la longitud del número para que no desborde la pantalla
            if len(self.entrada_actual) < 15:
                self.entrada_actual += digito
 
    def _agregar_punto_decimal(self):
        """Agrega un punto decimal evitando duplicados."""
        if self.reiniciar_entrada:
            self.entrada_actual = "0"
            self.reiniciar_entrada = False
        if "." not in self.entrada_actual:
            self.entrada_actual += "."
 
    def _borrar_ultimo(self):
        """Elimina el último carácter introducido."""
        if self.reiniciar_entrada:
            return
        self.entrada_actual = self.entrada_actual[:-1]
        if self.entrada_actual in ("", "-"):
            self.entrada_actual = "0"
 
    def _limpiar_todo(self):
        """Restablece la calculadora a su estado inicial (botón AC)."""
        self.entrada_actual = "0"
        self.operando_previo = None
        self.operador_pendiente = None
        self.reiniciar_entrada = False
        self.hubo_error = False
        self.label_expresion.configure(text="")
 
    def _cambiar_signo(self):
        """Invierte el signo del número actual (+/-)."""
        if self.entrada_actual != "0":
            if self.entrada_actual.startswith("-"):
                self.entrada_actual = self.entrada_actual[1:]
            else:
                self.entrada_actual = "-" + self.entrada_actual
 
    def _aplicar_porcentaje(self):
        """Convierte el número actual en su equivalente porcentual (÷100)."""
        try:
            valor = float(self.entrada_actual) / 100
            self.entrada_actual = self._formatear(valor)
        except ValueError:
            self._mostrar_error()
 
    # ------------------------------------------------------------------
    # Lógica de operaciones (sin usar eval)
    # ------------------------------------------------------------------
    def _seleccionar_operador(self, operador):
        """
        Guarda el operador elegido. Si ya existía una operación pendiente,
        la resuelve primero para permitir cálculos encadenados
        (ej: 10 + 5 × 2 se resuelve paso a paso, de izquierda a derecha).
        """
        if self.operador_pendiente is not None and not self.reiniciar_entrada:
            self._resolver_operacion_pendiente()
 
        try:
            self.operando_previo = float(self.entrada_actual)
        except ValueError:
            self._mostrar_error()
            return
 
        self.operador_pendiente = operador
        self.reiniciar_entrada = True
        self.label_expresion.configure(
            text=f"{self._formatear(self.operando_previo)} {operador}"
        )
 
    def _resolver_operacion_pendiente(self):
        """Ejecuta la operación pendiente usando el número actual como segundo operando."""
        try:
            segundo_operando = float(self.entrada_actual)
        except ValueError:
            self._mostrar_error()
            return
 
        resultado = self._calcular(self.operando_previo, self.operador_pendiente, segundo_operando)
        if resultado is None:
            return  # El error ya fue mostrado dentro de _calcular
 
        self.entrada_actual = self._formatear(resultado)
        self.operando_previo = resultado
 
    def _calcular_resultado(self):
        """Acción del botón '=': resuelve la operación pendiente y limpia el estado."""
        if self.operador_pendiente is None or self.operando_previo is None:
            return
 
        self._resolver_operacion_pendiente()
        self.operador_pendiente = None
        self.operando_previo = None
        self.reiniciar_entrada = True
        self.label_expresion.configure(text="")
 
    def _calcular(self, a, operador, b):
        """
        Realiza la operación matemática de forma segura (sin eval).
        Controla la división entre cero y cualquier error inesperado.
        Devuelve el resultado (float) o None si ocurrió un error.
        """
        try:
            if operador == "÷" and b == 0:
                raise ZeroDivisionError
 
            funcion = self.OPERACIONES[operador]
            return funcion(a, b)
 
        except ZeroDivisionError:
            self._mostrar_error("Error: div. por 0")
            return None
        except Exception:
            self._mostrar_error()
            return None
 
    # ------------------------------------------------------------------
    # Manejo de errores y formato de pantalla
    # ------------------------------------------------------------------
    def _mostrar_error(self, mensaje="Error"):
        """Muestra un mensaje de error en pantalla sin cerrar la aplicación."""
        self.entrada_actual = mensaje
        self.operando_previo = None
        self.operador_pendiente = None
        self.reiniciar_entrada = True
        self.hubo_error = True
 
    def _formatear(self, numero):
        """
        Convierte un float a texto legible:
        - Elimina el '.0' final si el número es entero.
        - Redondea a un máximo de 10 decimales para evitar errores de coma flotante.
        """
        if numero == int(numero) and abs(numero) < 1e15:
            return str(int(numero))
        texto = f"{round(numero, 10)}"
        return texto
 
    def _actualizar_pantalla(self):
        """Refleja el valor actual de 'entrada_actual' en la etiqueta de resultado."""
        self.label_resultado.configure(text=self.entrada_actual)
 
 
# ---------------------------------------------------------------------------
# Punto de entrada de la aplicación
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()