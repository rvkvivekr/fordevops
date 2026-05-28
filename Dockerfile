FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY app.py .
COPY streamit_app.py .
COPY xgb_carshare_model.pkl .
COPY start.sh .

RUN chmod +x start.sh

EXPOSE 8000 8501

CMD ["./start.sh"]