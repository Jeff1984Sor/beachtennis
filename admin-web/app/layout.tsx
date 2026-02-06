import "./globals.css";

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
        <main>{children}</main>
      </body>
    </html>
  );
}