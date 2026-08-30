# AUREA Mobile

**AUREA — The Gold Standard of Data**
**Bank XYZ Customer MDM App**

Mobile app for AUREA Master Data Management Platform — view your golden customer profile, accounts, and KYC status on the go.

---

## ✨ Features

- 🔐 **Secure Login** — username/password + biometric (fingerprint/face)
- 📊 **Dashboard** — golden customer card, quick stats, recent activity
- 👥 **Customer List (GC)** — search Golden Customers by CIF/name/NIK
- 💰 **Accounts (GA)** — view Golden Accounts, balances, products
- 👤 **Profile** — settings, biometric toggle, theme, language
- 🎨 **AUREA Branding** — gold + navy theme throughout

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Flutter 3.10+ |
| **Language** | Dart 3.0+ |
| **State Management** | Provider + Riverpod |
| **HTTP** | Dio + Flutter Secure Storage |
| **UI** | Material 3 + Google Fonts |
| **Charts** | fl_chart + Syncfusion |
| **Animations** | flutter_animate + Rive |
| **Auth** | local_auth + biometric_storage |

## 📱 Screenshots

| Splash | Login | Dashboard |
|---|---|---|
| Gold A on navy gradient | Navy gradient + gold AUREA | Golden Customer card hero |

## 🎨 Brand Identity

| | |
|---|---|
| **Name** | AUREA (Latin: "Golden") |
| **Tagline** | The Gold Standard of Data |
| **Primary Color** | Gold `#D4AF37` |
| **Background** | Navy `#0A1929` |
| **Brand Font** | Georgia (wordmark) |
| **UI Font** | Inter (body) |
| **App Icon** | Gold "A" + 3 golden dots (MD3G) |

## 📂 Project Structure

```
aurea-mobile/
├── lib/
│   ├── main.dart                       # App entry
│   ├── theme/
│   │   └── aurea_theme.dart            # Brand colors & ThemeData
│   ├── widgets/
│   │   └── aurea_logo.dart             # Reusable logo component
│   ├── screens/
│   │   ├── aurea_splash_screen.dart    # Splash with particles
│   │   ├── login_screen.dart           # Login + biometric
│   │   ├── home_screen.dart            # Bottom nav shell
│   │   ├── dashboard_screen.dart       # Dashboard
│   │   ├── customers_screen.dart       # Golden Customer list
│   │   ├── accounts_screen.dart        # Golden Account list
│   │   └── profile_screen.dart         # Profile + settings
│   ├── models/
│   │   ├── customer.dart               # Golden Customer
│   │   ├── account.dart                # Golden Account
│   │   └── user.dart                   # AUREA User
│   ├── providers/
│   │   └── auth_provider.dart          # Auth state
│   └── utils/
│       └── api_client.dart             # Dio + interceptors
├── android/                            # Android config
│   └── app/src/main/
│       ├── AndroidManifest.xml
│       └── res/                        # Generated app icons
├── ios/                                # iOS config
│   └── Runner/
│       ├── Info.plist
│       └── Assets.xcassets/            # Generated app icons
├── assets/
│   ├── icons/                          # Master icons
│   ├── images/
│   └── fonts/                          # (uses Google Fonts)
└── pubspec.yaml
```

## 🚀 Setup

### Prerequisites

- **Flutter** 3.10 or higher → https://docs.flutter.dev/get-started/install
- **Xcode** 15+ (for iOS)
- **Android Studio** + SDK 34 (for Android)
- **CocoaPods** (for iOS)

### Install

```bash
# Clone the repository (or extract aurea-mobile/)
cd aurea-mobile

# Get dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Or build for specific platform
flutter build apk         # Android APK
flutter build appbundle   # Android App Bundle (Play Store)
flutter build ios         # iOS (requires Xcode + Mac)
```

### First Run

1. Splash screen appears (3.5s, can be skipped)
2. Login screen with biometric option
3. Dashboard with golden customer hero card
4. 4 tabs: Dashboard / Customers / Accounts / Profile

## 🎨 Theme Switching

The app supports both light and dark themes via `ThemeMode.system`:

```dart
// In main.dart
themeMode: ThemeMode.system,  // follows device
// or
themeMode: ThemeMode.light,  // force light
// or
themeMode: ThemeMode.dark,   // force dark
```

## 🔐 Auth Flow

```
Splash → check token in secure storage
   ├─ has token + valid → HomeScreen
   └─ no token / invalid → LoginScreen
        ├─ username + password → API /auth/login
        │   ├─ 200 + user → HomeScreen
        │   └─ MFA required → MFA dialog
        └─ biometric → local_auth.verify()
```

## 📡 API Integration

The app expects a backend at:
```
https://api.aurea.bankxyz.co.id
```

Override for development in `lib/utils/api_client.dart`:
```dart
static const String _baseUrl = 'http://localhost:8080';
```

Required endpoints:
- `POST /auth/login` — login with username/password
- `POST /auth/refresh` — refresh access token
- `GET /auth/me` — get current user profile
- `GET /api/customers` — list golden customers
- `GET /api/customers/{cif}` — get customer detail
- `GET /api/accounts?cif={cif}` — list accounts by customer

## 🧪 Testing

```bash
# Run unit tests
flutter test

# Run integration tests
flutter test integration_test/

# With coverage
flutter test --coverage
```

## 📦 Build for Production

### Android

```bash
# Generate signing key (one-time)
keytool -genkey -v -keystore ~/aurea-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias aurea

# Configure signing in android/key.properties
# Then build
flutter build appbundle --release
```

### iOS

```bash
# Configure signing in Xcode
open ios/Runner.xcworkspace

# Build
flutter build ios --release
```

## 🌐 Localization

Currently supports:
- 🇮🇩 Bahasa Indonesia (default)
- 🇬🇧 English

To add a new language, edit `lib/l10n/app_*.arb` files.

## 📄 License

Proprietary — Bank XYZ Internal Use Only

---

**AUREA — The Gold Standard of Data** 💎
