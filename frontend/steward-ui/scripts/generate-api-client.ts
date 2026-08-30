/**
 * OpenAPI Client Generator
 *
 * Generates TypeScript types and API client methods from openapi.yaml spec.
 * Usage: npx tsx scripts/generate-api-client.ts [path-to-openapi.yaml]
 */
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

const OPENAPI_PATH = process.argv[2] || path.resolve(__dirname, '../../openapi.yaml');
const OUTPUT_DIR = path.resolve(__dirname, '../api-client');

interface OpenAPISpec {
  openapi: string;
  info: { title: string; version: string; description?: string };
  paths: Record<string, Record<string, OpenAPIOperation>>;
  components?: {
    schemas?: Record<string, any>;
    responses?: Record<string, any>;
    parameters?: Record<string, any>;
    securitySchemes?: Record<string, any>;
  };
}

interface OpenAPIOperation {
  summary?: string;
  description?: string;
  operationId?: string;
  tags?: string[];
  parameters?: OpenAPIParameter[];
  requestBody?: any;
  responses?: Record<string, any>;
  security?: any[];
  deprecated?: boolean;
}

interface OpenAPIParameter {
  name: string;
  in: 'query' | 'path' | 'header' | 'cookie';
  required?: boolean;
  description?: string;
  schema: any;
}

function resolveRef(ref: string, spec: OpenAPISpec): any {
  if (!ref.startsWith('#/')) return null;
  const parts = ref.substring(2).split('/');
  let result: any = spec;
  for (const part of parts) {
    result = result?.[part];
  }
  return result;
}

function getTypeNameFromRef(ref: string): string {
  if (!ref) return 'any';
  if (ref.startsWith('#/components/schemas/')) {
    return ref.substring('#/components/schemas/'.length);
  }
  return 'any';
}

function generateTsType(schema: any, spec: OpenAPISpec, required = false): string {
  if (!schema) return 'any';
  if (schema.$ref) {
    return getTypeNameFromRef(schema.$ref);
  }
  if (schema.enum) {
    return schema.enum.map((e: any) => JSON.stringify(e)).join(' | ');
  }
  if (schema.type === 'array') {
    return `${generateTsType(schema.items, spec)}[]`;
  }
  if (schema.type === 'object' || schema.properties) {
    return 'object'; // Will be defined as interface
  }
  if (schema.type === 'integer' || schema.type === 'number') {
    return 'number';
  }
  if (schema.type === 'boolean') {
    return 'boolean';
  }
  if (schema.type === 'string') {
    if (schema.format === 'date-time' || schema.format === 'date') return 'string';
    if (schema.format === 'uuid') return 'string';
    return 'string';
  }
  if (schema.oneOf) {
    return schema.oneOf.map((s: any) => generateTsType(s, spec)).join(' | ');
  }
  if (schema.allOf) {
    return schema.allOf.map((s: any) => generateTsType(s, spec)).join(' & ');
  }
  return 'any';
}

function generateInterface(name: string, schema: any, spec: OpenAPISpec): string {
  if (!schema || !schema.properties) {
    return `export type ${name} = ${generateTsType(schema || {}, spec)};\n`;
  }
  const requiredFields = new Set(schema.required || []);
  let result = `export interface ${name} {\n`;
  for (const [propName, propSchema] of Object.entries(schema.properties)) {
    const optional = requiredFields.has(propName) ? '' : '?';
    const tsType = generateTsType(propSchema as any, spec, requiredFields.has(propName));
    const description = (propSchema as any).description ? ` /** ${(propSchema as any).description} */\n  ` : '';
    result += `  ${description}${propName}${optional}: ${tsType};\n`;
  }
  if (schema.description) {
    result = `/**\n * ${schema.description}\n */\n` + result;
  }
  result += `}\n`;
  return result;
}

