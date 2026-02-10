FROM nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /TKG-Forecasting-Evaluation
WORKDIR /TKG-Forecasting-Evaluation

RUN apt update -y

RUN apt install -y git

CMD ["bash"]
