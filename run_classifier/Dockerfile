
FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-5
WORKDIR /source
RUN git clone -b v2.5.0  --single-branch https://github.com/tensorflow/models.git 
RUN pip install -r models/official/requirements.txt 
ENV PYTHONPATH=/source/models

#ENTRYPOINT ["/bin/bash", "-c"]
#CMD ["echo TensorFlow Model Garden image"]
ENTRYPOINT ["python"]
CMD ["-c", "print('Hello')"]
