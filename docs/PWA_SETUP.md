# Progressive Web App (PWA) Setup

## Overview

The Wellness Log is now configured as a **Progressive Web App (PWA)**, which allows users to install it on their devices (Android, iOS, desktop) and use it like a native app.

## What Changed

### 1. Service Worker Registration
- Added automatic service worker registration in `main.tsx`
- Enables offline functionality and faster loading

### 2. Web App Manifest
- Updated `manifest.webmanifest` with proper metadata
- Added required PWA icons (192x192 and 512x512)
- Set `display: standalone` for app-like experience
- Added proper theme colors and descriptions

### 3. HTML Meta Tags
- Added Apple-specific meta tags for iOS support
- Linked manifest file properly
- Added theme color for browser UI customization

### 4. PWA Icons
- Created placeholder icons (you should replace with custom ones)
- Icons support both regular and maskable formats
- Sizes: 192x192px and 512x512px

## How to Test

### Android (Chrome/Brave)

1. Open your wellness log in Chrome or Brave
2. Look for the install prompt (should appear automatically after a few seconds)
3. Or tap the menu (⋮) → "Install app" or "Add to Home screen"
4. The app will install and create an icon on your home screen
5. Open the installed app - it will run in standalone mode without browser UI

### iOS (Safari)

1. Open your wellness log in Safari
2. Tap the Share button (□↑)
3. Scroll down and tap "Add to Home Screen"
4. Customize the name if desired
5. Tap "Add"
6. The app icon will appear on your home screen

### Desktop (Chrome/Edge/Brave)

1. Open your wellness log
2. Look for the install icon (⊕) in the address bar
3. Or go to Menu → "Install Wellness Log"
4. The app will install and can be launched from your apps menu

## Installation Criteria

For the browser to show the "Install" prompt (instead of just "Add to Home screen"), your PWA must meet these criteria:

✅ **Manifest file** with:
- `name` and `short_name`
- `start_url`
- `display: standalone` or `fullscreen`
- At least one icon (192x192 or larger)

✅ **Service worker** registered and active

✅ **HTTPS** (or localhost for development)

✅ **Multiple page visits** (browser tracks engagement)

## Improving the Icons

The current icons are placeholders. To create professional icons:

### Option 1: PWA Builder (Recommended)
1. Go to https://www.pwabuilder.com/imageGenerator
2. Upload a 512x512px image with your app logo
3. Download the generated icon pack
4. Replace `pwa-192x192.png` and `pwa-512x512.png` in `/frontend/public/`

### Option 2: Manual Creation
1. Create a 512x512px PNG with your app branding
2. Use an image editor to create a 192x192px version
3. Ensure both have transparent backgrounds or solid colors
4. Replace the files in `/frontend/public/`

### Option 3: Use the HTML Generator
1. Open `/frontend/public/pwa-icon.html` in a browser
2. Modify the canvas drawing code to customize the icon
3. Click to download the generated icons
4. Save them as `pwa-192x192.png` and `pwa-512x512.png`

## Features Enabled

### Offline Support
- The service worker caches your app's assets
- Works without internet connection once installed
- API responses are cached for 24 hours

### App-Like Experience
- Runs in standalone mode (no browser UI)
- Appears in app launchers and task switchers
- Can be uninstalled like a regular app

### Fast Loading
- Cached assets load instantly
- Progressive enhancement for slow connections

## Customization

### Change App Name
Edit `/frontend/vite.config.ts`:
```typescript
manifest: {
  name: 'Your App Name',
  short_name: 'Short Name',
  ...
}
```

### Change Theme Color
Update the `theme_color` in both:
- `/frontend/vite.config.ts`
- `/frontend/index.html` (meta tag)

### Modify Caching Strategy
Edit the `workbox` configuration in `/frontend/vite.config.ts`

## Troubleshooting

### "Install" button doesn't appear
- Make sure you're using HTTPS (or localhost)
- Clear browser cache and reload
- Visit the app multiple times (some browsers require engagement)
- Check DevTools → Application → Manifest for errors

### Icons don't show up
- Verify icon files exist in `/frontend/public/`
- Check file names match manifest configuration
- Clear cache and reinstall

### App doesn't work offline
- Check DevTools → Application → Service Workers
- Verify service worker is registered and active
- Try uninstalling and reinstalling the app

## Testing in Development

The PWA features work in development mode too:
```bash
cd frontend
npm run dev
```

Then visit http://localhost:3000 and test the install functionality.

## Production Deployment

The PWA is fully configured for production. Just ensure:
1. Your server serves the app over HTTPS
2. All icon files are accessible
3. The manifest.webmanifest is served with correct MIME type

## References

- [PWA Checklist](https://web.dev/pwa-checklist/)
- [MDN: Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/)

