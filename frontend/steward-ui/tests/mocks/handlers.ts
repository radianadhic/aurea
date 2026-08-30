import { http, HttpResponse } from 'msw';
import type { Customer } from '~/types/customer';

const mockCustomers: Customer[] = [
  {
    id: 'cust-001',
    cifNumber: 'CIF-20260126-00045',
    customerType: 'INDIVIDUAL',
    fullName: 'Budi Santoso',
    dateOfBirth: '1985-04-12',
    placeOfBirth: 'Jakarta',
    gender: 'MALE',
    nationality: 'ID',
    maritalStatus: 'MARRIED',
    religion: 'ISLAM',
    occupation: 'Engineer',
    monthlyIncome: 15_000_000,
    kycStatus: 'APPROVED',
    kycExpiryDate: '2027-01-26',
    riskProfile: 'LOW',
    pepStatus: false,
    cifStatus: 'ACTIVE',
    branchId: 'JKT-001',
    tags: ['VIP'],
    createdAt: '2026-01-15T08:00:00Z',
    updatedAt: '2026-01-26T05:30:00Z',
    version: 3,
  },
  {
    id: 'cust-002',
    cifNumber: 'CIF-20260125-00198',
    customerType: 'INDIVIDUAL',
    fullName: 'Siti Aminah',
    dateOfBirth: '1990-08-23',
    placeOfBirth: 'Bandung',
    gender: 'FEMALE',
    nationality: 'ID',
    maritalStatus: 'SINGLE',
    religion: 'ISLAM',
    occupation: 'Doctor',
    monthlyIncome: 25_000_000,
    kycStatus: 'PENDING',
    riskProfile: 'MEDIUM',
    pepStatus: false,
    cifStatus: 'ACTIVE',
    branchId: 'BDG-001',
    createdAt: '2026-01-20T08:00:00Z',
    updatedAt: '2026-01-25T10:30:00Z',
    version: 2,
  },
];

export const handlers = [
  // Login
  http.post('*/api/v1/auth/login', async ({ request }) => {
    const body = await request.json() as any;
    if (body.username === 'admin' && body.password === 'admin') {
      return HttpResponse.json({
        accessToken: 'mock-access-token',
        refreshToken: 'mock-refresh-token',
        user: {
          id: '1',
          username: 'admin',
          email: 'admin@bankxyz.co.id',
          fullName: 'System Administrator',
          roles: ['SUPER_ADMIN'],
          permissions: ['*'],
        },
      });
    }
    return HttpResponse.json({ message: 'Invalid credentials' }, { status: 401 });
  }),

  // Get current user
  http.get('*/api/v1/auth/me', () => {
    return HttpResponse.json({
      id: '1',
      username: 'admin',
      email: 'admin@bankxyz.co.id',
      fullName: 'System Administrator',
      roles: ['SUPER_ADMIN'],
      permissions: ['*'],
    });
  }),

  // Customer search
  http.get('*/api/v1/customers/search', ({ request }) => {
    const url = new URL(request.url);
    const page = parseInt(url.searchParams.get('page') || '0');
    const size = parseInt(url.searchParams.get('size') || '20');
    const q = url.searchParams.get('q') || '';

    let filtered = mockCustomers;
    if (q) {
      filtered = mockCustomers.filter(
        (c) =>
          c.fullName?.toLowerCase().includes(q.toLowerCase()) ||
          c.cifNumber.includes(q)
      );
    }

    return HttpResponse.json({
      content: filtered,
      page,
      size,
      totalElements: filtered.length,
      totalPages: 1,
      first: true,
      last: true,
      numberOfElements: filtered.length,
      empty: filtered.length === 0,
    });
  }),

  // Get customer by ID
  http.get('*/api/v1/customers/:id', ({ params }) => {
    const customer = mockCustomers.find((c) => c.id === params.id);
    if (!customer) {
      return HttpResponse.json({ message: 'Not found' }, { status: 404 });
    }
    return HttpResponse.json(customer);
  }),

  // Create customer
  http.post('*/api/v1/customers', async ({ request }) => {
    const body = await request.json() as any;
    const newCustomer: Customer = {
      id: `cust-${Date.now()}`,
      cifNumber: `CIF-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${Math.floor(Math.random() * 10000).toString().padStart(5, '0')}`,
      customerType: body.customerType,
      fullName: body.fullName,
      kycStatus: 'PENDING',
      pepStatus: false,
      cifStatus: 'ACTIVE',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      version: 1,
      ...body,
    };
    return HttpResponse.json(newCustomer, { status: 201 });
  }),

  // Dashboard stats
  http.get('*/api/v1/dashboard/stats', () => {
    return HttpResponse.json({
      totalCustomers: 1_245_872,
      activeCustomers: 1_187_203,
      kycPending: 234,
      kycExpiring: 56,
      matchQueue: 89,
      matchAutoMerged: 23,
      exceptions: 12,
      exceptionsCritical: 3,
    });
  }),
];
