from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from random import uniform
import math  
import random

class AntAgent(Agent):
    unique_id = 'ant_'
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.load = None
        self.pos = pos
        self.s = 3
        self.k1 = 0.03
        self.k2 = 0.01
        self.alpha = 1.5
        self.f = 0

    def step(self):
        # compute f(xi) - mudeide lugar
        #  if unloaded ant AND cell occupiedby item xi:
        if (self.load is None and self.tem_dado(self.pos)):
            self.f = self.compute_fxi()
            pick_probability = self.compute_pp()      
            #pick up a item xi with probability pp(xi)
            #print ("f: {} - pick: {}".format(self.f, pick_probability))
            if (uniform(0, 1) <=  pick_probability):
                self.load = self.pega_dado(self.pos)
        
        # else if  ant carrying item xi and cell empty
        elif ((self.load is not None) and (not self.tem_dado(self.pos)) and not (self.tem_formiga(self.pos))):
            self.f = self.compute_fxi()
            drop_probability = self.compute_pd()      
            #pick up a item xi with probability pp(xi)
            #print ("f: {} - drop: {}".format(self.f, drop_probability))
            if (uniform(0, 1) <=  drop_probability):
                self.load = None
        self.move()
    
    def move (self):
        position = self.pos
        lista_vizinhos = self.model.grid.get_neighborhood(position, True, False, 1)
        lista_vizinhos_possiveis = list()
        for vizinho in lista_vizinhos:
            # se carrega dado, só vai em celula vazia
            if (self.load is not None):
                if (len(self.model.grid.get_cell_list_contents(vizinho)) == 0):
                    lista_vizinhos_possiveis.append(vizinho)
            # se nao carrega dado, vai em celulas sem formiga
            else:
                if (not self.tem_formiga(vizinho)):
                    lista_vizinhos_possiveis.append(vizinho)
        if (len(lista_vizinhos_possiveis) > 0):
            destino = random.choice(lista_vizinhos_possiveis)
            if (self.load is not None):
                self.model.grid.move_agent(self.load, destino)    
            self.model.grid.move_agent(self, destino)

    def tem_formiga(self, posicao):
        ocupantes = self.model.grid.get_cell_list_contents(posicao)
        for o in ocupantes:
            if (isinstance(o, AntAgent) and o != self) :
                return True
        return False

    def tem_dado(self, posicao):
        ocupantes = self.model.grid.get_cell_list_contents(posicao)
        for o in ocupantes:
            if (isinstance(o, DataAgent) and o != self.load) :
                return True
        return False

    def pega_dado(self, posicao):
        ocupantes = self.model.grid.get_cell_list_contents(posicao)
        for o in ocupantes:
            if (isinstance(o, DataAgent)) :
                return o
        return None
    
    def compute_fxi(self):
        ocupantes = self.model.grid.get_cell_list_contents(self.pos)
        for o in ocupantes:
            if (isinstance(o, DataAgent)) :
                return o.f(self.s, self.alpha)
        return 0

    def compute_pd(self):
        return (self.f/ (self.k2 + self.f))**2

    def compute_pp(self):
        return (self.k1/ (self.k1 + self.f))**2

class DataAgent(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.unique_id = 'data_'+ str(unique_id)
        self.index_df =  unique_id
        self.pos = pos

    def step(self):
        pass

    def __str__(self):
        return "ID: {}".format(self.unique_id)

    def f(self, s, alpha):
        #
        soma = 0
        # para cada dado na vizinhanca SxS
        vizinhos = self.model.grid.get_neighborhood(self.pos, True, False, 1)
        lista = list()
        for v in vizinhos:
            ocupantes = self.model.grid.get_cell_list_contents(v)
            for o in ocupantes:
                if (isinstance(o, DataAgent) and o != self) :
                    lista.append(o)
        for d in lista:
            soma = soma + (1 - ((self.euclidean(d))/alpha))
        f = soma / (s**2) 
        return f if f > 0 else 0

    #CALCULO DE DISTANCIA QUANDRADA ENTRE DOIS PADROES
    def euclidean(self, b):
        columns = ['sepal_length', 'sepal_width','petal_length','petal_width']
        i = 0

        a = self.model.data.iloc[self.index_df] 
        b = self.model.data.iloc[b.index_df]

        for feature in columns:
            i = i + ((a[feature] - b[feature]) ** 2 )
        return math.sqrt(i)