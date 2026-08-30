// =============================================
// AUREA Profile Screen
// =============================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../theme/aurea_theme.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final user = auth.user;

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              // Profile header
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: AureaColors.navyGradient,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    Container(
                      width: 80,
                      height: 80,
                      decoration: BoxDecoration(
                        gradient: AureaColors.goldGradient,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Center(
                        child: Text(
                          user?.initials ?? 'BS',
                          style: const TextStyle(
                            color: AureaColors.navy,
                            fontSize: 32,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      user?.fullName ?? 'Guest',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      user?.email ?? 'guest@aurea.app',
                      style: const TextStyle(
                        color: AureaColors.goldLight,
                        fontSize: 12,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AureaColors.gold,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        user?.role ?? 'Customer',
                        style: const TextStyle(
                          color: AureaColors.navy,
                          fontSize: 10,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Menu
              _buildMenuCard(context, [
                _MenuItem(
                  icon: Icons.person_outline,
                  title: 'Edit Profil',
                  onTap: () {},
                ),
                _MenuItem(
                  icon: Icons.lock_outline,
                  title: 'Keamanan & Biometrik',
                  trailing: Switch(
                    value: user?.biometricEnabled ?? false,
                    onChanged: (v) {},
                    activeColor: AureaColors.gold,
                  ),
                  onTap: () {},
                ),
                _MenuItem(
                  icon: Icons.notifications_outline,
                  title: 'Notifikasi',
                  onTap: () {},
                ),
                _MenuItem(
                  icon: Icons.language,
                  title: 'Bahasa',
                  subtitle: 'Bahasa Indonesia',
                  onTap: () {},
                ),
                _MenuItem(
                  icon: Icons.dark_mode_outlined,
                  title: 'Tema',
                  subtitle: 'Otomatis (Sistem)',
                  onTap: () {},
                ),
                _MenuItem(
                  icon: Icons.info_outline,
                  title: 'Tentang AUREA',
                  subtitle: 'Versi 1.0.0 • The Gold Standard',
                  onTap: () {},
                ),
              ]),

              const SizedBox(height: 16),

              // Logout
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: () {
                    auth.logout();
                  },
                  icon: const Icon(Icons.logout, size: 18),
                  label: const Text('Keluar'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AureaColors.error,
                    side: const BorderSide(color: AureaColors.error),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ),

              const SizedBox(height: 20),
              // Footer
              Text(
                'AUREA • Bank XYZ',
                style: TextStyle(
                  fontSize: 10,
                  color: AureaColors.textMuted,
                  letterSpacing: 2,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                'The Gold Standard of Data',
                style: TextStyle(
                  fontSize: 9,
                  color: AureaColors.goldDark,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1.5,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuCard(BuildContext context, List<_MenuItem> items) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AureaColors.gold.withValues(alpha: 0.15),
        ),
      ),
      child: Column(
        children: items.asMap().entries.map((entry) {
          final index = entry.key;
          final item = entry.value;
          return Column(
            children: [
              ListTile(
                leading: Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: AureaColors.gold.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(item.icon, color: AureaColors.goldDark, size: 18),
                ),
                title: Text(
                  item.title,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                subtitle: item.subtitle != null
                    ? Text(
                        item.subtitle!,
                        style: const TextStyle(
                          fontSize: 11,
                          color: AureaColors.textMuted,
                        ),
                      )
                    : null,
                trailing: item.trailing ??
                    const Icon(
                      Icons.chevron_right,
                      color: AureaColors.textMuted,
                    ),
                onTap: item.onTap,
              ),
              if (index < items.length - 1)
                Divider(
                  height: 1,
                  indent: 64,
                  color: AureaColors.gold.withValues(alpha: 0.1),
                ),
            ],
          );
        }).toList(),
      ),
    );
  }
}

class _MenuItem {
  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? trailing;
  final VoidCallback onTap;

  _MenuItem({
    required this.icon,
    required this.title,
    this.subtitle,
    this.trailing,
    required this.onTap,
  });
}
