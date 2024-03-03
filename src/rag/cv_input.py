from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_parse import LlamaParse

PERSIST_DIR = "./storage"
pdf_path = "input_cv/data-science-cv-example.pdf"
question = "Retrieve 3 jobs that are suitable for me"

parser = LlamaParse(
    result_type="markdown"
)


def user_query(pdf_path: str):
    input_cv = parser.load_data(pdf_path)

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(
        "You are a brilliant career adviser. Answer a question of job seekers with given information.\n"
        "If their CV information is given, use that information as well to answer the question.\n"
        "If you are asked to return jobs that are suitable for the job seeker, return Job ID, Title and Link.\n"
        "If you are not sure about the answer, return NA. \n"
        "You need to show the source nodes that you are using to answer the question at the end of your response.\n"
        f"CV: {input_cv[0]} \n"
        f"Question: {question}"
    )
    print(response)


if __name__ == "__main__":
    user_query(pdf_path)
