import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMyStatistics, updatePassword, deactivateAccount, extractErrorMessage } from '../api/client'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import Loading from '../components/ui/Loading'
import { PREDICTION_LABELS, formatPoints } from '../utils/format'

export default function Profile() {
  const { user, logout } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)

  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [pwLoading, setPwLoading] = useState(false)
  const [confirmDeactivate, setConfirmDeactivate] = useState(false)

  useEffect(() => {
    getMyStatistics().then(({ data }) => setStats(data)).catch(() => setStats(false))
  }, [])

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setPwLoading(true)
    try {
      await updatePassword({ current_password: currentPassword, new_password: newPassword })
      toast.success('Senha atualizada com sucesso.')
      setCurrentPassword('')
      setNewPassword('')
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setPwLoading(false)
    }
  }

  const handleDeactivate = async () => {
    try {
      await deactivateAccount()
      toast.success('Conta desativada.')
      logout()
      navigate('/login')
    } catch (err) {
      toast.error(extractErrorMessage(err))
    }
  }

  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Sua conta</p>
          <h1 className="h1">{user.nickname}</h1>
        </div>
      </div>

      <div className="stat-grid">
        <Stat label="Pontos" value={formatPoints(user.points)} tone="gold" />
        {stats === null && <Loading />}
        {stats && (
          <>
            <Stat label="Apostas feitas" value={stats.total_bets} />
            <Stat label="Vitórias" value={stats.won_bets} tone="turf" />
            <Stat label="Derrotas" value={stats.lost_bets} tone="scarlet" />
            <Stat label="Empates" value={stats.draw_bets} />
            <Stat label="Pendentes" value={stats.pending_bets} />
            <Stat label="Taxa de acerto" value={`${stats.win_rate.toFixed(1)}%`} />
            <Stat label="Pontos investidos" value={stats.points_invested} />
            <Stat label="Palpite favorito" value={PREDICTION_LABELS[stats.favorite_prediction] || '—'} />
            <Stat label="Seleção favorita" value={stats.favorite_team || '—'} />
          </>
        )}
      </div>

      <div className="panel">
        <h2 className="h2">Alterar senha</h2>
        <form onSubmit={handlePasswordChange} style={{ maxWidth: 360 }}>
          <div className="field">
            <label htmlFor="cur">Senha atual</label>
            <input id="cur" type="password" required value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="new">Nova senha</label>
            <input id="new" type="password" required minLength={8} value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
          </div>
          <button className="btn btn-primary" type="submit" disabled={pwLoading}>
            {pwLoading ? 'Salvando…' : 'Atualizar senha'}
          </button>
        </form>
      </div>

      <div className="panel">
        <h2 className="h2">Encerrar participação</h2>
        <p className="muted" style={{ marginBottom: 16 }}>
          Sua conta é desativada e você perde o acesso ao sistema, mas permanece no ranking com o histórico atual.
        </p>
        {!confirmDeactivate ? (
          <button className="btn btn-danger" onClick={() => setConfirmDeactivate(true)}>Desativar minha conta</button>
        ) : (
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn btn-danger" onClick={handleDeactivate}>Confirmar desativação</button>
            <button className="btn btn-ghost" onClick={() => setConfirmDeactivate(false)}>Cancelar</button>
          </div>
        )}
      </div>
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
