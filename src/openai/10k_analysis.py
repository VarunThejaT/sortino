import os
os.getenv("OPENAI_API_KEY")

from llama_index import download_loader, GPTSimpleVectorStore
from pathlib import Path

UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)

loader = UnstructuredReader()
doc_set = {}
all_docs = []
years = [2022] # , 2021, 2020, 2019]
for year in years:
    year_docs = loader.load_data(file=Path(f'./data/UBER/UBER_{year}.html'), split_documents=False)
    # insert year metadata into each year
    for d in year_docs:
        d.extra_info = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)

from llama_index import ServiceContext

service_context = ServiceContext.from_defaults(chunk_size_limit=512)


# reload from disk
from llama_index import StorageContext, load_index_from_storage

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context)