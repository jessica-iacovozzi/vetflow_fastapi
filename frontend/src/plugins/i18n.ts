import { createI18n } from 'vue-i18n';

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: {
      welcome: 'Welcome to VetFlow',
      name: 'Pet Name',
      age: 'Age',
      submit: 'Submit',
      required: '{field} is required',
      minLength: '{field} must be at least {length} characters'
    },
    es: {
      welcome: 'Bienvenido a VetFlow',
      name: 'Nombre de la mascota',
      age: 'Edad',
      submit: 'Enviar',
      required: '{field} es requerido',
      minLength: '{field} debe tener al menos {length} caracteres'
    }
  }
});
