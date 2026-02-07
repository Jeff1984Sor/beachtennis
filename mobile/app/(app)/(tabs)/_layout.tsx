import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { Redirect } from "expo-router";
import { Text, View } from "react-native";
import { useState } from "react";

import { useAuth } from "@/store/auth-store";
import { BottomSheet } from "@/components/BottomSheet";
import { Button } from "@/components/Button";

export default function TabsLayout() {
  const { me, activeRole, setActiveRole } = useAuth();
  const [open, setOpen] = useState(false);

  if (!me) return <Redirect href="/(auth)/login" />;

  const isGestor = activeRole === "gestor";
  const isAluno = activeRole === "aluno";

  return (
    <>
      <Tabs
        screenOptions={{
          headerStyle: { backgroundColor: "#0F172A" },
          headerTintColor: "#fff",
          tabBarActiveTintColor: "#F97316",
          headerRight: () => (
            <Text style={{ color: "#fff", marginRight: 14 }} onPress={() => setOpen(true)}>
              Trocar visão
            </Text>
          )
        }}
      >
        <Tabs.Screen name="agenda" options={{ title: isAluno ? "Minhas Aulas" : "Agenda", tabBarIcon: ({ color }) => <Ionicons name="calendar-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="alunos" options={{ href: isAluno ? null : "/(app)/(tabs)/alunos", title: "Alunos", tabBarIcon: ({ color }) => <Ionicons name="people-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="financeiro" options={{ title: "Financeiro", tabBarIcon: ({ color }) => <Ionicons name="wallet-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="contrato" options={{ href: isAluno ? "/(app)/(tabs)/contrato" : null, title: "Contrato", tabBarIcon: ({ color }) => <Ionicons name="document-text-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="relatorios" options={{ href: isGestor ? "/(app)/(tabs)/relatorios" : null, title: "Relatórios", tabBarIcon: ({ color }) => <Ionicons name="bar-chart-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="configuracoes" options={{ href: isGestor ? "/(app)/(tabs)/configuracoes" : null, title: "Config", tabBarIcon: ({ color }) => <Ionicons name="settings-outline" size={20} color={color} /> }} />
        <Tabs.Screen name="perfil" options={{ title: "Perfil", tabBarIcon: ({ color }) => <Ionicons name="person-circle-outline" size={20} color={color} /> }} />
      </Tabs>

      <BottomSheet open={open} onClose={() => setOpen(false)}>
        <View style={{ gap: 8 }}>
          {me.roles.map((role) => (
            <Button
              key={role}
              title={`${role.charAt(0).toUpperCase()}${role.slice(1)}${activeRole === role ? " (ativo)" : ""}`}
              onPress={() => {
                setActiveRole(role);
                setOpen(false);
              }}
              variant={activeRole === role ? "primary" : "ghost"}
            />
          ))}
        </View>
      </BottomSheet>
    </>
  );
}
