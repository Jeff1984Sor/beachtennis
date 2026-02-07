import { TextInput, View, Text } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Input({ label, ...props }: any) {
  const { theme } = useThemeCtx();
  return (
    <View style={{ gap: 6 }}>
      <Text style={{ color: theme.colors.muted, fontWeight: "600" }}>{label}</Text>
      <TextInput
        placeholderTextColor={theme.colors.muted}
        {...props}
        style={{
          borderWidth: 1,
          borderColor: theme.colors.border,
          backgroundColor: theme.colors.surface,
          borderRadius: theme.radius.md,
          color: theme.colors.text,
          paddingHorizontal: 14,
          paddingVertical: 14,
          fontSize: 16
        }}
      />
    </View>
  );
}
