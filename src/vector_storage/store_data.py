import logging
import sys
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore
import nest_asyncio

nest_asyncio.apply()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("src/data/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Either way we can now query the index
query_engine = index.as_query_engine()
response = query_engine.query(
    "You are a brilliant career adviser. Answer a question of job seekers with given information.\n"
    "Also you need to show the source nodes that you are using to answer the question at the end of your response.\n"
    "If you are asked to return jobs that are suitable for the job seeker, return Job ID, Title and Link.\n"
    "Question: I am a data scientist with 3 years of experience in the UK. Give me 3 jobs that are suitable for me"
)
print(response)

index.storage_context.persist()
