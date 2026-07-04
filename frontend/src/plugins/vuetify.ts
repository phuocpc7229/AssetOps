import 'vuetify/styles'

import { createVuetify, type ThemeDefinition } from 'vuetify'

const assetOpsTheme: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#020713',
    surface: '#071528',
    primary: '#0a84ff',
    secondary: '#00d8ff',
    accent: '#126bff',
    error: '#ff4d5e',
    info: '#1e9bff',
    success: '#00d48a',
    warning: '#ff951a',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'assetOpsTheme',
    themes: {
      assetOpsTheme,
    },
  },
  defaults: {
    VBtn: {
      rounded: 'lg',
      height: 48,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
      color: 'secondary',
    },
  },
})
