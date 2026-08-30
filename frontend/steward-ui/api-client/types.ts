/**
 * Auto-generated TypeScript Types (sample)
 * This is a sample/sample of what `npm run generate:api` would produce
 * from the openapi.yaml spec. In real usage, the script regenerates this file.
 *
 * DO NOT EDIT MANUALLY.
 */

// ==================== Customer ====================

export type CustomerType = 'INDIVIDUAL' | 'CORPORATE' | 'SYRIAH';

export type KycStatus =
  | 'PENDING'
  | 'IN_REVIEW'
  | 'APPROVED'
  | 'REJECTED'
  | 'EXPIRED'
  | 'FAILED';

export type RiskProfile = 'LOW' | 'MEDIUM' | 'HIGH';

export type CustomerStatus =
  | 'ACTIVE'
  | 'DORMANT'
  | 'CLOSED'
  | 'BLACKLIST'
  | 'DECEASED'
  | 'SUSPENDED';

export interface Customer {
  id: string;
  cifNumber: string;
  customerType: CustomerType;
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: 'MALE' | 'FEMALE';
  nationality?: string;
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
  religion?: string;
  occupation?: string;
  monthlyIncome?: number;
  kycStatus: KycStatus;
  kycExpiryDate?: string;
  riskProfile?: RiskProfile;
  pepStatus: boolean;
  cifStatus: CustomerStatus;
  branchId?: string;
  tags?: string[];
  customFields?: Record<string, any>;
  createdAt: string;
  createdBy?: string;
  updatedAt: string;
  updatedBy?: string;
  version: number;
}

export interface CustomerCreateRequest {
  customerType: CustomerType;
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: 'MALE' | 'FEMALE';
  nationality?: string;
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
  religion?: string;
  occupation?: string;
  monthlyIncome?: number;
  branchId?: string;
  email?: string;
  mobilePhone?: string;
  customFields?: Record<string, any>;
  tags?: string[];
}

