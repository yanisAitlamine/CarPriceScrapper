from scrapegraphai.graphs import SearchLinkGraph
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
import json

# ************************************************
# Define the configuration for the graph
# ************************************************

link_graph_config = {
    "llm": {
        "model": "ollama/llama3",
        "temperature": 0,
        "format": "json",  # Ollama needs the format to be specified explicitly
        # "base_url": "http://localhost:11434", # set ollama URL arbitrarily
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        # "base_url": "http://localhost:11434",  # set ollama URL arbitrarily
    },
    "verbose": True,
    "headless": False
}

graph_config = {
    "llm": {
        "model": "ollama/llama3",  # Specify the model for the llm
        "temperature": 0,  # Set temperature parameter for llm
        "format": "json",  # Specify the output format as JSON for Ollama
        "base_url": "http://localhost:11434",  # Set the base URL for Ollama
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",  # Specify the model for embeddings
        "base_url": "http://localhost:11434",  # Set the base URL for Ollama
    },
    "verbose": True,  # Enable verbose mode for debugging purposes
}

model ="civic"
brand="honda"

# ************************************************
# Define usefull functions
# ************************************************

def createCarsDict(car_data):
    car_dict={}
    for brand_info in car_data["brands"]:
        brand_name = brand_info["brand"]
        model_names = [model["name"] for model in brand_info["models"]]
        car_dict[brand_name] = model_names
    return car_dict

def getLinks(brand, model, link_scraper_graph):
    
    link_scraper_graph.source="https://www.google.com/search?q="+brand+"+"+model+"+occasion"

    result = link_scraper_graph.run()

    output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation

    line_list = set(output.split("\n"))  # Split the JSON string into lines

    return [line for line in line_list if (model in line and "google" not in line)]

def getPriceFromLink(link):
    smart_scraper_graph.source=link
    result = smart_scraper_graph.run()
    result["source"]=link
    return result

# Load JSON data from a file
with open('TemplateInput.json', 'r') as file:
    car_data = json.load(file)

# Create the dictionary
car_dict = createCarsDict(car_data)
print(car_dict)

# Initialize LinkScraperGraph with source, and configuration
link_scraper_graph = SearchLinkGraph(
        source="https://www.google.com/search?q="+brand+"+"+model+"+occasion",
        config=link_graph_config
    )

# Initialize SmartScraperGraph with prompt, source, and configuration
smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the prices of the "+brand+" "+model+" along with the version, just give me the number no blank space or '€' characters, if the price is a price range like '11000-14000' only give me the average in that case it would me 12500 don't give me the price range",
    source="",
    config=graph_config
)

links_list = getLinks(brand, model, link_scraper_graph)
    
# ************************************************
# Get graph execution info
# ************************************************

graph_exec_info = link_scraper_graph.get_execution_info()
print(prettify_exec_info(graph_exec_info))

for link in links_list:
    result=getPriceFromLink(link)
    print (result)
    
    # Prettify the result and display the JSON


    output = json.dumps(result, indent = 2)  # Convert result to JSON format with indentation

    price_list = output.split("\n")  # Split the JSON string into lines

    # Print each line of the JSON separately
    for elements in price_list:
        print(elements)
