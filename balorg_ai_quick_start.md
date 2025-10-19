# Balorg AI Quick Start Guide

## 🚀 Getting Started with Multi-Platform Development

This guide provides quick reference commands and configurations for developing Balorg AI across all target platforms.

---

## 📱 Android Development Quick Start

### Prerequisites
```bash
# Install Java Development Kit
sudo apt install openjdk-17-jdk

# Install Android Studio
# Download from: https://developer.android.com/studio

# Install Flutter (if using Flutter)
git clone https://github.com/flutter/flutter.git
export PATH="$PATH:`pwd`/flutter/bin"
flutter doctor
```

### Project Setup
```bash
# Create new Flutter project
flutter create balorg_ai
cd balorg_ai

# Add dependencies
flutter pub add tensorflow_lite
flutter pub add http
flutter pub add shared_preferences

# Run on Android device/emulator
flutter run
```

### Build for Release
```bash
# Build APK
flutter build apk --release

# Build App Bundle (for Play Store)
flutter build appbundle --release

# Output location:
# build/app/outputs/bundle/release/app-release.aab
# build/app/outputs/apk/release/app-release.apk
```

### Signing Configuration
Create `android/key.properties`:
```properties
storePassword=<your-password>
keyPassword=<your-password>
keyAlias=balorg-ai
storeFile=<path-to-keystore>
```

---

## 🍎 iOS Development Quick Start

### Prerequisites
```bash
# Requires macOS with Xcode
xcode-select --install

# Install CocoaPods
sudo gem install cocoapods

# Install Flutter (if using)
# (same as Android setup)
```

### Project Setup
```bash
# Open iOS project
cd ios
pod install
open Runner.xcworkspace

# Configure signing in Xcode:
# Select Runner target → Signing & Capabilities
# Set Team and Bundle Identifier
```

### Build for Release
```bash
# Build iOS app
flutter build ios --release

# Or build IPA for distribution
flutter build ipa --release

# Output location:
# build/ios/ipa/balorg_ai.ipa
```

### TestFlight Distribution
```bash
# Archive and upload using Xcode or
xcrun altool --upload-app \
  --type ios \
  --file build/ios/ipa/balorg_ai.ipa \
  --apiKey <API_KEY> \
  --apiIssuer <ISSUER_ID>
```

---

## 🪟 Windows Development Quick Start

### Prerequisites
```bash
# Install Node.js
# Download from: https://nodejs.org

# Install Electron
npm install -g electron

# Install Python (for backend)
# Download from: https://python.org
```

### Project Setup
```bash
# Create Electron app
mkdir balorg-ai-desktop
cd balorg-ai-desktop
npm init -y

# Install dependencies
npm install electron electron-builder
npm install --save-dev @electron-forge/cli

# Initialize Electron Forge
npx electron-forge import
```

### Main Process (main.js)
```javascript
const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

const PYTHON_SHUTDOWN_TIMEOUT = 5000; // 5 seconds
let pythonProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  // Start Python backend - use python3 for better compatibility
  const pythonScript = path.join(__dirname, 'backend', 'server.py');
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  pythonProcess = spawn(pythonCmd, [pythonScript]);
  
  // Handle Python process errors
  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python backend:', err);
    app.quit();
  });
  
  pythonProcess.on('exit', (code) => {
    if (code !== 0) {
      console.error(`Python backend exited with code ${code}`);
    }
  });
  
  createWindow();
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    // Graceful shutdown with timeout fallback
    pythonProcess.kill('SIGTERM');
    setTimeout(() => {
      if (pythonProcess && !pythonProcess.killed) {
        pythonProcess.kill('SIGKILL');
      }
    }, PYTHON_SHUTDOWN_TIMEOUT);
  }
  app.quit();
});
```

### Preload Script (preload.js) - For Secure IPC
```javascript
const { contextBridge, ipcRenderer } = require('electron');

// Validate input data
function validateInferenceData(data) {
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid inference data');
  }
  // Add more specific validation as needed
  return true;
}

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('api', {
  inference: (data) => {
    validateInferenceData(data);
    return ipcRenderer.invoke('run-inference', data);
  },
  getStatus: () => ipcRenderer.invoke('get-status')
});
```

### Build for Release
```bash
# Build for Windows
npm run make

# Or use electron-builder
npx electron-builder --win --x64

# Output location:
# out/make/squirrel.windows/x64/balorg-ai-setup.exe
```

### MSIX Package for Microsoft Store
```bash
# Install electron-windows-store
npm install -g electron-windows-store

# Convert to MSIX
electron-windows-store \
  --input-directory ./out/balorg-ai-win32-x64 \
  --output-directory ./appx \
  --package-name "BalorgAI" \
  --publisher-display-name "Your Company"
```

