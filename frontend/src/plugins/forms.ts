import { defineRule, configure } from 'vee-validate';
import { localize } from '@vee-validate/i18n';
import * as yup from 'yup';

defineRule('required', (value: string) => {
  return !!value?.trim() || '{field} is required';
});

defineRule('minLength', (value: string, [limit]: [number]) => {
  return value?.length >= limit || `{field} must be at least ${limit} characters`;
});

configure({
  generateMessage: localize({
    en: {
      messages: {
        required: 'This field is required',
      },
    },
    fr: {
      messages: {
        required: 'Ce champ est obligatoire',
      },
    },
  }),
});

export const validationSchema = yup.object({
  name: yup.string().required().min(2),
  age: yup.number().required().positive().integer()
});
