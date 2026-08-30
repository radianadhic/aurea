// =============================================
// User Model - AUREA Mobile User
// =============================================

class AureaUser {
  final String id;
  final String username;
  final String fullName;
  final String email;
  final String? phone;
  final String? avatarUrl;
  final List<String> roles;
  final String? branchId;
  final bool biometricEnabled;
  final String? cif;             // Own CIF if customer

  AureaUser({
    required this.id,
    required this.username,
    required this.fullName,
    required this.email,
    this.phone,
    this.avatarUrl,
    this.roles = const [],
    this.branchId,
    this.biometricEnabled = false,
    this.cif,
  });

  factory AureaUser.fromJson(Map<String, dynamic> json) {
    return AureaUser(
      id: json['id'] as String,
      username: json['username'] as String,
      fullName: json['fullName'] as String,
      email: json['email'] as String,
      phone: json['phone'] as String?,
      avatarUrl: json['avatarUrl'] as String?,
      roles: (json['roles'] as List?)?.map((e) => e.toString()).toList() ?? [],
      branchId: json['branchId'] as String?,
      biometricEnabled: json['biometricEnabled'] as bool? ?? false,
      cif: json['cif'] as String?,
    );
  }

  String get initials {
    final parts = fullName.trim().split(' ');
    if (parts.isEmpty) return '?';
    if (parts.length == 1) return parts[0].substring(0, 1).toUpperCase();
    return (parts[0].substring(0, 1) + parts[1].substring(0, 1)).toUpperCase();
  }

  String get role => roles.isNotEmpty ? roles.first : 'User';
}
