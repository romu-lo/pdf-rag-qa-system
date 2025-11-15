import re

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader


def _can_load(file_path: str) -> bool:
    return re.search(r'\.pdf$', file_path, re.IGNORECASE) is not None

def load(file_path: str):
    if _can_load(file_path):
        loader = PyMuPDFLoader(file_path, mode="page")
        documents = loader.load()
        return documents
    else:
        raise ValueError("Unsupported file format. Only PDF files are supported.")


# file_path = "../resources/case_files/LB5001.pdf"
# file_path = "../resources/case_files/MN414_0224.pdf"
file_path = "../resources/case_files/WEG-CESTARI-manual-iom-guia-consulta-rapida-50111652-pt-en-es-web.pdf"
# file_path = "../resources/case_files/WEG-motores-eletricos-guia-de-especificacao-50032749-brochure-portuguese-web.pdf"
try:
    docs = load(file_path)
    for doc in docs:
        print(doc)
except ValueError as e:
    print(e)
