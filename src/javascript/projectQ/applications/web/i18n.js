import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import locale_de_DE from './locales/de-DE.json';


// Initialize the localization adapter
i18n
  .use( initReactI18next ) // passes i18n down to react-i18next
  .init({
    resources: {
      'de-DE': locale_de_DE,
    },
    lng: "de-DE",
    interpolation: {
      escapeValue: true
    },
    defaultNS: 'projectQ'
  });

export default i18n;

