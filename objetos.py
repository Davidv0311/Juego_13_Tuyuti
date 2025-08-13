import arcade
class TipoObjeto1(arcade.Sprite):
    def __init__(self, imagen, x, y, ancho, alto):
        super().__init__(imagen, center_x=x, center_y=y)
        self.width = ancho
        self.height = alto
        self.destruido = False
        self.textura_normal = arcade.load_texture(imagen)
        self.textura_destruido = arcade.load_texture("imagenes/objeto_destruido.png")
        
    def cambiar_textura(self, nueva_textura=None):
        if nueva_textura:
            self.texture = arcade.load_texture(nueva_textura)
        else:
            self.texture = self.textura_destruido
        self.destruido = True

class TipoObjeto2(arcade.Sprite):
    def __init__(self, imagen, x, y, ancho, alto):
        super().__init__(imagen, center_x=x, center_y=y)
        self.width = ancho
        self.height = alto
        self.destruido = False
        self.textura_normal = arcade.load_texture(imagen)
        self.textura_destruido = arcade.load_texture("imagenes/objeto2_destruido.png")
        
    def cambiar_textura2(self, nueva_textura=None):
        if nueva_textura:
            self.texture = arcade.load_texture(nueva_textura)
        else:
            self.texture = self.textura_destruido
        self.destruido = True