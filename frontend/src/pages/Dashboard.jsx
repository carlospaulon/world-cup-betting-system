import { useEffect, useState, useMemo, useCallback } from 'react'
import { getMatches, extractErrorMessage } from '../api/client'
import MatchTicket from '../components/MatchTicket'
import Loading from '../components/ui/Loading'
import EmptyState from '../components/ui/EmptyState'
import SortSelect from '../components/ui/SortSelect'
import { useToast } from '../context/ToastContext'
import { toSortableTime } from '../utils/format'

const STATUS_OPTIONS = [
  { value: 'TIMED', label: 'Agendadas' },
  { value: 'IN_PLAY', label: 'Ao vivo' },
  { value: 'FINISHED', label: 'Encerradas' },
  { value: 'POSTPONED', label: 'Adiadas' },
]

// Ajuste os values conforme os códigos de competição usados no seu backend/import.
const COMPETITION_OPTIONS = [
  { value: 'WC', label: 'Copa do Mundo 2026' },
  { value: 'BSA', label: 'Brasileirão' },
]

export default function Dashboard() {
  const toast = useToast()
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [team, setTeam] = useState('')
  const [status, setStatus] = useState('TIMED')
  const [competition, setCompetition] = useState('WC')
  const [sortOrder, setSortOrder] = useState('desc')

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const { data } = await getMatches({
        team: team || undefined,
        match_status: status,
        competition,
      })
      setMatches(data)
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [team, status, competition])

  useEffect(() => { load() }, [load])

  const sortedMatches = useMemo(() => {
    const copy = [...matches]
    copy.sort((a, b) => {
      const diff = toSortableTime(a.match_date) - toSortableTime(b.match_date)
      // "Mais recentes primeiro" = a que vai acontecer mais próxima de agora (data mais cedo).
      // "Mais antigas primeiro" = a que ainda vai demorar mais para acontecer (data mais tarde).
      return sortOrder === 'desc' ? diff : -diff
    })
    return copy
  }, [matches, sortOrder])

  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Apostas</p>
          <h1 className="h1">Partidas para apostar</h1>
        </div>
      </div>

      <div className="filterbar">
        <input
          placeholder="Buscar por seleção…"
          value={team}
          onChange={(e) => setTeam(e.target.value)}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          {STATUS_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <select value={competition} onChange={(e) => setCompetition(e.target.value)}>
          {COMPETITION_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <SortSelect value={sortOrder} onChange={setSortOrder} />
      </div>

      {loading ? (
        <Loading label="Carregando partidas…" />
      ) : sortedMatches.length === 0 ? (
        <EmptyState
          title="Nenhuma partida encontrada"
          subtitle={`Não há partidas ${statusSubtitle(status)} para esta competição no momento.`}
        />
      ) : (
        <div className="ticket-grid">
          {sortedMatches.map((m) => (
            <MatchTicket key={m.id} match={m} onBetPlaced={load} />
          ))}
        </div>
      )}
    </div>
  )
}

function statusSubtitle(status) {
  const map = {
    TIMED: 'agendadas',
    IN_PLAY: 'ao vivo',
    FINISHED: 'encerradas',
    POSTPONED: 'adiadas',
  }
  return map[status] || ''
}
