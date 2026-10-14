export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <span className="logo-icon">⬡</span>
        <span className="logo-text">TaskBoard</span>
      </div>
      <nav className="sidebar-nav">
        <div className="nav-section-label">WORKSPACE</div>
        <a href="#" className="nav-item active">
          <span className="nav-icon">▦</span> Dashboard
        </a>
        <a href="#" className="nav-item">
          <span className="nav-icon">☰</span> All Tasks
        </a>
        <a href="#" className="nav-item">
          <span className="nav-icon">◈</span> Projects
        </a>
        <a href="#" className="nav-item">
          <span className="nav-icon">◷</span> Timeline
        </a>
        <div className="nav-section-label">TEAM</div>
        <a href="#" className="nav-item">
          <span className="nav-icon">⊕</span> Members
        </a>
        <a href="#" className="nav-item">
          <span className="nav-icon">◎</span> Reports
        </a>
        <div className="nav-section-label">SETTINGS</div>
        <a href="#" className="nav-item">
          <span className="nav-icon">⚙</span> Settings
        </a>
      </nav>
      <div className="sidebar-footer">
        <div className="user-avatar">A</div>
        <div className="user-info">
          <span className="user-name">Admin User</span>
          <span className="user-role">Administrator</span>
        </div>
      </div>
    </aside>
  )
}
