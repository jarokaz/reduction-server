
FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-5
WORKDIR /

# Install Reduction Server NCCL plugin
RUN apt remove -y google-fast-socket \
&&  echo "deb https://packages.cloud.google.com/apt google-fast-socket main" | tee /etc/apt/sources.list.d/google-fast-socket.list \
&&  curl -s -L https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
&&  apt update && apt install -y google-reduction-server

# Install Official Models and Text libraries
RUN pip install tf-models-official==2.5.0 tensorflow-text==2.5.0


# Copies the trainer code to the docker image.
COPY trainer /trainer

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python"]
CMD ["-c", "print('TF Model Garden')"]
