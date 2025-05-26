# RAG Application

This repository contains the microservices for a Retrieval-Augmented Generation (RAG) based AI assistant system.

## Overview
This architecture separates responsibilities into independent, containerized microservices:
1. Document Ingestion Service – Parses and prepares documents for embedding.
2. Embedding & Indexing Service – Converts documents into vector embeddings and stores them in a FAISS index.
3. Query Service – Receives user queries, retrieves relevant context from FAISS, and forwards it to the LLM.
4. LLM Service – (Pluggable) Interfaces with an external LLM provider such as OpenAI or Gemini.


## Setup

Instructions will be provided to build, run, and test each service using Docker and FastAPI.
1. Clone the repository
git clone https://github.com/your-org/rag-agent.git
cd rag-agent


2. Add environment variables
Create .env file in llm_service/:
OPENAI_API_KEY=your_api_key_here

3. Build and run all services with Docker Compose
docker compose up --build


## Tech Stack Overview
Tech Stack               |        Service	Technologies
Document Ingestion	     |      Python, FastAPI, PDF/Text parsing libraries
Embedding & Indexing 	   |      Python, Sentence Transformers, FAISS
Query Service	           |      Python, FastAPI, REST API
LLM Service	             |      Python, FastAPI, OpenAI/Gemini API integration
Containerization	       |      Docker, Docker Compose


Thanks for Reading !!
