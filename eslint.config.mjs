import globals from "globals";
import pluginJs from "@eslint/js";
import { defineConfig } from "eslint/config";

/** @type {import('eslint').Linter.Config[]} */
export default defineConfig([
  pluginJs.configs.recommended,
  {
    languageOptions: {
      globals: { ...globals.node, ...globals.browser },
      ecmaVersion: 9,
      sourceType: "module",
      parserOptions: {
        ecmaFeatures: {
          globalReturn: true,
        },
      },
    },
  },
]);
