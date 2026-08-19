import { useEffect, useState, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { getMatches, importMatches, finishMatch, extractErrorMessage } from '../../api/client'
import Loading from '../../components/ui/Loading'
import EmptyState from '../../components/ui/EmptyState'
import SortSelect from '../../components/ui/SortSelect'
import { useToast } from '../../context/ToastContext'
import { useAuth } from '../../context/AuthContext'
import { formatDate, toSortableTime, MATCH_STATUS_LABELS } from '../../utils/format'

const TABS = [
  { value: 'TIMED', label: 'Agendadas' },
  { value: 'IN_PLAY', label: 'Ao vivo' },
  { value: 'FINISHED', label: 'Encerradas' },
  { value: 'POSTPONED', label: 'Adiadas' },
]

// Ajuste os values conforme os códigos de competição do seu endpoint de importação.
const COMPETITIONS = [
  { value: 'WC', label: 'Copa do Mundo 2026' },
  { value: 'BSA', label: 'Brasileirão' },
]

export default function AdminMatches() {
  const toast = useToast()
  const { refreshUser } = useAuth()
  const [tab, setTab] = useState('TIMED')
  const [competitionFilter, setCompetitionFilter] = useState('WC')
  const [importCompetition, setImportCompetition] = useState('WC')
  const [sortOrder, setSortOrder] = useState('desc')
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [importing, setImporting] = useState(false)
  const [finishingId, setFinishingId] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const { data } = await getMatches({
        match_status: tab,
        competition: competitionFilter,
      })
      setMatches(data)
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, competitionFilter])

  useEffect(() => { load() }, [load])

  const sortedMatches = useMemo(() => {
    const copy = [...matches]
    copy.sort((a, b) => {
      const diff = toSortableTime(a.match_date) - toSortableTime(b.match_date)
      // mesma semântica do Dashboard: "recentes" = mais próxima de agora
      return sortOrder === 'desc' ? diff : -diff
    })
    return copy
  }, [matches, sortOrder])

  const handleImport = async () => {
    setImporting(true)
    try {
      await importMatches(importCompetition)
      toast.success('Importação concluída.')
      load()
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setImporting(false)
    }
  }

  const handleFinish = async (id) => {
    setFinishingId(id)
    try {
      await finishMatch(id)
      toast.success('Partida finalizada e apostas liquidadas.')
      await refreshUser()
      load()
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setFinishingId(null)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18, flexWrap: 'wrap', gap: 10 }}>
        <div className="tabs" style={{ marginBottom: 0 }}>
          {TABS.map((t) => (
            <button key={t.value} className={`tab-btn${tab === t.value ? ' active' : ''}`} onClick={() => setTab(t.value)}>
              {t.label}
            </button>
          ))}
        </div>
        <div className="filterbar" style={{ marginBottom: 0 }}>
          <select value={competitionFilter} onChange={(e) => setCompetitionFilter(e.target.value)}>
            {COMPETITIONS.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
          <SortSelect value={sortOrder} onChange={setSortOrder} />
          <select value={importCompetition} onChange={(e) => setImportCompetition(e.target.value)}>
            {COMPETITIONS.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
          <button className="btn btn-primary" onClick={handleImport} disabled={importing}>
            {importing ? 'Importando…' : 'Importar'}
          </button>
        </div>
      </div>

      {loading ? (
        <Loading />
      ) : sortedMatches.length === 0 ? (
        <EmptyState title="Nenhuma partida nesse status" subtitle="Ajuste o status ou a competição selecionada." />
      ) : (
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>Data</th><th>Competição</th><th>Partida</th><th>Fase</th><th>Status</th><th>Placar</th><th></th>
              </tr>
            </thead>
            <tbody>
              {sortedMatches.map((m) => (
                <tr key={m.id}>
                  <td>{formatDate(m.match_date)}</td>
                  <td>{m.competition || '—'}</td>
                  <td><Link to={`/partidas/${m.id}`}>{m.home_team} x {m.away_team}</Link></td>
                  <td>{m.stage?.replaceAll('_', ' ')}</td>
                  <td>{MATCH_STATUS_LABELS[m.status] || m.status}</td>
                  <td>{m.status === 'FINISHED' ? `${m.home_score} - ${m.away_score}` : '—'}</td>
                  <td style={{ display: 'flex', gap: 8 }}>
                    <Link className="btn btn-ghost btn-sm" to={`/admin/partidas/${m.id}/apostas`}>Apostas</Link>
                    {(m.status === 'TIMED' || m.status === 'IN_PLAY') && (
                      <button className="btn btn-primary btn-sm" onClick={() => handleFinish(m.id)} disabled={finishingId === m.id}>
                        {finishingId === m.id ? 'Buscando…' : 'Finalizar'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
