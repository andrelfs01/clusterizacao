from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import AntAgent, DataAgent
import pandas as pd


class Modelo(Model):
    """
    A model with some number of ants and data.
    """
    m = 5
    ants = 1
    data = pd.DataFrame()

    def __init__(self, ants=1000, grid_size=5, data=pd.DataFrame() ):
        super().__init__()
        #self.running = True
        self.ants = ants
        self.m = grid_size
        self.grid = MultiGrid(int(self.m), int(self.m), True)
        self.schedule = RandomActivation(self)
        self.verbose = False  # Print-monitoring
        self.data = data

        # Create ants
        for i in range(self.ants):
            # Add the agent ant to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while len(self.grid.get_cell_list_contents((x, y))) != 0:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                print("re-posicionando")
            a = AntAgent("ant_"+str(i), (x, y), self)
            self.schedule.add(a)            
            self.grid.place_agent(a, (x, y))

        # Create data
        for i in self.data.index:
            # Add the agent ant to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while len(self.grid.get_cell_list_contents((x, y))) != 0:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                print("re-posicionando")
            d = DataAgent(i, (x, y), self)
            self.schedule.add(d)
            self.grid.place_agent(d, (x, y))

    def step(self):
        #print(self.data)
        self.schedule.step()
        #self.datacollector.collect(self)

    def run_model(self, step_count=2000):

        if self.verbose:
            print('Initial number ants: ',
                  self.ants)
            print('Initial data: ',
                  self.data)

        for i in range(step_count):
            self.step()



