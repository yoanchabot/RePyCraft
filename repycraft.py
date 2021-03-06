import sys
import math
import random
import time

from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

#Moitié de la taille du monde
WORLD_SIZE = 25
HILL_PROB = 5
TREE_PROB = 15
HILL_MAX_SIZE = 10

world = {}

class Model:
    def get_tex(self,file):
        tex = pyglet.image.load(file).texture
        #Gestion minification et magnification
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):
        # Contient pour chaque position du monde la texture du bloc correspondant
        self.world = {}

        self.textures = {}
        #Stone
        self.textures['stone'] = {}
        self.textures['stone']['top'] = self.get_tex('resources/textures/blocks/stone.png')
        self.textures['stone']['bottom'] = self.get_tex('resources/textures/blocks/stone.png')
        self.textures['stone']['side'] = self.get_tex('resources/textures/blocks/stone.png')
        #Grass
        self.textures['grass'] = {}
        self.textures['grass']['top'] = self.get_tex('resources/textures/blocks/_grass_top.png')
        self.textures['grass']['bottom'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['grass']['side'] = self.get_tex('resources/textures/blocks/grass_side.png')
        #Dirt
        self.textures['dirt'] = {}
        self.textures['dirt']['top'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['dirt']['bottom'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['dirt']['side'] = self.get_tex('resources/textures/blocks/dirt.png')
        #Log Acacia
        self.textures['logAcacia'] = {}
        self.textures['logAcacia']['top'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        self.textures['logAcacia']['bottom'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        self.textures['logAcacia']['side'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        # Leaves Acacia
        self.textures['leavesAcacia'] = {}
        self.textures['leavesAcacia']['top'] = self.get_tex('resources/textures/blocks/leaves_acacia.png')
        self.textures['leavesAcacia']['bottom'] = self.get_tex('resources/textures/blocks/leaves_acacia.png')
        self.textures['leavesAcacia']['side'] = self.get_tex('resources/textures/blocks/leaves_acacia.png')
        #Log Oak
        self.textures['logOak'] = {}
        self.textures['logOak']['top'] = self.get_tex('resources/textures/blocks/log_oak.png')
        self.textures['logOak']['bottom'] = self.get_tex('resources/textures/blocks/log_oak.png')
        self.textures['logOak']['side'] = self.get_tex('resources/textures/blocks/log_oak.png')
        #Leaves Oak
        self.textures['leavesOak'] = {}
        self.textures['leavesOak']['top'] = self.get_tex('resources/textures/blocks/leaves_oak.png')
        self.textures['leavesOak']['bottom'] = self.get_tex('resources/textures/blocks/leaves_oak.png')
        self.textures['leavesOak']['side'] = self.get_tex('resources/textures/blocks/leaves_oak.png')

        self.batch = pyglet.graphics.Batch()

        #Génération du sol
        n = WORLD_SIZE
        y = 0
        for x in range(-n, n + 1, 1):
            for z in range(-n, n + 1, 1):
                self.addBlock((x, y, z), 'grass')
                self.addBlock((x, y-1, z), 'dirt')
                self.addBlock((x, y-2, z), 'stone')
                self.addBlock((x, y-3, z), 'stone')

        #Génération de collines
        o = WORLD_SIZE - HILL_MAX_SIZE
        for _ in range(HILL_PROB):
            #Position de la colline
            xHill = random.randint(-o,o)
            zHill = random.randint(-o,o)
            yHill = -1
            #Hauteur et largeur
            hHill = random.randint(1,HILL_MAX_SIZE)
            sHill = random.randint(4,8)
            d = 1
            for y in range(yHill, yHill + hHill):
                for x in range(xHill - sHill, xHill + sHill + 1):
                    for z in range(zHill - sHill, zHill + sHill + 1):
                        if (x - xHill) ** 2 + (z - zHill) ** 2 > (sHill + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.addBlock((x, y, z), 'grass')
                #Décremente petit à petit la largeur afin de créer une forme pyramidale
                sHill -= d

        #Génération d'arbres
        for _ in range(TREE_PROB):
            xTree = random.randint(-WORLD_SIZE, WORLD_SIZE)
            zTree = random.randint(-WORLD_SIZE, WORLD_SIZE)
            self.addTree((xTree,0,zTree),'oak')

    def draw(self):
        self.batch.draw()

    def addHill(self,position,type):
        print()

    def addTree(self,position,type):
        """
            Ajoute un arbre à la position passée en paramètre
            Parameters:
            position: tuple (x,y,z) contenant la position de l'arbre à ajouter
            type: le type de l'arbre (e.g. oak, acacia, etc.)
        """
        x, y, z = position
        size = random.randint(3,7)
        for sizeTrunc in range(0,size):
            self.addBlock((x, sizeTrunc-1, z), 'logOak')
        for y in range(size-1, size*2):
            self.addBlock((x-1, y, z-1), 'leavesOak')
            self.addBlock((x-1, y, z), 'leavesOak')
            self.addBlock((x-1, y, z+1), 'leavesOak')
            self.addBlock((x, y, z-1), 'leavesOak')
            self.addBlock((x, y, z), 'leavesOak')
            self.addBlock((x, y, z+1), 'leavesOak')
            self.addBlock((x+1, y, z-1), 'leavesOak')
            self.addBlock((x+1, y, z), 'leavesOak')
            self.addBlock((x+1, y, z+1), 'leavesOak')

    def addBlock(self, position, type):
        """
            Ajoute un bloc à la position passée en paramètre
            Parameters:
            position: tuple (x,y,z) contenant la position du bloc à ajouter
            type: le type du bloc (e.g. grass, stone, etc.)
        """
        #Ajout du bloc dans la map du monde
        if position in self.world:
            self.removeBlock(position)
        self.world[position] = type
        #Création des vertex associés au bloc
        x, y, z = position
        X, Y, Z = x + 1, y + 1, z + 1
        texCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['bottom'], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['top'], ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), texCoords)

    def removeBlock(self, position):
        """
        Supprime le bloc situé à la position donnée en paramètre
        Parameters:
            position: tuple (x,y,z) contenant la position du bloc à supprimer
        """
        del self.world[position]

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0]<-90:
            self.rot[0] = -90

    def update(self,dt,keys):
        s = dt * 10
        rotY = -self.rot[1] / 180 * math.pi
        dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        if keys[key.Z]: self.pos[0] += dx; self.pos[2] -= dz
        if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz
        if keys[key.Q]: self.pos[0] -= dz; self.pos[2] -= dx
        if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx
        if keys[key.SPACE]: self.pos[1] += s
        if keys[key.LSHIFT]: self.pos[1] -= s

class Window(pyglet.window.Window):
    # Display FPS
    fpsDisplay = pyglet.clock.ClockDisplay()

    def push(self, pos, rot):
        glPushMatrix()
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2],)
    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.Projection()
        gluPerspective(70,self.width/self.height,0.05,1000)
        self.Model()

    #Gestion de l'exclusivité de la souris (ne sort pas de la fenêtre, plus de curseur (x et y meaningless))
    def setLock(self,state):
        self.lock = state
        self.set_exclusive_mouse(state)
    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(854,480)
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)
        #Permet de stocker l'état courant du clavier (accessible comme un dictionnaire)
        self.keys = key.KeyStateHandler()
        #Association du handler à la fenêtre afin de stocker ses evts clavier
        self.push_handlers(self.keys)

        pyglet.clock.schedule(self.update)

        #Model
        self.model = Model()
        #Player
        self.player = Player((0.5, 1.5, 1.5), (-30, 0))

    #Traitement des mouvements de la souris
    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    #Traitement des clics de la souris
    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            print("Clic gauche")

    #Traitement des evts clavier
    def on_key_press(self,symbol,modifiers):
        #ESCAPE permet de sortir la souris du mode exclusif
        if symbol == key.ESCAPE:
            self.close()
        #E permet de passer la souris en mode exclusif
        elif symbol == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.player.update(dt,self.keys)

    #Rafraichissement de l'affichage
    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
        # Display FPS
        #self.fpsDisplay.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(width=1708, height=960, caption='RePyCraft', resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()