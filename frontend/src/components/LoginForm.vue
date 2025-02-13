<script setup lang="ts">
import { useForm } from 'vee-validate';
import { validationSchema } from '@/plugins/forms';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const { handleSubmit, errors } = useForm({
  validationSchema
});

const onSubmit = handleSubmit((values: any) => {
  console.log('Form submitted:', values);
});
</script>

<template>
  <form @submit="onSubmit">
    <div>
      <label>{{ t('email') }}</label>
      <input name="email" type="email" />
      <span v-if="errors.email">{{ errors.email }}</span>
    </div>
    
    <div>
      <label>{{ t('password') }}</label>
      <input name="password" type="password" />
      <span v-if="errors.password">{{ errors.password }}</span>
    </div>
    
    <button type="submit">{{ t('submit') }}</button>
  </form>
</template>
