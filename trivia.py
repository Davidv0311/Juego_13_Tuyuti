import arcade
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

class Pregunta:
    def __init__(self, texto, opciones, respuesta_correcta):
        self.texto = texto
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta

class SistemaTrivia:
    def __init__(self):
        self.todas_las_preguntas = self.cargar_todas_preguntas()
        self.total_preguntas = 5
        self.preguntas = self.seleccionar_preguntas_aleatorias()
        self.pregunta_actual = None
        self.respuesta_seleccionada = None
        self.mostrar_trivia = False
        self.mostrar_resultado = False
        self.respuesta_correcta_seleccionada = False
        self.tiempo_resultado = 0
        
        # Nuevos atributos para el conteo
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        self.preguntas_respondidas = 0
        
        self.sonido_correcto = None
        self.sonido_incorrecto = None
        try:
            self.sonido_correcto = arcade.load_sound("sonidos/resp_correcta.mp3")
        except Exception as e:
            print("No se pudo cargar sonidos/resp_correcta.mp3:", e)

        try:
            self.sonido_incorrecto = arcade.load_sound("sonidos/resp_incorrecta.wav")
        except Exception as e:
            print("No se pudo cargar sonidos/resp_incorrecta.wav:", e)
            
        self.musica_pregunta = None
        self._musica_player = None 
        
        try:
        # Usa .ogg o .wav si notas latencia al iniciar con .mp3
            self.musica_pregunta = arcade.load_sound("sonidos/musica_trivia.mp3")
        except Exception as e:
            print("No se pudo cargar sonidos/musica_trivia.mp3:", e)
            self.musica_pregunta = None
            
    def _iniciar_musica_pregunta(self):

        """Reproduce la música de la pantalla de pregunta en loop."""
        if self.musica_pregunta and not self._musica_player:
            # loop=True para que continúe hasta que la detengas
            self._musica_player = arcade.play_sound(self.musica_pregunta, volume=0.5, loop=True)

    def _detener_musica_pregunta(self):
        """Detiene la música si está sonando."""
        if self._musica_player:
            try:
            # Según la versión de Arcade/Pyglet, puede ser stop() o pause()
                self._musica_player.pause()
            except Exception:
                pass
            self._musica_player = None

        self.sonido_correcto = None
        self.sonido_incorrecto = None
        try:
            self.sonido_correcto = arcade.load_sound("sonidos/resp_correcta.mp3")
        except Exception as e:
            print("No se pudo cargar sonidos/resp_correcta.mp3:", e)

        try:
            self.sonido_incorrecto = arcade.load_sound("sonidos/resp_incorrecta.wav")
        except Exception as e:
            print("No se pudo cargar sonidos/resp_incorrecta.wav:", e)

    def reiniciar_trivia(self):
        """Reinicia todo el sistema de trivia para un nuevo juego"""
        self.preguntas = self.seleccionar_preguntas_aleatorias()
        self.pregunta_actual = None
        self.respuesta_seleccionada = None
        self.mostrar_trivia = False
        self.mostrar_resultado = False
        self.respuesta_correcta_seleccionada = False
        self.tiempo_resultado = 0
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        self.preguntas_respondidas = 0

    def cargar_todas_preguntas(self):
        return [
            Pregunta(
                "¿Cuál era el nombre del fortín paraguayo que resistió el primer gran ataque boliviano en septiembre de 1932?",
                ["Fortín López", "Fortín Boquerón", "Fortín Corrales", "Fortín Toledo"],
                1
            ),
            Pregunta(
                "¿Qué general paraguayo fue conocido como 'El Mariscal de la Victoria' tras la Guerra del Chaco?",
                ["Rafael Franco", "José Félix Estigarribia", "Patricio Escobar", "Bernardino Caballero"],
                1
            ),
            Pregunta(
                "¿Cuál fue el nombre de la operación militar paraguaya que logró la reconquista del Chaco Central?",
                ["Operación Murciélago", "Operación Cóndor", "Operación Piraña", "Operación Yacaré"],
                0
            ),
            Pregunta(
                "¿En qué batalla los paraguayos lograron su mayor victoria defensiva contra las fuerzas bolivianas?",
                ["Batalla de Campo Grande", "Batalla de Nanawa", "Batalla de Alihuatá", "Batalla de Cañada Strongest"],
                1
            ),
            Pregunta(
                "¿Cuál era el apodo del coronel paraguayo Rafael Franco durante la guerra?",
                ["El León del Chaco", "El Cóndor", "El Centauro del Norte", "El Mariscal López"],
                1
            ),
            Pregunta(
                "¿Qué empresa petrolera estadounidense tenía concesiones en territorio boliviano del Chaco?",
                ["Shell Oil", "Standard Oil", "Texaco", "Gulf Oil"],
                1
            ),
            Pregunta(
                "¿Cuál fue la duración exacta de la Guerra del Chaco en años?",
                ["2 años y 8 meses", "3 años y 2 meses", "3 años y 8 meses", "4 años exactos"],
                1
            ),
            Pregunta(
                "¿Qué río marcaba aproximadamente la frontera este del territorio en disputa?",
                ["Río Paraguay", "Río Pilcomayo", "Río Verde", "Río Bermejo"],
                0
            ),
            Pregunta(
                "¿Cuál fue el último fortín importante que Paraguay conquistó antes del armisticio?",
                ["Fortín Ballivián", "Villa Montes", "El Carmen", "Boyuibe"],
                1
            ),
            Pregunta(
                "¿Qué porcentaje aproximado de las bajas bolivianas se debieron a enfermedades tropicales?",
                ["40%", "55%", "65%", "75%"],
                2
            ),
            Pregunta(
                "¿Cómo se llamaba el sistema defensivo paraguayo de trincheras interconectadas?",
                ["Línea Maginot Chaqueña", "Sistema Kundt", "Línea Estigarribia", "Red de Boquerón"],
                2
            ),
            Pregunta(
                "¿En qué año se firmó el Protocolo de Paz que estableció el armisticio definitivo?",
                ["1935", "1936", "1937", "1938"],
                0
            )
        ]

    def seleccionar_preguntas_aleatorias(self):
        return random.sample(self.todas_las_preguntas, self.total_preguntas)

    def iniciar_pregunta(self):
        if self.preguntas:
            self.pregunta_actual = self.preguntas.pop(0)
            self.respuesta_seleccionada = None
            self.mostrar_trivia = True
            self.mostrar_resultado = False
            self._iniciar_musica_pregunta()  # ¡Agrega esta línea!
            return True
        return False

    def juego_terminado(self):
        """Verifica si el juego ha terminado (todas las preguntas respondidas)"""
        return self.preguntas_respondidas >= self.total_preguntas

    def jugador_gano(self):
        """Determina si el jugador ganó (más respuestas correctas que incorrectas)"""
        return self.respuestas_correctas > self.respuestas_incorrectas

    def dibujar_trivia(self):
        if not self.mostrar_trivia or not self.pregunta_actual:
            return

        self.dibujar_fondo_degradado()
        self.dibujar_panel_principal()
        self.dibujar_pregunta()
        self.dibujar_opciones()
        self.dibujar_contador_preguntas()

    def dibujar_contador_preguntas(self):
        """Dibuja el contador de preguntas en la esquina superior derecha"""
        texto = f"Pregunta {self.preguntas_respondidas} de {self.total_preguntas}"
        arcade.draw_text(
            texto,
            SCREEN_WIDTH - 20, SCREEN_HEIGHT - 40,
            arcade.color.WHITE, 18,
            align="right", anchor_x="right",
            font_name="Arial", bold=True
        )
        
        # También mostrar el marcador
        marcador = f"Correctas: {self.respuestas_correctas} | Incorrectas: {self.respuestas_incorrectas}"
        arcade.draw_text(
            marcador,
            SCREEN_WIDTH - 20, SCREEN_HEIGHT - 70,
            arcade.color.WHITE, 16,
            align="right", anchor_x="right",
            font_name="Arial"
        )

    def dibujar_fondo_degradado(self):
        num_strips = 50
        for i in range(num_strips):
            factor = i / num_strips
            r = int(50 + (100 - 50) * factor)
            g = int(70 + (140 - 70) * factor)
            b = int(30 + (80 - 30) * factor)
            
            strip_height = SCREEN_HEIGHT / num_strips
            y_pos = i * strip_height
            
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH,
                y_pos, y_pos + strip_height,
                (r, g, b, 220)
            )
        
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 20, 40, 100)
        )

    def dibujar_panel_principal(self): #no aparece nada
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 398, SCREEN_WIDTH // 2 + 402,
            SCREEN_HEIGHT // 2 - 248, SCREEN_HEIGHT // 2 + 252,
            (0, 0, 0, 100)
        )
        
        arcade.draw_lrbt_rectangle_filled(#ventana de la trivia
            SCREEN_WIDTH // 2 - 400, SCREEN_WIDTH // 2 + 400,
            SCREEN_HEIGHT // 2 - 250, SCREEN_HEIGHT // 2 + 250,
            (228, 214, 187, 240)
        )
        
        arcade.draw_lrbt_rectangle_outline(#Borde de ventana de trivia
            SCREEN_WIDTH // 2 - 400, SCREEN_WIDTH // 2 + 400,
            SCREEN_HEIGHT // 2 - 250, SCREEN_HEIGHT // 2 + 250,
            (160, 130, 90), 5
            #(230, 195, 121), 5
        )

    def dibujar_pregunta(self):
        arcade.draw_text(  #aun no se determina que objeto es
            self.pregunta_actual.texto,
            SCREEN_WIDTH // 2 + 2,
            SCREEN_HEIGHT // 2 + 192,
            (0, 0, 0, 0), 22,
            align="center", anchor_x="center",
            font_name="Times new roman", bold=True, width=720, multiline=True
        )
        
        arcade.draw_text( #Tipografía de la pregunta
            self.pregunta_actual.texto,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 190,
            arcade.color.BLACK, 20,
            align="center", anchor_x="center",
            font_name="Cinzel", bold=True, width=720, multiline=True
        )

    def dibujar_opciones(self):
        for i, opcion in enumerate(self.pregunta_actual.opciones):
            y_pos = SCREEN_HEIGHT // 2 + 60 - i * 80
            
            if self.mostrar_resultado:
                if i == self.pregunta_actual.respuesta_correcta:
                    color_fondo = (46, 204, 113, 220)
                    color_borde = (39, 174, 96)
                elif i == self.respuesta_seleccionada and i != self.pregunta_actual.respuesta_correcta:
                    color_fondo = (231, 76, 60, 220)
                    color_borde = (192, 57, 43)
                else:
                    color_fondo = (189, 195, 199, 180)
                    color_borde = (127, 140, 141)
            else:
                if self.respuesta_seleccionada == i:
                    color_fondo = (52, 152, 219, 200)
                    color_borde = (41, 128, 185)
                else:
                    color_fondo = (236, 240, 241, 200)
                    color_borde = (189, 195, 199)
            
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH // 2 - 348, SCREEN_WIDTH // 2 + 352,
                y_pos - 32, y_pos + 32,
                (0, 0, 0, 80)
            )
            
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH // 2 - 350, SCREEN_WIDTH // 2 + 350,
                y_pos - 30, y_pos + 30,
                color_fondo
            )
            
            arcade.draw_lrbt_rectangle_outline(
                SCREEN_WIDTH // 2 - 350, SCREEN_WIDTH // 2 + 350,
                y_pos - 30, y_pos + 30,
                color_borde, 3
            )
            
            arcade.draw_circle_filled(
                SCREEN_WIDTH // 2 - 310, y_pos,
                20, color_borde
            )
            
            arcade.draw_text(#no se que hace
                str(i + 1),
                SCREEN_WIDTH // 2 - 310, y_pos - 10,
                arcade.color.WHITE, 18,
                align="center", anchor_x="center",
                font_name="Arial", bold=True
            )
            
            color_texto = arcade.color.WHITE if self.respuesta_seleccionada == i and not self.mostrar_resultado else (44, 62, 80)
            if self.mostrar_resultado and (i == self.pregunta_actual.respuesta_correcta or 
                                         (i == self.respuesta_seleccionada and i != self.pregunta_actual.respuesta_correcta)):
                color_texto = arcade.color.WHITE
            
            arcade.draw_text(#letra de respuestas sombras
                opcion,
                SCREEN_WIDTH // 2 - 260 + 1, y_pos - 9,
                (0, 0, 0, 100), 17,
                align="left", anchor_x="left",
                font_name="Cinzel", bold=True, width=550
            )
            
            arcade.draw_text(#letra de respuestas
                opcion,
                SCREEN_WIDTH // 2 - 260, y_pos - 8,
                (0, 0, 0, 255), 17,
                #color_texto, 17,
                align="left", anchor_x="left",
                font_name="Cinzel", bold=True, width=550
            )

    def seleccionar_respuesta(self, opcion):
        if not self.mostrar_resultado and self.pregunta_actual:
            self.respuesta_seleccionada = opcion
            self.mostrar_resultado = True
            self.respuesta_correcta_seleccionada = (opcion == self.pregunta_actual.respuesta_correcta)
            self.tiempo_resultado = 0
            
            # Actualizar contadores
            self.preguntas_respondidas += 1
            if self.respuesta_correcta_seleccionada and self.sonido_correcto:
                self.respuestas_correctas += 1
                arcade.play_sound(self.sonido_correcto, volume=0.7)
            elif not self.respuesta_correcta_seleccionada and self.sonido_incorrecto:
                self.respuestas_incorrectas += 1
                arcade.play_sound(self.sonido_incorrecto, volume=0.7)
                
            self._detener_musica_pregunta()

            if self.respuesta_correcta_seleccionada and self.sonido_correcto:
                arcade.play_sound(self.sonido_correcto, volume=0.7)
            elif not self.respuesta_correcta_seleccionada and self.sonido_incorrecto:
                arcade.play_sound(self.sonido_incorrecto, volume=0.7)

            if self.respuesta_correcta_seleccionada and self.sonido_correcto:
                arcade.play_sound(self.sonido_correcto, volume=0.7)
            elif not self.respuesta_correcta_seleccionada and self.sonido_incorrecto:
                arcade.play_sound(self.sonido_incorrecto, volume=0.7)

    def verificar_respuesta(self):
        resultado = self.respuesta_correcta_seleccionada
        self.mostrar_trivia = False
        self.mostrar_resultado = False
        return resultado

    def punto_en_opcion(self, x, y, indice_opcion):
        y_pos = SCREEN_HEIGHT // 2 + 60 - indice_opcion * 80
        return (SCREEN_WIDTH // 2 - 350 < x < SCREEN_WIDTH // 2 + 350 and
                y_pos - 30 < y < y_pos + 30)