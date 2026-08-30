// =============================================
// Account Model - Golden Account (MD3G)
// =============================================

class Account {
  final String id;             // GA ID
  final String accountNumber;
  final String cif;            // Customer CIF
  final String productType;    // SAVINGS, CHECKING, LOAN, etc
  final String productName;    // Tabungan Emas, Deposito, etc
  final String currency;       // IDR, USD
  final double balance;
  final double availableBalance;
  final String status;         // ACTIVE, DORMANT, CLOSED
  final DateTime openedDate;
  final DateTime? closedDate;
  final String branchId;
  final double? interestRate;

  Account({
    required this.id,
    required this.accountNumber,
    required this.cif,
    required this.productType,
    required this.productName,
    this.currency = 'IDR',
    required this.balance,
    required this.availableBalance,
    this.status = 'ACTIVE',
    required this.openedDate,
    this.closedDate,
    required this.branchId,
    this.interestRate,
  });

  factory Account.fromJson(Map<String, dynamic> json) {
    return Account(
      id: json['id'] as String,
      accountNumber: json['accountNumber'] as String,
      cif: json['cif'] as String,
      productType: json['productType'] as String,
      productName: json['productName'] as String,
      currency: json['currency'] as String? ?? 'IDR',
      balance: (json['balance'] as num).toDouble(),
      availableBalance: (json['availableBalance'] as num).toDouble(),
      status: json['status'] as String? ?? 'ACTIVE',
      openedDate: DateTime.parse(json['openedDate'] as String),
      closedDate: json['closedDate'] != null
          ? DateTime.parse(json['closedDate'] as String)
          : null,
      branchId: json['branchId'] as String,
      interestRate: (json['interestRate'] as num?)?.toDouble(),
    );
  }
}
