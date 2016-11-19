from mesa import Agent
import random
from random import randint

from shape_model.items import Item

class BaseStation(Agent):
    '''
    A BaseStation is an Agent that cannot move
    '''
    def __init__(self, model,pos,id):
        self.model = model
        self.pos = pos
        self.id = id

        self.items = []
        self.delivered_items = 0;
        pass

    def step(self):
        if randint(1, 10) <= 1:
            x = random.randrange(self.model.width)
            y = random.randrange(self.model.height)
            while not self.model.grid.is_cell_empty((x, y)):
                x = random.randrange(self.model.width)
                y = random.randrange(self.model.height)
            itemdestination = (x,y)
            item = Item(destination=itemdestination, priority=0,id=str(self.id) + "_" + str(len(self.items)))
            self.items.append(item)
            print("Created item {}, destination: {}, priority:{}".format(item.id, item.destination,item.priority))


    def pickupItem(self):
        if not len(self.items)== 0:
            item = random.choice(self.items)
            self.items.remove(item)
            self.delivered_items += 1
            return item
        else:
            return None

    def get_number_of_items(self, delivered=False):
        if delivered:
            return self.delivered_items;
        return len(self.items)