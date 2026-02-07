import { Pressable, Text, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function ListItem({ title, subtitle, right, onPress }: { title: string; subtitle?: string; right?: string; onPress?: () => void }) {
  const { theme } = useThemeCtx();
  return <Pressable onPress={onPress} style={{ paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: theme.colors.border, flexDirection: "row", justifyContent: "space-between", gap: 12 }}><View style={{ flex: 1 }}><Text style={{ color: theme.colors.text, fontWeight: "700" }}>{title}</Text>{subtitle ? <Text style={{ color: theme.colors.muted }}>{subtitle}</Text> : null}</View>{right ? <Text style={{ color: theme.colors.secondary, fontWeight: "700" }}>{right}</Text> : null}</Pressable>;
}
