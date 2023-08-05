FROM level12/python-test-multi

COPY . /app
WORKDIR /app/pip-reqs
RUN pip install tox
RUN mkdir .artifacts

ENTRYPOINT tox