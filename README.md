# crawler_email_py

This is a simple email crawler written in Python.

## Requirements

- Python 3.6+
- Docker

## Docker

- RabbitMQ
- Minio

## Usage

Create data and logs folder in the root directory.

```bash 
mkdir data
mkdir logs
mkdir attachments
```

Added your variables in the .env file.

````bash
cp .env.example .env
````

Required variables:

- `IMAP_GMAIL_HOST`
- `IMAP_GMAIL_EMAIL`
- `IMAP_GMAIL_PASSWORD`
- `LOCAL_FILE_PATH`

Start RabbitMQ and Minio

```bash
docker-compose up -d
```

Access RabbitMQ at http://localhost:15672/ with username and password `guest`.

Access Minio at http://localhost:9002/ with username and password `minioadmin`.

Install dependencies

```bash
pip install -r requirements.txt
```

Run the script

```bash
python3 main.py
```