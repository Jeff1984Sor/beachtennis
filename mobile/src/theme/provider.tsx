import { createContext, PropsWithChildren, useContext } from "react";
import { Branding, useAppTheme } from "@/theme";

type ThemeCtx = { theme: ReturnType<typeof useAppTheme> };
const Ctx = createContext<ThemeCtx | null>(null);

export function ThemeProvider({ branding, children }: PropsWithChildren<{ branding?: Branding | null }>) {
  const theme = useAppTheme(branding);
  return <Ctx.Provider value={{ theme }}>{children}</Ctx.Provider>;
}

export function useThemeCtx() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useThemeCtx must be used inside ThemeProvider");
  return ctx;
}
