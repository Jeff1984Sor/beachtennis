import { Redirect } from "expo-router";
import { useAuth } from "@/store/auth-store";

export default function Index() {
  const { me } = useAuth();
  return <Redirect href={me ? "/(app)/(tabs)/agenda" : "/(auth)/login"} />;
}
