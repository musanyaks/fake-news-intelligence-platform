export const metadata = {
  title: 'TruthLens - Check Before You Share',
  description: 'Free AI-powered misinformation detection for Kenya and East Africa',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, -apple-system, sans-serif', background: '#0f172a', color: '#fff' }}>
        {children}
      </body>
    </html>
  )
}
