const STATUS_COLORS = {
  todo: '#f59e0b',
  in_progress: '#3b82f6',
  review: '#8b5cf6',
  done: '#10b981',
}

const PRIORITY_COLORS = {
  low: '#6b7280',
  medium: '#3b82f6',
  high: '#f59e0b',
  critical: '#ef4444',
}

export default function TaskTable({ tasks, onUpdateStatus, onDelete }) {
  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <span className="empty-icon">◈</span>
        <p>No tasks found. Create your first task!</p>
      </div>
    )
  }

  return (
    <div className="task-table-wrapper">
      <table className="task-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Assignee</th>
            <th>Due Date</th>
            <th>Tags</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id}>
              <td className="task-title-cell">
                <span className="task-title">{task.title}</span>
                {task.description && (
                  <span className="task-desc">{task.description}</span>
                )}
              </td>
              <td>
                <select
                  className="status-select"
                  value={task.status}
                  style={{ '--status-color': STATUS_COLORS[task.status] }}
                  onChange={(e) => onUpdateStatus(task.id, e.target.value)}
                >
                  <option value="todo">To Do</option>
                  <option value="in_progress">In Progress</option>
                  <option value="review">Review</option>
                  <option value="done">Done</option>
                </select>
              </td>
              <td>
                <span
                  className="priority-badge"
                  style={{ '--priority-color': PRIORITY_COLORS[task.priority] }}
                >
                  {task.priority}
                </span>
              </td>
              <td>
                {task.assignee ? (
                  <span className="assignee-chip">{task.assignee}</span>
                ) : (
                  <span className="unassigned">—</span>
                )}
              </td>
              <td className="due-date">{task.due_date || '—'}</td>
              <td>
                {task.tags
                  ? task.tags.split(',').map((t) => (
                      <span key={t} className="tag-chip">{t.trim()}</span>
                    ))
                  : '—'}
              </td>
              <td>
                <button
                  className="delete-btn"
                  onClick={() => onDelete(task.id, task.title)}
                  title="Delete task"
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
