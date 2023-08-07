import numpy
import PySimpleGUI as sg

DIMENSION = 15 #dpi
N = 30

class Game:
#SELF  apunta al atributo de la clase  self.(nombre atributo) significado=MISMO(mismo objeto) //se usa para acceder al objeto de la clase(nombre objeto creado = self)
    def __init__(self, T=200): #CONSTRUCTOR creado dos matrices, anterior (anterior) y nueva (la que se va a generar), se instancia la clase y viene derecho para aca
        self.N = N
        self.matriz_anterior = numpy.zeros(N * N, dtype='i').reshape(N, N) # i (int) /RESHAPE rearma la matrix
        self.matriz = numpy.zeros(N * N, dtype='i').reshape(N, N) #numpy.zeros(): devuelve un array del tamaño y tipo indicados inicializando sus valores con ceros
        self.T = T   #numpy.zeros me crea una matriz llena de ceros

        for i in range(0, self.N):
            for j in range(0, self.N): #DESDE HASTA N seteamos la matriz con ceros
                self.matriz_anterior[i][j] = 0
        self.main_graphics() #grafica toda la ventana completa
        self.setup()
#PLAY Esta es el loop principal del juego, recorre las matrices (anterior y nueva) para ver
#cómo reacciona la próxima generación, controlando el conteo configurado.

    def play(self):
        """ LOOP PRINCIPAL. """

        self.tick = 1 # TICK Las marcas son los valores utilizados para mostrar puntos específicos en el eje de coordenadas.
        while self.tick <= self.T:

            for i in range(self.N): # i  representa filas , j representa las columnas 
                for j in range(self.N):
                    live = self.rodeo(i, j)
                    if (self.matriz_anterior[i][j] == 1 and live < 2): #si esta vivo y tiene menos de dos vecinos, MUERE
                        self.matriz[i][j] = 0
                    elif (self.matriz_anterior[i][j] == 1 and (live == 2 or live == 3)): #si esta vivo y tiene 2 o 3 vecinos vivos, VIVE
                        self.matriz[i][j] = 1
                    elif (self.matriz_anterior[i][j] == 1 and live > 3): #si esta vivo y tiene mas de 3 vecinos vivos? si es si, MUERE (sobrepoblacion) 
                        self.matriz[i][j] = 0
                    elif (self.matriz_anterior[i][j] == 0 and live == 3): #si es apagado y tiene 3 vecinos vivos, VIVE
                        self.matriz[i][j] = 1

            self.matriz_anterior = self.matriz.copy()
            self.drawing()
            self.tick += 1 #contador de tiempo. delay. tic de reloj. 

    def rodeo(self, i, j):
        s = 0
        for x in [i - 1, i, i + 1]:   # ?
            for y in [j - 1, j, j + 1]:
                if (x == i and y == j): #omitimos el punto en si. solo queremos los vecinos 
                    continue
                if (x != self.N and y != self.N): #si un cuadrado paso de cero a uno. 
                    s += self.matriz_anterior[x][y]
                elif (x == self.N and y != self.N):  #matriz toroidal , fuera cuadricula
                    s += self.matriz_anterior[0][y]
                elif (x != self.N and y == self.N):
                    s += self.matriz_anterior[x][0]
                else:
                    s += self.matriz_anterior[0][0]
        return s #retorna s a la linea 30

    def main_graphics(self):
        self.graph = sg.Graph((600, 600), (0, 0), (450, 450), key='GRAPH', #ventana grafica 600 x 600 pixeles, 450 x 450 marcos
                              change_submits=True, drag_submits=False,
                              background_color='Gray')
        layout = [
            [
                [
                    [
                        sg.Text('Delay (ms)'),
                        sg.Slider((0, 800), 100,orientation='h', # 0-800 tiempo, 100 por defecto 
                                  key='SLIDER', enable_events=True, size=(20, 15)),
                        sg.Text('       Nro Generaciones'),
                        sg.Slider([0, 1000], default_value=22, orientation='h', #0-1000 iteraciones, 22 por defecto
                                  size=(20, 15),enable_events=True, key='SLIDER2')
                    ],
                    sg.Button('COMENZAR', key='INICIO', disabled=False),
                    sg.Text('           Coloque celdas iniciales', key='SUBTITLE', size=(30, 1), font='ARIAL 10',)

                ],
                self.graph #cuadro gris
            ]
        ]

        self.window = sg.Window('Juego de la Vida (Conway)', layout, finalize=True)
        event, values = self.window.read(timeout=0) #evento que nos va a ir marcando el ciclo 
        self.delay = values['SLIDER']

    def drawing(self): #Lleva a cabo ,junto con la función loop, el GRAFICADO y la actualización del cuadro
