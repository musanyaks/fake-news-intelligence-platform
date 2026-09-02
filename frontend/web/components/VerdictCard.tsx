'use client'

const COLORS: Record<string, string> = {
  green: '#22c55e',
  yellow: '#eab308',
  orange: '#f97316',
  red: '#ef4444',
  blue: '#3b82f6',
  purple: '#a855f7',
}

export default function VerdictCard({ result }: { result: any }) {
  const color = COLORS[result.verdict_color] || '#fff'

  return (
    <div style={{
      borderRadius: 16,
      padding: 32,
      background: '#1e293b',
      border: `2px solid ${color}`,
      maxWidth: 720,
      margin: '0 auto',
    }}>
      <div style={{ textAlign: 'center', marginBottom: 24 }}>
        <div style={{
          display: 'inline-block',
          padding: '8px 24px',
          borderRadius: 999,
          background: color,
          color: '#000',
          fontWeight: 800,
          fontSize: 20,
          letterSpacing: 1,
        }}>
          {result.verdict.toUpperCase()}
        </div>
      </div>

      <p style={{ fontSize: 18, lineHeight: 1.6, textAlign: 'center', marginBottom: 24 }}>
        {result.explanation}
      </p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
        gap: 16,
        marginBottom: 24,
      }}>
        <ScoreBox label="Truth Score" value={result.truth_score} />
        <ScoreBox label="Confidence" value={Math.round(result.confidence * 100)} />
        <ScoreBox label="Evidence" value={result.evidence_score} />
        <ScoreBox label="Sources" value={result.source_credibility} />
      </div>

      <div style={{
        padding: 16,
        borderRadius: 12,
        background: '#0f172a',
        fontSize: 16,
        fontWeight: 600,
        textAlign: 'center',
      }}>
        {result.recommendation}
      </div>

      {result.fact_checks?.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3 style={{ fontSize: 16, marginBottom: 12 }}>Fact Checks Found</h3>
          {result.fact_checks.map((fc: any, i: number) => (
            <a key={i} href={fc.url} target="_blank" rel="noopener" style={{
              display: 'block',
              padding: 12,
              borderRadius: 8,
              background: '#334155',
              color: '#fff',
              textDecoration: 'none',
              marginBottom: 8,
              fontSize: 14,
            }}>
              <strong>{fc.source}</strong> — {fc.title} <span style={{ color: '#94a3b8' }}>({fc.verdict})</span>
            </a>
          ))}
        </div>
      )}
    </div>
  )
}

function ScoreBox({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ textAlign: 'center', padding: 12, background: '#0f172a', borderRadius: 12 }}>
      <div style={{ fontSize: 28, fontWeight: 800 }}>{value}</div>
      <div style={{ fontSize: 12, color: '#94a3b8', textTransform: 'uppercase' }}>{label}</div>
    </div>
  )
}
