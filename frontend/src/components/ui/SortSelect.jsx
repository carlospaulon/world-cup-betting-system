export default function SortSelect({ value, onChange, label = 'Ordenar' }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      aria-label={label}
    >
      <option value="desc">Mais recentes primeiro</option>
      <option value="asc">Mais antigas primeiro</option>
    </select>
  )
}
