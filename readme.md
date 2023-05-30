gcloud builds submit --tag gcr.io/archersproj/aaemail  --project=archersproj

gcloud run deploy --image gcr.io/<ProjectName>/<AppName> --platform managed  --project=<ProjectName> --allow-unauthenticated