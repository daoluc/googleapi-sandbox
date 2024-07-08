# googleapi-sandbox

To create a Python virtual environment, use the following command:

``` bash
python -m venv .venv
```

To activate the virtual environment, depending on your operating system, use one of the following commands:

- For Windows:

``` bash
.venv\Scripts\activate
```

- For macOS and Linux:

``` bash
source .venv/bin/activate
```

- Run fastapi

```bash
fastapi dev main.py
fastapi run main.py
```

- Update requirements.txt

```bash
pipreqs --force --ignore bin,etc,include,lib,lib64
```

- Docker

```bash
docker build -t googleapi-sandbox:0.1 .
docker run --name googleapi-sandbox -d -p 8000:8000 googleapi-sandbox:0.1
docker logs googleapi-sandbox
```

- Gcloud

```bash
docker tag googleapi-sandbox:0.1 gcr.io/turing-seeker-428221-k7/googleapi-sandbox:0.1
gcloud builds submit --tag gcr.io/turing-seeker-428221-k7/googleapi-sandbox:0.1
gcloud run deploy googleapi-sandbox --image gcr.io/turing-seeker-428221-k7/googleapi-sandbox:0.1 --platform managed --region us-central1 --allow-unauthenticated
```
