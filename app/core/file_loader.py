import os
from typing import List

from docx import Document


def load_documents_from_folder(folder_path: str) -> List[Document]:
    docs = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".docx"):
            path = os.path.join(folder_path, filename)
            docs.append(Document(path))
    return docs