---

## 🍏 macOS Development Quick Start

### Prerequisites
```bash
# Requires macOS
# Xcode Command Line Tools
xcode-select --install

# Node.js and Electron (same as Windows)
```

### Build for Release
```bash
# Build for macOS
npm run make

# Or create DMG
npx electron-builder --mac --x64 --arm64

# Sign the app (required for distribution)
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  "Balorg AI.app"
```

### Notarization for Distribution
```bash
# Create ZIP for notarization
ditto -c -k --keepParent "Balorg AI.app" balorg-ai.zip

# Submit for notarization
xcrun altool --notarize-app \
  --primary-bundle-id "com.yourcompany.balorgai" \
  --username "your@email.com" \
  --password "@keychain:AC_PASSWORD" \
  --file balorg-ai.zip

# Check status
xcrun altool --notarization-info <REQUEST_UUID> \
  --username "your@email.com" \
  --password "@keychain:AC_PASSWORD"

# Staple the notarization
xcrun stapler staple "Balorg AI.app"
```

---

## 🐧 Linux Development Quick Start

### Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm python3 python3-pip

# Install Electron
npm install -g electron
```

### Build for Release
```bash
# Build AppImage
npx electron-builder --linux AppImage

# Build DEB package
npx electron-builder --linux deb

# Build RPM package
npx electron-builder --linux rpm

# Build Snap
npx electron-builder --linux snap
```

### Snap Configuration (snapcraft.yaml)
```yaml
name: balorg-ai
version: '1.0.0'
summary: Balorg AI Application
description: Deep learning AI framework
base: core20
confinement: strict
grade: stable

apps:
  balorg-ai:
    command: balorg-ai
    plugs:
      - desktop
      - network
      - home

parts:
  balorg-ai:
    plugin: dump
    source: ./dist
```

---

## 🎮 PlayStation 5 Development Quick Start

### Prerequisites
```bash
# 1. PlayStation Partners Account
# Apply at: https://partners.playstation.net

# 2. PS5 DevKit (after approval)
# Order through PlayStation Partners portal

# 3. Install PS5 SDK
# Download from PlayStation Partners portal
# Requires signed NDA
```

### Unity Setup for PS5
```bash
# Install Unity Hub
# Download from: https://unity.com

# Install Unity version with PS5 support
# (Requires PS5 SDK to be installed first)

# Create new Unity project
unity-hub create --name BalorgAI --template 3D

# Add PS5 platform module
# File → Build Settings → Add PS5 Platform
```

### Unity Project Structure
```
BalorgAI/
├── Assets/
│   ├── Scripts/
│   │   ├── BalorgAIManager.cs
│   │   └── PS5Integration.cs
│   ├── Plugins/
│   │   └── BalorgAICore.dll  (C++ AI core)
│   ├── Scenes/
│   │   └── MainScene.unity
│   └── UI/
├── Packages/
│   └── manifest.json
└── ProjectSettings/
```

### C++ Native Plugin (for PS5)
```cpp
// BalorgAICore.cpp
#include "ps5_sdk.h"
#include "balorg_ai.h"

extern "C" {
    __declspec(dllexport) void InitializeAI() {
        // Initialize PS5-optimized AI engine
        initPS5GPU();
        loadModels();
    }
    
    __declspec(dllexport) float* RunInference(float* input, int size) {
        // Run inference on PS5 GPU
        return balorg_inference(input, size);
    }
}
```

### Unity C# Wrapper
```csharp
// BalorgAIManager.cs
using UnityEngine;
using System.Runtime.InteropServices;

public class BalorgAIManager : MonoBehaviour
{
    [DllImport("BalorgAICore")]
    private static extern void InitializeAI();
    
    [DllImport("BalorgAICore")]
    private static extern float[] RunInference(float[] input, int size);
    
    void Start()
    {
        InitializeAI();
    }
    
    public float[] ProcessInput(float[] data)
    {
        return RunInference(data, data.Length);
    }
}
```

### Build for PS5
```bash
# In Unity:
# File → Build Settings → PS5
# Configure build settings
# Build

# Or via command line:
unity -quit -batchmode \
  -projectPath /path/to/BalorgAI \
  -buildTarget PS5 \
  -executeMethod BuildScript.BuildPS5
