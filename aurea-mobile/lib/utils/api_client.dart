// =============================================
// AUREA API Client
// Dio-based HTTP client with auth interceptor
// =============================================

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  static const String _baseUrl = 'https://api.aurea.bankxyz.co.id';
  // For development:
  // static const String _baseUrl = 'http://localhost:8080';

  static const String _accessTokenKey = 'aurea_access_token';
  static const String _refreshTokenKey = 'aurea_refresh_token';

  final Dio _dio;
  final FlutterSecureStorage _storage;

  ApiClient({Dio? dio, FlutterSecureStorage? storage})
      : _dio = dio ??
            Dio(BaseOptions(
              baseUrl: _baseUrl,
              connectTimeout: const Duration(seconds: 30),
              receiveTimeout: const Duration(seconds: 30),
              sendTimeout: const Duration(seconds: 30),
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Client': 'AUREA-Mobile/1.0.0',
              },
            )),
        _storage = storage ?? const FlutterSecureStorage() {
    _setupInterceptors();
  }

  void _setupInterceptors() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Attach access token
        final token = await _storage.read(key: _accessTokenKey);
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (error, handler) async {
        // Handle 401 - try refresh
        if (error.response?.statusCode == 401) {
          final refreshed = await _refreshToken();
          if (refreshed) {
            // Retry original request
            final response = await _dio.fetch(error.requestOptions);
            return handler.resolve(response);
          }
        }
        return handler.next(error);
      },
    ));
  }

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await _storage.read(key: _refreshTokenKey);
      if (refreshToken == null) return false;

      final response = await _dio.post('/auth/refresh', data: {
        'refreshToken': refreshToken,
      });

      if (response.statusCode == 200) {
        final newToken = response.data['accessToken'] as String;
        await _storage.write(key: _accessTokenKey, value: newToken);
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  // Auth
  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await _dio.post('/auth/login', data: {
      'username': username,
      'password': password,
    });
    return response.data as Map<String, dynamic>;
  }

  Future<void> logout() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }

  // Customers (Golden Customer)
  Future<List<dynamic>> getCustomers({int page = 0, int size = 20}) async {
    final response = await _dio.get('/api/customers', queryParameters: {
      'page': page,
      'size': size,
    });
    return response.data['content'] as List<dynamic>;
  }

  Future<Map<String, dynamic>> getCustomer(String cif) async {
    final response = await _dio.get('/api/customers/$cif');
    return response.data as Map<String, dynamic>;
  }

  // Accounts (Golden Account)
  Future<List<dynamic>> getAccountsByCif(String cif) async {
    final response = await _dio.get('/api/accounts', queryParameters: {
      'cif': cif,
    });
    return response.data['content'] as List<dynamic>;
  }

  // User profile
  Future<Map<String, dynamic>> getProfile() async {
    final response = await _dio.get('/api/users/me');
    return response.data as Map<String, dynamic>;
  }
}
