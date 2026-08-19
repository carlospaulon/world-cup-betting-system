import { useEffect, useState } from 'react'
import {
  getAllUsersAdmin, getUserByCpfAdmin, promoteToAdmin, downloadUserCsv, extractErrorMessage,
} from '../../api/client'
import Loading from '../../components/ui/Loading'
import EmptyState from '../../components/ui/EmptyState'
import { useToast } from '../../context/ToastContext'
import { formatDateShort, formatPoints } from '../../utils/format'

export default function AdminUsers() {
  const toast = useToast()
  const [users, setUsers] = useState(null)
  const [cpf, setCpf] = useState('')
  const [busyId, setBusyId] = useState(null)

  const load = () => {
    setUsers(null)
    getAllUsersAdmin()
      .then(({ data }) => setUsers(data))
      .catch((err) => { toast.error(extractErrorMessage(err)); setUsers([]) })
  }

  useEffect(load, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!cpf.trim()) { load(); return }
    try {
      const { data } = await getUserByCpfAdmin(cpf.trim())
      setUsers(Array.isArray(data) ? data : [data])
    } catch (err) {
      toast.error(extractErrorMessage(err))
      setUsers([])
    }
  }

  const handlePromote = async (userId) => {
    setBusyId(userId)
    try {
      await promoteToAdmin(userId)
      toast.success('Usuário promovido a administrador.')
      load()
    } catch (err) {
      toast.error(extractErrorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div>
      <form className="filterbar" onSubmit={handleSearch}>
        <input placeholder="Buscar por CPF…" value={cpf} onChange={(e) => setCpf(e.target.value)} style={{ minWidth: 220 }} />
        <button className="btn btn-primary btn-sm" type="submit">Buscar</button>
        {cpf && <button type="button" className="btn btn-ghost btn-sm" onClick={() => { setCpf(''); load() }}>Limpar</button>}
      </form>

      {users === null ? (
        <Loading />
      ) : users.length === 0 ? (
        <EmptyState title="Nenhum usuário encontrado" />
      ) : (
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th>Apelido</th><th>E-mail</th><th>CPF</th><th>Cadastro</th><th>Pontos</th><th>Status</th><th></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.nickname}</td>
                  <td>{u.email}</td>
                  <td>{u.cpf}</td>
                  <td>{formatDateShort(u.created_at)}</td>
                  <td>{formatPoints(u.points)}</td>
                  <td style={{ display: 'flex', gap: 6 }}>
                    {u.is_admin && <span className="badge-admin">Admin</span>}
                    {!u.is_active && <span className="badge-inactive">Inativo</span>}
                  </td>
                  <td style={{ display: 'flex', gap: 6 }}>
                    {!u.is_admin && (
                      <button className="btn btn-ghost btn-sm" disabled={busyId === u.id} onClick={() => handlePromote(u.id)}>
                        {busyId === u.id ? '…' : 'Promover'}
                      </button>
                    )}
                    <button className="btn btn-ghost btn-sm" onClick={() => downloadUserCsv(u.cpf)}>CSV</button>
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
