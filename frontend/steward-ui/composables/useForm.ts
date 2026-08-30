/**
 * useForm composable - VeeValidate-style form management.
 * Provides reactive form state, validation, submission, error handling.
 */
import { ref, reactive, computed, watch } from 'vue';

export type ValidationRule = (value: any, formData?: Record<string, any>) => true | string | Promise<true | string>;

export interface FieldOptions {
  initialValue?: any;
  rules?: ValidationRule[];
  validateOn?: 'change' | 'blur' | 'submit';
  label?: string;
}

export class FormValidator {
  private rules: ValidationRule[];

  constructor(rules: ValidationRule[] = []) {
    this.rules = rules;
  }

  async validate(value: any, formData?: Record<string, any>): Promise<true | string> {
    for (const rule of this.rules) {
      try {
        const result = await rule(value, formData);
        if (result !== true) return result;
      } catch (e: any) {
        return e.message || 'Validation error';
      }
    }
    return true;
  }
}

// Built-in validators
export const required = (message = 'Field ini wajib diisi'): ValidationRule =>
  (value) => (value !== null && value !== undefined && value !== '' ? true : message);

export const minLength = (min: number, message?: string): ValidationRule =>
  (value) => (value && value.length >= min ? true : message || `Minimal ${min} karakter`);

export const maxLength = (max: number, message?: string): ValidationRule =>
  (value) => (value && value.length <= max ? true : message || `Maksimal ${max} karakter`);

export const email = (message = 'Format email tidak valid'): ValidationRule =>
  (value) => {
    if (!value) return true;
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(value) ? true : message;
  };

export const numeric = (message = 'Harus berupa angka'): ValidationRule =>
  (value) => {
    if (!value) return true;
    return !isNaN(Number(value)) ? true : message;
  };

export const integer = (message = 'Harus berupa bilangan bulat'): ValidationRule =>
  (value) => {
    if (!value) return true;
    return Number.isInteger(Number(value)) ? true : message;
  };

export const min = (min: number, message?: string): ValidationRule =>
  (value) => (Number(value) >= min ? true : message || `Minimal ${min}`);

export const max = (max: number, message?: string): ValidationRule =>
  (value) => (Number(value) <= max ? true : message || `Maksimal ${max}`);

export const between = (min: number, max: number, message?: string): ValidationRule =>
  (value) => (Number(value) >= min && Number(value) <= max ? true : message || `Antara ${min} - ${max}`);

export const nik = (message = 'NIK harus 16 digit angka'): ValidationRule =>
  (value) => {
    if (!value) return true;
    return /^[0-9]{16}$/.test(value) ? true : message;
  };

export const phone = (message = 'Nomor telepon tidak valid'): ValidationRule =>
  (value) => {
    if (!value) return true;
    return /^(\+62|62|0)[0-9]{8,13}$/.test(value) ? true : message;
  };

export const match = (fieldName: string, message?: string): ValidationRule =>
  (value, formData) => {
    if (!formData) return true;
    return value === formData[fieldName] ? true : message || `Tidak cocok dengan ${fieldName}`;
  };

export const regex = (pattern: RegExp, message = 'Format tidak valid'): ValidationRule =>
  (value) => {
    if (!value) return true;
    return pattern.test(value) ? true : message;
  };

export const url = (message = 'URL tidak valid'): ValidationRule =>
  (value) => {
    if (!value) return true;
    try {
      new URL(value);
      return true;
    } catch {
      return message;
    }
  };

export interface UseFormOptions {
  initialValues?: Record<string, any>;
  validateOn?: 'change' | 'blur' | 'submit';
  onSubmit?: (values: Record<string, any>) => void | Promise<void>;
  onSuccess?: (values: Record<string, any>) => void;
  onError?: (errors: Record<string, string>) => void;
}

export function useForm(options: UseFormOptions = {}) {
  const values = reactive<Record<string, any>>({ ...(options.initialValues || {}) });
  const errors = reactive<Record<string, string>>({});
  const touched = reactive<Record<string, boolean>>({});
  const submitting = ref(false);
  const submitted = ref(false);
  const isDirty = computed(() => Object.keys(touched).length > 0);
  const isValid = computed(() => Object.keys(errors).length === 0);

  const fieldValidators: Record<string, FormValidator> = {};
  const validateOnMap: Record<string, 'change' | 'blur' | 'submit'> = {};

  function defineField(name: string, fieldOptions: FieldOptions = {}) {
    if (fieldOptions.initialValue !== undefined && values[name] === undefined) {
      values[name] = fieldOptions.initialValue;
    }
    if (fieldOptions.rules) {
      fieldValidators[name] = new FormValidator(fieldOptions.rules);
    }
    validateOnMap[name] = fieldOptions.validateOn || options.validateOn || 'submit';

    // Watch for value changes to auto-validate
    watch(
      () => values[name],
      async () => {
        if (validateOnMap[name] === 'change' || (touched[name] && validateOnMap[name] === 'blur')) {
          await validateField(name);
        }
      }
    );

    return {
      name,
      value: computed(() => values[name]),
      error: computed(() => errors[name] || ''),
      touched: computed(() => touched[name] || false),
      handleChange: (e: any) => {
        const newValue = e?.target?.value !== undefined ? e.target.value : e;
        values[name] = newValue;
        touched[name] = true;
      },
      handleBlur: () => {
        touched[name] = true;
        if (validateOnMap[name] === 'blur') {
          validateField(name);
        }
      },
    };
  }

  async function validateField(name: string): Promise<boolean> {
    const validator = fieldValidators[name];
    if (!validator) {
      delete errors[name];
      return true;
    }
    const result = await validator.validate(values[name], values);
    if (result === true) {
      delete errors[name];
      return true;
    } else {
      errors[name] = result;
      return false;
    }
  }

  async function validate(): Promise<boolean> {
    const fieldNames = Object.keys(fieldValidators);
    const results = await Promise.all(fieldNames.map((n) => validateField(n)));
    // Mark all as touched
    fieldNames.forEach((n) => (touched[n] = true));
    return results.every((r) => r);
  }

  function reset(values2?: Record<string, any>) {
    Object.keys(values).forEach((k) => delete values[k]);
    Object.keys(errors).forEach((k) => delete errors[k]);
    Object.keys(touched).forEach((k) => delete touched[k]);
    if (values2) {
      Object.assign(values, values2);
    } else if (options.initialValues) {
      Object.assign(values, options.initialValues);
    }
  }

  function setFieldValue(name: string, value: any) {
    values[name] = value;
  }

  function setFieldError(name: string, error: string) {
    errors[name] = error;
  }

  async function handleSubmit(e?: Event) {
    e?.preventDefault();
    submitted.value = true;
    submitting.value = true;

    try {
      const valid = await validate();
      if (!valid) {
        options.onError?.({ ...errors });
        return false;
      }
      if (options.onSubmit) {
        await options.onSubmit({ ...values });
      }
      options.onSuccess?.({ ...values });
      return true;
    } finally {
      submitting.value = false;
    }
  }

  return {
    values,
    errors,
    touched,
    submitting: computed(() => submitting.value),
    submitted: computed(() => submitted.value),
    isDirty,
    isValid,
    defineField,
    validate,
    validateField,
    reset,
    setFieldValue,
    setFieldError,
    handleSubmit,
  };
}
