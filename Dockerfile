FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu20.04
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /TKG-Forecasting-Evaluation
WORKDIR /TKG-Forecasting-Evaluation

RUN apt update -y

RUN apt install -y git

CMD ["bash"]
