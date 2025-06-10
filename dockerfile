FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "agent_swarm.main:fastapi", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on"]