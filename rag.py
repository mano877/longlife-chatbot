import os, sys
from dotenv import load_dotenv
from groq import Groq
from search import search

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])
MIN_SCORE = 0.5

SYSTEM = (
    "You are the customer support assistant for Long Life Furnishers, a furniture store in Mansehra, Pakistan. "
        "Reply in the customer's language style: if they write Roman Urdu (Urdu in English letters), reply in Roman Urdu; if English, reply in English. "
    "If the message is only a greeting (hi, hello, salam), greet them back warmly and say you can help with delivery, returns, warranty, payment, custom orders, showroom location and hours. Do not include any FAQ details in a greeting reply. "
    "For questions, answer ONLY from the FAQ context and include every relevant detail from it. Do not add any information that isn't in the FAQ. "
    "For questions, answer ONLY from the FAQ context. Do not add any information that isn't in the FAQ. "
    "If the answer isn't there, say you're not sure and suggest contacting the store on WhatsApp. "
    "Keep answers short and friendly."
)

def answer(question):
    hits = [h for h in search(question, k=5) if h[2] >= MIN_SCORE]
    context = "\n\n".join(f"Q: {q}\nA: {c}" for q, c, _ in hits) or "No relevant FAQ found."
    resp = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"FAQ context:\n{context}\n\nCustomer question: {question}"},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(answer(sys.argv[1]))