-- =============================================
-- MASTER DATA SEED - Indonesian Banking Context
-- =============================================
-- Generated: 26 Agustus 2026
-- Source: Standard Indonesian banking product catalog & branch hierarchy

-- =============================================
-- BRANCH SERVICE: Regions
-- =============================================
INSERT INTO branch_service.regions (id, code, name, regional_director) VALUES
('11111111-1111-1111-1111-111111111001', 'REG-JKT', 'Regional Jakarta', 'Bambang Suryadi'),
('11111111-1111-1111-1111-111111111002', 'REG-BDG', 'Regional Bandung', 'Suryanto Wijaya'),
('11111111-1111-1111-1111-111111111003', 'REG-SBY', 'Regional Surabaya', 'Hendra Kusuma'),
('11111111-1111-1111-1111-111111111004', 'REG-MDN', 'Regional Medan', 'Joko Santoso'),
('11111111-1111-1111-1111-111111111005', 'REG-SMG', 'Regional Semarang', 'Agus Prabowo'),
('11111111-1111-1111-1111-111111111006', 'REG-MKS', 'Regional Makassar', 'Andi Patorai'),
('11111111-1111-1111-1111-111111111007', 'REG-DPS', 'Regional Denpasar', 'I Wayan Sudirta'),
('11111111-1111-1111-1111-111111111008', 'REG-PLM', 'Regional Palembang', 'Yusuf Effendi');

-- =============================================
-- BRANCH SERVICE: Branches
-- =============================================
INSERT INTO branch_service.branches (id, code, name, type, region_id, address, city, province, postal_code, phone, active) VALUES
-- Jakarta (KCU = Kantor Cabang Utama, KCP = Kantor Cabang Pembantu)
('22222222-2222-2222-2222-222222222001', 'KCU-JKT-001', 'KCU Jakarta Sudirman', 'KCU', '11111111-1111-1111-1111-111111111001', 'Jl. Jend. Sudirman No. 1', 'Jakarta Pusat', 'DKI Jakarta', '10210', '+62-21-5700001', TRUE),
('22222222-2222-2222-2222-222222222002', 'KCU-JKT-002', 'KCU Jakarta Thamrin', 'KCU', '11111111-1111-1111-1111-111111111001', 'Jl. M.H. Thamrin No. 1', 'Jakarta Pusat', 'DKI Jakarta', '10310', '+62-21-5700002', TRUE),
('22222222-2222-2222-2222-222222222003', 'KCP-JKT-PDM-01', 'KCP Pondok Indah', 'KCP', '11111111-1111-1111-1111-111111111001', 'Jl. Pondok Indah No. 1', 'Jakarta Selatan', 'DKI Jakarta', '12310', '+62-21-5700010', TRUE),
('22222222-2222-2222-2222-222222222004', 'KCP-JKT-KBG-01', 'KCP Kebon Jeruk', 'KCP', '11111111-1111-1111-1111-111111111001', 'Jl. Kebon Jeruk No. 1', 'Jakarta Barat', 'DKI Jakarta', '11530', '+62-21-5700011', TRUE),
-- Bandung
('22222222-2222-2222-2222-222222222005', 'KCU-BDG-001', 'KCU Bandung Asia Afrika', 'KCU', '11111111-1111-1111-1111-111111111002', 'Jl. Asia Afrika No. 100', 'Bandung', 'Jawa Barat', '40111', '+62-22-5700001', TRUE),
('22222222-2222-2222-2222-222222222006', 'KCP-BDG-DGO-01', 'KCP Dago', 'KCP', '11111111-1111-1111-1111-111111111002', 'Jl. IR. H. Djuanda No. 1', 'Bandung', 'Jawa Barat', '40135', '+62-22-5700010', TRUE),
-- Surabaya
('22222222-2222-2222-2222-222222222007', 'KCU-SBY-001', 'KCU Surabaya Tunjungan', 'KCU', '11111111-1111-1111-1111-111111111003', 'Jl. Tunjungan No. 1', 'Surabaya', 'Jawa Timur', '60275', '+62-31-5700001', TRUE),
-- Medan
('22222222-2222-2222-2222-222222222008', 'KCU-MDN-001', 'KCU Medan Balai Kota', 'KCU', '11111111-1111-1111-1111-111111111004', 'Jl. Balai Kota No. 1', 'Medan', 'Sumatera Utara', '20112', '+62-61-5700001', TRUE),
-- Semarang
('22222222-2222-2222-2222-222222222009', 'KCU-SMG-001', 'KCU Semarang Pandanaran', 'KCU', '11111111-1111-1111-1111-111111111005', 'Jl. Pandanaran No. 1', 'Semarang', 'Jawa Tengah', '50134', '+62-24-5700001', TRUE),
-- Makassar
('22222222-2222-2222-2222-222222222010', 'KCU-MKS-001', 'KCU Makassar Pengayoman', 'KCU', '11111111-1111-1111-1111-111111111006', 'Jl. Pengayoman No. 1', 'Makassar', 'Sulawesi Selatan', '90114', '+62-411-570001', TRUE),
-- Denpasar
('22222222-2222-2222-2222-222222222011', 'KCU-DPS-001', 'KCU Denpasar Renon', 'KCU', '11111111-1111-1111-1111-111111111007', 'Jl. Raya Puputan No. 1', 'Denpasar', 'Bali', '80234', '+62-361-570001', TRUE),
-- Palembang
('22222222-2222-2222-2222-222222222012', 'KCU-PLM-001', 'KCU Palembang Sudirman', 'KCU', '11111111-1111-1111-1111-111111111008', 'Jl. Jend. Sudirman No. 1', 'Palembang', 'Sumatera Selatan', '30129', '+62-711-570001', TRUE);

