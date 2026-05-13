import html2text
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import json

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

texts = []
metadatas = []
with open("timeline.json", "r") as timeline_file:
    timeline = json.loads(timeline_file.read())
    texts = [timeline_entry["title"] for timeline_entry in timeline]

vectordb = FAISS.from_texts(texts, embedding_model)

vectordb.save_local("timeline_dict")