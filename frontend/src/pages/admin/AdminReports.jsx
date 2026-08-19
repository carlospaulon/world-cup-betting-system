import { useEffect, useState } from 'react'
import {
  getSystemStatistics, downloadSystemCsv, downloadMatchCsv, downloadTeamCsv, downloadUserCsv,
  retrainMlModel, extractErrorMessage,
} from '../../api/client'
import Loading from '../../components/ui/Loading'
import { useToast } from '../../context/ToastContext'
import { formatPoints } from '../../utils/format'

export default function AdminReports() {
  const toast = useToast()
  const [stats, setStats] = useState(null)
  const [matchId, setMatchId] = useState('')
  const [team, setTeam] = useState('')
  const [cpf, setCpf] = useState('')
  const [retraining, setRetraining] = useState(false)

  const handleRetrain = async () => {
    setRetraining(true)
    try {
      await retrainMlModel()
      toast.success('Modelo de previsão retreinado com os dados mais recentes.')
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setRetraining(false)
    }
  }

  useEffect(() => {
    getSystemStatistics()
      .then(({ data }) => setStats(data))
      .catch((err) => toast.error(extractErrorMessage(err)))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const guardedDownload = (fn, value, label) => {
    if (!value.trim()) { toast.error(`Informe ${label} para exportar.`); return }
    fn(value.trim())
  }

  return (
    <div>
      {stats === null ? (
        <Loading />
      ) : (
        <div className="stat-grid">
          <Stat label="Usuários" value={stats.total_users} />
          <Stat label="Ativos" value={stats.active_users} tone="turf" />
          <Stat label="Apostas" value={stats.total_bets} />
          <Stat label="Pontos em circulação" value={formatPoints(stats.total_points_in_system)} tone="gold" />
          <Stat label="Partidas" value={stats.total_matches} />
          <Stat label="Em aberto" value={stats.matches_open} tone="turf" />
          <Stat label="Encerradas" value={stats.matches_finished} />
        </div>
      )}

      <div className="panel">
        <h2 className="h2">Modelo de previsão (ML)</h2>
        <p className="muted" style={{ marginBottom: 16 }}>
          Retreina o modelo com os resultados mais recentes. Faça isso depois de importar novas partidas
          ou finalizar jogos, para que as previsões considerem os dados atualizados.
        </p>
        <button className="btn btn-primary btn-sm" onClick={handleRetrain} disabled={retraining}>
          {retraining ? 'Retreinando…' : 'Retreinar modelo'}
        </button>
      </div>

      <div className="panel">
        <h2 className="h2">Relatórios em CSV</h2>
        <p className="muted" style={{ marginBottom: 18 }}>Exportações não incluem CPF nem senha dos usuários.</p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <ReportRow label="Sistema completo">
            <button className="btn btn-primary btn-sm" onClick={downloadSystemCsv}>Baixar CSV</button>
          </ReportRow>

          <ReportRow label="Estatísticas de uma partida (ID)">
            <input value={matchId} onChange={(e) => setMatchId(e.target.value)} placeholder="ex: 1" style={inputStyle} />
            <button className="btn btn-ghost btn-sm" onClick={() => guardedDownload(downloadMatchCsv, matchId, 'o ID da partida')}>Baixar</button>
          </ReportRow>

          <ReportRow label="Estatísticas de uma seleção">
            <input value={team} onChange={(e) => setTeam(e.target.value)} placeholder="ex: Brazil" style={inputStyle} />
            <button className="btn btn-ghost btn-sm" onClick={() => guardedDownload(downloadTeamCsv, team, 'o nome da seleção')}>Baixar</button>
          </ReportRow>

          <ReportRow label="Estatísticas de um usuário (CPF)">
            <input value={cpf} onChange={(e) => setCpf(e.target.value)} placeholder="somente números" style={inputStyle} />
            <button className="btn btn-ghost btn-sm" onClick={() => guardedDownload(downloadUserCsv, cpf, 'o CPF do usuário')}>Baixar</button>
          </ReportRow>
        </div>
      </div>
    </div>
  )
}

const inputStyle = {
  background: 'var(--surface-2)', border: '1px solid var(--border-strong)', color: 'var(--text)',
  borderRadius: 6, padding: '8px 10px', fontSize: 13.5, minWidth: 200,
}

function ReportRow({ label, children }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
      <span style={{ minWidth: 240, fontSize: 13.5, color: 'var(--text-dim)' }}>{label}</span>
      {children}
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
