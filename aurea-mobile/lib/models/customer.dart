// =============================================
// Customer Model - Golden Customer (MD3G)
// =============================================

class Customer {
  final String id;             // GC ID
  final String cif;            // CIF number
  final String fullName;
  final String nik;            // National ID
  final String? email;
  final String? phone;
  final DateTime? dateOfBirth;
  final String? gender;        // M/F
  final String? address;
  final String segment;        // VIP, Mass Affluent, etc
  final String tier;           // GOLD, SILVER, BRONZE
  final double clv;            // Customer Lifetime Value
  final String? riskLevel;     // LOW, MEDIUM, HIGH
  final String kycStatus;      // VERIFIED, PENDING, REJECTED
  final DateTime createdAt;
  final DateTime updatedAt;

  Customer({
    required this.id,
    required this.cif,
    required this.fullName,
    required this.nik,
    this.email,
    this.phone,
    this.dateOfBirth,
    this.gender,
    this.address,
    required this.segment,
    this.tier = 'BRONZE',
    this.clv = 0,
    this.riskLevel,
    this.kycStatus = 'PENDING',
    required this.createdAt,
    required this.updatedAt,
  });

  factory Customer.fromJson(Map<String, dynamic> json) {
    return Customer(
      id: json['id'] as String,
      cif: json['cif'] as String,
      fullName: json['fullName'] as String,
      nik: json['nik'] as String,
      email: json['email'] as String?,
      phone: json['phone'] as String?,
      dateOfBirth: json['dateOfBirth'] != null
          ? DateTime.parse(json['dateOfBirth'] as String)
          : null,
      gender: json['gender'] as String?,
      address: json['address'] as String?,
      segment: json['segment'] as String? ?? 'Mass Market',
      tier: json['tier'] as String? ?? 'BRONZE',
      clv: (json['clv'] as num?)?.toDouble() ?? 0,
      riskLevel: json['riskLevel'] as String?,
      kycStatus: json['kycStatus'] as String? ?? 'PENDING',
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'cif': cif,
      'fullName': fullName,
      'nik': nik,
      'email': email,
      'phone': phone,
      'dateOfBirth': dateOfBirth?.toIso8601String(),
      'gender': gender,
      'address': address,
      'segment': segment,
      'tier': tier,
      'clv': clv,
      'riskLevel': riskLevel,
      'kycStatus': kycStatus,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  String get initials {
    final parts = fullName.trim().split(' ');
    if (parts.isEmpty) return '?';
    if (parts.length == 1) return parts[0].substring(0, 1).toUpperCase();
    return (parts[0].substring(0, 1) + parts[1].substring(0, 1)).toUpperCase();
  }
}
