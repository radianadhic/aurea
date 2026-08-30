// =============================================
// AUREA Dashboard Screen
// =============================================

import 'package:flutter/material.dart';
import '../theme/aurea_theme.dart';
import '../widgets/aurea_logo.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          color: AureaColors.gold,
          onRefresh: () async {
            await Future.delayed(const Duration(seconds: 1));
          },
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Greeting
                _buildGreeting(context),
                const SizedBox(height: 20),

                // Hero card (Golden Data)
                _buildGoldenDataCard(context),
                const SizedBox(height: 20),

                // Quick stats
                const Text(
                  'QUICK STATS',
                  style: TextStyle(
                    fontSize: 11,
                    letterSpacing: 2,
                    fontWeight: FontWeight.w700,
                    color: AureaColors.textMuted,
                  ),
                ),
                const SizedBox(height: 12),
                _buildStatGrid(context),
                const SizedBox(height: 20),

                // Recent activity
                const Text(
                  'AKTIVITAS TERBARU',
                  style: TextStyle(
                    fontSize: 11,
                    letterSpacing: 2,
                    fontWeight: FontWeight.w700,
                    color: AureaColors.textMuted,
                  ),
                ),
                const SizedBox(height: 12),
                _buildActivityList(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildGreeting(BuildContext context) {
    return Row(
      children: [
        // AUREA mark
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: AureaColors.navy,
            borderRadius: BorderRadius.circular(8),
          ),
          child: const Padding(
            padding: EdgeInsets.all(6),
            child: AureaLogo(
              variant: AureaLogoVariant.mark,
              width: 28,
              height: 28,
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Selamat datang,',
                style: TextStyle(
                  fontSize: 12,
                  color: AureaColors.textSecondary,
                ),
              ),
              const SizedBox(height: 2),
              Row(
                children: [
                  ShaderMask(
                    shaderCallback: (bounds) =>
                        AureaColors.goldGradient.createShader(
                      Rect.fromLTWH(0, 0, bounds.width, bounds.height),
                    ),
                    child: const Text(
                      'Budi Santoso',
                      style: TextStyle(
                        fontSize: 18,
                        fontFamily: 'Georgia',
                        fontWeight: FontWeight.w700,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        IconButton(
          icon: const Icon(Icons.notifications_outlined),
          onPressed: () {},
        ),
      ],
    );
  }

  Widget _buildGoldenDataCard(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: AureaColors.navyGradient,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AureaColors.gold.withValues(alpha: 0.3),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(6),
                    decoration: BoxDecoration(
                      color: AureaColors.gold.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: const Icon(
                      Icons.star,
                      color: AureaColors.gold,
                      size: 14,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Text(
                    'GOLDEN CUSTOMER',
                    style: TextStyle(
                      fontSize: 10,
                      color: AureaColors.goldLight,
                      letterSpacing: 2,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: AureaColors.success,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Text(
                  'VERIFIED',
                  style: TextStyle(
                    fontSize: 9,
                    color: Colors.white,
                    letterSpacing: 1,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text(
            'VIP Customer',
            style: TextStyle(
              fontSize: 14,
              color: AureaColors.goldLight,
              letterSpacing: 1,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Budi Santoso',
            style: TextStyle(
              fontSize: 22,
              color: Colors.white,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'CIF: GC-2024-001847',
            style: TextStyle(
              fontSize: 12,
              color: AureaColors.navy100,
              fontFamily: 'monospace',
            ),
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'CLV',
                      style: TextStyle(
                        fontSize: 10,
                        color: AureaColors.navy200,
                        letterSpacing: 1.5,
                      ),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Rp 25.4M',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 1,
                height: 36,
                color: AureaColors.navy300,
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'TIER',
                      style: TextStyle(
                        fontSize: 10,
                        color: AureaColors.navy200,
                        letterSpacing: 1.5,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        const Icon(Icons.star, color: AureaColors.gold, size: 16),
                        const Icon(Icons.star, color: AureaColors.gold, size: 16),
                        const Icon(Icons.star, color: AureaColors.gold, size: 16),
                        const SizedBox(width: 2),
                        Text(
                          'GOLD',
                          style: TextStyle(
                            fontSize: 12,
                            color: AureaColors.goldLight,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 1,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatGrid(BuildContext context) {
    final stats = [
      {'label': 'TOTAL NASABAH', 'value': '1.24M', 'icon': Icons.people, 'color': AureaColors.gold},
      {'label': 'REKENING AKTIF', 'value': '892K', 'icon': Icons.account_balance, 'color': AureaColors.success},
      {'label': 'PRODUK', 'value': '1.4K', 'icon': Icons.inventory, 'color': AureaColors.info},
      {'label': 'CHURN RISK', 'value': '12K', 'icon': Icons.warning, 'color': AureaColors.warning},
    ];

    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 1.7,
      children: stats.map((s) {
        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: AureaColors.gold.withValues(alpha: 0.15),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.all(6),
                    decoration: BoxDecoration(
                      color: (s['color'] as Color).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Icon(s['icon'] as IconData, color: s['color'] as Color, size: 16),
                  ),
                  Icon(Icons.arrow_upward, color: AureaColors.success, size: 14),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    s['value'] as String,
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w700,
                      color: AureaColors.navy,
                    ),
                  ),
                  Text(
                    s['label'] as String,
                    style: const TextStyle(
                      fontSize: 9,
                      color: AureaColors.textMuted,
                      letterSpacing: 1.5,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildActivityList(BuildContext context) {
    final activities = [
      {
        'icon': Icons.add_circle_outline,
        'color': AureaColors.success,
        'title': 'Nasabah baru didaftarkan',
        'subtitle': 'Siti Wahyuni • 5 menit lalu',
      },
      {
        'icon': Icons.sync,
        'color': AureaColors.info,
        'title': 'Matching selesai',
        'subtitle': '12 records matched • 1 jam lalu',
      },
      {
        'icon': Icons.check_circle_outline,
        'color': AureaColors.gold,
        'title': 'KYC verified',
        'subtitle': 'Ahmad Rizki • 3 jam lalu',
      },
    ];

    return Column(
      children: activities.map((a) {
        return Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: AureaColors.gold.withValues(alpha: 0.1),
            ),
          ),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: (a['color'] as Color).withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(a['icon'] as IconData, color: a['color'] as Color, size: 18),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      a['title'] as String,
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AureaColors.navy,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      a['subtitle'] as String,
                      style: const TextStyle(
                        fontSize: 11,
                        color: AureaColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: AureaColors.textMuted, size: 20),
            ],
          ),
        );
      }).toList(),
    );
  }
}