-- =============================================
-- PRODUCT SERVICE: Product Categories
-- =============================================
INSERT INTO product_service.product_categories (id, code, name, description, active, display_order) VALUES
('33333333-3333-3333-3333-333333333001', 'SAVINGS', 'Tabungan', 'Rekening tabungan untuk nasabah perorangan dan korporasi', TRUE, 1),
('33333333-3333-3333-3333-333333333002', 'CURRENT', 'Giro', 'Rekening giro untuk transaksi bisnis', TRUE, 2),
('33333333-3333-3333-3333-333333333003', 'DEPOSIT', 'Deposito', 'Simpanan berjangka dengan bunga tetap', TRUE, 3),
('33333333-3333-3333-3333-333333333004', 'CREDIT_CARD', 'Kartu Kredit', 'Kartu kredit dengan berbagai benefit', TRUE, 4),
('33333333-3333-3333-3333-333333333005', 'LOAN', 'Kredit', 'Pinjaman dengan berbagai tujuan', TRUE, 5),
('33333333-3333-3333-3333-333333333006', 'MORTGAGE', 'KPR', 'Kredit Pemilikan Rumah', TRUE, 6),
('33333333-3333-3333-3333-333333333007', 'INVESTMENT', 'Investasi', 'Reksa dana, obligasi, dan produk investasi', TRUE, 7),
('33333333-3333-3333-3333-333333333008', 'INSURANCE', 'Asuransi', 'Asuransi jiwa dan umum', TRUE, 8),
('33333333-3333-3333-3333-333333333009', 'CURRENCY', 'Valas', 'Transaksi valuta asing', TRUE, 9);

