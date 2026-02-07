import { createContext, PropsWithChildren, useContext, useEffect, useMemo, useState } from "react";
import { apiRequest, loadTokens, saveTokens, TokenPair } from "@/api/client";
import { MeResponse } from "@/api/types";
import { Branding, Role } from "@/theme";

type AuthContextType = {
  loading: boolean;
  me: MeResponse | null;
  branding: Branding | null;
  activeRole: Role | null;
  setActiveRole: (role: Role) => void;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  reload: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: PropsWithChildren) {
  const [loading, setLoading] = useState(true);
  const [me, setMe] = useState<MeResponse | null>(null);
  const [branding, setBranding] = useState<Branding | null>(null);
  const [activeRole, setActiveRoleState] = useState<Role | null>(null);

  const setActiveRole = (role: Role) => setActiveRoleState(role);

  const loadBranding = async () => {
    try {
      const data = await apiRequest<Branding>("/public/branding", undefined, false);
      setBranding(data);
    } catch {
      setBranding({ nome_empresa: "Beach Tennis" });
    }
  };

  const reload = async () => {
    const profile = await apiRequest<MeResponse>("/auth/me");
    setMe(profile);
    setActiveRoleState((prev) => (prev && profile.roles.includes(prev) ? prev : profile.roles[0]));
  };

  const signIn = async (email: string, password: string) => {
    const tokens = await apiRequest<TokenPair>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    }, false);
    await saveTokens(tokens);
    await reload();
  };

  const signOut = async () => {
    await saveTokens(null);
    setMe(null);
    setActiveRoleState(null);
  };

  useEffect(() => {
    (async () => {
      await loadBranding();
      const tokens = await loadTokens();
      if (tokens?.access_token) {
        try {
          await reload();
        } catch {
          await saveTokens(null);
        }
      }
      setLoading(false);
    })();
  }, []);

  const value = useMemo(
    () => ({ loading, me, branding, activeRole, setActiveRole, signIn, signOut, reload }),
    [loading, me, branding, activeRole]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
