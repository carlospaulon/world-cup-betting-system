import { useState } from 'react'
import { Link } from 'react-router-dom'
import { createBet, extractErrorMessage } from '../api/client'
import { useToast } from '../context/ToastContext'
import { useAuth } from '../context/AuthContext'
import { formatDate, tagClassForMatch, MATCH_STATUS_LABELS } from '../utils/format'
import PredictionPanel from './PredictionPanel'

export default function MatchTicket({ match, onBetPlaced, linkable = true }) {
  const { user, refreshUser } = useAuth()
  const toast = useToast()
  const [prediction, setPrediction] = useState(null)
  const [points, setPoints] = useState(10)
  const [submitting, setSubmitting] = useState(false)

  const canBet = match.status === 'TIMED'
  const isFinished = match.status === 'FINISHED'

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prediction) {
      toast.error('Escolha um resultado antes de apostar.')
      return
    }
    if (!points || points < 1) {
      toast.error('Informe uma quantidade de pontos válida.')
      return
    }
    setSubmitting(true)
    try {
      await createBet({ match_id: match.id, prediction, points_bet: Number(points) })
      toast.success(`Aposta registrada em ${match.home_team} x ${match.away_team}.`)
      setPrediction(null)
      await refreshUser()
      onBetPlaced?.()
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  const TopWrapper = linkable ? Link : 'div'
  const topWrapperProps = linkable
    ? { to: `/partidas/${match.id}`, className: 'ticket-top ticket-top-link' }
    : { className: 'ticket-top' }

  return (
    <article className="ticket">
      <TopWrapper {...topWrapperProps}>
        <div className="ticket-meta">
          <span className={tagClassForMatch(match.status)}>{MATCH_STATUS_LABELS[match.status] || match.status}</span>
          <span className="ticket-date">{formatDate(match.match_date)}</span>
        </div>

        <div className="matchup">
          <div className="team">
            <div className="team-name">{match.home_team}</div>
            {isFinished && <div className="team-score">{match.home_score}</div>}
          </div>
          <div className="vs">{isFinished ? '' : 'VS'}</div>
          <div className="team">
            <div className="team-name">{match.away_team}</div>
            {isFinished && <div className="team-score">{match.away_score}</div>}
          </div>
        </div>
      </TopWrapper>

      <div className="perforation" />

      <div className="ticket-bottom">
        <div className="stage-line">
          {match.competition ? `${match.competition} · ` : ''}
          {match.stage?.replaceAll('_', ' ') || 'Fase de grupos'} · #{match.api_match_id}
        </div>

        <div className="odds-row">
          <OddFlip
            label="Casa"
            value={match.odds_home}
            active={prediction === 'HOME_TEAM'}
            disabled={!canBet}
            onClick={() => setPrediction('HOME_TEAM')}
          />
          <OddFlip
            label="Empate"
            value={match.odds_draw}
            active={prediction === 'DRAW'}
            disabled={!canBet}
            onClick={() => setPrediction('DRAW')}
          />
          <OddFlip
            label="Fora"
            value={match.odds_away}
            active={prediction === 'AWAY_TEAM'}
            disabled={!canBet}
            onClick={() => setPrediction('AWAY_TEAM')}
          />
        </div>

        {canBet && user && (
          <form className="bet-form-row" onSubmit={handleSubmit}>
            <input
              type="number"
              min={1}
              value={points}
              onChange={(e) => setPoints(e.target.value)}
              aria-label="Pontos a apostar"
            />
            <button className="btn btn-primary btn-sm" type="submit" disabled={submitting}>
              {submitting ? 'Enviando…' : 'Apostar'}
            </button>
          </form>
        )}

        {!canBet && !isFinished && (
          <span className="muted" style={{ fontSize: 12.5 }}>Apostas fechadas para esta partida.</span>
        )}

        {!isFinished && <PredictionPanel matchId={match.id} />}
      </div>
    </article>
  )
}

function OddFlip({ label, value, active, disabled, onClick }) {
  return (
    <button
      type="button"
      className={`odds-flip${active ? ' selected' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      <span className="odds-flip-label">{label}</span>
      <span className="odds-flip-value">{value != null ? Number(value).toFixed(2) : '—'}</span>
    </button>
  )
}
