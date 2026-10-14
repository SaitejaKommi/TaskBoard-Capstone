import { useState, useEffect, useCallback } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Header from './components/Header.jsx'
import KpiCards from './components/KpiCards.jsx'
import TaskTable from './components/TaskTable.jsx'
import CreateTaskModal from './components/CreateTaskModal.jsx'
import ActivityFeed from './components/ActivityFeed.jsx'
import './styles/app.css'

const API_BASE = '/api'

export default function App() {
  const [tasks, setTasks] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [statusFilter, setStatusFilter] = useState('all')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [activities, setActivities] = useState([])

  const fetchAll = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const [tasksRes, statsRes] = await Promise.all([
        fetch(`${API_BASE}/tasks`),
        fetch(`${API_BASE}/tasks/stats`),
      ])
      if (!tasksRes.ok || !statsRes.ok) throw new Error('Failed to fetch data')
      const tasksData = await tasksRes.json()
      const statsData = await statsRes.json()
      setTasks(tasksData)
      setStats(statsData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  const addActivity = (msg) => {
    setActivities(prev => [
      { id: Date.now(), message: msg, time: new Date().toLocaleTimeString() },
      ...prev.slice(0, 9),
    ])
  }

  const handleCreateTask = async (taskData) => {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(taskData),
    })
    if (!res.ok) throw new Error('Failed to create task')
    const newTask = await res.json()
    addActivity(`Task created: "${newTask.title}"`)
    fetchAll()
    return newTask
  }

  const handleUpdateTaskStatus = async (taskId, newStatus) => {
    const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    })
    if (!res.ok) throw new Error('Failed to update task')
    const updated = await res.json()
    addActivity(`Task "${updated.title}" moved to ${newStatus.replace('_', ' ')}`)
    fetchAll()
  }

  const handleDeleteTask = async (taskId, title) => {
    if (!confirm(`Delete task "${title}"?`)) return
    await fetch(`${API_BASE}/tasks/${taskId}`, { method: 'DELETE' })
    addActivity(`Task deleted: "${title}"`)
    fetchAll()
  }

  const filteredTasks = statusFilter === 'all'
    ? tasks
    : tasks.filter(t => t.status === statusFilter)

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Header
          onCreateTask={() => setShowCreateModal(true)}
          taskCount={stats?.total ?? 0}
        />
        {error && (
          <div className="error-banner">
            ⚠️ Backend Error: {error}
            <button onClick={fetchAll} className="retry-btn">Retry</button>
          </div>
        )}
        {loading ? (
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading TaskBoard...</p>
          </div>
        ) : (
          <div className="dashboard-body">
            <KpiCards stats={stats} />
            <div className="content-row">
              <div className="table-section">
                <div className="filter-bar">
                  {['all', 'todo', 'in_progress', 'review', 'done'].map(s => (
                    <button
                      key={s}
                      className={`filter-btn ${statusFilter === s ? 'active' : ''}`}
                      onClick={() => setStatusFilter(s)}
                    >
                      {s === 'all' ? 'All' : s.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}
                    </button>
                  ))}
                </div>
                <TaskTable
                  tasks={filteredTasks}
                  onUpdateStatus={handleUpdateTaskStatus}
                  onDelete={handleDeleteTask}
                />
              </div>
              <ActivityFeed activities={activities} />
            </div>
          </div>
        )}
      </div>
      {showCreateModal && (
        <CreateTaskModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateTask}
        />
      )}
    </div>
  )
}
