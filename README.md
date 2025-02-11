# RAGMovieKnowledgeGraph

Film veritabanı üzerinde doğal dil sorguları yapabilen, Neo4j graf veritabanı ve LangChain tabanlı bir soru-cevap sistemi.

## Proje Açıklaması

RAGMovieKnowledgeGraph, filmler, yönetmenler, oyuncular ve film türleri arasındaki ilişkileri graf veritabanında modelleyerek, kullanıcıların doğal dil ile sorgular yapmasına olanak sağlayan bir sistem sunar. Proje, şu temel bileşenleri içerir:

- **Neo4j Graf Veritabanı**: Film endüstrisi verilerini ve ilişkilerini saklar
- **LangChain**: Doğal dil işleme ve soru-cevap zincirleri için kullanılır
- **OpenAI**: Doğal dil sorgularını Cypher sorgularına çevirmek için kullanılır
- **HuggingFace Embeddings**: Metin temsilleri için kullanılır

### Veri Modeli

Sistem aşağıdaki veri tiplerini ve ilişkilerini içerir:

- **Film**: title, description
- **Yönetmen**: name, description
- **Oyuncu**: name, description
- **Tür**: name

İlişkiler:
- YONETTI (Yönetmen -> Film)
- OYUNCUSU_OLDUGU (Oyuncu -> Film)
- TURU (Film -> Tür)

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install langchain neo4j python-dotenv openai
```

2. Neo4j veritabanı bağlantı bilgilerinizi ayarlayın:
```python
NEO4J_URI = "your-neo4j-uri"
NEO4J_USERNAME = "your-username"
NEO4J_PASSWORD = "your-password"
```

3. OpenAI API anahtarınızı ayarlayın:
```python
OPENAI_API_KEY = "your-openai-api-key"
```

## Kullanım

1. Sistemi başlatın:
```python
python main.py
```

2. Doğal dil ile sorgular yapın. Örnek sorgular:
- "Christopher Nolan'ın yönettiği filmler nelerdir?"
- "Inception filminde oynayan aktörler kimlerdir?"
- "Aksiyon türündeki filmleri listele"
- "Heath Ledger'in oynadığı filmler hangileri?"

## Özellikler

- **Doğal Dil İşleme**: Kullanıcı sorguları otomatik olarak Cypher sorgularına çevrilir
- **Graf Tabanlı Sorgulama**: İlişkisel veriler üzerinde karmaşık sorgular yapabilme
- **Genişletilebilir Veri Modeli**: Yeni veri tipleri ve ilişkiler eklenebilir
- **Hata Yönetimi**: Sorgu hataları için güvenli hata yakalama
- **İnteraktif Arayüz**: Kullanıcı dostu komut satırı arayüzü

## Teknik Detaylar

### LangChain Bileşenleri

1. **GraphCypherQAChain**: 
   - Doğal dil sorgularını Cypher sorgularına çevirir
   - Sorgu sonuçlarını anlamlı yanıtlara dönüştürür

2. **PromptTemplate**:
   - Cypher sorguları için şablon
   - Yanıt formatı için şablon

3. **Neo4jGraph**:
   - Graf veritabanı bağlantısı
   - Sorgu yürütme

### Veri Oluşturma

`create_sample_data()` fonksiyonu örnek veri seti oluşturur:
- Inception ve The Dark Knight filmleri
- Christopher Nolan ve diğer yönetmenler
- Çeşitli oyuncular
- Film türleri ve ilişkileri

### Soru-Cevap Zinciri

`create_qa_chain()` fonksiyonu şunları yapar:
- ChatOpenAI modeli başlatır
- Sorgu ve yanıt şablonlarını ayarlar
- GraphCypherQAChain'i yapılandırır
