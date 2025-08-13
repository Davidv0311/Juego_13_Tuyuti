import arcade

ANCHO_PANTALLA = 1400
ALTO_PANTALLA = 700

class Boton(arcade.Sprite):
    def __init__(self, imagen_normal, imagen_hover, escala=1, tipo=""):
        super().__init__(imagen_normal, escala)
        self.textura_normal = arcade.load_texture(imagen_normal)
        self.textura_hover = arcade.load_texture(imagen_hover)
        self.texture = self.textura_normal
        self.tipo = tipo
        
    def on_hover(self, x, y):
        if self.collides_with_point((x, y)):
            self.texture = self.textura_hover
            return True
        self.texture = self.textura_normal
        return False

class PantallaVictoria:
    def __init__(self):
        self.fondo_list = arcade.SpriteList()
        self.botones_list = arcade.SpriteList()
        self.music_player = None

    def setup(self):
        fondo = arcade.Sprite("imagenes/fondo_ganaste.png")
        fondo.center_x = ANCHO_PANTALLA / 2
        fondo.center_y = ALTO_PANTALLA / 2
        fondo.width = ANCHO_PANTALLA
        fondo.height = ALTO_PANTALLA
        self.fondo_list.append(fondo)

        boton_reinicio = Boton(
            "imagenes/REINICIAR_BOTON.png",
            "imagenes/REINICIAR_BOTON_HOVER.png",
            0.3,
            "reiniciar"
        )
        boton_reinicio.center_x = ANCHO_PANTALLA / 2
        boton_reinicio.center_y = ALTO_PANTALLA / 2 - 225
        self.botones_list.append(boton_reinicio)

        boton_salir = Boton(
            "imagenes/boton_salir.png",
            "imagenes/boton_salir_hover.png",
            0.3,
            "salir"
        )
        boton_salir.center_x = ANCHO_PANTALLA / 2
        boton_salir.center_y = ALTO_PANTALLA / 2 - 300
        self.botones_list.append(boton_salir)

        try:
            sound = arcade.load_sound("sonidos/musica_ganaste.mp3")
            self.music_player = arcade.play_sound(sound, volume=0.5, loop=True)
        except:
            print("No se pudo cargar la música de fondo")

    def stop_music(self):
        if self.music_player:
            arcade.stop_sound(self.music_player)

    def on_draw(self):
        self.fondo_list.draw()
        self.botones_list.draw()
        arcade.draw_text(
            "",
            ANCHO_PANTALLA / 2,
            ALTO_PANTALLA - 150,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            bold=True
        )

    def on_mouse_motion(self, x, y, dx, dy):
        for boton in self.botones_list:
            boton.on_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for boton in self.botones_list:
            if boton.collides_with_point((x, y)):
                return boton.tipo
        return None