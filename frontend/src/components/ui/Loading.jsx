export default function Loading({ label = 'Carregando…' }) {
  return (
    <div className="loading-wrap">
      <span className="spinner" />
      {label}
    </div>
  )
}
