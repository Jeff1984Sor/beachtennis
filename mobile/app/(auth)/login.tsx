import { LinearGradient } from "expo-linear-gradient";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, router } from "expo-router";
import { Image, Text, View } from "react-native";

import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Input } from "@/components/Input";
import { useAuth } from "@/store/auth-store";
import { useToast } from "@/store/toast-store";

const schema = z.object({ email: z.string().email(), password: z.string().min(3) });

type FormData = z.infer<typeof schema>;

export default function LoginScreen() {
  const { signIn, branding } = useAuth();
  const { show } = useToast();
  const { setValue, handleSubmit, watch, formState: { isSubmitting } } = useForm<FormData>({ resolver: zodResolver(schema), defaultValues: { email: "gestor@local", password: "gestor123" } });

  const onSubmit = handleSubmit(async (data) => {
    try {
      await signIn(data.email, data.password);
      router.replace("/(app)/(tabs)/agenda");
    } catch {
      show("Credenciais inválidas");
    }
  });

  return (
    <LinearGradient colors={["#0F766E", "#0C4A6E", "#0F172A"]} style={{ flex: 1, padding: 20, justifyContent: "center", gap: 18 }}>
      <View style={{ alignItems: "center", gap: 10 }}>
        {branding?.logo_url ? <Image source={{ uri: branding.logo_url }} style={{ width: 64, height: 64, borderRadius: 14 }} /> : null}
        <Text style={{ color: "#fff", fontSize: 28, fontWeight: "800" }}>{branding?.nome_empresa || "Beach Tennis"}</Text>
        <Text style={{ color: "#DBEAFE" }}>Gestão completa da escola em um app</Text>
      </View>
      <Card>
        <Input label="E-mail" autoCapitalize="none" keyboardType="email-address" value={watch("email")} onChangeText={(t: string) => setValue("email", t)} />
        <Input label="Senha" secureTextEntry value={watch("password")} onChangeText={(t: string) => setValue("password", t)} />
        <Button title="Entrar" onPress={onSubmit} loading={isSubmitting} />
        <Link href="#" style={{ textAlign: "center", color: "#334155", fontWeight: "600" }}>Esqueci minha senha</Link>
      </Card>
    </LinearGradient>
  );
}
