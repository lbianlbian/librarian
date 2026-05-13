# Librarian

A way for worldbuilders to chat with their worlds. Uses langchain and arcade graph db and World Anvil. 

## Steps
1. download articles and timeline from World Anvil
2. put articles into a FAISS vector database
3. put timeline entries into another FAISS vector database to act as dictionary to timeline entry titles
4. make a graph database of the timeline in sequential order to avoid mixing of events in responses
5. given a query, retrieve the relevant articles, retrieve the relevant timeline entries and their graph database nodes for temporal context, send to LLM and get response. 
