FROM python:3.8-slim

COPY dist/*.whl /

# hadolint ignore=DL3013
RUN pip --no-cache-dir install /*.whl

CMD ["tuxbuild", "--help"]
