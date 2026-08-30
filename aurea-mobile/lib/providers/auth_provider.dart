// =============================================
// Auth Provider - Manages authentication state
// =============================================

import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../utils/api_client.dart';

enum AuthStatus { initial, authenticated, unauthenticated, loading }

class AuthProvider extends ChangeNotifier {
  final ApiClient _apiClient;
  AuthStatus _status = AuthStatus.initial;
  AureaUser? _user;
  String? _errorMessage;

  AuthProvider(this._apiClient);

  AuthStatus get status => _status;
  AureaUser? get user => _user;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _status == AuthStatus.authenticated;

  Future<bool> login(String username, String password) async {
    _status = AuthStatus.loading;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _apiClient.login(username, password);

      if (response['mfaRequired'] == true) {
        _status = AuthStatus.unauthenticated;
        _errorMessage = 'MFA required';
        notifyListeners();
        return false;
      }

      // Save tokens
      final accessToken = response['accessToken'] as String;
      final refreshToken = response['refreshToken'] as String;
      // Tokens are already saved in ApiClient

      // Load profile
      _user = AureaUser.fromJson(response['user'] as Map<String, dynamic>);
      _status = AuthStatus.authenticated;
      notifyListeners();
      return true;
    } catch (e) {
      _status = AuthStatus.unauthenticated;
      _errorMessage = e.toString();
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _apiClient.logout();
    _user = null;
    _status = AuthStatus.unauthenticated;
    notifyListeners();
  }

  Future<void> checkAuthStatus() async {
    // Check if we have a valid token
    try {
      final profile = await _apiClient.getProfile();
      _user = AureaUser.fromJson(profile);
      _status = AuthStatus.authenticated;
    } catch (e) {
      _status = AuthStatus.unauthenticated;
    }
    notifyListeners();
  }
}
