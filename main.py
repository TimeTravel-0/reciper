#!/usr/bin/env python

class port:
    def __init__(self,name="unnamed"):
        self.name = name
        self.loaded = False
    def load(self, line):
        j, self.name, block_id, self.direction, self.relative_amount, self.unit, self.allow_open = line        
        self.loaded = True
        #self.identify()
    def identify(self):
        if self.loaded:
           print "   ~~~~PORT~~~~\n   name: %s\n   direction: %s\n   relative_amount: %s\n   unit: %s\n   allow_open: %s"%(self.name, self.direction, self.relative_amount, self.unit, self.allow_open)
    def get_direction(self):
        return self.direction
    def get_name(self):
        return self.name
    def draw(self):
        
        my_font = pygame.font.SysFont("Courier", 16)
        
        color = (0,0,128)
        if self.direction == "out":
            color = (128,0,0)
        if self.direction == "in":
            color = (0,128,0)
        return my_font.render(self.name, True, color)
        

class block:
    def __init__(self,name="unnamed",position=[0,0]):
        self.name = ""
        self.position = position
        self.inputs = []
        self.outputs = []
        self.loaded = False
        self.width = 0
        self.height = 0
        self.dragged = False
        return
    def __exit__(self):
        return

    def identify(self):
        if self.loaded:       
            print "~~~~BLOCK~~~~\nname: %s\nduration: %f\noperation: %s\ninputs: %i\noutputs: %i"%(self.name, self.duration, self.operation, len(self.inputs),len(self.outputs))
            for i in self.inputs:
                i.identify()
            for i in self.outputs:
                i.identify()

    def load_block(self, i, blocks_f):
        for line in blocks_f:
            if line[0] == i:
                #print "loading:",line
                i, self.name, self.duration, self.operation = line
                self.loaded = True
        return

    def load_ports(self, i, ports_f):
        if not self.loaded:
            return
        for line in ports_f:
            if line[2] == i:
                new_port = port()
                new_port.load(line)
                d = new_port.get_direction()
                if d == "out":
                    self.outputs.append(new_port)
                if d == "in":
                    self.inputs.append(new_port)

    def draw(self, surface):

        
        my_font = pygame.font.SysFont("Courier", 16)
        label = my_font.render(self.name, True, (0,0,0))
        surface.fill((200,200,200), (self.position[0], self.position[1], self.width, self.height))

        in_max_width = 0
        out_max_width = 0
         
        surface.blit(label, [self.position[0]+self.width/2-label.get_width()/2, self.position[1]])
        for i,v in enumerate(self.inputs):
            d = v.draw()
            p = [self.position[0], self.position[1] +i*d.get_height()+20]
            surface.blit(d,  p)
            self.height = max(self.height, p[1]-self.position[1]+d.get_height())
            in_max_width = max(in_max_width, d.get_width())
        for i,v in enumerate(self.outputs):
            d = v.draw()
            p = [self.position[0]+ self.width - d.get_width(), self.position[1] +i*d.get_height()+20]
            surface.blit(d, p)
            self.height = max(self.height, p[1]-self.position[1]+d.get_height())
            out_max_width = max(out_max_width, d.get_width())
        self.width = max(self.width, out_max_width + in_max_width+20)
        return

    def hit(self, pos):
        if pos[0]>self.position[0]:
            if pos[1]>self.position[1]:
                if pos[0]<self.position[0]+self.width:
                    if pos[1]<self.position[1]+self.height:
                        return True
        return False

    def drag(self, pos):
        if not self.hit(pos):
            return
        self.dragged = True
        self.drag_start_offset = [pos[0]-self.position[0],pos[1]-self.position[1]]
        return

    def drop(self, pos):
        self.move(pos)
        self.dragged = False
        return                
                
    def move(self, pos):
        if self.dragged:
            self.position[0] = pos[0] - self.drag_start_offset[0]
            self.position[1] = pos[1] - self.drag_start_offset[1]
        return



class recipe:
    def __init__(self):
        self.blocks = []
        return
    def load(self,instances_fn, links_fn, blocks_fn, ports_fn):
        instances_f = self.csvload(instances_fn)
        links_f = self.csvload(links_fn)
        blocks_f = self.csvload(blocks_fn)
        ports_f = self.csvload(ports_fn)

        #print instances_f
        #print links_f
        #print blocks_f
        #print ports_f

        for instance in instances_f:
            i,j,x,y = instance
            new_block = block("",[x,y])
            new_block.load_block(j,blocks_f)
            new_block.load_ports(j,ports_f)
            new_block.identify()
            
            self.blocks.append(new_block)

    def csvload(self,fn):
        f = file(fn,"r")
        d=f.readlines()
        f.close()
        lines = []
        for line in d:
            items = line.rstrip().split(";")
            items = [self.csvinterpret(i) for i in items]
            lines.append(items)
        return lines[1:]

    def csvinterpret(self,data):
        try:
            data_int = int(data)
            data_float = float(data)
            if data_float-data_int > 1/4096:
                data = data_float
            else:
                data = data_int
        except:
            data = data
        return data

    def draw(self, surface):
        for b in self.blocks:
            b.draw(surface)
            
    def drag(self, pos):
        for b in self.blocks:
            b.drag(pos)

    def drop(self, pos):
        for b in self.blocks:
            b.drop(pos)

    def move(self, pos):
        for b in self.blocks:
            b.move(pos)


import pygame
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1024, 768))

r = recipe()
r.load("instances.csv","links.csv","blocks.csv","ports.csv")

clock = pygame.time.Clock()
loop = True
while loop:
    screen.fill((250, 250, 250))
    r.draw(screen)
    pygame.display.flip()
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            r.drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            r.drop(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            r.move(event.pos)
        elif event.type == pygame.KEYDOWN:
            pressed_key = event.key
pygame.quit()