-- =============================================
-- PRODUCT SERVICE: Products (Indonesian banking products)
-- =============================================
INSERT INTO product_service.products (id, code, name, description, category_id, product_type, currency, min_balance, min_age, max_age, risk_level, active) VALUES
-- Tabungan (Savings)
('44444444-4444-4444-4444-444444444001', 'TAB-BIASA', 'Tabungan Biasa', 'Tabungan reguler untuk nasabah umum', '33333333-3333-3333-3333-333333333001', 'SAVINGS', 'IDR', 50000, 17, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444002', 'TAB-PELAJAR', 'Tabungan Pelajar', 'Tabungan khusus pelajar (usia 12-25)', '33333333-3333-3333-3333-333333333001', 'SAVINGS', 'IDR', 10000, 12, 25, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444003', 'TAB-PLAN', 'Tabungan Rencana', 'Tabungan dengan target', '33333333-3333-3333-3333-333333333001', 'SAVINGS', 'IDR', 100000, 17, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444004', 'TAB-SYARIAH', 'Tabungan Syariah iB', 'Tabungan dengan prinsip syariah', '33333333-3333-3333-3333-333333333001', 'SAVINGS', 'IDR', 100000, 17, NULL, 'LOW', TRUE),
-- Giro
('44444444-4444-4444-4444-444444444005', 'GIRO-BISNIS', 'Giro Bisnis', 'Giro untuk badan usaha', '33333333-3333-3333-3333-333333333002', 'CURRENT_ACCOUNT', 'IDR', 1000000, NULL, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444006', 'GIRO-PEMERINTAH', 'Giro Pemerintah', 'Giro untuk instansi pemerintah', '33333333-3333-3333-3333-333333333002', 'CURRENT_ACCOUNT', 'IDR', 5000000, NULL, NULL, 'LOW', TRUE),
-- Deposito
('44444444-4444-4444-4444-444444444007', 'DEP-1BLN', 'Deposito 1 Bulan', 'Deposito jangka waktu 1 bulan', '33333333-3333-3333-3333-333333333003', 'TIME_DEPOSIT', 'IDR', 8000000, 17, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444008', 'DEP-3BLN', 'Deposito 3 Bulan', 'Deposito jangka waktu 3 bulan', '33333333-3333-3333-3333-333333333003', 'TIME_DEPOSIT', 'IDR', 8000000, 17, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444009', 'DEP-6BLN', 'Deposito 6 Bulan', 'Deposito jangka waktu 6 bulan', '33333333-3333-3333-3333-333333333003', 'TIME_DEPOSIT', 'IDR', 8000000, 17, NULL, 'LOW', TRUE),
('44444444-4444-4444-4444-444444444010', 'DEP-12BLN', 'Deposito 12 Bulan', 'Deposito jangka waktu 12 bulan', '33333333-3333-3333-3333-333333333003', 'TIME_DEPOSIT', 'IDR', 8000000, 17, NULL, 'LOW', TRUE),
-- Kartu Kredit
('44444444-4444-4444-4444-444444444011', 'CC-CLASSIC', 'Kartu Kredit Classic', 'Limit Rp 5-20 juta', '33333333-3333-3333-3333-333333333004', 'CREDIT_CARD', 'IDR', NULL, 21, 65, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444012', 'CC-GOLD', 'Kartu Kredit Gold', 'Limit Rp 20-50 juta', '33333333-3333-3333-3333-333333333004', 'CREDIT_CARD', 'IDR', NULL, 21, 65, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444013', 'CC-PLATINUM', 'Kartu Kredit Platinum', 'Limit Rp 50-200 juta', '33333333-3333-3333-3333-333333333004', 'CREDIT_CARD', 'IDR', NULL, 21, 70, 'MEDIUM', TRUE),
-- Kredit
('44444444-4444-4444-4444-444444444014', 'KRD-MULTIGUNA', 'Kredit Multiguna', 'Pinjaman untuk berbagai keperluan', '33333333-3333-3333-3333-333333333005', 'LOAN', 'IDR', NULL, 21, 65, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444015', 'KRD-PERUSAHAAN', 'Kredit Perusahaan', 'Pinjaman untuk badan usaha', '33333333-3333-3333-3333-333333333005', 'LOAN', 'IDR', NULL, NULL, NULL, 'MEDIUM', TRUE),
-- KPR
('44444444-4444-4444-4444-444444444016', 'KPR-PROPERTY', 'KPR Properti', 'Pinjaman untuk pembelian rumah', '33333333-3333-3333-3333-333333333006', 'MORTGAGE', 'IDR', NULL, 21, 65, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444017', 'KPR-REFI', 'KPR Refinancing', 'Pinjaman dengan agunan rumah', '33333333-3333-3333-3333-333333333006', 'MORTGAGE', 'IDR', NULL, 21, 70, 'MEDIUM', TRUE),
-- Investasi
('44444444-4444-4444-4444-444444444018', 'INV-REKSADANA', 'Reksa Dana', 'Reksa dana pasar uang, pendapatan tetap, saham', '33333333-3333-3333-3333-333333333007', 'INVESTMENT', 'IDR', 100000, 17, NULL, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444019', 'INV-OBLIGASI', 'Obligasi', 'Obligasi pemerintah dan korporasi', '33333333-3333-3333-3333-333333333007', 'INVESTMENT', 'IDR', 1000000, 17, NULL, 'LOW', TRUE),
-- Asuransi
('44444444-4444-4444-4444-444444444020', 'ASR-JIWA', 'Asuransi Jiwa', 'Asuransi jiwa dengan berbagai manfaat', '33333333-3333-3333-3333-333333333008', 'INSURANCE', 'IDR', NULL, 17, 65, 'LOW', TRUE),
-- Valas
('44444444-4444-4444-4444-444444444021', 'VAL-USD', 'USD Savings', 'Tabungan dalam USD', '33333333-3333-3333-3333-333333333009', 'CURRENCY', 'USD', 100, 17, NULL, 'MEDIUM', TRUE),
('44444444-4444-4444-4444-444444444022', 'VAL-EUR', 'EUR Savings', 'Tabungan dalam EUR', '33333333-3333-3333-3333-333333333009', 'CURRENCY', 'EUR', 100, 17, NULL, 'MEDIUM', TRUE);

-- =============================================
-- ADMIN SERVICE: Roles
-- =============================================
INSERT INTO admin_service.roles (id, code, name, description, is_system_role, active) VALUES
('55555555-5555-5555-5555-555555555001', 'SUPER_ADMIN', 'Super Administrator', 'Full system access (system role)', TRUE, TRUE),
('55555555-5555-5555-5555-555555555002', 'ADMIN', 'Administrator', 'System administration', TRUE, TRUE),
('55555555-5555-5555-5555-555555555003', 'STEWARD_CIF', 'CIF Steward', 'Manage customer data', TRUE, TRUE),
('55555555-5555-5555-5555-555555555004', 'STEWARD_PRODUCT', 'Product Steward', 'Manage product catalog', TRUE, TRUE),
('55555555-5555-5555-5555-555555555005', 'ANALYST', 'Data Analyst', 'View analytics & reports', TRUE, TRUE),
('55555555-5555-5555-5555-555555555006', 'EXECUTIVE', 'Executive', 'View executive dashboard', TRUE, TRUE),
('55555555-5555-5555-5555-555555555007', 'COMPLIANCE', 'Compliance Officer', 'Compliance & regulatory', TRUE, TRUE),
('55555555-5555-5555-5555-555555555008', 'AUDITOR', 'Auditor', 'Read-only audit access', TRUE, TRUE),
('55555555-5555-5555-5555-555555555009', 'BRANCH_MANAGER', 'Branch Manager', 'Branch-level approval', TRUE, TRUE);

-- =============================================
-- ADMIN SERVICE: Permissions (sample - 50 permissions)
-- =============================================
INSERT INTO admin_service.permissions (id, code, name, resource, action) VALUES
-- Customer permissions
('66666666-6666-6666-6666-666666666001', 'customer:read', 'View customer data', 'customer', 'read'),
('66666666-6666-6666-6666-666666666002', 'customer:write', 'Create/update customer', 'customer', 'write'),
('66666666-6666-6666-6666-666666666003', 'customer:delete', 'Delete customer', 'customer', 'delete'),
('66666666-6666-6666-6666-666666666004', 'customer:merge', 'Merge duplicate customers', 'customer', 'merge'),
('66666666-6666-6666-6666-666666666005', 'customer:blacklist', 'Blacklist customer', 'customer', 'blacklist'),
('66666666-6666-6666-6666-666666666006', 'customer:export', 'Export customer data', 'customer', 'export'),
('66666666-6666-6666-6666-666666666007', 'customer:kyc:approve', 'Approve KYC', 'customer', 'kyc_approve'),
-- Product permissions
('66666666-6666-6666-6666-666666666010', 'product:read', 'View products', 'product', 'read'),
('66666666-6666-6666-6666-666666666011', 'product:write', 'Create/update product', 'product', 'write'),
('66666666-6666-6666-6666-666666666012', 'product:delete', 'Delete product', 'product', 'delete'),
-- Branch permissions
('66666666-6666-6666-6666-666666666020', 'branch:read', 'View branches', 'branch', 'read'),
('66666666-6666-6666-6666-666666666021', 'branch:write', 'Create/update branch', 'branch', 'write'),
-- Audit permissions
('66666666-6666-6666-6666-666666666030', 'audit:read', 'View audit log', 'audit', 'read'),
('66666666-6666-6666-6666-666666666031', 'audit:export', 'Export audit log', 'audit', 'export'),
-- Workflow permissions
('66666666-6666-6666-6666-666666666040', 'workflow:read', 'View workflows', 'workflow', 'read'),
('66666666-6666-6666-6666-666666666041', 'workflow:write', 'Create/update workflow', 'workflow', 'write'),
('66666666-6666-6666-6666-666666666042', 'workflow:approve', 'Approve workflow task', 'workflow', 'approve'),
-- Report permissions
('66666666-6666-6666-6666-666666666050', 'report:read', 'View reports', 'report', 'read'),
('66666666-6666-6666-6666-666666666051', 'report:run', 'Run report', 'report', 'run'),
('66666666-6666-6666-6666-666666666052', 'report:export', 'Export report', 'report', 'export'),
-- ML permissions
('66666666-6666-6666-6666-666666666060', 'ml:predict', 'Run ML prediction', 'ml', 'predict'),
('66666666-6666-6666-6666-666666666061', 'ml:model:write', 'Manage ML models', 'ml', 'model_write'),
-- Notification permissions
('66666666-6666-6666-6666-666666666070', 'notification:send', 'Send notification', 'notification', 'send'),
('66666666-6666-6666-6666-666666666071', 'notification:template:write', 'Manage templates', 'notification', 'template_write'),
-- Admin permissions
('66666666-6666-6666-6666-666666666080', 'admin:user:read', 'View users', 'admin', 'user_read'),
('66666666-6666-6666-6666-666666666081', 'admin:user:write', 'Manage users', 'admin', 'user_write'),
('66666666-6666-6666-6666-666666666082', 'admin:role:read', 'View roles', 'admin', 'role_read'),
('66666666-6666-6666-6666-666666666083', 'admin:role:write', 'Manage roles', 'admin', 'role_write'),
('66666666-6666-6666-6666-666666666084', 'admin:config:write', 'Manage system config', 'admin', 'config_write'),
('66666666-6666-6666-6666-666666666085', 'admin:br:write', 'Manage business rules', 'admin', 'br_write');

-- =============================================
-- ADMIN SERVICE: Role-Permission mappings (sample)
-- =============================================
-- SUPER_ADMIN: all permissions
INSERT INTO admin_service.role_permissions (role_id, permission_id)
SELECT '55555555-5555-5555-5555-555555555001', id FROM admin_service.permissions;

-- STEWARD_CIF: customer permissions
INSERT INTO admin_service.role_permissions (role_id, permission_id) VALUES
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666001'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666002'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666004'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666007'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666020'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666030'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666040'),
('55555555-5555-5555-5555-555555555003', '66666666-6666-6666-6666-666666666042');

-- COMPLIANCE: audit + KYC approve
INSERT INTO admin_service.role_permissions (role_id, permission_id) VALUES
('55555555-5555-5555-5555-555555555007', '66666666-6666-6666-6666-666666666001'),
('55555555-5555-5555-5555-555555555007', '66666666-6666-6666-6666-666666666007'),
('55555555-5555-5555-5555-555555555007', '66666666-6666-6666-6666-666666666030'),
('55555555-5555-5555-5555-555555555007', '66666666-6666-6666-6666-666666666031'),
('55555555-5555-5555-5555-555555555007', '66666666-6666-6666-6666-666666666042');

-- AUDITOR: read-only audit
INSERT INTO admin_service.role_permissions (role_id, permission_id) VALUES
('55555555-5555-5555-5555-555555555008', '66666666-6666-6666-6666-666666666001'),
('55555555-5555-5555-5555-555555555008', '66666666-6666-6666-6666-666666666030'),
('55555555-5555-5555-5555-555555555008', '66666666-6666-6666-6666-666666666050');

-- ANALYST: report permissions
INSERT INTO admin_service.role_permissions (role_id, permission_id) VALUES
('55555555-5555-5555-5555-555555555005', '66666666-6666-6666-6666-666666666001'),
('55555555-5555-5555-5555-555555555005', '66666666-6666-6666-6666-666666666050'),
('55555555-5555-5555-5555-555555555005', '66666666-6666-6666-6666-666666666051'),
('55555555-5555-5555-5555-555555555005', '66666666-6666-6666-6666-666666666052');

-- EXECUTIVE: dashboard only
INSERT INTO admin_service.role_permissions (role_id, permission_id) VALUES
('55555555-5555-5555-5555-555555555006', '66666666-6666-6666-6666-666666666050');

-- =============================================
-- ADMIN SERVICE: Default Users
-- =============================================
-- Password = 'Admin@123' (BCrypt hash; will be reset on first login)
-- Note: In production, users are managed via Keycloak
INSERT INTO admin_service.users (id, username, email, full_name, branch_id, department, position, mfa_enabled, active, keycloak_user_id) VALUES
('77777777-7777-7777-7777-777777777001', 'admin', 'admin@bankxyz.co.id', 'System Administrator', 'KCU-JKT-001', 'IT', 'System Admin', TRUE, TRUE, 'kc-admin-001'),
('77777777-7777-7777-7777-777777777002', 'steward.budi', 'budi.setiawan@bankxyz.co.id', 'Budi Setiawan', 'KCU-JKT-001', 'Operations', 'CIF Steward', TRUE, TRUE, 'kc-steward-001'),
('77777777-7777-7777-7777-777777777003', 'steward.siti', 'siti.aminah@bankxyz.co.id', 'Siti Aminah', 'KCU-JKT-002', 'Operations', 'CIF Steward', FALSE, TRUE, 'kc-steward-002'),
('77777777-7777-7777-7777-777777777004', 'manager.jakarta', 'manager.jakarta@bankxyz.co.id', 'Andi Wijaya', 'KCU-JKT-001', 'Operations', 'Branch Manager', TRUE, TRUE, 'kc-manager-001'),
('77777777-7777-7777-7777-777777777005', 'compliance.eko', 'compliance@bankxyz.co.id', 'Eko Prabowo', 'KCU-JKT-001', 'Compliance', 'Compliance Officer', TRUE, TRUE, 'kc-compliance-001'),
('77777777-7777-7777-7777-777777777006', 'analyst.dewi', 'analyst@bankxyz.co.id', 'Dewi Lestari', 'KCU-JKT-001', 'Analytics', 'Data Analyst', FALSE, TRUE, 'kc-analyst-001'),
('77777777-7777-7777-7777-777777777007', 'auditor.rina', 'auditor@bankxyz.co.id', 'Rina Susanto', 'KCU-JKT-001', 'Internal Audit', 'Senior Auditor', TRUE, TRUE, 'kc-auditor-001'),
('77777777-7777-7777-7777-777777777008', 'executive.budi', 'executive@bankxyz.co.id', 'Budi Santoso', 'KCU-JKT-001', 'Executive', 'CEO', TRUE, TRUE, 'kc-exec-001');

-- User-Role mappings
INSERT INTO admin_service.user_roles (user_id, role_id, granted_by) VALUES
('77777777-7777-7777-7777-777777777001', '55555555-5555-5555-5555-555555555001', '77777777-7777-7777-7777-777777777001'), -- admin -> SUPER_ADMIN
('77777777-7777-7777-7777-777777777002', '55555555-5555-5555-5555-555555555003', '77777777-7777-7777-7777-777777777001'), -- steward.budi -> STEWARD_CIF
('77777777-7777-7777-7777-777777777003', '55555555-5555-5555-5555-555555555003', '77777777-7777-7777-7777-777777777001'), -- steward.siti -> STEWARD_CIF
('77777777-7777-7777-7777-777777777004', '55555555-5555-5555-5555-555555555009', '77777777-7777-7777-7777-777777777001'), -- manager -> BRANCH_MANAGER
('77777777-7777-7777-7777-777777777005', '55555555-5555-5555-5555-555555555007', '77777777-7777-7777-7777-777777777001'), -- compliance -> COMPLIANCE
('77777777-7777-7777-7777-777777777006', '55555555-5555-5555-5555-555555555005', '77777777-7777-7777-7777-777777777001'), -- analyst -> ANALYST
('77777777-7777-7777-7777-777777777007', '55555555-5555-5555-5555-555555555008', '77777777-7777-7777-7777-777777777001'), -- auditor -> AUDITOR
('77777777-7777-7777-7777-777777777008', '55555555-5555-5555-5555-555555555006', '77777777-7777-7777-7777-777777777001'); -- executive -> EXECUTIVE

-- =============================================
-- NOTIFICATION SERVICE: Default Templates (Bahasa Indonesia)
-- =============================================
INSERT INTO notification_service.notification_templates (id, name, code, channel, language, subject, body, variables, version, active, created_by) VALUES
('88888888-8888-8888-8888-888888888001', 'Welcome Email', 'WELCOME_EMAIL', 'EMAIL', 'id',
 'Selamat Datang di Bank XYZ - {{fullName}}',
 '<h1>Halo {{fullName}},</h1><p>Selamat datang di Bank XYZ. CIF Anda: <strong>{{cifNumber}}</strong></p><p>Anda sekarang dapat mengakses semua layanan perbankan kami.</p><p>Terima kasih telah memilih Bank XYZ.</p>',
 '["fullName", "cifNumber"]', 1, TRUE, '77777777-7777-7777-7777-777777777001'),

('88888888-8888-8888-8888-888888888002', 'KYC Reminder', 'KYC_REMINDER', 'EMAIL', 'id',
 'Pengingat KYC - {{fullName}}',
 '<p>Halo {{fullName}},</p><p>KYC Anda akan kadaluarsa pada <strong>{{expiryDate}}</strong>. Mohon perbarui dokumen KYC Anda.</p>',
 '["fullName", "expiryDate"]', 1, TRUE, '77777777-7777-7777-7777-777777777001'),

('88888888-8888-8888-8888-888888888003', 'KYC Reminder SMS', 'KYC_REMINDER_SMS', 'SMS', 'id',
 NULL,
 'Bank XYZ: KYC Anda ({{cifNumber}}) akan kadaluarsa {{expiryDate}}. Mohon perbarui di cabang terdekat.',
 '["cifNumber", "expiryDate"]', 1, TRUE, '77777777-7777-7777-7777-777777777001'),

('88888888-8888-8888-8888-888888888004', 'OTP SMS', 'OTP_SMS', 'SMS', 'id',
 NULL,
 'Bank XYZ: Kode OTP Anda adalah {{otpCode}}. Berlaku 5 menit. Jangan berikan ke siapapun.',
 '["otpCode"]', 1, TRUE, '77777777-7777-7777-7777-777777777001'),

('88888888-8888-8888-8888-888888888005', 'Transaction Alert', 'TXN_ALERT', 'SMS', 'id',
 NULL,
 'Bank XYZ: Transaksi {{txnType}} Rp{{amount}} di {{merchant}} pada {{dateTime}}. Saldo: Rp{{balance}}.',
 '["txnType", "amount", "merchant", "dateTime", "balance"]', 1, TRUE, '77777777-7777-7777-7777-777777777001'),

('88888888-8888-8888-8888-888888888006', 'Password Reset Email', 'PWD_RESET_EMAIL', 'EMAIL', 'id',
 'Reset Password Bank XYZ',
 '<p>Halo {{fullName}},</p><p>Klik link berikut untuk reset password Anda:</p><p><a href="{{resetLink}}">Reset Password</a></p><p>Link berlaku 1 jam.</p>',
 '["fullName", "resetLink"]', 1, TRUE, '77777777-7777-7777-7777-777777777001');

-- =============================================
-- BUSINESS RULES: Sample starter rules
-- =============================================
INSERT INTO admin_service.business_rules (id, name, code, description, rule_type, scope, condition_expression, action, error_message, priority, active, version, created_by) VALUES
('99999999-9999-9999-9999-999999999001', 'NIK must be 16 digits', 'NIK_LENGTH_CHECK', 'Validasi NIK harus 16 digit angka', 'VALIDATION', 'CUSTOMER.IDENTIFIER.NIK',
 'length(value) == 16 && regex(value, "^[0-9]{16}$")',
 'BLOCK', 'NIK harus 16 digit angka', 10, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999002', 'Email must be valid format', 'EMAIL_FORMAT_CHECK', 'Validasi format email', 'VALIDATION', 'CUSTOMER.CONTACT.EMAIL',
 'regex(value, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")',
 'BLOCK', 'Format email tidak valid', 20, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999003', 'Mobile phone must start with 08 or +62', 'PHONE_FORMAT_CHECK', 'Validasi nomor telepon Indonesia', 'VALIDATION', 'CUSTOMER.CONTACT.MOBILE',
 'regex(value, "^(\\+62|0)8[0-9]{8,11}$")',
 'BLOCK', 'Nomor HP harus format Indonesia (08xx atau +628xx)', 30, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999004', 'Age must be >= 17', 'MIN_AGE_CHECK', 'Nasabah minimal 17 tahun', 'VALIDATION', 'CUSTOMER.DATE_OF_BIRTH',
 'yearsBetween(value, today()) >= 17',
 'BLOCK', 'Usia minimal 17 tahun untuk menjadi nasabah', 5, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999005', 'High risk requires enhanced KYC', 'HIGH_RISK_KYC', 'Customer high-risk butuh enhanced KYC', 'ROUTING', 'CUSTOMER.RISK_PROFILE',
 'value == "HIGH"',
 'ROUTE', 'Customer dengan risk profile HIGH wajib menjalani enhanced KYC', 50, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999006', 'PEP requires compliance approval', 'PEP_APPROVAL', 'PEP butuh approval compliance', 'APPROVAL', 'CUSTOMER.PEP_STATUS',
 'value == true',
 'WARN', 'Customer PEP (Politically Exposed Person) memerlukan approval compliance officer', 60, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999007', 'CIF number auto-generate', 'CIF_AUTO_GEN', 'Auto-generate CIF number jika kosong', 'TRANSFORMATION', 'CUSTOMER.CIF_NUMBER',
 'isEmpty(value)',
 'TRANSFORM', 'CIF number akan di-generate otomatis dengan format CIF-YYYY-NNNNNNNN', 1, TRUE, 1, '77777777-7777-7777-7777-777777777001'),

('99999999-9999-9999-9999-999999999008', 'Blacklist check on save', 'BLACKLIST_CHECK', 'Cek blacklist sebelum save customer', 'VALIDATION', 'CUSTOMER.CIF_STATUS',
 'value == "BLACKLIST"',
 'WARN', 'Customer ini masuk blacklist - mohon konfirmasi', 100, TRUE, 1, '77777777-7777-7777-7777-777777777001');

-- =============================================
-- SYSTEM CONFIG: Default configurations
-- =============================================
INSERT INTO admin_service.system_config (config_key, config_value, description, is_sensitive, updated_by) VALUES
('mdm.cif.prefix', '"CIF"'::jsonb, 'CIF number prefix', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.cif.format', '"CIF-{{year}}-{{sequence:08d}}"'::jsonb, 'CIF number format', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.kyc.expiry.years', '5'::jsonb, 'KYC validity in years', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.kyc.enhanced.expiry.years', '2'::jsonb, 'Enhanced KYC validity in years (for HIGH risk)', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.audit.retention.years', '10'::jsonb, 'Audit log retention in years (UU PDP)', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.matching.threshold.default', '0.85'::jsonb, 'Default match score threshold', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.matching.threshold.auto.merge', '0.95'::jsonb, 'Threshold for auto-merge (no review needed)', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.session.timeout.minutes', '15'::jsonb, 'User session timeout', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.password.min.length', '12'::jsonb, 'Minimum password length', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.password.expiry.days', '90'::jsonb, 'Password expiry in days', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.login.max.attempts', '10'::jsonb, 'Max failed login attempts before lockout', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.login.lockout.minutes', '15'::jsonb, 'Account lockout duration', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.api.rate.limit.standard', '60'::jsonb, 'Standard rate limit (req/min)', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.api.rate.limit.admin', '300'::jsonb, 'Admin rate limit (req/min)', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.export.max.rows', '100000'::jsonb, 'Max rows per export', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.backup.retention.days', '90'::jsonb, 'Backup retention in days', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.feature.churn.enabled', 'true'::jsonb, 'Enable churn prediction feature', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.feature.credit.scoring.enabled', 'true'::jsonb, 'Enable credit scoring feature', FALSE, '77777777-7777-7777-7777-777777777001'),
('mdm.feature.fraud.detection.enabled', 'true'::jsonb, 'Enable fraud detection feature', FALSE, '77777777-7777-7777-7777-777777777001');

-- =============================================
-- Summary
-- =============================================
-- 8 regions
-- 12 branches (KCU + KCP)
-- 9 product categories
-- 22 products (savings, giro, deposits, CC, loans, KPR, investments, insurance, forex)
-- 9 roles
-- 30 permissions
-- 8 users (admin, 2 stewards, manager, compliance, analyst, auditor, executive)
-- 6 notification templates (Bahasa Indonesia)
-- 8 business rules
-- 19 system config
-- 1 customer (already in V1.0.1)
