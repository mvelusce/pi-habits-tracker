#!/bin/bash
# Quick script to get a bearer token for the Wellness Log API

echo "🌿 Wellness Log - Get API Token"
echo "================================"
echo ""

# Default to localhost if no URL provided
API_URL="${1:-http://localhost:9696}"

read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo ""
echo ""

# Get the token
RESPONSE=$(curl -s -X POST "${API_URL}/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}")

# Check if login was successful
if echo "$RESPONSE" | grep -q "access_token"; then
  TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
  
  echo "✅ Login successful!"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Your Bearer Token:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$TOKEN"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "📋 Usage:"
  echo ""
  echo "1. In API Docs (${API_URL}/docs):"
  echo "   - Click 'Authorize' button"
  echo "   - Paste the token above"
  echo "   - Click 'Authorize' then 'Close'"
  echo ""
  echo "2. In cURL commands:"
  echo "   curl -H \"Authorization: Bearer ${TOKEN}\" ${API_URL}/api/wellbeing/"
  echo ""
  echo "3. Copy to clipboard (macOS):"
  echo "   echo \"${TOKEN}\" | pbcopy"
  echo ""
  echo "Token expires in 30 days."
  echo ""
else
  echo "❌ Login failed!"
  echo ""
  if echo "$RESPONSE" | grep -q "detail"; then
    ERROR=$(echo "$RESPONSE" | grep -o '"detail":"[^"]*"' | cut -d'"' -f4)
    echo "Error: $ERROR"
  else
    echo "Could not connect to API at ${API_URL}"
    echo "Make sure the backend is running: docker compose ps"
  fi
  echo ""
  exit 1
fi

