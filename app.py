from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts.prompt import PromptTemplate
import os
from dotenv import load_dotenv
from google.colab import userdata


OPENAI_API_KEY = userdata.get('OPENAI')

# Neo4j bağlantı bilgileri
NEO4J_URI = "neo4j+s://dde48c7a.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "igwCZKZmYMvBZPn7RB9cPYf926VbrcdalEygK4lQiuQ"

# Hugging Face model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Neo4j graph nesnesi oluşturma
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

# Örnek veri oluşturma fonksiyonu
def create_sample_data():
    # Film ve kişileri oluşturan Cypher sorgusu
    create_query = """
    MERGE (inception:Film {title: 'Inception', description: 'Rüya paylaşım teknolojisiyle kurumsal sırları çalan bir hırsızın hikayesi.'})
    MERGE (nolan:Yonetmen {name: 'Christopher Nolan', description: 'Inception, The Dark Knight gibi filmlerin yönetmeni.'})
    MERGE (leonardo:Oyuncu {name: 'Leonardo DiCaprio', description: 'Titanic ve Inception gibi filmlerle tanınan ünlü oyuncu.'})
    MERGE (joseph:Oyuncu {name: 'Joseph Gordon-Levitt', description: 'Inception ve 500 Days of Summer filmleriyle tanınan oyuncu.'})
    MERGE (ellen:Oyuncu {name: 'Ellen Page', description: 'Inception ve Juno filmleriyle tanınan oyuncu.'})

    MERGE (nolan)-[:YONETTI]->(inception)
    MERGE (leonardo)-[:OYUNCUSU_OLDUGU]->(inception)
    MERGE (joseph)-[:OYUNCUSU_OLDUGU]->(inception)
    MERGE (ellen)-[:OYUNCUSU_OLDUGU]->(inception)

    MERGE (darkknight:Film {title: 'The Dark Knight', description: "Batman'in Joker ile mücadelesini anlatan film."})
    MERGE (christian:Oyuncu {name: 'Christian Bale', description: 'Batman rolüyle tanınan oyuncu.'})
    MERGE (heath:Oyuncu {name: 'Heath Ledger', description: 'Joker rolüyle Oscar kazanan oyuncu.'})

    MERGE (nolan)-[:YONETTI]->(darkknight)
    MERGE (christian)-[:OYUNCUSU_OLDUGU]->(darkknight)
    MERGE (heath)-[:OYUNCUSU_OLDUGU]->(darkknight)

    MERGE (aksiyon:Tur {name: 'Aksiyon'})
    MERGE (bilimkurgu:Tur {name: 'Bilim Kurgu'})
    MERGE (dram:Tur {name: 'Dram'})

    MERGE (inception)-[:TURU]->(bilimkurgu)
    MERGE (inception)-[:TURU]->(aksiyon)
    MERGE (darkknight)-[:TURU]->(aksiyon)
    MERGE (darkknight)-[:TURU]->(dram)
    """
    
    graph.query(create_query)
    print("Örnek veri başarıyla oluşturuldu!")

# Özel sorgulama şablonu
CYPHER_TEMPLATE = """
Verilen soruyu yanıtlamak için bir Cypher sorgusu oluştur.

Soru: {query}

Neo4j veritabanı şeması:
- Film düğümleri: title, description özellikleriyle
- Oyuncu düğümleri: name, description özellikleriyle
- Yonetmen düğümleri: name, description özellikleriyle
- Tur düğümleri: name özelliğiyle
- İlişkiler: OYUNCUSU_OLDUGU, YONETTI, TURU

Cypher sorgusu:
"""

# Özel yanıt şablonu
RESPONSE_TEMPLATE = """
Verilen Cypher sorgusu ve sonuçlarına dayanarak soruyu yanıtla.

Soru: {query}
Cypher Sorgusu: {cypher_query}
Sonuçlar: {results}

Yanıt:
"""

# QA zinciri oluşturma
def create_qa_chain():
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    
    cypher_prompt = PromptTemplate(
        template=CYPHER_TEMPLATE,
        input_variables=["query"]
    )
    
    qa_prompt = PromptTemplate(
        template=RESPONSE_TEMPLATE,
        input_variables=["query", "cypher_query", "results"]
    )
    
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt,
        verbose=True,
        return_direct=True,
        return_intermediate_steps=False,
        allow_dangerous_requests=True
    )
    
    return chain

def main():
    # Örnek veriyi oluştur
    create_sample_data()
    
    # QA zincirini oluştur
    qa_chain = create_qa_chain()
    
    print("\nFilm Bilgi Grafiği RAG Sistemi")
    print("Çıkmak için 'q' yazın")
    
    while True:
        question = input("\nSorunuzu girin: ")
        if question.lower() == 'q':
            break
            
        try:
            # Soruyu yanıtla
            response = qa_chain({"query": question})
            print("\nYanıt:", response)
        except Exception as e:
            print(f"\nHata oluştu: {str(e)}")

if __name__ == "__main__":
    main()