import { View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function LoadingSkeleton({ height = 72 }: { height?: number }) {
  const { theme } = useThemeCtx();
  return <View style={{ height, borderRadius: 14, backgroundColor: `${theme.colors.border}70` }} />;
}
