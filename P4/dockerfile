FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Gunakan mirror PyPI agar download sangat cepat
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

COPY . .

CMD ["python", "main.py"]