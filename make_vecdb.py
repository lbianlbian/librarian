import html2text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

ARTICLES_DIR = "articles"
# Custom separators for Paragraphs and Markdown Lists
custom_separators = [
    "\n\n",      # 1. First, try to split by double newlines (Paragraphs)
    "\n* ",      # 2. Next, try to split at the start of a bullet point
    "\n- ",      # 3. Same for dashes
    "\n",        # 4. Then single newlines
    ". ",        # 5. Then sentences
    " ",         # 6. Finally, words
    ""           # 7. Last resort: characters
]
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Ideal for all-MiniLM-L6-v2
    chunk_overlap=50,      # Small overlap to keep context across chunks
    separators=custom_separators,
    is_separator_regex=False
)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

texts = []
metadatas = []
for article in os.listdir(ARTICLES_DIR):
    full_article_path = os.path.join(ARTICLES_DIR, article)
    # name-of-article.txt --> name of article
    article_title = " ".join(article.replace(".txt", "").split("-"))
    with open(full_article_path, "r") as article_file:
        html = article_file.read()
        h = html2text.HTML2Text()
        h.ignore_links = False  # Keep links if they're useful for context
        markdown_text = h.handle(html)
        # prepend article name so that different historical events don't get mixed together
        full_text = f"From {article_title}:\n{markdown_text}"
        texts.append(full_text)
        metadatas.append({"article_name": article_title})

docs = text_splitter.create_documents(texts, metadatas=metadatas)

vectordb = FAISS.from_documents(docs, embedding_model)

vectordb.save_local("world_anvil_local")
