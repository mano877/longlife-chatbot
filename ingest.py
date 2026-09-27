
import json, os
import psycopg
from dotenv import load_dotenv
from fastembed import TextEmbedding
from pgvector.psycopg import register_vector

load_dotenv()
model = TextEmbedding("BAAI/bge-small-en-v1.5")

with open("data/faqs.json", encoding="utf-8") as file:
    faqs = json.load(file)

rows = []
for faq in faqs:
    variants = [faq["question"]] + [q.strip() + "?" for q in faq.get("question_ur", "").split("?") if q.strip()]
    rows += [(faq["category"], v, faq["content"]) for v in variants]

vectors = list(model.passage_embed([q for _, q, _ in rows]))

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    register_vector(conn)
    conn.execute("TRUNCATE faq_chunks RESTART IDENTITY")
    with conn.cursor() as cur:
                cur.executemany(
            "INSERT INTO faq_chunks (category, question, content, embedding) VALUES (%s, %s, %s, %s)",
            [(cat, q, c, v) for (cat, q, c), v in zip(rows, vectors)],
        )
                vectors = list(model.passage_embed([f"{q}\n{c}" for _, q, c in rows]))
print(f"Inserted {len(faqs)} FAQs")
