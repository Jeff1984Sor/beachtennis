import { Text, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function EmptyState({ title, subtitle }: { title: string; subtitle: string }) {
  const { theme } = useThemeCtx();
  return <View style={{ padding: 24, alignItems: "center", gap: 6 }}><Text style={{ color: theme.colors.text, fontWeight: "800", fontSize: 17 }}>{title}</Text><Text style={{ color: theme.colors.muted, textAlign: "center" }}>{subtitle}</Text></View>;
}
