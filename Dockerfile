ARG PY_IMAGE
ARG PY_IMAGE_VERSION

# first stage
FROM ${PY_IMAGE}:${PY_IMAGE_VERSION} AS requirements-cache
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --upgrade pip ; \
    pip install --user -r requirements.txt

# second unnamed stage
FROM ${PY_IMAGE}:${PY_IMAGE_VERSION}

WORKDIR /app

# copy only the dependencies installation from the 1st stage image
COPY --from=requirements-cache /root/.local /root/.local
COPY . .

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

CMD ["python3", "main.py"]
