import { AuthProvider } from "../context/AuthContext";
import "../styles/globals.css";

export const metadata = {
  title: "Paper Trading App",
  description: "Crypto paper-trading dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}