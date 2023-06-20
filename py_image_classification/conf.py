import configparser
import logging
import os

logger = logging.getLogger()

INFERENCE_CONFIGS = {
    "SAAD_CNEWS": ["saad_cnews",{"generique": "saad_gen_cnews"}],
    "SAAD_LCI": ["saad_lci", {"generique": "saad_gen_lci"}],
    "SAAP": ["saap"],
    "SAAJ": ["saaj"],
}

MODELS_PATHS = {
    "saad_cnews": "/data_ia/saad_cnews_prod",
    "saad_gen_cnews": "/data_ia/saad_gen_cnews_prod",
    "saad_lci": "/path_to_data",
    "saad_gen_lci": "/path_to_data",
    "saap": "/data_ia/saap_dev",
    "saaj": "/path_to_data",
}

DATASET_PATHS = {
    "saap": "dataset_example/SAAP",
    "saad_cnews": "dataset_example/SAAD_CNEWS",
    "saad_gen_cnews": "dataset_example/SAAD_GEN_CNEWS"
}

MODEL_PARAMETERS = {}

DEFAULT_BATCH_SIZE = 64

def load_config(conf):
    cp = configparser.ConfigParser()
    cp.read('conf.ini')
    try:
        conf["BATCH_SIZE"] = int(cp["MODEL_PARAMETERS"]["BATCH_SIZE"])
    except:
        conf["BATCH_SIZE"] = DEFAULT_BATCH_SIZE
        logger.debug(f"Batch_size is not present in {os.getcwd()}/conf.ini section MODEL_PARAMETERS. Using default value {DEFAULT_BATCH_SIZE} instead.")


load_config(MODEL_PARAMETERS)