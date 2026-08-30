// =============================================
// AUREA Accounts Screen - Golden Account list
// =============================================

import 'package:flutter/material.dart';
import '../theme/aurea_theme.dart';
import '../widgets/aurea_logo.dart';

class AccountsScreen extends StatelessWidget {
  const AccountsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              const Text(
                'GOLDEN ACCOUNTS',
                style: TextStyle(
                  fontSize: 11,
                  color: AureaColors.goldDark,
                  letterSpacing: 2,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 4),
              const Text(
                'Rekening Saya',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w700,
                  color: AureaColors.navy,
                ),
              ),
              const SizedBox(height: 20),
              // Total balance card
              _buildTotalCard(),
              const SizedBox(height: 20),
              // Account list
              const Text(
                'DAFTAR REKENING',
                style: TextStyle(
                  fontSize: 11,
                  color: AureaColors.textMuted,
                  letterSpacing: 2,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 12),
              ..._buildAccountCards(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTotalCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: AureaColors.goldGradient,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AureaColors.gold.withValues(alpha: 0.4),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'TOTAL SALDO',
                style: TextStyle(
                  fontSize: 11,
                  color: AureaColors.navy,
                  letterSpacing: 2,
                  fontWeight: FontWeight.w700,
                ),
              ),
              Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: AureaColors.navy,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Icon(
                  Icons.account_balance_wallet,
                  color: AureaColors.gold,
                  size: 16,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          const Text(
            'Rp 47.350.000',
            style: TextStyle(
              fontSize: 32,
              color: AureaColors.navy,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Across 3 accounts • Updated 2 min ago',
            style: TextStyle(
              fontSize: 11,
              color: AureaColors.navy.withValues(alpha: 0.7),
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildAccountCards() {
    final accounts = [
      {
        'name': 'Tabungan Emas',
        'number': '001-847-001',
        'balance': 'Rp 25.450.000',
        'type': 'SAVINGS',
        'icon': Icons.savings,
      },
      {
        'name': 'Deposito Berjangka',
        'number': '001-847-002',
        'balance': 'Rp 15.000.000',
        'type': 'DEPOSIT',
        'icon': Icons.account_balance,
      },
      {
        'name': 'Tabungan Regular',
        'number': '001-847-003',
        'balance': 'Rp 6.900.000',
        'type': 'SAVINGS',
        'icon': Icons.savings_outlined,
      },
    ];

    return accounts.map((acc) {
      return Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: AureaColors.gold.withValues(alpha: 0.15),
          ),
        ),
        child: Row(
          children: [
            Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: AureaColors.navy,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(acc['icon'] as IconData, color: AureaColors.gold, size: 22),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    acc['name'] as String,
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: AureaColors.navy,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    '${acc['type']} • ${acc['number']}',
                    style: const TextStyle(
                      fontSize: 11,
                      color: AureaColors.textSecondary,
                      fontFamily: 'monospace',
                    ),
                  ),
                ],
              ),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  acc['balance'] as String,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: AureaColors.goldDark,
                  ),
                ),
                const SizedBox(height: 2),
                const Text(
                  'Available',
                  style: TextStyle(
                    fontSize: 9,
                    color: AureaColors.textMuted,
                    letterSpacing: 1,
                  ),
                ),
              ],
            ),
          ],
        ),
      );
    }).toList();
  }
}
