import { useState } from 'react'
import { getMatchPrediction, extractErrorMessage } from '../api/client'
import { useToast } from '../context/ToastContext'

export default function PredictionPanel({ matchId }) {
  const toast = useToast()
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)

  const handleToggle = async () => {
    if (open) { setOpen(false); return }
    setOpen(true)
    if (prediction) return
    setLoading(true)
    try {
      const { data } = await getMatchPrediction(matchId)
      setPrediction(data)
    } catch (err) {
      toast.error(extractErrorMessage(err))
      setOpen(false)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ marginTop: 4 }}>
      <button type="button" className="btn btn-ghost btn-sm" onClick={handleToggle}>
        {open ? 'Ocultar previsão do modelo' : 'Ver previsão do modelo (ML)'}
      </button>

      {open && (
        <div style={{
          marginTop: 10, padding: '12px 14px', borderRadius: 'var(--radius-s)',
          background: 'var(--surface-2)', border: '1px solid var(--border)',
        }}>
          {loading ? (
            <span className="muted" style={{ fontSize: 12.5 }}>Calculando estimativa…</span>
          ) : prediction ? (
            <>
              <ProbBar label="Casa" value={prediction.home_win_probability} />
              <ProbBar label="Empate" value={prediction.draw_probability} />
              <ProbBar label="Fora" value={prediction.away_win_probability} />
              <p className="field-hint" style={{ marginTop: 10, marginBottom: 0 }}>
                Estimativa estatística de um modelo treinado sobre partidas anteriores. Não é garantia de
                resultado e não substitui as odds oficiais calculadas pelos apostadores.
              </p>
            </>
          ) : null}
        </div>
      )}
    </div>
  )
}

function ProbBar({ label, value }) {
  const pct = Math.round((value ?? 0) * 100)
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11.5, marginBottom: 4 }}>
        <span className="muted">{label}</span>
        <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--gold-strong)' }}>{pct}%</span>
      </div>
      <div style={{ height: 6, borderRadius: 4, background: 'var(--surface-3)', overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${pct}%`, background: 'var(--gold)', borderRadius: 4 }} />
      </div>
    </div>
  )
}
