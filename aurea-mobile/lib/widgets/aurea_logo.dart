// =============================================
// AUREA Logo Widget
// Renders the AUREA logo in 3 variants
// =============================================

import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../theme/aurea_theme.dart';

enum AureaLogoVariant { mark, horizontal, stacked }

class AureaLogo extends StatelessWidget {
  final AureaLogoVariant variant;
  final double? width;
  final double? height;
  final Color? tintColor;

  const AureaLogo({
    super.key,
    this.variant = AureaLogoVariant.mark,
    this.width,
    this.height,
    this.tintColor,
  });

  // Inline SVG for the AUREA mark (icon only)
  static const String _markSvg = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="#0A1929"/>
  <path d="M 100 30 L 165 170 L 140 170 L 125 138 L 75 138 L 60 170 L 35 170 Z" fill="url(#g)"/>
  <path d="M 83 122 L 117 122 L 110 105 L 90 105 Z" fill="#0A1929"/>
  <circle cx="70" cy="155" r="3" fill="#FFD764"/>
  <circle cx="100" cy="155" r="3" fill="#FFD764"/>
  <circle cx="130" cy="155" r="3" fill="#FFD764"/>
</svg>
''';

  // Inline SVG for AUREA wordmark with tagline
  static const String _stackedSvg = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
  </defs>
  <!-- Logo mark -->
  <g transform="translate(100, 30)">
    <circle cx="100" cy="100" r="95" fill="#0A1929"/>
    <path d="M 100 30 L 165 170 L 140 170 L 125 138 L 75 138 L 60 170 L 35 170 Z" fill="url(#g)"/>
    <path d="M 83 122 L 117 122 L 110 105 L 90 105 Z" fill="#0A1929"/>
    <circle cx="70" cy="155" r="3" fill="#FFD764"/>
    <circle cx="100" cy="155" r="3" fill="#FFD764"/>
    <circle cx="130" cy="155" r="3" fill="#FFD764"/>
  </g>
  <!-- AUREA text -->
  <text x="200" y="320" text-anchor="middle" font-family="Georgia, serif"
        font-size="64" font-weight="700" fill="url(#g)" letter-spacing="10">AUREA</text>
  <!-- Divider -->
  <line x1="100" y1="345" x2="300" y2="345" stroke="#D4AF37" stroke-width="2"/>
  <!-- Tagline -->
  <text x="200" y="380" text-anchor="middle" font-family="Inter, sans-serif"
        font-size="14" fill="#0A1929" letter-spacing="6">THE GOLD STANDARD OF DATA</text>
</svg>
''';

  @override
  Widget build(BuildContext context) {
    switch (variant) {
      case AureaLogoVariant.mark:
        return SizedBox(
          width: width ?? 64,
          height: height ?? 64,
          child: SvgPicture.string(_markSvg),
        );

      case AureaLogoVariant.horizontal:
        // Render mark + text side by side using Row
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: (height ?? 48) * 1.0,
              height: height ?? 48,
              child: SvgPicture.string(_markSvg),
            ),
            const SizedBox(width: 12),
            Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ShaderMask(
                  shaderCallback: (bounds) => AureaColors.goldGradient.createShader(
                    Rect.fromLTWH(0, 0, bounds.width, bounds.height),
                  ),
                  child: Text(
                    'AUREA',
                    style: TextStyle(
                      fontSize: (height ?? 48) * 0.5,
                      fontFamily: 'Georgia',
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                      letterSpacing: 3,
                      height: 1.0,
                    ),
                  ),
                ),
                if (height == null || height! >= 40)
                  Text(
                    'THE GOLD STANDARD',
                    style: TextStyle(
                      fontSize: 9,
                      color: AureaColors.textMuted,
                      letterSpacing: 2,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
              ],
            ),
          ],
        );

      case AureaLogoVariant.stacked:
        return SizedBox(
          width: width ?? 200,
          height: height ?? 250,
          child: SvgPicture.string(_stackedSvg),
        );
    }
  }
}

/// AUREA Splash Logo (with pulse animation)
class AureaSplashLogo extends StatefulWidget {
  final double size;
  const AureaSplashLogo({super.key, this.size = 150});

  @override
  State<AureaSplashLogo> createState() => _AureaSplashLogoState();
}

class _AureaSplashLogoState extends State<AureaSplashLogo>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _pulseAnimation;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 2500),
      vsync: this,
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 0.6, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _scaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Cubic(0.34, 1.56, 0.64, 1),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Stack(
          alignment: Alignment.center,
          children: [
            // Pulsing glow
            Container(
              width: widget.size,
              height: widget.size,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: AureaColors.gold.withValues(
                      alpha: 0.3 * _pulseAnimation.value,
                    ),
                    blurRadius: 40 * _pulseAnimation.value,
                    spreadRadius: 10 * _pulseAnimation.value,
                  ),
                ],
              ),
            ),
            // Logo with scale-in
            Transform.scale(
              scale: _scaleAnimation.value,
              child: AureaLogo(
                variant: AureaLogoVariant.mark,
                width: widget.size,
                height: widget.size,
              ),
            ),
          ],
        );
      },
    );
  }
}
