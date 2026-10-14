export default function Header({ onCreateTask, taskCount }) {
  return (
    <header className="dashboard-header">
      <div className="header-left">
        <h1 className="page-title">Dashboard</h1>
        <span className="breadcrumb">Workspace / Dashboard</span>
      </div>
      <div className="header-right">
        <div className="header-meta">
          <span className="task-counter">{taskCount} tasks</span>
        </div>
        <button className="create-btn" onClick={onCreateTask}>
          + New Task
        </button>
      </div>
    </header>
  )
}
