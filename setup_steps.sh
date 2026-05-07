# ── Step 1: Enable Bedrock model access ───────────────────────────────
# Go to AWS Console → Bedrock → Model access
# Enable: Claude 3.5 Sonnet (anthropic.claude-3-5-sonnet-20241022-v2:0)

# ── Step 2: Create your Lambda function ───────────────────────────────
# AWS Console → Lambda → Create function
#   Runtime: Python 3.12
#   Architecture: x86_64
# Paste lambda_function.py into the inline editor and Deploy

# ── Step 3: Give Lambda permission to call Bedrock ────────────────────
# In your Lambda → Configuration → Permissions → Role name (click it)
# IAM → Add permissions → Attach policies
# Add: AmazonBedrockFullAccess

# ── Step 4: Enable a Function URL (no API Gateway needed!) ────────────
# Lambda → Configuration → Function URL → Create function URL
#   Auth type: NONE (public, fine for dev)
#   CORS: Enable → Allow origin: *
# Copy the URL — paste it into index.html as LAMBDA_URL

# ── Step 5: Test it from the terminal ─────────────────────────────────
curl -X POST YOUR_LAMBDA_FUNCTION_URL_HERE \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "wise_sensei",
    "mood": "tired and stressed",
    "goal": "stress relief",
    "duration": 20
  }'

# ── Step 6: Open index.html in your browser ───────────────────────────
# Just double-click it locally — no server needed for dev!
# Later you can upload it to S3 for public hosting.