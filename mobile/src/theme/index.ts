import { useColorScheme } from "react-native";

export type Role = "gestor" | "professor" | "aluno";

export type Branding = {
  nome_empresa: string;
  tema?: Record<string, string> | null;
  fonte?: string | null;
  logo_url?: string | null;
};

export type Theme = {
  colors: {
    bg: string;
    surface: string;
    text: string;
    muted: string;
    border: string;
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    danger: string;
  };
  spacing: { xs: number; sm: number; md: number; lg: number; xl: number };
  radius: { sm: number; md: number; lg: number; xl: number };
};

const lightBase: Theme = {
  colors: {
    bg: "#F4F8FB",
    surface: "#FFFFFF",
    text: "#0F172A",
    muted: "#475569",
    border: "#D8E2EC",
    primary: "#F97316",
    secondary: "#0F766E",
    success: "#16A34A",
    warning: "#D97706",
    danger: "#DC2626"
  },
  spacing: { xs: 4, sm: 8, md: 12, lg: 16, xl: 24 },
  radius: { sm: 8, md: 12, lg: 16, xl: 24 }
};

const darkBase: Theme = {
  ...lightBase,
  colors: {
    ...lightBase.colors,
    bg: "#071118",
    surface: "#0D1B24",
    text: "#E2E8F0",
    muted: "#94A3B8",
    border: "#1E3342"
  }
};

export function useAppTheme(branding?: Branding | null): Theme {
  const scheme = useColorScheme();
  const base = scheme === "dark" ? darkBase : lightBase;
  return {
    ...base,
    colors: {
      ...base.colors,
      primary: branding?.tema?.primary || base.colors.primary,
      secondary: branding?.tema?.secondary || base.colors.secondary
    }
  };
}
