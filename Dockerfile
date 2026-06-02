FROM python:3.10-slim

WORKDIR /app

# --------------------------------
# SYSTEM DEPENDENCIES
# --------------------------------

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------
# COPY REQUIREMENTS
# --------------------------------

COPY requirements.txt .

# --------------------------------
# INSTALL PYTHON DEPENDENCIES
# --------------------------------

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------
# COPY PROJECT
# --------------------------------

COPY . .

# --------------------------------
# EXPOSE STREAMLIT PORT
# --------------------------------

EXPOSE 8501

# --------------------------------
# RUN STREAMLIT
# --------------------------------

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]