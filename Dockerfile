FROM python:3.13-slim

WORKDIR /code

COPY requirements.txt .

# Install CPU-only torch FIRST from PyTorch's CPU wheel index. On aarch64 Linux
# the default torch wheel pulls ~2GB of unusable NVIDIA CUDA libraries (there is
# no GPU in this container). Installing torch==2.11.0+cpu up front satisfies the
# torch pin below, so the CUDA build is never resolved. Keeps the image lean.
RUN pip install --no-cache-dir torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data/policies ./data/policies

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]