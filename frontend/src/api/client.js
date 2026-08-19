import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const api = axios.create({ baseURL: API_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Normalizes FastAPI error shapes (AppException handler + 422 validation) into a single string
export function extractErrorMessage(error) {
  const data = error?.response?.data
  if (!data) return 'Não foi possível conectar ao servidor.'
  if (data.message) return data.message
  if (Array.isArray(data.detail)) {
    return data.detail.map((d) => d.msg).join(' · ')
  }
  if (typeof data.detail === 'string') return data.detail
  return 'Algo deu errado. Tente novamente.'
}

/* ---------------- Auth ---------------- */
export const registerUser = (payload) => api.post('/auth/register', payload)

export const loginUser = (email, password) => {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  return api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
}

/* ---------------- Users ---------------- */
export const getMe = () => api.get('/users/me')
export const updatePassword = (payload) => api.patch('/users/me/password', payload)
export const deactivateAccount = () => api.patch('/users/me/deactivate')
export const getMyPoints = () => api.get('/users/me/points')
export const getRanking = () => api.get('/users/me/points/ranking')

export const getAllUsersAdmin = () => api.get('/users/admin/all')
export const getUsersStatusAdmin = () => api.get('/users/admin/users')
export const getUserByCpfAdmin = (cpf) => api.get(`/users/admin/users/${cpf}`)
export const promoteToAdmin = (userId) => api.patch(`/users/admin/${userId}/role`)

/* ---------------- Matches ---------------- */
export const getMatches = (params) => api.get('/matches', { params })
export const getMatchById = (id) => api.get(`/matches/${id}`)
export const getTeamHistory = (team) => api.get(`/matches/history/${encodeURIComponent(team)}`)
export const importMatches = (competition) =>
  api.post('/matches/admin/import', null, { params: competition ? { competition } : {} })
export const finishMatch = (id) => api.patch(`/matches/admin/${id}/finish`)
export const updateMatchStatus = (matchId, status) =>
  api.patch(`/matches/admin/${matchId}/status`, null, { params: { match_status: status } })
export const getMatchBetsAdmin = (id) => api.get(`/matches/admin/${id}/bets`)

/* ---------------- Bets ---------------- */
export const createBet = (payload) => api.post('/bets', payload)
export const getMyBets = (betStatus) =>
  api.get('/bets', { params: betStatus ? { bet_status: betStatus } : {} })
export const getBetById = (id) => api.get(`/bets/${id}`)
export const multiplyBet = (id, factor) => api.patch(`/bets/${id}/multiply`, { factor })

/* ---------------- ML Predictions ---------------- */
export const getMatchPrediction = (matchId) => api.get(`/predictions/matches/${matchId}`)
export const retrainMlModel = () => api.post('/predictions/admin/ml/retrain')

/* ---------------- Statistics ---------------- */
export const getMyStatistics = () => api.get('/statistics/users/me')
export const getUserStatisticsAdmin = (userId) => api.get(`/statistics/admin/users/${userId}`)
export const getTeamStatistics = (team) => api.get('/statistics/team', { params: { team } })
export const getSystemStatistics = () => api.get('/statistics/admin/system')
export const getMatchStatisticsAdmin = (matchId) => api.get(`/statistics/admin/matches/${matchId}`)

/* ---------------- Reports (CSV downloads) ---------------- */
const downloadCsv = async (url, params, filename) => {
  const res = await api.get(url, { params, responseType: 'blob' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(res.data)
  link.download = filename
  link.click()
  URL.revokeObjectURL(link.href)
}
export const downloadSystemCsv = () => downloadCsv('/reports/admin/system/csv', {}, 'estatisticas_sistema.csv')
export const downloadUserCsv = (cpf) => downloadCsv('/reports/admin/user/csv', { cpf }, `usuario_${cpf}.csv`)
export const downloadMatchCsv = (matchId) =>
  downloadCsv('/reports/admin/match/csv', { match_id: matchId }, `partida_${matchId}.csv`)
export const downloadTeamCsv = (team) =>
  downloadCsv('/reports/admin/team/csv', { team }, `selecao_${team}.csv`)
