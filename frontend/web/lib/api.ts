const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export async function verifyClaim(query: string, type: string = 'text') {
  const res = await fetch(`${API_BASE}/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, type }),
  })
  if (!res.ok) throw new Error('Verification failed')
  return res.json()
}
