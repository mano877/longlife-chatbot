import os, sys
import psycopg
from dotenv import load_dotenv
from fastembed import TextEmbedding
from pgvector.psycopg import register_vector

load_dotenv()
model = TextEmbedding("BAAI/bge-small-en-v1.5")

def search(query, k=3):
    qvec = next(model.query_embed(query))
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        register_vector(conn)
        return conn.execute(
            "SELECT question, content, score FROM ("
            "  SELECT DISTINCT ON (content) question, content, 1 - (embedding <=> %s) AS score"
            "  FROM faq_chunks ORDER BY content, embedding <=> %s"
            ") t ORDER BY score DESC LIMIT %s",
            (qvec, qvec, k),
        ).fetchall()
       
if __name__ == "__main__":
    for question, _, score in search(sys.argv[1]):
        print(f"{score:.2f} | {question}")