export default function ActivityFeed({ activities }) {
  return (
    <aside className="activity-feed">
      <div className="feed-header">
        <h3>Activity Feed</h3>
        <span className="feed-badge">{activities.length}</span>
      </div>
      {activities.length === 0 ? (
        <div className="feed-empty">No recent activity</div>
      ) : (
        <ul className="feed-list">
          {activities.map((a) => (
            <li key={a.id} className="feed-item">
              <span className="feed-dot" />
              <div>
                <p className="feed-msg">{a.message}</p>
                <span className="feed-time">{a.time}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
      <div className="pipeline-indicator">
        <div className="pipeline-label">Pipeline Status</div>
        <div className="pipeline-stages">
          <div className="stage active">Build</div>
          <div className="stage-arrow">→</div>
          <div className="stage active">Test</div>
          <div className="stage-arrow">→</div>
          <div className="stage active">Scan</div>
          <div className="stage-arrow">→</div>
          <div className="stage active">Deploy</div>
        </div>
      </div>
    </aside>
  )
}
