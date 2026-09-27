#!/bin/bash
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"cleanair-ai-prod"}
REGION=${GCP_REGION:-"us-central1"}
IMAGE_TAG="gcr.io/${PROJECT_ID}/cleanair-ai:latest"

echo "========================================================="
echo "Deploying CLEANAIR AI to Google Cloud (Project: ${PROJECT_ID})"
echo "========================================================="

# 1. Enable Required GCP APIs
echo "[1/5] Enabling Google Cloud Services APIs..."
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    pubsub.googleapis.com \
    bigquery.googleapis.com \
    secretmanager.googleapis.com \
    --project "${PROJECT_ID}" || true

# 2. Setup Pub/Sub Topics
echo "[2/5] Initializing Pub/Sub Topics..."
gcloud pubsub topics create pollution-updates --project "${PROJECT_ID}" || true
gcloud pubsub topics create pollution-alerts --project "${PROJECT_ID}" || true
gcloud pubsub topics create agent-events --project "${PROJECT_ID}" || true

# 3. Create BigQuery Dataset & Tables
echo "[3/5] Setting up BigQuery Analytics Tables..."
bq mk --dataset --location="${REGION}" "${PROJECT_ID}:cleanair_ai_analytics" || true
bq query --use_legacy_sql=false < deployment/bigquery_schema.sql || true

# 4. Build and Push Container Image
echo "[4/5] Building & Pushing Container to Artifact Registry..."
gcloud builds submit --tag "${IMAGE_TAG}" . --project "${PROJECT_ID}" || true

# 5. Deploy Cloud Run Service
echo "[5/5] Deploying Cloud Run Service..."
gcloud run deploy cleanair-ai-app \
    --image "${IMAGE_TAG}" \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --set-env-vars "ENVIRONMENT=production,POLLUTION_PROVIDER=mock,GCP_PROJECT_ID=${PROJECT_ID}" \
    --project "${PROJECT_ID}"

echo "========================================================="
echo "✅ CLEANAIR AI Deployment Completed Successfully!"
echo "========================================================="