export interface CustomerUpdateRequest {
  fullName?: string;
  legalName?: string;
  dateOfBirth?: string;
  placeOfBirth?: string;
  gender?: 'MALE' | 'FEMALE';
  nationality?: string;
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
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

export interface CustomerSearchRequest {
  q?: string;
  cifStatus?: CustomerStatus;
  kycStatus?: KycStatus;
  riskProfile?: RiskProfile;
  branchId?: string;
  customerType?: CustomerType;
  dateOfBirthFrom?: string;
  dateOfBirthTo?: string;
  monthlyIncomeMin?: number;
  monthlyIncomeMax?: number;
  page?: number;
  size?: number;
  sortBy?: string;
  direction?: 'asc' | 'desc';
}

// ==================== Matching ====================

export type MatchType = 'EXACT' | 'FUZZY' | 'PHONETIC' | 'TRANSACTION';

export type MatchStatus =
  | 'PENDING'
  | 'IN_REVIEW'
  | 'AUTO_MERGED'
  | 'MANUALLY_MERGED'
  | 'REJECTED'
  | 'ESCALATED';

export interface MatchCandidate {
  id: string;
  customerId: string;
  cifNumber: string;
  fullName: string;
  dateOfBirth?: string;
  nik?: string;
  email?: string;
  mobilePhone?: string;
  address?: string;
  matchScore: number;
  matchedFields: string[];
  isPrimary: boolean;
  mergeSelected: boolean;
}

export interface MatchGroup {
  id: string;
  matchType: MatchType;
  matchScore: number;
  algorithm: string;
  status: MatchStatus;
  memberCount: number;
  reviewerId?: string;
  reviewerName?: string;
  reviewedAt?: string;
  resolutionNotes?: string;
  rejectionReason?: string;
  autoDetected: boolean;
  createdAt: string;
  updatedAt: string;
  candidates: MatchCandidate[];
}

export interface MergeRequest {
  primaryId: string;
  secondaryIds: string[];
  manual: boolean;
  notes?: string;
}

// ==================== KYC ====================

export interface KycDocument {
  id: string;
  type: 'KTP' | 'NPWP' | 'PASSPORT' | 'SELFIE' | 'SIGNATURE' | 'PROOF_OF_ADDRESS' | 'OTHER';
  fileName: string;
  fileSize: number;
  uploadedAt: string;
  verified: boolean;
  verifiedBy?: string;
  expiryDate?: string;
  url: string;
}

export interface KycCase {
  id: string;
  cifNumber: string;
  customerName: string;
  customerId: string;
  kycStatus: KycStatus;
  kycLevel: 'STANDARD' | 'ENHANCED' | 'SIMPLIFIED';
  riskScore: number;
  pepStatus: boolean;
  sanctionsStatus: 'CLEAR' | 'MATCH' | 'POTENTIAL_MATCH' | 'PENDING';
  documentCompleteness: number;
  daysSinceLastUpdate: number;
  assignedTo?: string;
  assignedToId?: string;
  submittedAt: string;
  reviewDeadline?: string;
  documents: KycDocument[];
  flags: string[];
}

export interface KycDecisionRequest {
  decision: 'APPROVE' | 'REJECT';
  notes?: string;
  kycLevel?: string;
  validUntil?: string;
  reason?: string;
}

// ==================== Audit ====================

export type AuditAction =
  | 'CUSTOMER_CREATE'
  | 'CUSTOMER_UPDATE'
  | 'CUSTOMER_DELETE'
  | 'CUSTOMER_VIEW'
  | 'KYC_APPROVE'
  | 'KYC_REJECT'
  | 'KYC_REVIEW'
  | 'MATCH_AUTO'
  | 'MATCH_MERGE'
  | 'MATCH_REJECT'
  | 'MATCH_ESCALATE'
  | 'BLACKLIST_ADD'
  | 'BLACKLIST_REMOVE'
  | 'CONFIG_CHANGE'
  | 'RULE_CHANGE'
  | 'PERMISSION_CHANGE'
  | 'LOGIN'
  | 'LOGOUT'
  | 'LOGIN_FAILED';

export type AuditResult = 'SUCCESS' | 'FAILURE' | 'PARTIAL_SUCCESS';

export interface AuditChange {
  field: string;
  oldValue: any;
  newValue: any;
}

export interface AuditEntry {
  id: string;
  timestamp: string;
  userId: string;
  username: string;
  userFullName?: string;
  userRole?: string;
  action: AuditAction;
  entity: string;
  entityId: string;
  ipAddress: string;
  userAgent: string;
  changes?: AuditChange[];
  metadata?: Record<string, any>;
  result: AuditResult;
  errorMessage?: string;
  sessionId?: string;
  correlationId?: string;
  sourceService?: string;
}

export interface AuditSearchRequest {
  userId?: string;
  username?: string;
  action?: AuditAction;
  entity?: string;
  entityId?: string;
  result?: AuditResult;
  fromDate?: string;
  toDate?: string;
  page?: number;
  size?: number;
}

// ==================== Auth ====================

export interface LoginRequest {
  username: string;
  password: string;
  mfaCode?: string;
}

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  user: {
    id: string;
    username: string;
    email: string;
    fullName: string;
    roles: string[];
    permissions: string[];
  };
  mfaRequired?: boolean;
  mfaMethod?: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  fullName: string;
  employeeId?: string;
  branchId?: string;
  branchName?: string;
  roles: string[];
  permissions: string[];
  avatarUrl?: string;
  lastLoginAt?: string;
}

// ==================== Common ====================

export interface ApiError {
  timestamp: string;
  status: number;
  error: string;
  message: string;
  path: string;
  traceId?: string;
  validationErrors?: Record<string, string>;
}

export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  first: boolean;
  last: boolean;
  numberOfElements: number;
  empty: boolean;
}
