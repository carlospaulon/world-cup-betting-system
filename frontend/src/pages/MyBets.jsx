import { useEffect, useState, useMemo, useCallback } from 'react'
import { getMyBets, multiplyBet, extractErrorMessage } from '../api/client'
import Loading from '../components/ui/Loading'
import EmptyState from '../components/ui/EmptyState'
import SortSelect from '../components/ui/SortSelect'
import { useToast } from '../context/ToastContext'
import { useAuth } from '../context/AuthContext'
import { PREDICTION_LABELS, BET_STATUS_LABELS, pillClassForBet, formatBRT, formatPoints, toSortableTime } from '../utils/format'

const TABS = [
  { value: '', label: 'Todas' },
  { value: 'PENDING', label: 'Pendentes' },
  { value: 'SETTLED', label: 'Liquidadas' },
  { value: 'CANCELLED', label: 'Canceladas' },
]

export default function MyBets() {
  const toast = useToast()
  const { refreshUser } = useAuth()
  const [bets, setBets] = useState([])
  const [tab, setTab] = useState('')
  const [sortOrder, setSortOrder] = useState('desc')
  const [loading, setLoading] = useState(true)
  const [busyId, setBusyId] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const { data } = await getMyBets(tab || undefined)
      setBets(data)
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab])

  useEffect(() => { load() }, [load])

  const sortedBets = useMemo(() => {
    const copy = [...bets]
    copy.sort((a, b) => {
      const diff = toSortableTime(a.created_at) - toSortableTime(b.created_at)
      return sortOrder === 'asc' ? diff : -diff
    })
    return copy
  }, [bets, sortOrder])

  const handleMultiply = async (bet, factor) => {
    setBusyId(bet.id)
    try {
      await multiplyBet(bet.id, factor)
      toast.success(`Aposta multiplicada por x${factor}.`)
      await refreshUser()
      load()
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Histórico</p>
          <h1 className="h1">Minhas apostas</h1>
        </div>
        <div className="filterbar" style={{ marginBottom: 0 }}>
          <SortSelect value={sortOrder} onChange={setSortOrder} />
        </div>
      </div>

      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t.value}
            className={`tab-btn${tab === t.value ? ' active' : ''}`}
            onClick={() => setTab(t.value)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <Loading />
      ) : sortedBets.length === 0 ? (
        <EmptyState title="Nenhuma aposta por aqui" subtitle="Vá até as partidas e faça seu primeiro palpite." />
      ) : (
        <div className="bet-list">
          {sortedBets.map((bet) => (
            <div className="bet-row" key={bet.id}>
              <div>
                <div className="bet-row-match">{bet.home_team} x {bet.away_team}</div>
                <div className="bet-row-sub">{formatBRT(bet.created_at)}</div>
              </div>
              <div>
                <div className="bet-row-sub" style={{ marginTop: 0 }}>Palpite</div>
                {PREDICTION_LABELS[bet.prediction] || bet.prediction}
              </div>
              <div>
                <div className="bet-row-sub" style={{ marginTop: 0 }}>Pontos</div>
                {formatPoints(bet.points_bet)}
              </div>
              <div>
                <div className="bet-row-sub" style={{ marginTop: 0 }}>Odd</div>
                {Number(bet.odds).toFixed(2)}
              </div>
              <div>
                <span className={`pill ${pillClassForBet(bet)}`}>
                  {bet.status === 'PENDING' ? BET_STATUS_LABELS.PENDING : (bet.result ? { WON: 'Ganhou', LOST: 'Perdeu', DRAW: 'Empate' }[bet.result] : BET_STATUS_LABELS[bet.status])}
                </span>
              </div>
              <div>
                {bet.status === 'PENDING' && (
                  <select
                    disabled={busyId === bet.id}
                    defaultValue=""
                    onChange={(e) => {
                      const factor = Number(e.target.value)
                      if (factor) handleMultiply(bet, factor)
                      e.target.value = ''
                    }}
                    style={{
                      background: 'var(--surface-2)', color: 'var(--text)',
                      border: '1px solid var(--border-strong)', borderRadius: 6, padding: '6px 8px', fontSize: 12.5,
                    }}
                  >
                    <option value="" disabled>Multiplicar</option>
                    <option value="2">x2</option>
                    <option value="3">x3</option>
                    <option value="4">x4</option>
                    <option value="5">x5</option>
                  </select>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
