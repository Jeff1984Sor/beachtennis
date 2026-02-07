import { PropsWithChildren } from "react";
import { View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Card({ children }: PropsWithChildren) {
  const { theme } = useThemeCtx();
  return <View style={{ backgroundColor: theme.colors.surface, borderRadius: theme.radius.lg, borderWidth: 1, borderColor: theme.colors.border, padding: theme.spacing.lg, gap: theme.spacing.md }}>{children}</View>;
}
