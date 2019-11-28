from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import AntAgent, DataAgent, BordaAgent
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

class Modelo(Model):
    """
    A model with some number of ants and data.
    """
    m = 5
    ants = 1
    data = pd.DataFrame()
    grid_clusters = {}
    lista_bordas = list()

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
        if (self.schedule.steps == 500 or self.schedule.steps == 1000 or self.schedule.steps == 1500 or
        self.schedule.steps == 2000 or self.schedule.steps == 2500 or
        self.schedule.steps == 3000 or self.schedule.steps == 3500 or
        self.schedule.steps == 4000 or self.schedule.steps == 4500 or
        self.schedule.steps == 5000):
            self.validar_clusters()
        if (self.schedule.steps == 510 or self.schedule.steps == 1010 or self.schedule.steps == 1510 or
        self.schedule.steps == 2010 or self.schedule.steps == 2510 or
        self.schedule.steps == 3010 or self.schedule.steps == 3510 or
        self.schedule.steps == 4010 or self.schedule.steps == 4510 or
        self.schedule.steps == 5010):
            self.remover_bordas()
        self.schedule.step()

    def validar_clusters(self):
        #print(self.grid.grid)
        x = list()
        y = list()
        ids = list()
        #classes= list()

        for l in self.grid.grid:
            for c in l:
                for agent in c:
                    #print ("{} - {}".format(agent.unique_id, agent.pos))
                    if "data_" in agent.unique_id:
                        #coloca o dado no data frame
                        x_pos, y_pos = agent.pos
                        ids.append(agent)
                        x.append(x_pos)
                        y.append(y_pos)

        positions = np.column_stack((x, y))
        clustering = DBSCAN(eps=2, min_samples=3).fit(positions)
        
        self.grid_clusters = {}
        self.avaliar_clusters(clustering.labels_, ids)
        self.apresentar_clusters()  
        self.definir_bordas()
        

    def avaliar_clusters(self, indicacoes, agentes):
        for i in range(len(indicacoes)):
            #print("{} - {}".format(agentes[i], indicacoes[i]))
            if indicacoes[i] == -1:
                continue
            if indicacoes[i] in self.grid_clusters.keys():
                cluster = self.grid_clusters.get(indicacoes[i])
                cluster.append(agentes[i])
                self.grid_clusters.update({indicacoes[i]: cluster})
            else:
                cluster = list()
                cluster.append(agentes[i])
                self.grid_clusters.update({indicacoes[i]: cluster})

        classes = list(self.data['class'].unique())

        for numero_cluster in self.grid_clusters.keys():
            cluster = self.grid_clusters.get(numero_cluster)
            indices = list()
            for a in self.grid_clusters.get(numero_cluster):
                indices.append(a.index_df)
                
            dados = self.data.loc[indices, :]
            gini = self.gini_index(dados,classes)
            self.grid_clusters.update({numero_cluster: {'agentes': cluster,'gini':gini}})

    def definir_bordas(self):
        for k in self.grid_clusters.keys():
            #print("Cluster {}:".format(k))
            #indices = list()
            for a in self.grid_clusters.get(k)['agentes']:
                #print(self.grid.get_neighbors(a.pos, True))
                x, y = a.pos

                if (x+1 >= self.grid.width):
                    xp1 = 0
                else:
                    xp1 = x+1

                if (x-1 < 0):
                    xm1 = self.grid.width - 1
                else:
                    xm1 = x - 1
                
                if (y+1 >= self.grid.width):
                    yp1 = 0
                else: 
                    yp1 = y + 1

                if (y-1 < 0):
                    ym1 = self.grid.width - 1
                else:
                    ym1 = y -1

                # x + 1
                if (not self.tem_dado((xp1 ,y))):
                    self.add_borda((xp1 ,y))
                # x - 1
                if (not self.tem_dado((xm1 ,y))):
                    self.add_borda((xm1 ,y))
                # y + 1 
                if (not self.tem_dado((x, yp1))):
                    self.add_borda((x, yp1))
                # y - 1 
                if (not self.tem_dado((x ,ym1))):
                    self.add_borda((x, ym1))
                # x - 1 y - 1
                if (not self.tem_dado((xm1 ,ym1))):
                    self.add_borda((xm1, ym1))
                # x - 1 y + 1
                if (not self.tem_dado((xm1 ,yp1))):
                    self.add_borda((xm1, yp1))
                # x + 1 y - 1
                if (not self.tem_dado((xp1 ,ym1))):
                    self.add_borda((xp1, ym1))
                # x + 1 y + 1
                if (not self.tem_dado((xp1 ,yp1))):
                    self.add_borda((xp1, yp1))

    def gini_index(self, dados, classes):
        # quantidade de elementos no cluster
        n_instances = len(dados)
        # calculo do indice de gini
        gini = 0.0
        score = 0.0
        # indice do grupo, analisando o indice para cada classe
        for classe in classes:
            saida = dados['class'].value_counts()
            if hasattr(saida, classe):
                p = saida.loc[classe] / n_instances
            else:
                p = 0
            score += p * p
        # ponderando o indice pelo tamenho do grupo
        gini += (1.0 - score)
        return gini

    def apresentar_clusters(self):
        with open('log_aca.txt', 'a') as f:
            print("Step: {}".format(self.schedule.steps), file=f)
            for k in self.grid_clusters.keys():
                print("Cluster {}:".format(k), file=f)
                indices = list()
                for a in self.grid_clusters.get(k)['agentes']:
                    indices.append(a.index_df)
                dados = self.data.loc[indices, :]
                print("Dados no cluster:", file=f)
                print(dados['class'].value_counts(), file=f)
                print("Gini index: {}".format(self.grid_clusters.get(k)['gini']), file=f)
                print("", file=f)

    def tem_dado(self, posicao):
        ocupantes = self.grid.get_cell_list_contents(posicao)
        for o in ocupantes:
            if (isinstance(o, DataAgent) or isinstance(o, BordaAgent) ) :
                return True
        return False
    
    def add_borda(self, posicao):
        a = BordaAgent("borda", posicao, self)
        self.schedule.add(a)  
        self.lista_bordas.append(a)       
        self.grid.place_agent(a, (posicao))

    def remover_bordas(self):
        print("removendo")
        for o in self.lista_bordas:
            if (isinstance(o, BordaAgent) ) :
                print("borda")
                self.grid.remove_agent(o)
        self.lista_bordas = list()
