from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
import pandas as pd
from agents import AntAgent, DataAgent
from model import Modelo as modelo


def aca_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is AntAgent:
        portrayal["Shape"] = "resources/ant.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    elif type(agent) is DataAgent:
        portrayal["Shape"] = "resources/data.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "White"

    return portrayal


chart_element = ChartModule([{"Label": "Ant", "Color": "#AA0000"},
                             {"Label": "Data", "Color": "#666666"}])

columns = ['sepal_length', 'sepal_width','petal_length','petal_width','class']
df = pd.read_csv('../iris.data', names=columns)

model_params = {                
                "ants": UserSettableParameter('slider', 'ants', 20, 1, 40),
                "grid_size": 25,
                "data": df
                }

canvas_element = CanvasGrid(aca_portrayal, model_params["grid_size"], model_params["grid_size"], 750, 750)

server = ModularServer(modelo, [canvas_element], "ACA", model_params)
server.port = 8522
server.launch()