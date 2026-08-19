import { useEffect, useState, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getMatchById, getTeamHistory, getMatches, extractErrorMessage } from '../api/client'
import MatchTicket from '../components/MatchTicket'
import Loading from '../components/ui/Loading'
import { useToast } from '../context/ToastContext'
import { formatDateShort } from '../utils/format'

export default function MatchDetail() {
  const { id } = useParams()
  const toast = useToast()
  const [match, setMatch] = useState(null)
  const [homeHistory, setHomeHistory] = useState([])
  const [awayHistory, setAwayHistory] = useState([])
  const [loading, setLoading] = useState(true)

  // Função isolada de carregamento (sem disparar re-render em loop)
  const fetchAllData = useCallback(async (isInitial = false) => {
    if (isInitial) setLoading(true)
    try {
      const { data } = await getMatchById(id)
      let updatedMatch = { ...data }

      if (data.status === 'TIMED' || data.status === 'IN_PLAY') {
        try {
          const { data: list } = await getMatches({
            match_status: data.status,
            competition: data.competition,
            is_bet_available: true,
          })
          const withOdds = list.find((m) => m.id === data.id)
          if (withOdds) {
            updatedMatch = {
              ...updatedMatch,
              odds_home: withOdds.odds_home,
              odds_away: withOdds.odds_away,
              odds_draw: withOdds.odds_draw,
            }
          }
        } catch (_) {}
      }

      setMatch(updatedMatch)

      // Histórico é buscado apenas no carregamento inicial para economizar requisições
      if (isInitial) {
        const [home, away] = await Promise.all([
          getTeamHistory(data.home_team).catch(() => ({ data: [] })),
          getTeamHistory(data.away_team).catch(() => ({ data: [] })),
        ])

        const now = Date.now()
        const recentFirst = (list) =>
          list
            .filter((m) => m.id !== data.id && new Date(m.match_date).getTime() <= now)
            .sort((a, b) => new Date(b.match_date) - new Date(a.match_date))
            .slice(0, 5)

        setHomeHistory(recentFirst(home.data))
        setAwayHistory(recentFirst(away.data))
      }
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      if (isInitial) setLoading(false)
    }
  }, [id, toast])

  // Roda uma única vez na montagem
  useEffect(() => {
    fetchAllData(true)
  }, [id]) // Depende apenas do id da URL

  // Callback leve exclusivo para atualizar após apostar
  const handleBetPlaced = useCallback(() => {
    fetchAllData(false)
  }, [fetchAllData])

  if (loading) return <div className="container page"><Loading /></div>
  if (!match) return null

  return (
    <div className="container page">
      <Link to="/" className="muted" style={{ fontSize: 13 }}>&larr; Voltar às partidas</Link>

      <div style={{ maxWidth: 420, margin: '20px 0 36px' }}>
        <MatchTicket match={match} linkable={false} onBetPlaced={handleBetPlaced} />
      </div>

      <div className="section-head"><h2 className="h2">Retrospecto recente</h2></div>
      <p className="muted" style={{ marginTop: -14, marginBottom: 20 }}>
        Últimas 5 partidas encerradas de cada seleção até a data de hoje.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <HistoryPanel title={match.home_team} history={homeHistory} />
        <HistoryPanel title={match.away_team} history={awayHistory} />
      </div>
    </div>
  )
}

function HistoryPanel({ title, history }) {
  return (
    <div className="panel">
      <div className="h2" style={{ fontSize: 16 }}>{title}</div>
      {history.length === 0 ? (
        <p className="muted" style={{ fontSize: 13 }}>Sem partidas encerradas anteriores registradas.</p>
      ) : (
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr><th>Data</th><th>Partida</th><th>Placar</th></tr>
            </thead>
            <tbody>
              {history.map((m) => (
                <tr key={m.id}>
                  <td>{formatDateShort(m.match_date)}</td>
                  <td>{m.home_team} x {m.away_team}</td>
                  <td>{m.home_score} - {m.away_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}