import { createContext, PropsWithChildren, useContext, useMemo, useState } from "react";
import { Animated, Text, View } from "react-native";

type ToastApi = { show: (message: string) => void };

const ToastContext = createContext<ToastApi | null>(null);

export function ToastProvider({ children }: PropsWithChildren) {
  const [message, setMessage] = useState("");
  const [visible, setVisible] = useState(false);
  const [fade] = useState(new Animated.Value(0));

  const show = (text: string) => {
    setMessage(text);
    setVisible(true);
    Animated.sequence([
      Animated.timing(fade, { toValue: 1, duration: 150, useNativeDriver: true }),
      Animated.delay(1800),
      Animated.timing(fade, { toValue: 0, duration: 200, useNativeDriver: true })
    ]).start(() => setVisible(false));
  };

  const value = useMemo(() => ({ show }), []);

  return (
    <ToastContext.Provider value={value}>
      {children}
      {visible ? (
        <Animated.View style={{ position: "absolute", bottom: 42, left: 20, right: 20, opacity: fade }}>
          <View style={{ backgroundColor: "#0F172A", borderRadius: 12, padding: 12 }}>
            <Text style={{ color: "#fff", textAlign: "center", fontWeight: "600" }}>{message}</Text>
          </View>
        </Animated.View>
      ) : null}
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used inside ToastProvider");
  return ctx;
}
