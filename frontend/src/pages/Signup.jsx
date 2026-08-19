import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

const initialForm = {
  nickname: '', email: '', cpf: '', password: '', date_of_birth: '',
}

export default function Signup() {
  const { register } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    const result = await register(form)
    setLoading(false)
    if (result.ok) {
      toast.success('Conta criada! Faça login para continuar.')
      navigate('/login')
    } else {
      setError(result.message)
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card" style={{ maxWidth: 460 }}>
        <h1 className="auth-title">Criar conta</h1>
        <p className="auth-sub">Você começa com 100 pontos para apostar na Copa do Mundo 2026.</p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="nickname">Apelido</label>
            <input id="nickname" required minLength={3} value={form.nickname} onChange={update('nickname')} placeholder="craque2026" />
          </div>
          <div className="field">
            <label htmlFor="email">E-mail</label>
            <input id="email" type="email" required value={form.email} onChange={update('email')} placeholder="voce@email.com" />
          </div>
          <div className="field">
            <label htmlFor="cpf">CPF</label>
            <input id="cpf" required minLength={11} maxLength={14} value={form.cpf} onChange={update('cpf')} placeholder="000.000.000-00" />
          </div>
          <div className="field">
            <label htmlFor="dob">Data de nascimento</label>
            <input id="dob" type="date" required value={form.date_of_birth} onChange={update('date_of_birth')} />
            <p className="field-hint">É preciso ser maior de 18 anos para apostar.</p>
          </div>
          <div className="field">
            <label htmlFor="password">Senha</label>
            <input id="password" type="password" required minLength={8} value={form.password} onChange={update('password')} placeholder="••••••••" />
            <p className="field-hint">8+ caracteres, com maiúscula, minúscula, número e símbolo.</p>
          </div>
          <button className="btn btn-primary btn-block" type="submit" disabled={loading}>
            {loading ? 'Criando conta…' : 'Criar conta'}
          </button>
        </form>

        <div className="auth-switch">
          Já tem conta? <Link to="/login">Entrar</Link>
        </div>
      </div>
    </div>
  )
}
