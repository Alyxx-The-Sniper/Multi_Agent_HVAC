FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8000"]