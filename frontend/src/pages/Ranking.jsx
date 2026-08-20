import { useEffect, useState } from 'react'
import { getRanking, extractErrorMessage } from '../api/client'
import Loading from '../components/ui/Loading'
import EmptyState from '../components/ui/EmptyState'
import { useToast } from '../context/ToastContext'
import { formatPoints } from '../utils/format'

export default function Ranking() {
  const toast = useToast()
  const [rows, setRows] = useState(null)

  useEffect(() => {
    getRanking()
      .then(({ data }) => setRows(data))
      .catch((err) => { toast.error(extractErrorMessage(err)); setRows([]) })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Classificação</p>
          <h1 className="h1">Ranking de apostadores</h1>
        </div>
      </div>

      {rows === null ? (
        <Loading />
      ) : rows.length === 0 ? (
        <EmptyState title="Ranking ainda vazio" subtitle="Assim que houver apostas ganhas, o ranking aparece aqui." />
      ) : (
        <table className="rank-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Apostador</th>
              <th>Acertos</th>
              <th style={{ textAlign: 'right' }}>Pontos</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={`${r.nickname}-${i}`}>
                <td className={`rank-pos${i < 3 ? ' top' : ''}`}>{i + 1}</td>
                <td>{r.nickname}</td>
                <td>{r.bets_wins}</td>
                <td className="rank-points">{formatPoints(r.points)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
