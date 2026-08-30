/**
 * Customer (CIF) TypeScript types
 */

export type CustomerType = 'INDIVIDUAL' | 'CORPORATE' | 'SYARIAH';
export type Gender = 'MALE' | 'FEMALE';
export type MaritalStatus = 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
export type KycStatus = 'PENDING' | 'IN_REVIEW' | 'APPROVED' | 'REJECTED' | 'EXPIRED' | 'FAILED';
export type RiskProfile = 'LOW' | 'MEDIUM' | 'HIGH';
export type CustomerStatus = 'ACTIVE' | 'DORMANT' | 'CLOSED' | 'BLACKLIST' | 'DECEASED' | 'SUSPENDED';

export interface Customer {
  id: string;
  cifNumber: string;
  customerType: CustomerType;
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: Gender;
  nationality?: string;
  maritalStatus?: MaritalStatus;
  religion?: string;
  occupation?: string;
  monthlyIncome?: number;
  kycStatus: KycStatus;
  kycExpiryDate?: string;
  riskProfile?: RiskProfile;
  pepStatus: boolean;
  cifStatus: CustomerStatus;
  branchId?: string;
  regionCode?: string;
  tags?: string[];
  customFields?: Record<string, any>;
  createdAt: string;
  createdBy?: string;
  updatedAt: string;
  updatedBy?: string;
  version: number;
}

export interface CustomerSearchFilters {
  cifStatus?: CustomerStatus;
  kycStatus?: KycStatus;
  riskProfile?: RiskProfile;
  branchId?: string;
  customerType?: CustomerType;
  dateOfBirthFrom?: string;
  dateOfBirthTo?: string;
  monthlyIncomeMin?: number;
  monthlyIncomeMax?: number;
  [key: string]: any;
}

export interface CustomerCreatePayload {
  customerType: CustomerType;
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: Gender;
  nationality?: string;
  maritalStatus?: MaritalStatus;
  religion?: string;
  occupation?: string;
  monthlyIncome?: number;
  branchId?: string;
  email?: string;
  mobilePhone?: string;
  customFields?: Record<string, any>;
  tags?: string[];
}

export interface CustomerUpdatePayload {
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: Gender;
  nationality?: string;
  maritalStatus?: MaritalStatus;
  religion?: string;
  occupation?: string;
  monthlyIncome?: number;
  kycStatus?: KycStatus;
  kycExpiryDate?: string;
  riskProfile?: RiskProfile;
  pepStatus?: boolean;
  cifStatus?: CustomerStatus;
  branchId?: string;
  email?: string;
  mobilePhone?: string;
  customFields?: Record<string, any>;
  tags?: string[];
}

// Status badge color mapping
export const STATUS_BADGE_TYPES: Record<string, string> = {
  // Customer status
  ACTIVE: 'success',
  APPROVED: 'success',
  DORMANT: 'info',
  PENDING: 'warning',
  IN_REVIEW: 'warning',
  CLOSED: 'info',
  EXPIRED: 'info',
  REJECTED: 'danger',
  FAILED: 'danger',
  BLACKLIST: 'danger',
  DECEASED: 'info',
  SUSPENDED: 'warning',
  // Risk
  LOW: 'success',
  MEDIUM: 'warning',
  HIGH: 'danger',
};

// Constants for selects
export const CUSTOMER_TYPES: { value: CustomerType; label: string }[] = [
  { value: 'INDIVIDUAL', label: 'Individual' },
  { value: 'CORPORATE', label: 'Corporate' },
  { value: 'SYARIAH', label: 'Syariah' },
];

export const GENDERS: { value: Gender; label: string }[] = [
  { value: 'MALE', label: 'Laki-laki' },
  { value: 'FEMALE', label: 'Perempuan' },
];

export const MARITAL_STATUSES: { value: MaritalStatus; label: string }[] = [
  { value: 'SINGLE', label: 'Belum Menikah' },
  { value: 'MARRIED', label: 'Menikah' },
  { value: 'DIVORCED', label: 'Cerai' },
  { value: 'WIDOWED', label: 'Duda/Janda' },
];

export const RELIGIONS = [
  'ISLAM',
  'KRISTEN',
  'KATOLIK',
  'HINDU',
  'BUDDHA',
  'KONGHUCU',
  'LAINNYA',
];

export const KYC_STATUSES: { value: KycStatus; label: string; type: string }[] = [
  { value: 'PENDING', label: 'Pending', type: 'warning' },
  { value: 'IN_REVIEW', label: 'In Review', type: 'warning' },
  { value: 'APPROVED', label: 'Approved', type: 'success' },
  { value: 'REJECTED', label: 'Rejected', type: 'danger' },
  { value: 'EXPIRED', label: 'Expired', type: 'info' },
  { value: 'FAILED', label: 'Failed', type: 'danger' },
];

export const RISK_PROFILES: { value: RiskProfile; label: string; type: string }[] = [
  { value: 'LOW', label: 'Low Risk', type: 'success' },
  { value: 'MEDIUM', label: 'Medium Risk', type: 'warning' },
  { value: 'HIGH', label: 'High Risk', type: 'danger' },
];

export const CUSTOMER_STATUSES: { value: CustomerStatus; label: string; type: string }[] = [
  { value: 'ACTIVE', label: 'Active', type: 'success' },
  { value: 'DORMANT', label: 'Dormant', type: 'info' },
  { value: 'CLOSED', label: 'Closed', type: 'info' },
  { value: 'BLACKLIST', label: 'Blacklist', type: 'danger' },
  { value: 'DECEASED', label: 'Deceased', type: 'info' },
  { value: 'SUSPENDED', label: 'Suspended', type: 'warning' },
];
