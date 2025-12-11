# Authentication Implementation Summary

## Overview
Added password-protected authentication to the Wellness Log application with single-user support.

## Backend Changes

### New Files
1. **`backend/app/auth.py`** - Authentication utilities
   - Password hashing with bcrypt
   - JWT token generation and validation
   - User authentication functions
   - `get_current_user` dependency for route protection

2. **`backend/app/routers/auth.py`** - Authentication endpoints
   - `POST /api/auth/login` - User login
   - `POST /api/auth/register` - Initial user registration (only if no users exist)
   - `GET /api/auth/me` - Get current user info
   - `GET /api/auth/check-setup` - Check if initial setup is complete

3. **`backend/create_user.py`** - CLI script for creating users
   - Interactive script to create the initial user
   - Prevents creation of multiple users

### Modified Files
1. **`backend/app/models.py`**
   - Added `User` model with username, hashed_password, and is_active fields

2. **`backend/app/schemas.py`**
   - Added authentication schemas: `Token`, `TokenData`, `UserLogin`, `UserCreate`, `User`

3. **`backend/app/main.py`**
   - Added auth router
   - All API routes are now protected except auth endpoints

4. **`backend/app/routers/lifestyle_factors.py`**
   - Added `dependencies=[Depends(get_current_user)]` to protect routes

5. **`backend/app/routers/wellbeing.py`**
   - Added `dependencies=[Depends(get_current_user)]` to protect routes

6. **`backend/app/routers/analytics.py`**
   - Added `dependencies=[Depends(get_current_user)]` to protect routes

7. **`backend/app/routers/export.py`**
   - Added `dependencies=[Depends(get_current_user)]` to protect routes

## Frontend Changes

### New Files
1. **`frontend/src/contexts/AuthContext.tsx`** - Authentication context
   - Manages authentication state
   - Provides login, register, logout functions
   - Checks setup status and validates tokens

2. **`frontend/src/pages/Login.tsx`** - Login/Setup page
   - Initial setup screen for first-time users
   - Login screen for returning users
   - Beautiful gradient UI with form validation

### Modified Files
1. **`frontend/src/lib/api.ts`**
   - Added request interceptor to include JWT token in all API calls
   - Added response interceptor to handle 401 errors and redirect to login

2. **`frontend/src/App.tsx`**
   - Wrapped app with `AuthProvider`
   - Added `ProtectedRoutes` component
   - Shows loading state while checking authentication
   - Redirects to login if not authenticated

3. **`frontend/src/components/Layout.tsx`**
   - Added logout button in header
   - Imports and uses `useAuth` hook

## Security Features

1. **Password Hashing**: Bcrypt with automatic salt generation
2. **JWT Tokens**: 30-day expiration for convenience
3. **Token Storage**: Browser localStorage
4. **Protected Routes**: All API endpoints except auth require authentication
5. **Single User**: Only one user account allowed
6. **Environment Variable Support**: SECRET_KEY can be set via environment variable

## Database Changes

A new `users` table will be automatically created when the backend starts:
- `id` (primary key)
- `username` (unique, indexed)
- `hashed_password`
- `created_at`
- `is_active`

## Migration Guide for Existing Users

If you already have the app running with data:

1. **Pull the latest changes**:
   ```bash
   git pull origin main
   ```

2. **Rebuild the containers**:
   ```bash
   docker compose down
   docker compose build
   docker compose up -d
   ```

3. **Create your user account**:
   - Option A: Use the web interface (recommended)
     - Navigate to your app URL
     - You'll see the setup screen
     - Create your username and password
   
   - Option B: Use the CLI script
     ```bash
     docker compose exec backend python create_user.py
     ```

4. **Your existing data is preserved**:
   - All your lifestyle factors, entries, and wellbeing metrics remain intact
   - Only the authentication layer is added on top

## Configuration

### Environment Variables
- `SECRET_KEY` (optional): JWT secret key. Defaults to a placeholder that should be changed in production.

Generate a secure secret key:
```bash
openssl rand -hex 32
```

Then add to your `.env` file or docker-compose.yml:
```
SECRET_KEY=your-generated-secret-key-here
```

## Testing the Implementation

1. Start the app: `docker compose up -d`
2. Navigate to http://localhost:9797
3. You should see the Initial Setup screen
4. Create a username and password
5. After login, all features should work as before
6. Try logging out and logging back in
7. Test that you cannot access API endpoints without authentication

## Security Recommendations

1. **Change the SECRET_KEY** in production
2. **Use HTTPS** in production (especially important for login)
3. **Use a strong password** (the app requires minimum 4 characters, but use more)
4. **Keep your server secure** as this is a single-user system
5. **Regular backups** of your SQLite database

## Troubleshooting

### Issue: Can't create user via web interface
- **Solution**: Use the CLI script: `docker compose exec backend python create_user.py`

### Issue: Forgot password
- **Solution**: Delete user and recreate:
  ```bash
  docker compose exec backend python -c "from app.database import SessionLocal; from app.models import User; db = SessionLocal(); db.query(User).delete(); db.commit(); print('User deleted')"
  docker compose exec backend python create_user.py
  ```

### Issue: Token expired or invalid
- **Solution**: Log out and log back in, or clear browser localStorage

### Issue: Want to disable authentication
- **Solution**: Remove `dependencies=[Depends(get_current_user)]` from all routers (not recommended)

