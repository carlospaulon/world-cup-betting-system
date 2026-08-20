import { useState } from 'react'
import { getTeamStatistics, extractErrorMessage } from '../api/client'
import Loading from '../components/ui/Loading'
import { useToast } from '../context/ToastContext'

export default function TeamStats() {
  const toast = useToast()
  const [team, setTeam] = useState('')
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  const search = async (e) => {
    e.preventDefault()
    if (!team.trim()) return
    setLoading(true)
    setStats(null)
    try {
      const { data } = await getTeamStatistics(team.trim())
      setStats(data)
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Retrospecto</p>
          <h1 className="h1">Seleções</h1>
        </div>
      </div>

      <form className="filterbar" onSubmit={search}>
        <input
          placeholder="Nome da seleção (ex: Brazil)"
          value={team}
          onChange={(e) => setTeam(e.target.value)}
          style={{ minWidth: 260 }}
        />
        <button className="btn btn-primary" type="submit">Buscar</button>
      </form>

      {loading && <Loading />}

      {stats && (
        <>
          <div className="h2" style={{ marginBottom: 14 }}>{stats.team}</div>
          <div className="stat-grid">
            <Stat label="Partidas" value={stats.matches} />
            <Stat label="Vitórias" value={stats.wins} tone="turf" />
            <Stat label="Empates" value={stats.draws} />
            <Stat label="Derrotas" value={stats.losses} tone="scarlet" />
            <Stat label="Gols pró" value={stats.goals_scored} />
            <Stat label="Gols contra" value={stats.goals_conceded} />
            <Stat label="Saldo de gols" value={stats.goal_difference} tone={stats.goal_difference >= 0 ? 'turf' : 'scarlet'} />
            <Stat label="Aproveitamento" value={`${stats.win_rate.toFixed(1)}%`} tone="gold" />
          </div>
        </>
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
