


import sys
# system

sys.path.append("../")




from .core.file_loader import FILE_LOADERS,FileLoader
from .config import SUPPORT_FILE_TYPES,EMBEDDINGS_SIZES

base_loader=FileLoader(FILE_LOADERS,SUPPORT_FILE_TYPES)

from .core.text_spliter import ChineseTextSplitter,CharacterTextSplitter,LineTextSplitter

base_splitter=LineTextSplitter()



import yaml
# api
from .core.api import AiproxyAPI,OpenaiAPI,LocalModelAPI,TestModelAPI,MultiModelAPI
from idkb_work.settings import BASE_DIR
with open(str((BASE_DIR/'work/config.yaml').absolute()),mode='rt') as f:
    ycfg = yaml.safe_load(f)


APIS={
    'openai':OpenaiAPI(api_key=ycfg['ApiUrl.test.apikey'],base_url=ycfg['ApiUrl.test.url']),
    'test':TestModelAPI(api_key=ycfg['ApiUrl.test.apikey'],base_url=ycfg['ApiUrl.test.url']),
    'aiproxy':AiproxyAPI(api_key=ycfg['ApiUrl.aiproxy.apikey'],base_url=ycfg['ApiUrl.aiproxy.url']),
    'local':LocalModelAPI(api_key=ycfg['ApiUrl.local.apikey'],base_url=ycfg['ApiUrl.local.url']),
}
base_api=MultiModelAPI(APIS)



# db
from .core.vdb import MilvusDB,MilvusCollection,get_FileAbstract_fields
base_db=MilvusDB(host=ycfg['Milvus.host'],port=ycfg['Milvus.port'])
for embeddings_size in EMBEDDINGS_SIZES:
    if not base_db.has_collection(f'FileAbstract_{embeddings_size}'):
        base_db.create_collection(f"FileAbstract_{embeddings_size}",get_FileAbstract_fields(embeddings_size),f"FileAbstract_{embeddings_size}")
        kb_collection=base_db.get_collection(f"FileAbstract_{embeddings_size}")
        MilvusCollection(kb_collection,f"FileAbstract",f"{embeddings_size}").update_index('embeddings')


