import "./globals.css";
import TopNav from "./components/top-nav";

export const metadata = {
  title: "Beach Tennis Admin",
  description: "Admin web para escola de Beach Tennis"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <TopNav />
        <main>{children}</main>
      </body>
    </html>
  );
}