```

### PS5 Submission Package
```
BalorgAI-PS5/
├── eboot.bin              (Main executable)
├── param.sfo              (Metadata)
├── icon0.png              (App icon)
├── pic1.png               (Background image)
├── data/                  (Game data)
└── sce_sys/              (System files)
```

---

## 🔧 Backend API Setup (All Platforms)

### Python FastAPI Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn tensorflow torch

# Create requirements.txt
pip freeze > requirements.txt
```

### FastAPI Server (server.py)
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf

app = FastAPI()

# Enable CORS for desktop/mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model
model = tf.keras.models.load_model('models/balorg_ai.h5')

@app.get("/")
async def root():
    return {"message": "Balorg AI API", "version": "1.0.0"}

@app.post("/inference")
async def run_inference(file: UploadFile = File(...)):
    # Read input data
    contents = await file.read()
    data = np.frombuffer(contents, dtype=np.float32)
    
    # Run inference
    result = model.predict(data.reshape(1, -1))
    
    return {"result": result.tolist()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Start Backend Server
```bash
# Development
uvicorn server:app --reload --port 8000

# Production
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📦 CI/CD Pipeline Setup

### GitHub Actions for Multi-Platform Builds

Create `.github/workflows/build.yml`:
```yaml
name: Build All Platforms

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v3
        with:
          name: android-apk
          path: build/app/outputs/apk/release/

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build ios --release --no-codesign
      
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run build:windows
      
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run build:macos
      
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run build:linux
```

---

## 🧪 Testing Commands

### Unit Tests
```bash
# Flutter
flutter test

# Node.js/Electron
npm test

# Python backend
pytest tests/
```

### Integration Tests
```bash
# Flutter integration tests
flutter drive --target=test_driver/app.dart

# E2E tests with Electron
npm run test:e2e
```

### Performance Testing
```bash
# Flutter performance
flutter drive --profile --trace-startup \
  --target=test_driver/perf_test.dart

# Backend load testing
pip install locust
locust -f tests/load_test.py
```

---

## 📊 Monitoring & Analytics

### Add Analytics to Mobile
```dart
// Flutter Firebase Analytics
import 'package:firebase_analytics/firebase_analytics.dart';

FirebaseAnalytics analytics = FirebaseAnalytics.instance;

void trackInference() {
  analytics.logEvent(
    name: 'ai_inference',
    parameters: {'model': 'balorg_v1', 'duration_ms': 150},
  );
}
```

### Backend Monitoring
```python
# Add Prometheus metrics
from prometheus_client import Counter, Histogram
from prometheus_client import start_http_server

inference_counter = Counter('inference_total', 'Total inferences')
inference_duration = Histogram('inference_duration_seconds', 
                               'Inference duration')

@app.post("/inference")
@inference_duration.time()
async def run_inference(data: dict):
    inference_counter.inc()
    # ... inference code ...
```

---

## 🔐 Security Best Practices

### API Key Management
```bash
# Never commit secrets to git
echo ".env" >> .gitignore
echo "*.key" >> .gitignore

# Use environment variables
export API_KEY="your-secret-key"
export DATABASE_URL="your-db-url"
```

### Code Signing Certificates
```bash
# Store certificates securely
# Use CI/CD secrets for automation
# Never commit private keys

# GitHub Secrets for signing
# Settings → Secrets → Actions
# Add: ANDROID_KEYSTORE, IOS_CERTIFICATE, etc.
```

---

## 📚 Additional Resources

### Official Documentation
- **Flutter:** https://flutter.dev/docs
- **Electron:** https://www.electronjs.org/docs
- **Unity:** https://docs.unity3d.com
- **FastAPI:** https://fastapi.tiangolo.com
- **TensorFlow:** https://www.tensorflow.org/api_docs

### Platform Guidelines
- **Google Play:** https://play.google.com/console/about/guides/
- **App Store:** https://developer.apple.com/app-store/review/guidelines/
- **Microsoft Store:** https://docs.microsoft.com/en-us/windows/uwp/publish/
- **PlayStation:** https://partners.playstation.net

### Community Support
- **Flutter Discord:** https://discord.gg/flutter
- **Unity Forums:** https://forum.unity.com
- **Stack Overflow:** Tag your questions appropriately

---

## 🚀 Quick Commands Reference

```bash
# Android
flutter build apk --release
flutter build appbundle --release

# iOS
flutter build ios --release
flutter build ipa --release

# Windows
npm run build:windows
npx electron-builder --win

# macOS
npm run build:macos
npx electron-builder --mac

# Linux
npm run build:linux
npx electron-builder --linux

# Backend
uvicorn server:app --reload
pytest tests/

# Git
git add .
git commit -m "Update"
git push origin main
```

---

**This quick start guide provides the essential commands and configurations needed to begin developing Balorg AI across all target platforms.**
