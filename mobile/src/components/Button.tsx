import { Pressable, Text, ActivityIndicator } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Button({ title, onPress, variant = "primary", loading = false }: { title: string; onPress: () => void; variant?: "primary" | "ghost"; loading?: boolean }) {
  const { theme } = useThemeCtx();
  return (
    <Pressable
      onPress={onPress}
      style={{
        backgroundColor: variant === "primary" ? theme.colors.primary : "transparent",
        borderColor: theme.colors.border,
        borderWidth: variant === "ghost" ? 1 : 0,
        borderRadius: theme.radius.md,
        paddingVertical: theme.spacing.md,
        paddingHorizontal: theme.spacing.lg,
        alignItems: "center"
      }}
    >
      {loading ? <ActivityIndicator color={variant === "primary" ? "#fff" : theme.colors.text} /> : <Text style={{ color: variant === "primary" ? "#fff" : theme.colors.text, fontWeight: "700" }}>{title}</Text>}
    </Pressable>
  );
}
