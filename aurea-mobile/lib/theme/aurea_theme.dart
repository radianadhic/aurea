// =============================================
// AUREA Theme - The Gold Standard of Data
// Brand colors & ThemeData for AUREA Mobile
// =============================================

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

/// AUREA brand color palette
class AureaColors {
  AureaColors._();

  // Gold (primary brand color)
  static const Color gold = Color(0xFFD4AF37);
  static const Color goldLight = Color(0xFFFFD764);
  static const Color goldDark = Color(0xFFB8860B);
  static const Color gold50 = Color(0xFFFFF9E6);
  static const Color gold100 = Color(0xFFFFF0BF);
  static const Color gold200 = Color(0xFFFFE599);

  // Navy (primary dark)
  static const Color navy = Color(0xFF0A1929);
  static const Color navyLight = Color(0xFF1A2F47);
  static const Color navy50 = Color(0xFFE6EBF2);
  static const Color navy100 = Color(0xFFB3C2D2);
  static const Color navy200 = Color(0xFF809AB3);
  static const Color navy300 = Color(0xFF4D7193);

  // Semantic colors
  static const Color success = Color(0xFF16A34A);
  static const Color warning = Color(0xFFEA580C);
  static const Color error = Color(0xFFDC2626);
  static const Color info = Color(0xFF0284C7);

  // Neutral
  static const Color white = Color(0xFFFFFFFF);
  static const Color background = Color(0xFFF8F9FA);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color border = Color(0xFFE5E7EB);
  static const Color textPrimary = Color(0xFF0A1929);
  static const Color textSecondary = Color(0xFF6B7280);
  static const Color textMuted = Color(0xFF9CA3AF);

  // Gradients
  static const LinearGradient goldGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [goldLight, gold, goldDark],
    stops: [0.0, 0.5, 1.0],
  );

  static const LinearGradient navyGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [navy, navyLight],
  );

  static const RadialGradient navyRadial = RadialGradient(
    center: Alignment.topCenter,
    radius: 1.5,
    colors: [navyLight, navy],
  );
}

/// AUREA Theme - Light & Dark
class AureaTheme {
  AureaTheme._();

