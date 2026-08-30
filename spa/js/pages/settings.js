/**
 * AUREA SPA — Settings Page
 */

const SettingsPage = {
  route: 'settings',
  title: 'Settings',
  subtitle: 'User preferences and system configuration',

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">🔧 Settings</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
        </div>

        <div class="card" style="max-width: 600px;">
          <h2 style="font-size: 14px; font-weight: 700; margin-bottom: 16px;">🎨 Appearance</h2>
          <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border);">
            <div>
              <div style="font-weight: 600;">Theme</div>
              <div style="font-size: 12px; color: var(--text-muted);">Light or dark mode</div>
            </div>
            <button class="btn btn-secondary" id="themeBtn">${window.store.state.theme === 'dark' ? '☀️ Light' : '🌙 Dark'}</button>
          </div>
        </div>

        <div class="card" style="max-width: 600px; margin-top: 20px;">
          <h2 style="font-size: 14px; font-weight: 700; margin-bottom: 16px;">🔌 Connection</h2>
          <div style="display: grid; gap: 12px;">
            <div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">ML Service URL</div>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 13px; padding: 8px 12px; background: var(--gray-50); border-radius: 6px;">${window.api.baseURL}</div>
            </div>
            <div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">User</div>
              <div style="font-size: 13px; padding: 8px 12px; background: var(--gray-50); border-radius: 6px;">${window.store.state.user?.email || 'admin@aurea.id'}</div>
            </div>
          </div>
        </div>

        <div class="card" style="max-width: 600px; margin-top: 20px;">
          <h2 style="font-size: 14px; font-weight: 700; margin-bottom: 16px;">ℹ️ About</h2>
          <div style="font-size: 13px; color: var(--text-muted); line-height: 1.7;">
            <p><strong>AUREA Platform</strong> v1.0.0</p>
            <p>The Gold Standard of Data — A MDM platform with 4 built-in AI engines.</p>
            <p style="margin-top: 12px;">© 2026 AUREA · Made in Indonesia 🇮🇩</p>
          </div>
        </div>
      </div>
    `;

    document.getElementById('themeBtn').onclick = () => {
      window.store.toggleTheme();
      this.render(container);
      Components.toast(`Theme: ${window.store.state.theme}`, 'success');
    };
  },

  unmount() {}
};

window.SettingsPage = SettingsPage;
