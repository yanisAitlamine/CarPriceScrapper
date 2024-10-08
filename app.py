from scrapegraphai.graphs import SearchLinkGraph
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
from pydantic import BaseModel,Field
from typing import List
import json

# ************************************************
# Define the configuration for the graph
# ************************************************

#specify the schema of the output
class Price(BaseModel):
    value: str = Field(description="Price of the car")

class Prices(BaseModel):
     prices: List[Price]

link_graph_config = {
    "llm": {
        "model": "ollama/llama3.1",
        "temperature": 0,
        "format": "json",  # Ollama needs the format to be specified explicitly
        "base_url": "http://localhost:11434"
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        "base_url": "http://localhost:11434"
    },
    "verbose": True,
    "headless": False
}

graph_config = {
    "llm": {
        "model": "ollama/llama3.1",  # Specify the model for the llm
        "temperature": 0,  # Set temperature parameter for llm
        "format": "json",  # Specify the output format as JSON for Ollama
        "base_url": "http://localhost:11434"
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",  # Specify the model for embeddings
        "base_url": "http://localhost:11434"
    },
    "verbose": True,  # Enable verbose mode for debugging purposes
}

# Initialize LinkScraperGraph with source, and configuration
link_scraper_graph = SearchLinkGraph(
        source="",
        config=link_graph_config
    )

# Initialize SmartScraperGraph with prompt, source, and configuration
smart_scraper_graph = SmartScraperGraph(
    prompt="",
    source="",
    config=graph_config,
    schema=Prices
)

# ************************************************
# Define usefull functions
# ************************************************

#return a list of links from a google search of a car model for retail (in France retail is 'occasion')
def getLinks(brand, model): 
    link_scraper_graph.source="https://www.google.com/search?q="+brand+"+"+model+"+occasion"
    result = link_scraper_graph.run()
        
    output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation
    line_list = set(output.split("\n"))  # Split the JSON string into lines

    return [line for line in line_list if (model.casefold() in line and "google".casefold() not in line)]

#returns a json for a website of the car versions available along with the prices associated
def getPriceFromLink(link, brand, model):
    smart_scraper_graph.prompt="This is a car retail website, list all the prices of the "+brand+" "+model
    smart_scraper_graph.source=link
    result = smart_scraper_graph.run()
    result["source"]=link
    return result

# Load JSON data from a file
with open('Templatefile.json', 'r') as file:
    car_data = json.load(file)

output_data=dict()

#for each model serach retail links on google and scrap the prices
for brand in car_data:
        output_data[brand]=dict()
        for model in car_data[brand]:    
            links_list = getLinks(brand, model)
            print(links_list)
    
            # ************************************************
            # Get graph execution info
            # ************************************************

            graph_exec_info = link_scraper_graph.get_execution_info()
            print(prettify_exec_info(graph_exec_info))
            output_data[brand][model]=dict()
            #link scraping works well so now I'm cheating to test only on the html in the project
            for link in links_list:
                output=getPriceFromLink(link, brand, model)
                print("output:\n")
                print(output)
                output_data[brand][model][output["source"]]=[price.replace(' ', '').replace('€', '').replace('$','') for price in output['prices']]
                graph_exec_info = smart_scraper_graph.get_execution_info()
                print(prettify_exec_info(graph_exec_info))

with open('Templatefile.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)