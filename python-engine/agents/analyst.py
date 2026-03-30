from database import embedding_model, pinecone_index
from logger import logger

def get_market_insight(niche: str):
    logger.info(f"Analyst Agent: Meneliti trend {niche}...")
    query_vec = embedding_model.encode(f"Trend viral {niche}").tolist()
    namespace = niche.lower().replace(" ", "-").replace("&", "n")
    search_res = pinecone_index.query(vector=query_vec, top_k=15, include_metadata=True, namespace=namespace)
    insight = "\n".join([res['metadata']['text'] for res in search_res.get('matches', [])])
    return insight if insight else "Tidak ada trend spesifik."