#principal del juego, como también actualizando los valores del label contador del
#generaciones.
        self.graph.erase() #dependiendo de la nueva configuracion se pintaran los cuadros, prendido o apagado
        for i in range(self.N):
            for j in range(self.N):
                if self.matriz_anterior[i][j]:
                    self.graph.draw_rectangle((i * DIMENSION, j * DIMENSION),  #DIBUJANDO EN GRIS siempre y cuando tenga valor 1, todo el tiempo
                                              (i * DIMENSION + DIMENSION,
                                               j * DIMENSION + DIMENSION),
                                              line_color='white', fill_color='Green')

        event, values = self.window.read(timeout=self.delay)
        self.delay = values['SLIDER'] #cantidad tiempo
        self.T = int(values['SLIDER2']) #cantidad de generaciones
        self.window['SUBTITLE'].update('Generacion {}'.format(self.tick))

    def setup(self): #funcion que nos permite elegir que celula estara viva o no. parametros antes de iniciar juego/ valores por default
        ids = []
        for i in range(self.N):
            ids.append([]) #append Con este método, puedes agregar un elemento al final de la lista. 
            for j in range(self.N):
                ids[i].append(0)

        while True: #CICLO INFINITO / detecta movimientos del mouse
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'INICIO':
                break
            mouse = values['GRAPH'] #funcion que nos permite tomar el movimiento del mouse

            if event == 'GRAPH':
                if mouse == (None, None): #si hizo click afuera del cuadro continua
                    continue
                mouse_x = mouse[0] // DIMENSION #capta movimiento del mouse, cuando arrancamos poniendo que celulas estan vivas
                mouse_y = mouse[1] // DIMENSION
                if self.matriz_anterior[mouse_x][mouse_y] == 1: #pregunta si esta pintado, si le hicimos click, si esta en 1 y hacemos clic pasa a cero. 
                    mouse_cords = ids[mouse_x][mouse_y]
                    self.graph.delete_figure(mouse_cords)
                    self.matriz_anterior[mouse_x][mouse_y] = 0 #setea la matriz en cero
                else: #entra aca si no esta pintado , al hacer clic a un despintado pasa a pintado
                    mouse_cords = self.graph.draw_rectangle((mouse_x * DIMENSION, mouse_y * DIMENSION), #PINTAMOS CON MOUSE
                                                            (mouse_x * DIMENSION + DIMENSION,
                                                             mouse_y * DIMENSION + DIMENSION),
                                                            line_color='black', fill_color='LightGray')
                    ids[mouse_x][mouse_y] = mouse_cords
                    self.matriz_anterior[mouse_x][mouse_y] = 1
        if event == sg.WIN_CLOSED: #evento que cierra la ventana 
            self.window.close()
            exit()
        else:
            self.window['INICIO'].update(disabled=True) #se detecta el evento del boton INICIO/ al apretarlo se desactiva y no se puede volver a apretar

if (__name__ == "__main__"):
    game = Game(T=200) #200 milisegundos, lo que tarda en mostrar un proceso y otro . intancia de la clase 
    game.play()
    sg.popup('  Fin de generaciones...')
    game.window.close()