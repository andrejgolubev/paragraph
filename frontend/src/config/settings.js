export const validationPreferences = {
  username: {
    minLength: 2,
    maxLength: 40,
    pattern: /^[a-zA-Zа-яА-ЯёЁ\s\.\-]+$/,
  },
  email: {
    pattern: /^\S+@\S+\.\S+$/,
  },
  password: {
    // pattern: /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
    minLength: 8,
  }
}