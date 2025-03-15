from dataiku.llm.agent_tools import BaseAgentTool
import logging
from exaai_client import ExaAIClient
from exaai_commons import (
    get_api_key_from_config
)

class ExaAISearchTool(BaseAgentTool):
    def set_config(self, config, plugin_config):
        print("ALX:set_config:config={}, plugin_config={}".format(config, plugin_config))
        self.config = config

    def get_descriptor(self, tool):
        print("ALX:get_descriptor")
        return {
            "description": "Searches the web. Returns an array of results. For each result, returns url title, and snippet",            
            "inputSchema" : {
                "$id": "https://dataiku.com/agents/tools/search/input",
                "title": "Input for the search tool",
                "type": "object",
                "properties" : {
                    "q" : {
                        "type": "string",
                        "description": "The query string"
                    }
                },
                "required": ["q"]            
            }
        }

    def invoke(self, input, trace):
        print("ALX:invoke")
        print("ALX:input={}, trace={}".format(input, trace))
        self.client = ExaAIClient(access_token=get_api_key_from_config(self.config))
        args = input["input"]
        q = args["q"]
        # api_key = self.config["google_search_api_connection"]["apiKey"]

        # This logger outputs the key in DEBUG mode ...
        logging.getLogger("googleapiclient.discovery").setLevel("INFO")

        # service = build("customsearch", "v1", developerKey=api_key)
        # res = service.cse().list(q=q, cx=self.config["cx"]).execute()
        query = {
            "query":q,"num_results":5,"text": True
        }

        response = self.client.post(
            "search",
            json=query
        )
        items = response.get("results", [])
        
        source_items = []
        results = []
        for item in items:
            print("ALX:item={}".format(item))
            source_item = {
                "type": "SIMPLE_DOCUMENT",
                "url": item["url"],
                "title": item["title"],
                "htmlSnippet": item.get("text", "")
            }
            if "pagemap" in item and "cse_thumbnail" in item["pagemap"] and "src" in item["pagemap"]["cse_thumbnail"]:
                source_item["thumbnailImageURL"] = item["pagemap"]["cse_thumbnail"]["src"]
                source_item["thumbnailImageW"] = item["pagemap"]["cse_thumbnail"].get("width")
                source_item["thumbnailImageH"] = item["pagemap"]["cse_thumbnail"].get("height")
            
            results.append({
                "url": item["url"],
                "title": item["title"],
                "snippet": item.get("text", "")
            })
            source_items.append(source_item)
            
        return { 
            "output" : results,
            "sources":  [{
                "toolCallDescription": "Performed Web Search for: %s" %q,
                "items" : source_items
            }]
        }