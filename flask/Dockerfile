FROM --platform=linux/amd64 python:3.8

RUN curl -LO "https://dl.k8s.io/release/v1.26.3/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    && kubectl version --client

RUN mkdir /app
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]