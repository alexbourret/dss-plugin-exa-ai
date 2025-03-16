from dataiku.connector import Connector
from exaai_client import ExaAIClient
from exaai_commons import (
    get_api_key_from_config, config_to_params, process_domains_parameters
)
from safe_logger import SafeLogger
from plugin_details import get_initialization_string


logger = SafeLogger("exa-ai connector", forbiden_keys=["exa_api_key"])


class ExaAISearchConnector(Connector):

    def __init__(self, config, plugin_config):
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class
        logger.info(get_initialization_string())
        logger.info("config={}".format(logger.filter_secrets(config)))
        self.client = ExaAIClient(access_token=get_api_key_from_config(config))
        config = process_domains_parameters(config)
        self.json_query = config_to_params(config)

    def get_read_schema(self):
        return None
        # return {
        #     "columns" :[
        #         {"name":"score", "type": "string"},
        #         {"name":"title", "type": "string"},
        #         {"name":"id", "type": "string"},
        #         {"name":"url", "type": "string"},
        #         {"name":"publishedDate", "type": "date"},
        #         {"name":"author", "type": "string"}
        #     ]
        # }

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        if not self.json_query.get("query"):
            logger.warning("No actual query, skipping the API call")
            return
        query = self.json_query
        # if records_limit > 0:
        #     query["num_results"] = records_limit
        response = self.client.post(
            "search",
            json=query
        )
        results = response.get("results", [])
        for result in results:
            yield result

    def get_writer(self, dataset_schema=None, dataset_partitioning=None,
                   partition_id=None, write_mode="OVERWRITE"):
        raise NotImplementedError

    def get_partitioning(self):
        raise NotImplementedError

    def list_partitions(self, partitioning):
        return []

    def partition_exists(self, partitioning, partition_id):
        raise NotImplementedError

    def get_records_count(self, partitioning=None, partition_id=None):
        raise NotImplementedError
