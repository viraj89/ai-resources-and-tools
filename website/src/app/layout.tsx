import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Insights Daily",
  description: "Your daily digest of trending AI tools and news, updated automatically.",
};

// Reusable Footer Component
const Footer = () => (
  <footer style={footerStyles.footer}>
    <div style={footerStyles.footerContent}>
      <span>Maintained by viraj89 © 2025</span>
      <a href="https://github.com/viraj89/ai-resources-and-tools" target="_blank" rel="noopener noreferrer">View Source on GitHub</a>
    </div>
    <div style={footerStyles.disclaimer}>
      Disclaimer: This content is aggregated automatically. Information may be outdated or inaccurate. Please verify all information and use at your own risk.
    </div>
  </footer>
);

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <main className="container">
        {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}

// Inline styles for the footer to keep it self-contained
const footerStyles = {
  footer: {
    textAlign: 'center' as const,
    color: '#6c757d',
    marginTop: '24px',
    padding: '12px 8px 8px 8px',
    borderTop: '1px solid #e0e6ed',
    background: 'none',
    borderRadius: 0,
    boxShadow: 'none',
    fontSize: '0.85rem',
  },
  footerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap' as const,
    gap: 8,
    marginBottom: 4,
  },
  disclaimer: {
    fontSize: '0.75rem',
    color: '#999',
    lineHeight: '1.2',
    margin: '0 auto',
    whiteSpace: 'normal' as const,
    textAlign: 'center' as const,
  },
};
