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
      <label for="fullname">{{ t('fullname') }}</label>
      <input name="fullname" type="text" />
      <span v-if="errors.fullname">{{ errors.fullname }}</span>
    </div>
    <div>
      <label for="email">{{ t('email') }}</label>
      <input name="email" type="email" />
      <span v-if="errors.email">{{ errors.email }}</span>
    </div>
    <div>
      <label for="preferredLanguage">{{ t('preferredLanguage') }}</label>
      <select name="preferredLanguage">
        <option value="en">English</option>
        <option value="fr">French</option>
      </select>
      <span v-if="errors.preferredLanguage">{{ errors.preferredLanguage }}</span>
    </div>
    <div>
      <label for="password">{{ t('password') }}</label>
      <input name="password" type="password" />
      <span v-if="errors.password">{{ errors.password }}</span>
    </div>
    <div>
      <label for="confirmPassword">{{ t('confirmPassword') }}</label>
      <input name="confirmPassword" type="password" />
      <span v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
    </div>
    <div>
        <label for="role">{{ t('role') }}</label>
        <select name="role">
            <option value="client">Client</option>
            <option value="vet">Veterinarian</option>
            <option value="tech">Technician</option>
            <option value="admin">Admin</option>
        </select>
        <span v-if="errors.role">{{ errors.role }}</span>
    </div>
    
    <button type="submit">{{ t('submit') }}</button>
  </form>
</template>
