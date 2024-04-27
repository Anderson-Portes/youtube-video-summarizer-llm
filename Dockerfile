FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt
CMD streamlit run app.py