# Use the official miniconda3 image as the base
FROM continuumio/miniconda3:24.7.1-0

# Set the working directory
WORKDIR /app

ARG OPENROUTER_API_KEY
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
ENV MONGO_URI="add your mongo URI"
ENV RUNNING_IN_DOCKER=true

# Copy the environment file and install script to the Docker image
COPY environment_linux.yml .
COPY install_packages.sh .

# Ensure the install script has execute permissions
RUN chmod +x install_packages.sh

# Run the install script using bash
RUN /bin/bash ./install_packages.sh

COPY stress-detection-algorithm-code-python /app/repo/stress-detection-algorithm-code-python

RUN pip install setuptools pymongo && pip install -e ./repo/stress-detection-algorithm-code-python/

# Activate the environment
SHELL ["conda", "run", "-n", "gloss-sensemaking", "/bin/bash", "-c"]

# Set the command to run when starting the container
CMD ["python"]
