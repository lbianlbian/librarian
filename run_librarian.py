from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_mistralai import ChatMistralAI

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DB_NAME = "timeline"
URL = f"http://localhost:2480/api/v1/query/{DB_NAME}"
AUTH = ('root', 'a81f46C3')

# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
model = ChatMistralAI(
    model="mistral-small-latest", # Or "codestral-latest" for code
    api_key="ut3fvNH5z4BBiAq88V07cMAGNLXos48P"
)

vectordb = FAISS.load_local("world_anvil_local", embedding_model, allow_dangerous_deserialization=True)
# vectordb = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
retriever = vectordb.as_retriever()
'''
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.001}  # this is distance = 1 - similarity, 0.6 means anything with 0.4 similarity or above
)
'''
timeline_vecdb = FAISS.load_local("timeline_dict", embedding_model, allow_dangerous_deserialization=True)
timeline_retriever = timeline_vecdb.as_retriever()
def take_metadata_query_timeline(input_dict):
    """Takes first retrieval docs, extracts ID/Title from metadata, queries Timeline DB."""
    # Logic: Get unique IDs or keys from the metadata of the first set of docs
    context = input_dict["context"]
    meta_keys = [doc.metadata.get("article_name") for doc in context]
    # Example: Query your timeline_dict vector store using these keys
    timeline_results = timeline_vecdb.similarity_search(str(meta_keys))
    timeline_entries = [timeline_result.page_content for timeline_result in timeline_results]
    cypher_query = f"""MATCH (target:Event) WHERE target.title IN {timeline_entries}
OPTIONAL MATCH (prev:Event)-[:NEXT]->(target)
OPTIONAL MATCH (target)-[:NEXT]->(next:Event)
RETURN 
    prev.title AS previous_event, 
    target.title AS current_event, 
    next.title AS next_event"""
    response = requests.post(
        URL, 
        auth=AUTH, 
        json={"language": "openCypher", "command": cypher_query}
    )
    timeline_context = []
    for seq in response.json()["result"]:
        prev_event = seq.get("previous_event", "START OF TIMELINE")
        next_event = seq.get("next_event", "END OF TIMELINE")
        timeline_context.append(f"{seq['current_event']} follows {prev_event} and precedes {next_event}")
    return ",".join(timeline_context)

template = '''You are a librarian in charge of keeping track of the history of this world. 
Respond to the query based on the following context: {context}, timeline context: {timeline_entries}, query: {query}'''

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | RunnablePassthrough.assign(timeline_entries=take_metadata_query_timeline)
    | prompt 
    | model
    | StrOutputParser()
    
)
result = chain.invoke(input("Enter query here: "))
print(result)