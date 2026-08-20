import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getMatchBetsAdmin, getMatchById, getMatchStatisticsAdmin, downloadMatchCsv, extractErrorMessage } from '../../api/client'
import Loading from '../../components/ui/Loading'
import EmptyState from '../../components/ui/EmptyState'
import { useToast } from '../../context/ToastContext'
import { formatBRT, PREDICTION_LABELS, BET_STATUS_LABELS, pillClassForBet, formatPoints } from '../../utils/format'

export default function AdminMatchBets() {
  const { id } = useParams()
  const toast = useToast()
  const [match, setMatch] = useState(null)
  const [bets, setBets] = useState(null)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    getMatchById(id).then(({ data }) => setMatch(data)).catch(() => {})
    getMatchBetsAdmin(id).then(({ data }) => setBets(data)).catch((err) => { toast.error(extractErrorMessage(err)); setBets([]) })
    getMatchStatisticsAdmin(id).then(({ data }) => setStats(data)).catch(() => setStats(null))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  return (
    <div className="container page">
      <Link to="/admin" className="muted" style={{ fontSize: 13 }}>&larr; Voltar</Link>

      <div className="section-head" style={{ marginTop: 16 }}>
        <div>
          <p className="eyebrow">Detalhe da partida</p>
          <h1 className="h1">{match ? `${match.home_team} x ${match.away_team}` : `Partida #${id}`}</h1>
        </div>
        <button className="btn btn-ghost" onClick={() => downloadMatchCsv(id)}>Exportar CSV</button>
      </div>

      {stats && (
        <div className="stat-grid">
          <Stat label="Total de apostas" value={stats.total_bets} />
          <Stat label="Casa" value={stats.bets_home_win} />
          <Stat label="Empate" value={stats.bets_draw} />
          <Stat label="Fora" value={stats.bets_away_win} />
          <Stat label="Odd casa" value={stats.odds_home.toFixed(2)} tone="gold" />
          <Stat label="Odd empate" value={stats.odds_draw.toFixed(2)} tone="gold" />
          <Stat label="Odd fora" value={stats.odds_away.toFixed(2)} tone="gold" />
        </div>
      )}

      {bets === null ? (
        <Loading />
      ) : bets.length === 0 ? (
        <EmptyState title="Nenhuma aposta registrada nesta partida" />
      ) : (
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr><th>Data</th><th>Palpite</th><th>Pontos</th><th>Odd</th><th>Status</th></tr>
            </thead>
            <tbody>
              {bets.map((b) => (
                <tr key={b.id}>
                  <td>{formatBRT(b.created_at)}</td>
                  <td>{PREDICTION_LABELS[b.prediction] || b.prediction}</td>
                  <td>{formatPoints(b.points_bet)}</td>
                  <td>{Number(b.odds).toFixed(2)}</td>
                  <td><span className={`pill ${pillClassForBet(b)}`}>{BET_STATUS_LABELS[b.status] || b.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

function Stat({ label, value, tone }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className={`stat-value${tone ? ` ${tone}` : ''}`}>{value}</div>
    </div>
  )
}
