import json
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_dir = Path("src/data/raw")
output_dir = Path("src/data/chunks")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "chunks.jsonl"

dir_loader = DirectoryLoader(
    raw_dir,
    glob="**/*.pdf",
    loader_cls=PyMuPDFLoader
)

documents = dir_loader.load()
print(f"PDF documents loaded: {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

with open(output_file, "w", encoding="utf-8") as f:
    for i, doc in enumerate(chunks):
        record = {
            "id": i,
            "text": doc.page_content,
            "metadata": {
                "source": doc.metadata.get("source"),
                "file_path": doc.metadata.get("file_path"),
                "page": doc.metadata.get("page"),
                "chunk_index": i
            }
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
