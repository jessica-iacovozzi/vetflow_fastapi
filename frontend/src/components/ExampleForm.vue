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
      <label>{{ t('name') }}</label>
      <input name="name" type="text" />
      <span v-if="errors.name">{{ errors.name }}</span>
    </div>
    
    <div>
      <label>{{ t('age') }}</label>
      <input name="age" type="number" />
      <span v-if="errors.age">{{ errors.age }}</span>
    </div>
    
    <button type="submit">{{ t('submit') }}</button>
  </form>
</template>
