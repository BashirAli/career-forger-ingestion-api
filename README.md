
# Career Forger Ingestion API v1.0
This Cloud Run API is part of the Career Forger project and is designed to ingest data that is uploaded to a GCS bucket, then notified by PubSub.
It uses the python Email package to parse and clean uploaded feedback sent as emails (and saved as .eml files). It is then sent to Pubsub for NLP analysis

See below for diagram
## Career Forger Architecture Diagram
![Personal Project - Career Forger v1.0 (1).jpeg](Personal%20Project%20-%20Career%20Forger%20v1.0%20%281%29.jpeg)

# Local Development
### 1. Build and Run Local Test
```commandline
docker-compose -f docker-compose-local.yml build career-forger-ingestion-api-local && docker-compose -f docker-compose-local.yml up career-forger-ingestion-api-local
```
**_NOTE:_**  There is a postman collection in the repo which can be used to test the endpoints, but 
you need to add your IP address in to an .env file for it to work


### 2. Build and Run Unit and Integration Tests
```commandline
docker-compose -f docker-compose.yml up --build 
```

#### Integration Tests
With the Docker Compose dev instance running:
```commandline
docker exec career-forger-ingestion-api-dev /bin/sh -c "poetry run pytest /home/appuser/tests/integration_tests/"
```

#### Unit Tests
With the Docker Compose dev instance running:
```commandline
docker exec career-forger-ingestion-api-dev /bin/sh -c "poetry run pytest /home/appuser/tests/unit_tests/"
```

#### Deploy to GCP Dev
For actually deploying to the dev environment
```
gcloud run deploy career-forger-ingestion-api-<your-name> \
 --image europe-west2-docker.pkg.dev/<GAR_NAME>:<VERSION_NUMBER> \
 --platform managed \
 --project <PROJECT_ID> \
 --region europe-west2 \
 --ingress=internal-and-cloud-load-balancing \
 --no-allow-unauthenticated \
 --service-account=<SA>.iam.gserviceaccount.com \
 --set-env-vars "GCP_PROJECT_ID=<PROJECT_ID>" --set-env-vars "SOURCE_BUCKET=<PROJECT_ID>-career_forger_email_bucket" \
 --min-instances=3 \
 --max-instances=10 \
 --concurrency=100 \
 --memory=2Gi \
 --cpu=4 \
 --vpc-connector serverless-conn-ew2 --vpc-egress all-traffic
```