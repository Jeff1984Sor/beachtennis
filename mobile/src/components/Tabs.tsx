import { Pressable, ScrollView, Text, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Tabs({ items, value, onChange }: { items: { key: string; label: string }[]; value: string; onChange: (k: string) => void }) {
  const { theme } = useThemeCtx();
  return <ScrollView horizontal showsHorizontalScrollIndicator={false}><View style={{ flexDirection: "row", gap: 8 }}>{items.map((it) => <Pressable key={it.key} onPress={() => onChange(it.key)} style={{ backgroundColor: value === it.key ? theme.colors.primary : theme.colors.surface, borderColor: theme.colors.border, borderWidth: 1, paddingHorizontal: 14, paddingVertical: 8, borderRadius: 999 }}><Text style={{ color: value === it.key ? "#fff" : theme.colors.text, fontWeight: "700" }}>{it.label}</Text></Pressable>)}</View></ScrollView>;
}
