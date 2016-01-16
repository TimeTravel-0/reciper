#!/usr/bin/env python

class link:
    def __init__(self):
        self.to_instance = False
        self.from_instance = False
        self.loaded = False
        return
    def load(self, line, objects):
        self.id, from_instance, to_instance, from_port, to_port = line
        for o in objects:
            print o.get_id()
            if o.get_id() == from_instance:
                self.from_instance = o
            if o.get_id() == to_instance:
                self.to_instance = o

        if self.to_instance and self.from_instance:				
            self.from_port = self.from_instance.get_output(from_port)
            self.to_port = self.to_instance.get_input(to_port)
		    #for l in o.get_inputs() + o.get_outputs()
		    #print l
		    #print line
            self.loaded = True
		
    def draw(self, surface):
        if not self.loaded:
            return
        start_point = self.from_instance.get_position()
        end_point = self.to_instance.get_position()
        
        start_point = self.from_port.get_anchor_position()
        end_point = self.to_port.get_anchor_position()
        color = [64,64,64]
        pygame.draw.aaline(surface, color, start_point, end_point,3)
        
        
        
        
        my_font = pygame.font.SysFont("Courier", 12)
        
        color = (128,128,128)
        
        r = my_font.render(str(self.id), True, color)
        x_pos = (start_point[0]+end_point[0])/2-r.get_width()/2
        y_pos = (start_point[1]+end_point[1])/2-r.get_height()/2
        
        surface.blit(r,  [x_pos,y_pos])        
        

class port:
    def __init__(self,name="unnamed"):
        self.name = name
        self.loaded = False
        self.height = 0
        self.width = 0
        self.position = [0,0]
    def load(self, line):
        self.port_id, self.name, self.block_id, self.direction, self.relative_amount, self.unit, self.allow_open = line        
        self.loaded = True
        #self.identify()
    def get_id(self):
		return self.port_id
    def identify(self):
        if self.loaded:
           print "   ~~~~PORT~~~~\n   name: %s\n   direction: %s\n   relative_amount: %s\n   unit: %s\n   allow_open: %s"%(self.name, self.direction, self.relative_amount, self.unit, self.allow_open)
    def get_direction(self):
        return self.direction
    def get_name(self):
        return self.name
    def get_anchor_position(self):
		if not self.loaded:
			return
		if self.direction == "in":
			anchor_x = self.position[0]
			anchor_y = self.position[1]+self.get_height()/2
			return [anchor_x, anchor_y]
		if self.direction == "out":
			anchor_x = self.position[0]+self.get_width()
			anchor_y = self.position[1]+self.get_height()/2
			return [anchor_x, anchor_y]
			
    def set_position(self,pos):
		self.position = pos
    def get_width(self):
		return self.width
    def get_height(self):
		return self.height
    def draw(self,surface):
        
        my_font = pygame.font.SysFont("Courier", 12)
        
        color = (0,0,128)
        if self.direction == "out":
            color = (128,0,0)
        if self.direction == "in":
            color = (0,128,0)
        r = my_font.render(self.name+" ("+str(self.relative_amount)+self.unit+") ["+str(self.port_id)+"]", True, color)
        self.width = r.get_width()
        self.height = r.get_height()
        
        surface.blit(r,  self.position)
        return #r
        

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
        self.id = False
        return
    def __exit__(self):
        return
        
    def get_position(self):
		return self.position
		
    def get_input(self,i):
		for item in self.inputs:
			if item.get_id() == i:
				return item

    def get_output(self,i):
		for item in self.outputs:
			if item.get_id() == i:
				return item				
			
        
    def get_id(self):
		return self.id

    def identify(self):
        if self.loaded:       
            print "~~~~BLOCK~~~~\nname: %s\nduration: %f\noperation: %s\ninputs: %i\noutputs: %i"%(self.name, self.duration, self.operation, len(self.inputs),len(self.outputs))
            for i in self.inputs:
                i.identify()
            for i in self.outputs:
                i.identify()

    def load_block(self, i, blocks_f, instance_id):
        for line in blocks_f:
            if line[0] == i:
                #print "loading:",line
                self.block_id, self.name, self.duration, self.operation = line
                self.id = instance_id
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

        
        my_font = pygame.font.SysFont("Courier", 14)
        label = my_font.render(self.name+ "["+str(self.id)+","+str(self.block_id)+"]", True, (0,0,0))
        surface.fill((200,200,200), (self.position[0], self.position[1], self.width, self.height))

        in_max_width = 0
        out_max_width = 0
         
        surface.blit(label, [self.position[0]+self.width/2-label.get_width()/2, self.position[1]])
        for i,v in enumerate(self.inputs):
            p = [self.position[0], self.position[1] +i*v.get_height()+20]
            v.set_position(p)
            v.draw(surface)
            self.height = max(self.height, p[1]-self.position[1]+v.get_height())
            in_max_width = max(in_max_width, v.get_width())
            
        for i,v in enumerate(self.outputs):
            p = [self.position[0]+ self.width - v.get_width(), self.position[1] +i*v.get_height()+20]
            v.set_position(p)
            v.draw(surface)
            self.height = max(self.height, p[1]-self.position[1]+v.get_height())
            out_max_width = max(out_max_width, v.get_width())
            
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
        self.links = []
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
            new_block.load_block(j,blocks_f,i)
            new_block.load_ports(j,ports_f)
            new_block.identify()
            self.blocks.append(new_block)
            
        for line in links_f:
			new_link = link()
			new_link.load(line, self.blocks)
			self.links.append(new_link)

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

        for l in self.links:
			l.draw(surface)		
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

screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)

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
        elif event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
pygame.quit()
