FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc

# Install pytorch and fastai
RUN pip install https://download.pytorch.org/whl/cu100/torch-1.0.1.post2-cp36-cp36m-linux_x86_64.whl
RUN pip install torchvision
RUN pip install git+https://github.com/fastai/fastai.git

# Install starlette and uvicorn
RUN pip install starlette uvicorn python-multipart aiohttp

ADD watch-classification.py watch-classification.py
ADD 1024-resnet34-90-watch-classification.pkl 1024-resnet34-90-watch-classification.pkl

# Run it once to trigger resnet download
RUN python watch-classification.py

EXPOSE 8008

# Start the server
CMD ["python", "watch-classification.py", "serve"]