import pymongo
import requests

client=pymongo.MongoClient("mongodb+srv://<usr>:<pswd>@cluster0.oewot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client.sample_mflix
collection=db.movies

hf_token="your api"
embedding_url="https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:
    response=requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs":text}
    )
    return response.json()



##run it once to modify the data base (add a column plot_embedding_hf)
# for doc in collection.find({"plot":{"$exists":True}}).limit(50):
#     doc['plot_embedding_hf']=generate_embedding(doc['plot'])
#     collection.replace_one({"_id": doc["_id"]},doc)

query="brain is not braining"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "plotSemanticSearch", 
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')