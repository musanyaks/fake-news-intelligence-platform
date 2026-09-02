'use client'

import { useState } from 'react'
import { verifyClaim } from '@/lib/api'
import VerdictCard from '@/components/VerdictCard'

export default function Home() {
  const [query, setQuery] = useState('')
  const [type, setType] = useState('text')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await verifyClaim(query, type)
      setResult(data)
    } catch (err: any) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ minHeight: '100vh', padding: '40px 20px' }}>
      <div style={{ maxWidth: 720, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <h1 style={{ fontSize: 48, fontWeight: 900, margin: 0, letterSpacing: -2 }}>TruthLens</h1>
          <p style={{ fontSize: 18, color: '#94a3b8', marginTop: 8 }}>
            Check news, URLs, and claims before you share
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ marginBottom: 40 }}>
          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            {['text', 'url'].map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setType(t)}
                style={{
                  padding: '8px 20px',
                  borderRadius: 8,
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: 600,
                  background: type === t ? '#3b82f6' : '#334155',
                  color: '#fff',
                }}
              >
                {t === 'text' ? 'Paste Text' : 'Paste URL'}
              </button>
            ))}
          </div>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={type === 'text'
              ? "Paste a news article, WhatsApp forward, or claim..."
              : "Paste a news article URL..."
            }
            rows={6}
            style={{
              width: '100%',
              padding: 16,
              borderRadius: 12,
              border: '1px solid #334155',
              background: '#1e293b',
              color: '#fff',
              fontSize: 16,
              resize: 'vertical',
              boxSizing: 'border-box',
            }}
          />

          <button
            type="submit"
            disabled={loading || !query.trim()}
            style={{
              marginTop: 12,
              width: '100%',
              padding: '16px 24px',
              borderRadius: 12,
              border: 'none',
              background: loading ? '#475569' : '#3b82f6',
              color: '#fff',
              fontSize: 18,
              fontWeight: 700,
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Checking...' : 'Verify Claim'}
          </button>
        </form>

        {error && (
          <div style={{
            padding: 16,
            borderRadius: 12,
            background: '#450a0a',
            color: '#fca5a5',
            textAlign: 'center',
            marginBottom: 24,
          }}>
            {error}
          </div>
        )}

        {result && <VerdictCard result={result} />}
      </div>
    </main>
  )
}
