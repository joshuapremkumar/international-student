FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["bash", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & python -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]