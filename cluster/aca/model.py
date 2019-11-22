from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import AntAgent, DataAgent
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        self.v = False
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
        if (self.schedule.steps == 5000  and not self.v):
            self.validar_clusters()
            self.v = True
        else:
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

    def validar_clusters(self):
        print(self.grid.grid)
        #grid é um multgrid
        x = list()
        y = list()
        classes= list()
        
        for l in self.grid.grid:
            for c in l:
                for agent in c:
                    print ("{} - {}".format(agent.unique_id, agent.pos))
                    if "data_" in agent.unique_id:
                        #coloca o dado no data frame
                        x_pos, y_pos = agent.pos
                        if (self.data.iloc[agent.index_df]['class'] == 'Iris-virginica'):
                            classe = 0
                        elif (self.data.iloc[agent.index_df]['class'] == 'Iris-setosa'):
                            classe = 1
                        else :
                            classe = 2 
                        x.append(x_pos)
                        y.append(y_pos)
                        classes.append(classe)
        print(x)
        print(y)
        Cluster = np.array(classes)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        scatter = ax.scatter(x,y,c=Cluster,s=50)
        # for i,j in centers:
        #     ax.scatter(i,j,s=50,c='red',marker='+')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.colorbar(scatter)
        plt.savefig('clusters.png')
        


