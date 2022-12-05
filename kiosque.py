"""
Kiosque

(c) 2022 by Mathieu, etc.

Projet pour une borne "Dans Mon Quartier" de Nils Chertier.

Concept:

1. Un gif animé en fond d'écran, plein écran
2. Un menu accessible au clavier (sélection en (gras ?) + entrée pour lancer)
3. Menu "tabat" --> 1 vidéo au hasard via VLC puis retour au menu
4. Menu "dans mon quartier" --> lancer DMQ, puis retour au menu.

TODO:

tout.

Animated GIF : https://pypi.org/project/pygame-animatedgif/
"""

import os,time
import pygame
import pygame.gfxdraw
import subprocess
import shutil
import platform
import json
from pygame_animatedgif import AnimatedGifSprite

normalColor = (0x3b,0x3e,0x4e)
highlightColor = (0xad,0x3e,0x4e)


class fontKiosque():
    def __init__(self, fontA, fontB, textA, textB, sizeA, sizeB, posAX, posBX, posAY, posBY, startX, startY, scale):
        self.posAX = posAX * scale
        self.posAY = posAY * scale
        self.posBX = posBX * scale
        self.posBY = posBY * scale
        self.startX = startX
        self.startY = startY
        self.fontA = pygame.font.Font(os.path.join("font",fontA),int(sizeA*scale))
        self.fontB = pygame.font.Font(os.path.join("font",fontB),int(sizeB*scale))
        self.textANS = self.fontA.render(textA, True, normalColor)
        self.textAS  = self.fontA.render(textA, True, highlightColor)
        self.textBNS = self.fontB.render(textB, True, normalColor)
        self.textBS  = self.fontB.render(textB, True, highlightColor)
        self.selected = False
        self.callbackfunc = None
        
    def drawOn(self,surface):
        if self.selected:
            surface.blit(self.textAS,(self.posAX+self.startX,self.posAY+self.startY))
            surface.blit(self.textBS,(self.posBX+self.startX,self.posBY+self.startY))

        else:
            surface.blit(self.textANS,(self.posAX+self.startX,self.posAY+self.startY))
            surface.blit(self.textBNS,(self.posBX+self.startX,self.posBY+self.startY))
            
    def select(self):
        self.selected = True
        
    def deselect(self):
        self.selected = False
        
    def setCallback(self, func):
        self.callbackfunc = func
        
    def callback(self):
        return self.callbackfunc()


def launchVideo(direct, w, h):    
    pygame.quit()
    vlc = "vlc"
    if platform.system() == "Windows":
        vlc = "vlc.exe"        
    for root,dirs,files in os.walk(os.path.join("media", direct)):
        for f in files:
            subprocess.run([shutil.which(vlc), "--fullscreen", "--no-video-title", "--no-keyboard-events", "--video-on-top","-Idummy", os.path.join(root, f), "vlc://quit"])
    print("quit and restart with %s %d %d"%(direct, w, h))
    return setup(w, h)

def launchGame(direct, executable, w, h):
    pygame.quit()    
    if not os.path.isabs(direct):
        subprocess.run([os.path.join("media",direct,executable)],shell=True)
    else:
        subprocess.run([os.path.join(direct,executable)],shell=True)
    print("quit and restart with %s %d %d"%(direct, w, h))
    return setup(w, h)

def setup(w=0, h=0):
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)    
    return screen

def main():

    print("begin")
    
    screen = setup(0,0)    

    dog = AnimatedGifSprite((0,0), os.path.join("img","fond_root.gif"))
    
    screenx = pygame.display.get_surface().get_width()
    screeny = pygame.display.get_surface().get_height()
    
    print("loaded")
        
    scale = min(screenx/dog.rect.width, screeny/dog.rect.height)
    dog.scale(scale)
    dog.rect.x = (screenx-dog.rect.width*scale)/2
    dog.rect.y = (screeny-dog.rect.height*scale)/2
    
    data = {}
    with open("conf/conf.json", "rb") as f:
        data = json.load(f)

    klist = []

    if "apps" in data.keys():
        for app in data["apps"].keys():
            fk = fontKiosque(data["apps"][app]["main"][0], data["apps"][app]["sub"][0], data["apps"][app]["main"][1], data["apps"][app]["sub"][1], data["apps"][app]["main"][2], data["apps"][app]["sub"][2], data["apps"][app]["main"][3], data["apps"][app]["sub"][3], data["apps"][app]["main"][4], data["apps"][app]["sub"][4], dog.rect.x, dog.rect.y, scale)
            fk.setCallback(lambda: launchGame(app, data["apps"][app]["app"], screenx, screeny))
            klist.append((data["apps"][app]["order"],fk))
    if "videos" in data.keys():
        for vid in data["videos"].keys():
            fk = fontKiosque(data["videos"][vid]["main"][0], data["videos"][vid]["sub"][0], data["videos"][vid]["main"][1], data["videos"][vid]["sub"][1], data["videos"][vid]["main"][2], data["videos"][vid]["sub"][2], data["videos"][vid]["main"][3], data["videos"][vid]["sub"][3], data["videos"][vid]["main"][4], data["videos"][vid]["sub"][4], dog.rect.x, dog.rect.y, scale)
            fk.setCallback(lambda: launchVideo(vid, screenx, screeny))
            klist.append((data["videos"][vid]["order"],fk))
            
    klist = sorted(klist, key=lambda klist: klist[0])
    
    olist=[]
    for a,b in klist:
        olist.append(b)
    klist = olist
    sprite_group = pygame.sprite.Group()
    sprite_group.add(dog)

    dog.play()
    
    print("loop")
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_q:            
                    pygame.quit()
                    return
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                    for i in range(3):
                        if i == selected:
                            klist[i].select()
                        else:
                            klist[i].deselect()
                                       
                if event.key == pygame.K_UP:
                    if selected > 0:
                        selected -= 1
                    else:
                        selected = 2
                    for i in range(3):
                        if i == selected:
                            klist[i].select()
                        else:
                            klist[i].deselect()

                
                if event.key == pygame.K_RETURN:
                    screen = klist[selected].callback()
                    pass


        sprite_group.update(screen)
        sprite_group.draw(screen)
        for fk in klist:
            fk.drawOn(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
