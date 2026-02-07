import { PropsWithChildren } from "react";
import { Modal as RNModal, Pressable, View } from "react-native";
import { useThemeCtx } from "@/theme/provider";

export function Modal({ open, onClose, children }: PropsWithChildren<{ open: boolean; onClose: () => void }>) {
  const { theme } = useThemeCtx();
  return <RNModal transparent visible={open} animationType="fade"><Pressable onPress={onClose} style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.25)", justifyContent: "center", padding: 20 }}><Pressable style={{ backgroundColor: theme.colors.surface, borderRadius: 16, padding: 16 }}>{children}</Pressable></Pressable></RNModal>;
}
