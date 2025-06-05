# Agent Swarm: Multi-Agent LLM System
A scalable, Dockerized multi-agent system built with Python and LangChain, designed to intelligently route and process user queries through specialized agents.

## 🔍 Overview
This system demonstrates a three-agent architecture:

Router Agent: Classifies incoming messages and directs them to the appropriate downstream agent.

Knowledge Agent: Answers questions using a RAG (Retrieval-Augmented Generation) pipeline with web-sourced data.

Customer Support Agent: Handles user-specific inquiries with customizable tools.

## Features:
✅ LLM-powered routing (LangChain)
✅ RAG pipeline for grounded responses
✅ Personality layer for human-like interactions
✅ FastAPI endpoint for seamless integration
✅ Dockerized for easy deployment

## 🛠️ Tech Stack
Language: Python

Frameworks: LangChain, FastAPI

Data: Vector DB (e.g., FAISS), Web Scraping (BeautifulSoup/Scrapy)

Infrastructure: Docker

## 🚀 Quick Start
bash
git clone https://github.com/Fugant1/AgentSwarm.git

cd agent_swarm  
docker build -t agent_swarm .  
docker run -p 8000:8000 agent_swarm  
API Endpoint: POST /chat (payload: {"message": "Your query", "user_id": "123"})

## 📂 Project Structure
agent_swarm/  
├── agents/               # Router, Knowledge, Customer agents  
├── api/                  # FastAPI endpoint  
├── data/                 # RAG data storage  
├── tests/                # Unit + E2E tests  
└── utils/                # RAG, personality layer 

## 📌 Why This Project?
Modular Design: Easily extendable with new agents/tools.

Production-Ready: Dockerized with comprehensive tests.

LLM Best Practices: Implements RAG and structured workflows.
