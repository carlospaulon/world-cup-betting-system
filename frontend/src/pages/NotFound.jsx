import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="container page" style={{ textAlign: 'center', paddingTop: 100 }}>
      <p className="eyebrow">Erro 404</p>
      <h1 className="h1" style={{ marginBottom: 14 }}>Fora de campo</h1>
      <p className="muted" style={{ marginBottom: 24 }}>Essa página não existe.</p>
      <Link className="btn btn-primary" to="/">Voltar ao início</Link>
    </div>
  )
}
