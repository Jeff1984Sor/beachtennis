import "react-native-gesture-handler";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { ActivityIndicator, View } from "react-native";

import { AuthProvider, useAuth } from "@/store/auth-store";
import { AppProviders } from "@/store/query-provider";
import { ToastProvider } from "@/store/toast-store";
import { ThemeProvider } from "@/theme/provider";

function RootNav() {
  const { loading, branding } = useAuth();
  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator />
      </View>
    );
  }

  return (
    <ThemeProvider branding={branding}>
      <StatusBar style="auto" />
      <Stack screenOptions={{ headerShown: false }} />
    </ThemeProvider>
  );
}

export default function Layout() {
  return (
    <AppProviders>
      <ToastProvider>
        <AuthProvider>
          <RootNav />
        </AuthProvider>
      </ToastProvider>
    </AppProviders>
  );
}
