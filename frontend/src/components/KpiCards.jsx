export default function KpiCards({ stats }) {
  if (!stats) return null
  const cards = [
    { label: 'Total Tasks', value: stats.total, color: '#6366f1', icon: '◈' },
    { label: 'To Do', value: stats.todo, color: '#f59e0b', icon: '○' },
    { label: 'In Progress', value: stats.in_progress, color: '#3b82f6', icon: '◷' },
    { label: 'In Review', value: stats.review, color: '#8b5cf6', icon: '◎' },
    { label: 'Done', value: stats.done, color: '#10b981', icon: '✓' },
    { label: 'High Priority', value: stats.high_priority, color: '#ef4444', icon: '▲' },
  ]
  return (
    <div className="kpi-grid">
      {cards.map((card) => (
        <div className="kpi-card" key={card.label} style={{ '--card-color': card.color }}>
          <div className="kpi-icon">{card.icon}</div>
          <div className="kpi-content">
            <div className="kpi-value">{card.value}</div>
            <div className="kpi-label">{card.label}</div>
          </div>
          <div className="kpi-bar" />
        </div>
      ))}
    </div>
  )
}
