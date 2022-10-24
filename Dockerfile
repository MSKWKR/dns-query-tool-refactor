FROM python:3.10-alpine3.16
LABEL maintainer=freedom.systems

# Create working directory
RUN mkdir -p /Project_DNS/DNS_engine


# Install all required packages
COPY ./requirements.txt /Project_DNS/DNS_engine/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /Project_DNS/DNS_engine/requirements.txt

# Copy all files from current working directory to the created WORKDIR
COPY ./ /Project_DNS/DNS_engine

WORKDIR /Project_DNS/DNS_engine

EXPOSE 8000

CMD ["uvicorn", "api_engine:app"]



