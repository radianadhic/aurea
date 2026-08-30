// =============================================
// AUREA Customers Screen - Golden Customer list
// =============================================

import 'package:flutter/material.dart';
import '../models/customer.dart';
import '../theme/aurea_theme.dart';

class CustomersScreen extends StatelessWidget {
  const CustomersScreen({super.key});

  // Mock data
  static final List<Customer> _customers = [
    Customer(
      id: 'GC-2024-001',
      cif: '001847',
      fullName: 'Budi Santoso',
      nik: '3201234567890001',
      email: 'budi.santoso@email.com',
      phone: '+62 812-1234-5678',
      segment: 'VIP',
      tier: 'GOLD',
      clv: 25400000,
      kycStatus: 'VERIFIED',
      createdAt: DateTime(2020, 3, 15),
      updatedAt: DateTime(2026, 1, 20),
    ),
    Customer(
      id: 'GC-2024-002',
      cif: '001848',
      fullName: 'Siti Wahyuni',
      nik: '3201234567890002',
      email: 'siti.wahyuni@email.com',
      phone: '+62 813-2345-6789',
      segment: 'Mass Affluent',
      tier: 'GOLD',
      clv: 12800000,
      kycStatus: 'VERIFIED',
      createdAt: DateTime(2021, 7, 22),
      updatedAt: DateTime(2026, 1, 18),
    ),
    Customer(
      id: 'GC-2024-003',
      cif: '001849',
      fullName: 'Ahmad Rizki Pratama',
      nik: '3201234567890003',
      email: 'ahmad.rizki@email.com',
      phone: '+62 811-3456-7890',
      segment: 'Mass Market',
      tier: 'SILVER',
      clv: 3200000,
      kycStatus: 'PENDING',
      createdAt: DateTime(2023, 1, 10),
      updatedAt: DateTime(2026, 1, 22),
    ),
    Customer(
      id: 'GC-2024-004',
      cif: '001850',
      fullName: 'Dewi Lestari',
      nik: '3201234567890004',
      email: 'dewi.lestari@email.com',
      phone: '+62 815-4567-8901',
      segment: 'Senior',
      tier: 'GOLD',
      clv: 9500000,
      kycStatus: 'VERIFIED',
      createdAt: DateTime(2019, 5, 3),
      updatedAt: DateTime(2026, 1, 15),
    ),
    Customer(
      id: 'GC-2024-005',
      cif: '001851',
      fullName: 'Eko Susanto',
      nik: '3201234567890005',
      email: 'eko.susanto@email.com',
      phone: '+62 818-5678-9012',
      segment: 'Student',
      tier: 'BRONZE',
      clv: 850000,
      kycStatus: 'VERIFIED',
      createdAt: DateTime(2024, 9, 1),
      updatedAt: DateTime(2026, 1, 23),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'GOLDEN CUSTOMERS',
                    style: TextStyle(
                      fontSize: 11,
                      color: AureaColors.goldDark,
                      letterSpacing: 2,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Daftar Nasabah',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w700,
                          color: AureaColors.navy,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: AureaColors.gold.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          '${_customers.length} records',
                          style: const TextStyle(
                            fontSize: 11,
                            color: AureaColors.goldDark,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 1,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  // Search
                  TextField(
                    decoration: InputDecoration(
                      hintText: 'Cari CIF, nama, NIK...',
                      prefixIcon: const Icon(Icons.search, size: 20),
                      filled: true,
                      fillColor: Theme.of(context).cardColor,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide: BorderSide(
                          color: AureaColors.gold.withValues(alpha: 0.15),
                        ),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide: BorderSide(
                          color: AureaColors.gold.withValues(alpha: 0.15),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            // List
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _customers.length,
                itemBuilder: (context, index) {
                  final customer = _customers[index];
                  return _buildCustomerCard(context, customer);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCustomerCard(BuildContext context, Customer customer) {
    Color tierColor;
    switch (customer.tier) {
      case 'GOLD':
        tierColor = AureaColors.gold;
        break;
      case 'SILVER':
        tierColor = const Color(0xFF94A3B8);
        break;
      default:
        tierColor = const Color(0xFFA16207);
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AureaColors.gold.withValues(alpha: 0.15),
        ),
      ),
      child: Row(
        children: [
          // Avatar
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              gradient: AureaColors.goldGradient,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Center(
              child: Text(
                customer.initials,
                style: const TextStyle(
                  color: AureaColors.navy,
                  fontWeight: FontWeight.w700,
                  fontSize: 16,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          // Info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        customer.fullName,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: AureaColors.navy,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: tierColor.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        customer.tier,
                        style: TextStyle(
                          fontSize: 9,
                          color: tierColor,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  'CIF: ${customer.cif} • ${customer.segment}',
                  style: const TextStyle(
                    fontSize: 11,
                    color: AureaColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 6),
                Row(
                  children: [
                    Icon(
                      customer.kycStatus == 'VERIFIED'
                          ? Icons.verified
                          : Icons.pending,
                      size: 12,
                      color: customer.kycStatus == 'VERIFIED'
                          ? AureaColors.success
                          : AureaColors.warning,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      customer.kycStatus,
                      style: TextStyle(
                        fontSize: 10,
                        color: customer.kycStatus == 'VERIFIED'
                            ? AureaColors.success
                            : AureaColors.warning,
                        fontWeight: FontWeight.w600,
                        letterSpacing: 0.5,
                      ),
                    ),
                    const SizedBox(width: 12),
                    const Icon(Icons.star, size: 12, color: AureaColors.gold),
                    const SizedBox(width: 4),
                    Text(
                      'CLV: Rp ${(customer.clv / 1000000).toStringAsFixed(1)}M',
                      style: const TextStyle(
                        fontSize: 10,
                        color: AureaColors.goldDark,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
