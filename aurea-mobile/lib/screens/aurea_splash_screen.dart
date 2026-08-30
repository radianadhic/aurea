// =============================================
// AUREA Splash Screen
// Auto-hides after 3.5s, click to skip
// =============================================

import 'dart:async';
import 'package:flutter/material.dart';
import '../theme/aurea_theme.dart';
import '../widgets/aurea_logo.dart';

class AureaSplashScreen extends StatefulWidget {
  final VoidCallback onComplete;
  final Duration duration;
  final bool showSkipHint;

  const AureaSplashScreen({
    super.key,
    required this.onComplete,
    this.duration = const Duration(milliseconds: 3500),
    this.showSkipHint = true,
  });

  @override
  State<AureaSplashScreen> createState() => _AureaSplashScreenState();
}

class _AureaSplashScreenState extends State<AureaSplashScreen>
    with TickerProviderStateMixin {
  late AnimationController _fadeController;
  late AnimationController _textController;
  late AnimationController _dividerController;
  late AnimationController _taglineController;
  late AnimationController _loaderController;
  late AnimationController _exitController;

  Timer? _autoHideTimer;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    )..forward();

    _textController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );

    _dividerController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _taglineController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );

    _loaderController = AnimationController(
      duration: const Duration(milliseconds: 1800),
      vsync: this,
    );

    _exitController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );

    // Stagger animations
    Future.delayed(const Duration(milliseconds: 600), () {
      if (mounted) _textController.forward();
    });
    Future.delayed(const Duration(milliseconds: 1200), () {
      if (mounted) _dividerController.forward();
    });
    Future.delayed(const Duration(milliseconds: 1500), () {
      if (mounted) _taglineController.forward();
    });
    Future.delayed(const Duration(milliseconds: 2000), () {
      if (mounted) _loaderController.repeat();
    });

    // Auto-hide
    _autoHideTimer = Timer(widget.duration, _complete);
  }

  void _complete() {
    if (!mounted) return;
    _exitController.forward().then((_) {
      widget.onComplete();
    });
  }

  @override
  void dispose() {
    _autoHideTimer?.cancel();
    _fadeController.dispose();
    _textController.dispose();
    _dividerController.dispose();
    _taglineController.dispose();
    _loaderController.dispose();
    _exitController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: Tween<double>(begin: 1.0, end: 0.0).animate(_exitController),
      child: GestureDetector(
        onTap: _complete,
        child: Container(
          width: double.infinity,
          height: double.infinity,
          decoration: const BoxDecoration(
            gradient: AureaColors.navyGradient,
          ),
          child: Stack(
            children: [
              // Floating particles
              ...List.generate(6, (i) => _buildParticle(i)),

              // Main content
              Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Logo mark
                    FadeTransition(
                      opacity: _fadeController,
                      child: AureaSplashLogo(size: 150),
                    ),

                    const SizedBox(height: 24),

                    // AUREA text
                    AnimatedBuilder(
                      animation: _textController,
                      builder: (context, child) {
                        return Opacity(
                          opacity: _textController.value,
                          child: ShaderMask(
                            shaderCallback: (bounds) =>
                                AureaColors.goldGradient.createShader(
                              Rect.fromLTWH(0, 0, bounds.width, bounds.height),
                            ),
                            child: const Text(
                              'AUREA',
                              style: TextStyle(
                                fontSize: 44,
                                fontFamily: 'Georgia',
                                fontWeight: FontWeight.w700,
                                color: Colors.white,
                                letterSpacing: 11,
                              ),
                            ),
                          ),
                        );
                      },
                    ),

                    const SizedBox(height: 12),

                    // Divider line
                    AnimatedBuilder(
                      animation: _dividerController,
                      builder: (context, child) {
                        return Container(
                          width: 280 * Curves.easeOutCubic.transform(
                              _dividerController.value),
                          height: 2,
                          decoration: const BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Colors.transparent,
                                AureaColors.gold,
                                Colors.transparent,
                              ],
                            ),
                          ),
                        );
                      },
                    ),

                    const SizedBox(height: 14),

                    // Tagline
                    FadeTransition(
                      opacity: _taglineController,
                      child: SlideTransition(
                        position: Tween<Offset>(
                          begin: const Offset(0, 0.2),
                          end: Offset.zero,
                        ).animate(_taglineController),
                        child: const Text(
                          'THE GOLD STANDARD OF DATA',
                          style: TextStyle(
                            fontSize: 11,
                            color: AureaColors.goldLight,
                            letterSpacing: 5,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ),

                    const SizedBox(height: 24),

                    // Loading bar
                    FadeTransition(
                      opacity: _loaderController,
                      child: AnimatedBuilder(
                        animation: _loaderController,
                        builder: (context, child) {
                          return Container(
                            width: 160,
                            height: 2,
                            decoration: BoxDecoration(
                              color: AureaColors.gold.withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(2),
                            ),
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(2),
                              child: Align(
                                alignment: Alignment.centerLeft,
                                child: FractionallySizedBox(
                                  widthFactor: 0.4,
                                  child: Container(
                                    decoration: const BoxDecoration(
                                      gradient: LinearGradient(
                                        colors: [
                                          Colors.transparent,
                                          AureaColors.gold,
                                          Colors.transparent,
                                        ],
                                      ),
                                    ),
                                    transform: Matrix4.translationValues(
                                      (_loaderController.value - 0.5) * 400,
                                      0,
                                      0,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    ),

                    const SizedBox(height: 60),

                    // Version
                    if (widget.showSkipHint)
                      AnimatedBuilder(
                        animation: _loaderController,
                        builder: (context, child) {
                          if (_loaderController.value < 0.5) {
                            return const SizedBox.shrink();
                          }
                          return const Text(
                            'Tap to skip',
                            style: TextStyle(
                              fontSize: 11,
                              color: AureaColors.navy200,
                              letterSpacing: 2,
                            ),
                          );
                        },
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildParticle(int index) {
    final positions = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85];
    final drifts = [30.0, -20.0, 40.0, -30.0, 25.0, -40.0];
    return Positioned(
      left: positions[index] * MediaQuery.of(context).size.width,
      bottom: -20,
      child: TweenAnimationBuilder<double>(
        duration: Duration(seconds: 6 + (index % 3)),
        tween: Tween(begin: 0, end: 1),
        builder: (context, t, child) {
          final y = -MediaQuery.of(context).size.height * t;
          final x = drifts[index] * t;
          return Transform.translate(
            offset: Offset(x, y),
            child: Opacity(
              opacity: t < 0.1 ? 0 : (t > 0.9 ? 1 - (t - 0.9) * 10 : 0.6),
              child: Container(
                width: 3,
                height: 3,
                decoration: const BoxDecoration(
                  color: AureaColors.gold,
                  shape: BoxShape.circle,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
