from database import embedding_model, pinecone_index
from logger import logger


def get_market_insight(niche: str):
    """
    Menganalisis tren pasar berdasarkan niche yang diberikan.
    """
    logger.info("Analyst Agent: Meneliti trend %s...", niche)
    query_vec = embedding_model.encode(f"Trend viral {niche}").tolist()
    namespace = niche.lower().replace(" ", "-").replace("&", "n")
    search_res = pinecone_index.query(
        vector=query_vec, top_k=15, include_metadata=True, namespace=namespace
    )
    insight = "\n".join(
        [match.metadata["text"] for match in search_res.matches if match.metadata]
    )
    return insight if insight else "Tidak ada trend spesifik."
