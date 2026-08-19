export default function EmptyState({ title, subtitle }) {
  return (
    <div className="empty-state">
      <div className="h2">{title}</div>
      {subtitle && <p className="muted">{subtitle}</p>}
    </div>
  )
}
