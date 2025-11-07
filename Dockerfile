# ---- Base image ----
    FROM python:3.11-slim

    # ---- Set working directory ----
    WORKDIR /app
    
    # ---- Copy project files ----
    COPY . /app
    
    # ---- Install dependencies ----
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---- Expose the default FastAPI port ----
    EXPOSE 8000
    
    # ---- Command to run the server ----
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    