  // === TEXT STYLES ===
  static TextTheme _buildTextTheme(Color textColor) {
    return GoogleFonts.interTextTheme().copyWith(
      // Brand display (AUREA wordmark)
      displayLarge: GoogleFonts.georgia(
        fontSize: 56,
        fontWeight: FontWeight.w700,
        letterSpacing: 12,
        color: textColor,
      ),
      displayMedium: GoogleFonts.georgia(
        fontSize: 44,
        fontWeight: FontWeight.w700,
        letterSpacing: 8,
        color: textColor,
      ),
      displaySmall: GoogleFonts.georgia(
        fontSize: 32,
        fontWeight: FontWeight.w700,
        letterSpacing: 4,
        color: textColor,
      ),
      // Headlines
      headlineLarge: GoogleFonts.inter(
        fontSize: 28,
        fontWeight: FontWeight.w700,
        color: textColor,
      ),
      headlineMedium: GoogleFonts.inter(
        fontSize: 24,
        fontWeight: FontWeight.w600,
        color: textColor,
      ),
      headlineSmall: GoogleFonts.inter(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        color: textColor,
      ),
      // Titles
      titleLarge: GoogleFonts.inter(
        fontSize: 18,
        fontWeight: FontWeight.w600,
        color: textColor,
      ),
      titleMedium: GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w500,
        color: textColor,
      ),
      titleSmall: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        color: textColor,
      ),
      // Body
      bodyLarge: GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        color: textColor,
      ),
      bodyMedium: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: textColor,
      ),
      bodySmall: GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.w400,
        color: AureaColors.textSecondary,
      ),
      // Labels
      labelLarge: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.5,
        color: textColor,
      ),
      labelMedium: GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        letterSpacing: 1,
        color: textColor,
      ),
      labelSmall: GoogleFonts.inter(
        fontSize: 10,
        fontWeight: FontWeight.w600,
        letterSpacing: 2,
        color: AureaColors.textMuted,
      ),
    );
  }

  // === LIGHT THEME ===
  static ThemeData get light {
    const ColorScheme colorScheme = ColorScheme.light(
      primary: AureaColors.gold,
      onPrimary: AureaColors.navy,
      primaryContainer: AureaColors.goldLight,
      onPrimaryContainer: AureaColors.navy,
      secondary: AureaColors.navy,
      onSecondary: AureaColors.gold,
      secondaryContainer: AureaColors.navyLight,
      onSecondaryContainer: AureaColors.goldLight,
      tertiary: AureaColors.goldDark,
      onTertiary: AureaColors.white,
      error: AureaColors.error,
      onError: AureaColors.white,
      surface: AureaColors.surface,
      onSurface: AureaColors.textPrimary,
      surfaceContainerHighest: AureaColors.background,
      onSurfaceVariant: AureaColors.textSecondary,
      outline: AureaColors.border,
      outlineVariant: AureaColors.gold100,
      shadow: Color(0x1A0A1929),
      scrim: Color(0x66000000),
      inverseSurface: AureaColors.navy,
      onInverseSurface: AureaColors.gold,
      inversePrimary: AureaColors.navy,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: AureaColors.background,
      textTheme: _buildTextTheme(AureaColors.textPrimary),
      primaryTextTheme: _buildTextTheme(AureaColors.navy),
      fontFamily: 'Inter',

      // AppBar
      appBarTheme: AppBarTheme(
        backgroundColor: AureaColors.white,
        foregroundColor: AureaColors.navy,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.inter(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AureaColors.navy,
        ),
        iconTheme: const IconThemeData(color: AureaColors.navy),
        systemOverlayStyle: const SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.dark,
        ),
      ),

      // Card
      cardTheme: CardThemeData(
        color: AureaColors.white,
        elevation: 0,
        shadowColor: AureaColors.navy.withValues(alpha: 0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(
            color: AureaColors.gold.withValues(alpha: 0.15),
            width: 1,
          ),
        ),
        margin: EdgeInsets.zero,
      ),

      // Elevated Button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AureaColors.gold,
          foregroundColor: AureaColors.navy,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          textStyle: GoogleFonts.inter(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),

      // Filled Button
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: AureaColors.gold,
          foregroundColor: AureaColors.navy,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),

      // Outlined Button
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AureaColors.goldDark,
          side: const BorderSide(color: AureaColors.gold, width: 1.5),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),

      // Text Button
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AureaColors.goldDark,
          textStyle: GoogleFonts.inter(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),

      // Input
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AureaColors.white,
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: AureaColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: AureaColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: AureaColors.gold, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: AureaColors.error),
        ),
        labelStyle: GoogleFonts.inter(
          fontSize: 14,
          color: AureaColors.textSecondary,
        ),
        hintStyle: GoogleFonts.inter(
          fontSize: 14,
          color: AureaColors.textMuted,
        ),
      ),

      // Divider
      dividerTheme: const DividerThemeData(
        color: AureaColors.border,
        thickness: 1,
        space: 1,
      ),

      // Bottom Navigation
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: AureaColors.white,
        selectedItemColor: AureaColors.gold,
        unselectedItemColor: AureaColors.textMuted,
        type: BottomNavigationBarType.fixed,
        elevation: 8,
        selectedLabelStyle: GoogleFonts.inter(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.5,
        ),
        unselectedLabelStyle: GoogleFonts.inter(
          fontSize: 11,
          fontWeight: FontWeight.w400,
        ),
      ),

      // Chip
      chipTheme: ChipThemeData(
        backgroundColor: AureaColors.gold.withValues(alpha: 0.1),
        labelStyle: GoogleFonts.inter(
          fontSize: 12,
          fontWeight: FontWeight.w500,
          color: AureaColors.goldDark,
        ),
        side: BorderSide(color: AureaColors.gold.withValues(alpha: 0.3)),
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),

      // Progress
      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: AureaColors.gold,
        linearTrackColor: AureaColors.gold50,
        circularTrackColor: AureaColors.gold50,
      ),

      // Slider
      sliderTheme: const SliderThemeData(
        activeTrackColor: AureaColors.gold,
        inactiveTrackColor: AureaColors.gold100,
        thumbColor: AureaColors.gold,
        overlayColor: Color(0x1AD4AF37),
      ),

      // Tab Bar
      tabBarTheme: TabBarThemeData(
        labelColor: AureaColors.navy,
        unselectedLabelColor: AureaColors.textMuted,
        indicatorColor: AureaColors.gold,
        indicatorSize: TabBarIndicatorSize.label,
        labelStyle: GoogleFonts.inter(
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
        unselectedLabelStyle: GoogleFonts.inter(
          fontSize: 14,
          fontWeight: FontWeight.w400,
        ),
      ),

      // Floating Action Button
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: AureaColors.gold,
        foregroundColor: AureaColors.navy,
        elevation: 4,
      ),

      // Switch
      switchTheme: SwitchThemeData(
        thumbColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) return AureaColors.gold;
          return AureaColors.textMuted;
        }),
        trackColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return AureaColors.gold.withValues(alpha: 0.4);
          }
          return AureaColors.border;
        }),
      ),

      // Dialog
      dialogTheme: DialogThemeData(
        backgroundColor: AureaColors.white,
        elevation: 8,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        titleTextStyle: GoogleFonts.inter(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AureaColors.navy,
        ),
      ),

      // Snackbar
      snackBarTheme: SnackBarThemeData(
        backgroundColor: AureaColors.navy,
        contentTextStyle: GoogleFonts.inter(
          fontSize: 14,
          color: AureaColors.white,
        ),
        actionTextColor: AureaColors.gold,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }

  // === DARK THEME ===
  static ThemeData get dark {
    const ColorScheme colorScheme = ColorScheme.dark(
      primary: AureaColors.gold,
      onPrimary: AureaColors.navy,
      primaryContainer: AureaColors.goldDark,
      onPrimaryContainer: AureaColors.goldLight,
      secondary: AureaColors.goldLight,
      onSecondary: AureaColors.navy,
      secondaryContainer: AureaColors.navyLight,
      onSecondaryContainer: AureaColors.gold,
      tertiary: AureaColors.gold,
      onTertiary: AureaColors.navy,
      error: AureaColors.error,
      onError: AureaColors.white,
      surface: AureaColors.navy,
      onSurface: AureaColors.white,
      surfaceContainerHighest: AureaColors.navyLight,
      onSurfaceVariant: AureaColors.navy200,
      outline: AureaColors.navy300,
      outlineVariant: AureaColors.navyLight,
      shadow: Color(0x33000000),
      scrim: Color(0xAA000000),
      inverseSurface: AureaColors.gold,
      onInverseSurface: AureaColors.navy,
      inversePrimary: AureaColors.gold,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: AureaColors.navy,
      textTheme: _buildTextTheme(AureaColors.white),
      primaryTextTheme: _buildTextTheme(AureaColors.gold),
      fontFamily: 'Inter',
      brightness: Brightness.dark,

      appBarTheme: AppBarTheme(
        backgroundColor: AureaColors.navy,
        foregroundColor: AureaColors.gold,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.inter(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AureaColors.white,
        ),
        iconTheme: const IconThemeData(color: AureaColors.gold),
        systemOverlayStyle: const SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.light,
        ),
      ),

      cardTheme: CardThemeData(
        color: AureaColors.navyLight,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(
            color: AureaColors.gold.withValues(alpha: 0.2),
            width: 1,
          ),
        ),
        margin: EdgeInsets.zero,
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AureaColors.gold,
          foregroundColor: AureaColors.navy,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          textStyle: GoogleFonts.inter(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AureaColors.navyLight,
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide(
              color: AureaColors.gold.withValues(alpha: 0.2)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide(
              color: AureaColors.gold.withValues(alpha: 0.2)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: AureaColors.gold, width: 2),
        ),
        labelStyle: GoogleFonts.inter(
          fontSize: 14,
          color: AureaColors.navy200,
        ),
      ),

      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: AureaColors.navy,
        selectedItemColor: AureaColors.gold,
        unselectedItemColor: AureaColors.navy200,
        type: BottomNavigationBarType.fixed,
        elevation: 8,
      ),

      dividerTheme: BorderSide(
        color: AureaColors.gold.withValues(alpha: 0.1),
        width: 1,
      ).toString().contains('1')
          ? const DividerThemeData(
              color: Color(0x1AFFD764),
              thickness: 1,
              space: 1,
            )
          : null,
    );
  }
}