function generateClient(spec: OpenAPISpec): string {
  let client = `/**
 * Auto-generated API Client
 * From OpenAPI spec: ${spec.info.title} v${spec.info.version}
 * Generated on: ${new Date().toISOString()}
 *
 * DO NOT EDIT MANUALLY.
 */

import type { AxiosInstance } from 'axios';
import type { PageResponse } from './common';

`;

  // Group by tag
  const byTag: Record<string, Array<{ path: string; method: string; op: OpenAPIOperation }>> = {};
  for (const [path, methods] of Object.entries(spec.paths)) {
    for (const [method, op] of Object.entries(methods)) {
      if (['parameters', 'summary', 'description'].includes(method)) continue;
      const tag = op.tags?.[0] || 'default';
      if (!byTag[tag]) byTag[tag] = [];
      byTag[tag].push({ path, method: method.toUpperCase(), op });
    }
  }

  for (const [tag, operations] of Object.entries(byTag)) {
    const className = tag.replace(/[^a-zA-Z0-9]/g, '') + 'Service';
    client += `/**\n * ${tag} API\n */\nexport class ${className} {\n`;
    client += `  constructor(private api: AxiosInstance) {}\n\n`;

    for (const { path, method, op } of operations) {
      const opName = op.operationId || `${method.toLowerCase()}_${path.replace(/[^a-zA-Z0-9]/g, '_')}`;
      const params = op.parameters || [];
      const pathParams = params.filter((p) => p.in === 'path');
      const queryParams = params.filter((p) => p.in === 'query');
      const requestBody = op.requestBody?.content?.['application/json']?.schema;

      // Build function signature
      const pathArgs = pathParams.map((p) => `${p.name}: ${generateTsType(p.schema, spec)}`).join(', ');
      const queryArgs = queryParams.length > 0
        ? `params?: { ${queryParams.map((p) => `${p.name}${p.required ? '' : '?'}: ${generateTsType(p.schema, spec)}`).join('; ')} }`
        : '';
      const bodyArg = requestBody ? `data: ${generateTsType(requestBody, spec)}` : '';

      const allArgs = [pathArgs, queryArgs, bodyArg].filter(Boolean).join(', ');

      // Build response type
      const successResponse = op.responses?.['200'] || op.responses?.['201'] || op.responses?.['default'];
      const responseSchema = successResponse?.content?.['application/json']?.schema;
      const responseType = responseSchema ? generateTsType(responseSchema, spec) : 'void';

      // Replace path params
      let urlPath = path;
      for (const p of pathParams) {
        urlPath = urlPath.replace(`{${p.name}}`, `\${${p.name}}`);
      }

      client += `  /**\n   * ${op.summary || opName}\n`;
      if (op.description) {
        client += `   * ${op.description.split('\n').join('\n   * ')}\n`;
      }
      client += `   */\n`;
      client += `  async ${opName}(${allArgs}): Promise<${responseType}> {\n`;
      client += `    return this.api.${method.toLowerCase()}(\`${urlPath}\`${queryArgs ? ', params' : ''}${bodyArg ? ', data' : ''});\n`;
      client += `  }\n\n`;
    }

    client += `}\n\n`;
  }

  return client;
}

function generateTypes(spec: OpenAPISpec): string {
  let types = `/**
 * Auto-generated TypeScript Types
 * From OpenAPI spec: ${spec.info.title} v${spec.info.version}
 * Generated on: ${new Date().toISOString()}
 *
 * DO NOT EDIT MANUALLY.
 */

`;

  if (!spec.components?.schemas) {
    return types;
  }

  for (const [name, schema] of Object.entries(spec.components.schemas)) {
    types += generateInterface(name, schema, spec) + '\n';
  }

  return types;
}

function generateCommon(): string {
  return `/**
 * Common API types
 */

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

export interface ApiError {
  timestamp: string;
  status: number;
  error: string;
  message: string;
  path: string;
  traceId?: string;
  validationErrors?: Record<string, string>;
}

export interface SortObject {
  field: string;
  direction: 'asc' | 'desc';
}
`;
}

async function main() {
  console.log(`📂 Reading OpenAPI spec: ${OPENAPI_PATH}`);

  if (!fs.existsSync(OPENAPI_PATH)) {
    console.error(`❌ OpenAPI spec not found: ${OPENAPI_PATH}`);
    process.exit(1);
  }

  const content = fs.readFileSync(OPENAPI_PATH, 'utf8');
  const spec = yaml.load(content) as OpenAPISpec;

  if (!spec.openapi || !spec.paths) {
    console.error('❌ Invalid OpenAPI spec: missing openapi version or paths');
    process.exit(1);
  }

  console.log(`📊 OpenAPI ${spec.openapi} - ${spec.info.title} v${spec.info.version}`);
  console.log(`🛣️  Paths: ${Object.keys(spec.paths).length}`);
  console.log(`📦 Schemas: ${Object.keys(spec.components?.schemas || {}).length}`);

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  // Generate types
  const typesContent = generateTypes(spec);
  fs.writeFileSync(path.join(OUTPUT_DIR, 'types.ts'), typesContent);
  console.log(`✅ Generated types.ts (${typesContent.length} bytes)`);

  // Generate client
  const clientContent = generateClient(spec);
  fs.writeFileSync(path.join(OUTPUT_DIR, 'client.ts'), clientContent);
  console.log(`✅ Generated client.ts (${clientContent.length} bytes)`);

  // Generate common
  const commonContent = generateCommon();
  fs.writeFileSync(path.join(OUTPUT_DIR, 'common.ts'), commonContent);
  console.log(`✅ Generated common.ts (${commonContent.length} bytes)`);

  // Generate index
  const indexContent = `export * from './types';
export * from './common';
export * from './client';
`;
  fs.writeFileSync(path.join(OUTPUT_DIR, 'index.ts'), indexContent);
  console.log(`✅ Generated index.ts`);

  console.log(`\n🎉 API client generated successfully at: ${OUTPUT_DIR}`);
  console.log(`\nUsage:
  import { CustomerService, Customer } from '~/api-client';

  const customerService = new CustomerService(api);
  const customer: Customer = await customerService.getCustomer('123');
`);
}

main().catch((e) => {
  console.error('❌ Generation failed:', e);
  process.exit(1);
});
