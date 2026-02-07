import { PropsWithChildren } from "react";
import { Modal as RNModal, Pressable, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function BottomSheet({ open, onClose, children }: PropsWithChildren<{ open: boolean; onClose: () => void }>) {
  const { theme } = useThemeCtx();
  return <RNModal transparent visible={open} animationType="slide"><Pressable onPress={onClose} style={{ flex: 1, justifyContent: "flex-end", backgroundColor: "rgba(0,0,0,0.25)" }}><View style={{ backgroundColor: theme.colors.surface, padding: 16, borderTopLeftRadius: 20, borderTopRightRadius: 20 }}>{children}</View></Pressable></RNModal>;
}
