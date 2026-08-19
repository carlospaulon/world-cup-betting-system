export const PREDICTION_LABELS = {
  HOME_TEAM: 'Casa',
  HOME_WIN: 'Casa',
  AWAY_TEAM: 'Fora',
  AWAY_WIN: 'Fora',
  DRAW: 'Empate',
}

export const RESULT_LABELS = {
  WON: 'Ganhou',
  LOST: 'Perdeu',
  DRAW: 'Empate',
}

export const BET_STATUS_LABELS = {
  PENDING: 'Pendente',
  SETTLED: 'Liquidada',
  CANCELLED: 'Cancelada',
}

export const MATCH_STATUS_LABELS = {
  TIMED: 'Agendada',
  IN_PLAY: 'Ao vivo',
  FINISHED: 'Encerrada',
  POSTPONED: 'Adiada',
}

// Backend grava datas em UTC sem timezone (func.now() / API externa).
// Deslocamos -3h manualmente para exibir no horário de Brasília,
// já que o navegador interpreta a string "naive" como horário local.
function shiftToBRT(iso) {
  const d = new Date(iso)
  d.setHours(d.getHours() - 3)
  return d
}

export function formatDate(iso) {
  if (!iso) return '—'
  return shiftToBRT(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export function formatDateShort(iso) {
  if (!iso) return '—'
  return shiftToBRT(iso).toLocaleDateString('pt-BR')
}

export function formatBRT(iso) {
  if (!iso) return '—'
  return shiftToBRT(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

// timestamp cru (ms) já ajustado, útil para ordenação por data
export function toSortableTime(iso) {
  if (!iso) return 0
  return shiftToBRT(iso).getTime()
}

// points agora pode vir como Decimal/float do backend (ex: aposta multiplicada por odd fracionária).
// Exibe inteiro quando possível, senão 2 casas decimais.
export function formatPoints(value) {
  if (value == null) return '0'
  const num = Number(value)
  return Number.isInteger(num) ? String(num) : num.toFixed(2)
}

export function pillClassForBet(bet) {
  if (bet.status === 'PENDING') return 'pill-pending'
  if (bet.result === 'WON') return 'pill-won'
  if (bet.result === 'LOST') return 'pill-lost'
  if (bet.result === 'DRAW') return 'pill-draw'
  return 'pill-cancelled'
}

export function tagClassForMatch(status) {
  if (status === 'IN_PLAY') return 'tag tag-live'
  if (status === 'TIMED') return 'tag tag-open'
  return 'tag tag-finished'
}
