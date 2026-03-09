const API = 'http://localhost:8000'

export async function generate(prompt) {
  const res = await fetch(`${API}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  })
  return res.json()
}

export async function analyze() {
  const res = await fetch(`${API}/analyze`, { method: 'POST' })
  return res.json()
}

export async function fix(issue) {
  const res = await fetch(`${API}/fix/${issue}`, { method: 'POST' })
  return res.json()
}
