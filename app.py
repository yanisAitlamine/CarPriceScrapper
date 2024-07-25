""" 
Basic example of scraping pipeline using SmartScraper
"""
from scrapegraphai.graphs import SearchLinkGraph
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
import json
# ************************************************
# Define the configuration for the graph
# ************************************************

model ="civic"
brand="honda"

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

# Initialize SmartScraperGraph with prompt, source, and configuration
smart_scraper_graph = SmartScraperGraph(
    #prompt="List all the content",  # Set prompt for scraping
    prompt="List me all the prices of the "+brand+" "+model+" along with the version, just give me the number no blank space or '€' characters, if the price is a price range like '11000-14000' only give me the average in that case it would me 12500 don't give me the price range",
    # Source URL or HTML content to scrape
    source="",
    config=graph_config  # Pass the graph configuration
)


# ************************************************
# Create the SearchLinkGraph instance and run it
# ************************************************


link_scraper_graph = SearchLinkGraph(
    source="https://www.google.com/search?q="+brand+"+"+model+"+occasion",
    config=link_graph_config
)

result = link_scraper_graph.run()
print(result)

output = json.dumps(result, indent=2)  # Convert result to JSON format with indentation

line_list = set(output.split("\n"))  # Split the JSON string into lines

filtered_lines = [line for line in line_list if (model in line and "google" not in line)]
# Print each line of the JSON separately
for line in filtered_lines:
    print(line)
    
# ************************************************
# Get graph execution info
# ************************************************

graph_exec_info = link_scraper_graph.get_execution_info()
print(prettify_exec_info(graph_exec_info))

for line in filtered_lines:
    smart_scraper_graph.source=line
    result = smart_scraper_graph.run()
    result["source"]=line
    print (result)
    
    # Prettify the result and display the JSON


    output = json.dumps(result, indent = 2)  # Convert result to JSON format with indentation

    price_list = output.split("\n")  # Split the JSON string into lines

    # Print each line of the JSON separately
    for elements in price_list:
        print(elements)
