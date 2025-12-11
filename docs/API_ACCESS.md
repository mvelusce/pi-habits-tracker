# Accessing the Wellness Log API with Authentication

## Getting Your Bearer Token

Since the API is now protected with authentication, you need a bearer token to access the API documentation and make direct API calls.

### Method 1: Get Token via cURL (Quick & Easy)

First, make sure you've created a user account. Then:

```bash
# Replace 'youruser' and 'yourpassword' with your actual credentials
curl -X POST "http://localhost:9696/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"youruser","password":"yourpassword"}'
```

This will return a JSON response like:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Copy the `access_token` value - this is your bearer token!

### Method 2: Extract Token from Browser (If you're already logged in)

1. Open your browser's Developer Tools (F12)
2. Go to the **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Click on **Local Storage** → Select your app's URL
4. Find the key `auth_token`
5. Copy its value - this is your bearer token!

## Using the Token in API Documentation

1. Navigate to the API docs: **http://localhost:9696/docs**
2. Click the **"Authorize"** button (green lock icon) at the top right
3. In the dialog, enter your token in this format:
   ```
   Bearer YOUR_TOKEN_HERE
   ```
   Or just paste the token (without "Bearer" prefix - the UI will add it)
4. Click **"Authorize"**
5. Click **"Close"**

Now you can test all the API endpoints! 🎉

## Using the Token in API Calls

### With cURL:

```bash
# Example: Get all lifestyle factors
curl -X GET "http://localhost:9696/api/lifestyle-factors/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Example: Get wellbeing metrics
curl -X GET "http://localhost:9696/api/wellbeing/?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Example: Create a lifestyle factor
curl -X POST "http://localhost:9696/api/lifestyle-factors/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Exercise",
    "description": "30 minutes of exercise",
    "color": "#10b981",
    "category": "Exercise"
  }'
```

### With Python:

```python
import requests

# Get your token
response = requests.post(
    "http://localhost:9696/api/auth/login",
    json={"username": "youruser", "password": "yourpassword"}
)
token = response.json()["access_token"]

# Use the token in requests
headers = {"Authorization": f"Bearer {token}"}

# Example: Get lifestyle factors
response = requests.get(
    "http://localhost:9696/api/lifestyle-factors/",
    headers=headers
)
lifestyle_factors = response.json()
print(lifestyle_factors)
```

### With JavaScript/Node.js:

```javascript
// Get your token
const loginResponse = await fetch('http://localhost:9696/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'youruser', password: 'yourpassword' })
});
const { access_token } = await loginResponse.json();

// Use the token in requests
const response = await fetch('http://localhost:9696/api/lifestyle-factors/', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const lifestyleFactors = await response.json();
console.log(lifestyleFactors);
```

## Token Information

- **Expiration**: Tokens expire after 30 days (43,200 minutes)
- **Storage**: Tokens are stored in browser localStorage for the web app
- **Refresh**: Log in again to get a new token when expired
- **Security**: Keep your token secure - anyone with your token can access your data

## Quick Reference Script

Save this as `get_token.sh` for quick access:

```bash
#!/bin/bash
# Get Bearer Token for Wellness Log API

read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo ""

TOKEN=$(curl -s -X POST "http://localhost:9696/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | grep -o '"access_token":"[^"]*"' \
  | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed. Check your credentials."
  exit 1
fi

echo "✅ Token retrieved successfully!"
echo ""
echo "Your bearer token:"
echo "$TOKEN"
echo ""
echo "Use in API calls with:"
echo "Authorization: Bearer $TOKEN"
```

Make it executable:
```bash
chmod +x get_token.sh
./get_token.sh
```

## Troubleshooting

### Issue: "Not authenticated" or 401 error
- **Solution**: Make sure you're including the token in the Authorization header
- Check that the token hasn't expired (30 days)
- Verify the token format: `Bearer YOUR_TOKEN_HERE`

### Issue: Token doesn't work in API docs
- **Solution**: Try adding just the token value without "Bearer" prefix
- Or try with the full format: `Bearer eyJhbGci...`

### Issue: Can't get token - login returns error
- **Solution**: Verify your username and password are correct
- Make sure you've created a user account first
- Check that the backend is running: `docker compose ps`

