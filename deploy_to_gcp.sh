#!/usr/bin/env bash
# ==============================================================================
# WittyWeights GCP Deployment Script
# Deploys:
# 1. Cloud Run Service (Web Landing Page + Subscriber Onboarding + Webhook)
# 2. Firestore (Zero-duplicate state tracking & subscriber database)
# 3. Secret Manager (Resend API key)
# 4. Cloud Scheduler (Mon-Fri 07:00 AM Cron)
# ==============================================================================

set -e

# Configuration - adjust project ID and region as desired
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="wittyweights"
CRON_TIMEZONE="${CRON_TIMEZONE:-Asia/Kolkata}"  # Set to your local timezone (e.g., America/New_York, Asia/Kolkata)

if [ -z "$PROJECT_ID" ]; then
  echo "❌ Error: GCP Project ID is not set. Run: export GCP_PROJECT_ID='your-project-id'"
  exit 1
fi

echo "======================================================================"
echo "🚀 Deploying WittyWeights to GCP Project: $PROJECT_ID ($REGION)"
echo "======================================================================"

# Step 1: Enable GCP Services
echo "1. Enabling required GCP APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  firestore.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  --project="$PROJECT_ID"

# Step 2: Initialize Firestore (if not already created)
echo "2. Checking Firestore database..."
gcloud firestore databases create --location="$REGION" --project="$PROJECT_ID" 2>/dev/null || echo "   ✓ Firestore database already initialized."

# Step 3: Configure Resend Secret in Secret Manager
echo "3. Checking Resend API key in Secret Manager..."
if ! gcloud secrets describe RESEND_API_KEY --project="$PROJECT_ID" >/dev/null 2>&1; then
  echo "   Enter your Resend API Key (starts with 're_'):"
  read -r RESEND_KEY
  echo -n "$RESEND_KEY" | gcloud secrets create RESEND_API_KEY --data-file=- --project="$PROJECT_ID"
fi

# Step 4: Build and Deploy Cloud Run Service
echo "4. Building and deploying Cloud Run Service..."
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --set-secrets="RESEND_API_KEY=RESEND_API_KEY:latest" \
  --set-env-vars="FROM_EMAIL=onboarding@resend.dev" \
  --project="$PROJECT_ID"

# Get deployed Cloud Run Service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")
echo "   ✓ Cloud Run Service is live at: $SERVICE_URL"

# Step 5: Configure Cloud Scheduler (Mon-Fri 07:00 AM)
echo "5. Configuring Cloud Scheduler (Mon-Fri 07:00 AM)..."
gcloud scheduler jobs delete wittyweights-weekday-dispatch --location="$REGION" --quiet 2>/dev/null || true

gcloud scheduler jobs create http wittyweights-weekday-dispatch \
  --location="$REGION" \
  --schedule="0 7 * * 1-5" \
  --time-zone="$CRON_TIMEZONE" \
  --uri="$SERVICE_URL/api/dispatch" \
  --http-method=POST \
  --oidc-service-account-email="$PROJECT_ID-compute@developer.gserviceaccount.com" \
  --project="$PROJECT_ID"

echo "======================================================================"
echo "🎉 DEPLOYMENT COMPLETE!"
echo "📍 Public Typewriter Landing Page & Signup: $SERVICE_URL"
echo "⏰ Mon-Fri Cron Dispatch Schedule: 07:00 AM ($CRON_TIMEZONE)"
echo "📬 Email Sender: Resend Sandbox (onboarding@resend.dev)"
echo "======================================================================"
