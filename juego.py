import arcade
from objetos import TipoObjeto1, TipoObjeto2
from inicio import PantallaInicio
from trivia import SistemaTrivia
from pantalla_derrota import PantallaDerrota
from pantalla_victoria import PantallaVictoria

ANCHO_PANTALLA = 1400
ALTO_PANTALLA = 700
TITULO_PANTALLA = "Guerra del Chaco - Juego Educativo"
TAM_OBJETO = 60

class MiJuego(arcade.Window):
    def __init__(self, ancho, alto, titulo):
        super().__init__(ancho, alto, titulo)
        arcade.set_background_color(arcade.color.AMAZON)
        
        self.fondo_list = arcade.SpriteList()
        self.lista_objetos1 = arcade.SpriteList()
        self.lista_objetos2 = arcade.SpriteList()
        
        self.pantalla_actual = "inicio"
        self.pantalla_inicio = PantallaInicio()
        self.pantalla_inicio.setup()
        
        # Pantallas de resultado
        self.pantalla_victoria = None
        self.pantalla_derrota = None
        
        self.trivia = SistemaTrivia()
        self.objeto_seleccionado = None
        self.esperando_respuesta = False
        self.tiempo_mostrar_resultado = 0
        
        self.fortines_destruidos = []
        self.objetos1_destruidos = []
        
        try:
            self.snd_explosion_ok = arcade.load_sound("sonidos/explosion.wav")  
        except Exception as e:
            print("No se pudo cargar sonidos/explosion.wav:", e)
            self.snd_explosion_ok = None

        try:
            self.snd_explosion_fail = arcade.load_sound("sonidos/explosion.wav")
        except Exception as e:
            print("No se pudo cargar sonidos/explosion.wav:", e)
            self.snd_explosion_fail = None

    def setup_juego(self):
        """
        -Prepara/Reinicia el estado inicial del juego:
        - Limpia todas las listas de sprites y objetos destruidos
        - Carga el fondo de pantalla
        - Coloca los objetos tipo 1 (bolivianos) y tipo 2 (paraguayos) en sus posiciones iniciales
        - Reinicia el sistema de trivia
        - Prepara las variables de estado del juego
        """
        try:
            self.fondo_list.clear()
            self.lista_objetos1.clear()
            self.lista_objetos2.clear()
            self.fortines_destruidos.clear()
            self.objetos1_destruidos.clear() 

            try:
                fondo = arcade.Sprite("imagenes/fondo.png")
                fondo.center_x = ANCHO_PANTALLA // 2
                fondo.center_y = ALTO_PANTALLA // 2
                fondo.width = ANCHO_PANTALLA
                fondo.height = ALTO_PANTALLA
                self.fondo_list.append(fondo)
            except:
                print("No se pudo cargar el fondo")
                
            #Objetos del lado izquierdo
            posiciones_izq = [(100, 100), (200, 300), (150, 500), (300, 600), (250, 200)]
            for x, y in posiciones_izq:
                try:
                    obj = TipoObjeto1("imagenes/objeto1.png", x, y, TAM_OBJETO, TAM_OBJETO)
                    self.lista_objetos1.append(obj)
                except:
                    print(f"No se pudo cargar objeto1 en posición {x}, {y}")

            # Objetos del lado derecho (paraguayos)
            posiciones_der = [(900, 150), (1000, 350), (1100, 550), (1200, 250), (1300, 450)]
            for x, y in posiciones_der:
                try:
                    obj = TipoObjeto2("imagenes/objeto2.png", x, y, TAM_OBJETO, TAM_OBJETO)
                    self.lista_objetos2.append(obj)
                except:
                    print(f"No se pudo cargar objeto2 en posición {x}, {y}")

            # Reiniciar el sistema de trivia
            self.trivia.reiniciar_trivia()
            self.esperando_respuesta = False
            self.tiempo_mostrar_resultado = 0
            
            # Limpiar pantallas de resultado
            self.pantalla_victoria = None
            self.pantalla_derrota = None
            
        except Exception as e:
            print(f"Error en setup_juego: {e}")
        
    def destruir_siguiente_fortin_paraguayo(self):
        """Destruye el siguiente fortín paraguayo disponible"""
        try:
            for obj in self.lista_objetos2:
                if obj not in self.fortines_destruidos:
                    obj.cambiar_textura2("imagenes/objeto2_destruido.png")
                    self.fortines_destruidos.append(obj)
                    break
        except Exception as e:
            print(f"Error destruyendo fortín paraguayo: {e}")

    def on_update(self, delta_time):
        try:
            if self.pantalla_actual == "juego" and self.trivia.mostrar_resultado:
                self.tiempo_mostrar_resultado += delta_time
                if self.tiempo_mostrar_resultado >= 2.0:
                    resultado = self.trivia.verificar_respuesta()
                    self.procesar_respuesta(resultado)
                    self.esperando_respuesta = False
                    self.tiempo_mostrar_resultado = 0
                    
                    if self.trivia.juego_terminado():
                        if self.trivia.jugador_gano():
                            self.pantalla_victoria = PantallaVictoria()
                            self.pantalla_victoria.setup()
                        else:
                            self.pantalla_derrota = PantallaDerrota()
                            self.pantalla_derrota.setup()
                        self.pantalla_actual = "resultado"
                        
        except Exception as e:
            print(f"Error en on_update: {e}")

    def on_mouse_press(self, x, y, button, modifiers):
        try:
            if self.pantalla_actual == "inicio":
                resultado = self.pantalla_inicio.on_mouse_press(x, y, button, modifiers)
                if resultado == "jugar":
                    self.pantalla_inicio.stop_music()
                    self.setup_juego()
                    self.pantalla_actual = "juego"
                elif resultado == "salir":
                    self.pantalla_inicio.stop_music()
                    arcade.close_window()
                    
            elif self.pantalla_actual == "resultado":
                resultado_accion = None
                
                if self.pantalla_victoria:
                    resultado_accion = self.pantalla_victoria.on_mouse_press(x, y, button, modifiers)
                elif self.pantalla_derrota:
                    resultado_accion = self.pantalla_derrota.on_mouse_press(x, y, button, modifiers)
                
                if resultado_accion == "reiniciar":
                    if self.pantalla_victoria:
                        self.pantalla_victoria.stop_music()
                    elif self.pantalla_derrota:
                        self.pantalla_derrota.stop_music()
                    self.setup_juego()
                    self.pantalla_actual = "juego"
                elif resultado_accion == "salir":
                    arcade.close_window()
                    
            elif self.pantalla_actual == "juego":
                if self.trivia.mostrar_trivia and not self.trivia.mostrar_resultado:
                    for i in range(len(self.trivia.pregunta_actual.opciones)):
                        if self.trivia.punto_en_opcion(x, y, i):
                            self.trivia.seleccionar_respuesta(i)
                            self.tiempo_mostrar_resultado = 0
                            break
                    return

                if not self.esperando_respuesta and not self.trivia.mostrar_trivia:
                    sprite = arcade.get_sprites_at_point((x, y), self.lista_objetos1)
                    if sprite and sprite[0] not in self.objetos1_destruidos:  # Verificar si no está destruido
                        self.objeto_seleccionado = sprite[0]
                        if self.trivia.iniciar_pregunta():
                            self.esperando_respuesta = True

        except Exception as e:
            print(f"Error en on_mouse_press: {e}")

    def procesar_respuesta(self, correcta):
        try:
            if correcta and isinstance(self.objeto_seleccionado, TipoObjeto1):
                self.objeto_seleccionado.cambiar_textura("imagenes/objeto_destruido.png")
                self.objetos1_destruidos.append(self.objeto_seleccionado)  # Registrar objeto destruido
                # Sonido de explosión "correcta"
                if self.snd_explosion_ok:
                    arcade.play_sound(self.snd_explosion_ok, volume=1.5)
            elif not correcta:
                self.destruir_siguiente_fortin_paraguayo()
                # Sonido de explosión "incorrecta"
                if self.snd_explosion_fail:
                    arcade.play_sound(self.snd_explosion_fail, volume=1.5)
        except Exception as e:
            print(f"Error procesando respuesta: {e}")

    def on_draw(self):
        try:
            self.clear()
            if self.pantalla_actual == "inicio":
                self.pantalla_inicio.on_draw()
            elif self.pantalla_actual == "resultado":
                self.clear()
                if self.pantalla_victoria:
                    self.pantalla_victoria.on_draw()
                elif self.pantalla_derrota:
                    self.pantalla_derrota.on_draw()
            elif self.pantalla_actual == "juego":
                self.fondo_list.draw()
                self.lista_objetos1.draw()
                self.lista_objetos2.draw()
                if self.trivia.mostrar_trivia:
                    self.trivia.dibujar_trivia()
        except Exception as e:
            print(f"Error en on_draw: {e}")

    def on_mouse_motion(self, x, y, dx, dy):
        try:
            if self.pantalla_actual == "inicio":
                self.pantalla_inicio.on_mouse_motion(x, y, dx, dy)
            elif self.pantalla_actual == "resultado":
                if self.pantalla_victoria:
                    self.pantalla_victoria.on_mouse_motion(x, y, dx, dy)
                elif self.pantalla_derrota:
                    self.pantalla_derrota.on_mouse_motion(x, y, dx, dy)
            elif self.pantalla_actual == "juego" and self.trivia.mostrar_trivia:
                if not self.trivia.mostrar_resultado:
                    for i in range(len(self.trivia.pregunta_actual.opciones)):
                        if self.trivia.punto_en_opcion(x, y, i):
                            break
        except Exception as e:
            print(f"Error en on_mouse_motion: {e}")

def main():
    juego = MiJuego(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_PANTALLA)
    arcade.run()

if __name__ == "__main__":
    main()