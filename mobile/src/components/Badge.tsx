import { Text, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Badge({ label, tone = "neutral" }: { label: string; tone?: "neutral" | "success" | "warning" | "danger" }) {
  const { theme } = useThemeCtx();
  const color = tone === "success" ? theme.colors.success : tone === "warning" ? theme.colors.warning : tone === "danger" ? theme.colors.danger : theme.colors.secondary;
  return <View style={{ backgroundColor: `${color}20`, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999 }}><Text style={{ color, fontWeight: "700", fontSize: 12 }}>{label}</Text></View>;
}
