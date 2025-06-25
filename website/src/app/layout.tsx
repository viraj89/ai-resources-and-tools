import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Insights Daily",
  description: "Your daily digest of trending AI tools and news, updated automatically.",
};

// Reusable Footer Component
const Footer = () => (
  <footer style={footerStyles.footer}>
    <div style={footerStyles.main}>
      <p>Maintained by viraj89 © 2025</p>
    </div>
    <div style={footerStyles.links}>
      <a href="https://github.com/viraj89/ai-resources-and-tools" target="_blank" rel="noopener noreferrer">
        View Source on GitHub
      </a>
    </div>
    <p style={footerStyles.disclaimer}>
      <strong>Disclaimer:</strong> This content is aggregated automatically. Information may be outdated or inaccurate. Please verify all information and use at your own risk.
    </p>
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
    marginTop: '50px',
    padding: '30px 20px',
    borderTop: '1px solid #e0e6ed',
  },
  main: {
    marginBottom: '8px',
  },
  links: {
    marginBottom: '15px'
  },
  disclaimer: {
    fontSize: '0.75rem',
    color: '#999',
    lineHeight: '1.5',
    maxWidth: '600px',
    margin: '0 auto',
  }
};
