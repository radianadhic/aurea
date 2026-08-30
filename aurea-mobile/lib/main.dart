// =============================================
// AUREA Mobile - Main App
// The Gold Standard of Data
// =============================================

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import 'theme/aurea_theme.dart';
import 'providers/auth_provider.dart';
import 'utils/api_client.dart';
import 'screens/aurea_splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Lock orientation
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  // Set system UI style
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));

  runApp(const AureaApp());
}

class AureaApp extends StatelessWidget {
  const AureaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiClient>(
          create: (_) => ApiClient(),
        ),
        ChangeNotifierProvider<AuthProvider>(
          create: (ctx) => AuthProvider(ctx.read<ApiClient>()),
        ),
      ],
      child: MaterialApp(
        title: 'AUREA',
        debugShowCheckedModeBanner: false,
        theme: AureaTheme.light,
        darkTheme: AureaTheme.dark,
        themeMode: ThemeMode.system,
        home: const AureaAppRoot(),
      ),
    );
  }
}

class AureaAppRoot extends StatefulWidget {
  const AureaAppRoot({super.key});

  @override
  State<AureaAppRoot> createState() => _AureaAppRootState();
}

class _AureaAppRootState extends State<AureaAppRoot> {
  bool _splashComplete = false;
  bool _checkingAuth = true;

  @override
  void initState() {
    super.initState();
    // Check auth status after splash
    Future.delayed(const Duration(milliseconds: 100), () async {
      if (!mounted) return;
      final auth = context.read<AuthProvider>();
      await auth.checkAuthStatus();
      setState(() => _checkingAuth = false);
    });
  }

  void _onSplashComplete() {
    setState(() => _splashComplete = true);
  }

  @override
  Widget build(BuildContext context) {
    if (!_splashComplete) {
      return AureaSplashScreen(onComplete: _onSplashComplete);
    }

    if (_checkingAuth) {
      return const Scaffold(
        backgroundColor: AureaColors.navy,
      );
    }

    return Consumer<AuthProvider>(
      builder: (context, auth, _) {
        if (auth.isAuthenticated) {
          return const HomeScreen();
        }
        return const LoginScreen();
      },
    );
  }
}
