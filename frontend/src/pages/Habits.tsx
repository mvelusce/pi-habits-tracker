import { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import { habitsApi, HabitStats } from '../lib/api'
import { Plus } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Habits() {
  const { habits, setHabits, addHabit, removeHabit } = useStore()
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [habitStats, setHabitStats] = useState<Record<number, HabitStats>>({})
  const [newHabit, setNewHabit] = useState({
    name: '',
    description: '',
    color: '#3B82F6',
    icon: '✓'
  })

  useEffect(() => {
    loadHabits()
  }, [])

  const loadHabits = async () => {
    try {
      setLoading(true)
      const response = await habitsApi.getAll()
      setHabits(response.data)
      
      // Load stats for each habit
      const statsPromises = response.data.map(h => habitsApi.getStats(h.id))
      const statsResults = await Promise.all(statsPromises)
      const statsMap: Record<number, HabitStats> = {}
      statsResults.forEach(res => {
        statsMap[res.data.habit_id] = res.data
      })
      setHabitStats(statsMap)
    } catch (error) {
      console.error('Error loading habits:', error)
      toast.error('Failed to load habits')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateHabit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!newHabit.name.trim()) {
      toast.error('Please enter a habit name')
      return
    }

    try {
      const response = await habitsApi.create(newHabit)
      addHabit(response.data)
      setNewHabit({ name: '', description: '', color: '#3B82F6', icon: '✓' })
      setShowCreateForm(false)
      toast.success('Habit created successfully! 🎉')
      loadHabits() // Reload to get stats
    } catch (error) {
      console.error('Error creating habit:', error)
      toast.error('Failed to create habit')
    }
  }

  const handleDeleteHabit = async (id: number, name: string) => {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) {
      return
    }

    try {
      await habitsApi.delete(id)
      removeHabit(id)
      toast.success('Habit deleted')
      loadHabits()
    } catch (error) {
      console.error('Error deleting habit:', error)
      toast.error('Failed to delete habit')
    }
  }

  const colorOptions = [
    { name: 'Blue', value: '#3B82F6' },
    { name: 'Green', value: '#10B981' },
    { name: 'Purple', value: '#8B5CF6' },
    { name: 'Red', value: '#EF4444' },
    { name: 'Orange', value: '#F59E0B' },
    { name: 'Pink', value: '#EC4899' },
  ]

  const iconOptions = ['✓', '💪', '🏃', '📚', '🧘', '💧', '🍎', '😴', '🎯', '✨']

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Manage Habits</h1>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
        >
          <Plus size={20} />
          <span>New Habit</span>
        </button>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <form onSubmit={handleCreateHabit} className="bg-white rounded-lg shadow-md p-6 space-y-4">
          <h3 className="text-lg font-semibold">Create New Habit</h3>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Habit Name *
            </label>
            <input
              type="text"
              value={newHabit.name}
              onChange={(e) => setNewHabit({ ...newHabit, name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="e.g., Exercise, Read, Meditate"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={newHabit.description}
              onChange={(e) => setNewHabit({ ...newHabit, description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Optional description..."
              rows={2}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Color
            </label>
            <div className="flex space-x-2">
              {colorOptions.map((color) => (
                <button
                  key={color.value}
                  type="button"
                  onClick={() => setNewHabit({ ...newHabit, color: color.value })}
                  className={`w-10 h-10 rounded-lg border-2 ${
                    newHabit.color === color.value ? 'border-gray-800 scale-110' : 'border-gray-300'
                  }`}
                  style={{ backgroundColor: color.value }}
                  title={color.name}
                />
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Icon
            </label>
            <div className="flex flex-wrap gap-2">
              {iconOptions.map((icon) => (
                <button
                  key={icon}
                  type="button"
                  onClick={() => setNewHabit({ ...newHabit, icon })}
                  className={`w-12 h-12 text-2xl border-2 rounded-lg ${
                    newHabit.icon === icon ? 'border-primary-600 bg-primary-50' : 'border-gray-300'
                  }`}
                >
                  {icon}
                </button>
              ))}
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              type="submit"
              className="flex-1 bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700"
            >
              Create Habit
            </button>
            <button
              type="button"
              onClick={() => setShowCreateForm(false)}
              className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Habits List */}
      <div className="space-y-4">
        {habits.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
            <p>No habits yet. Create your first one!</p>
          </div>
        ) : (
          habits
            .filter(h => h.is_active)
            .map((habit) => {
              const stats = habitStats[habit.id]
              
              return (
                <div
                  key={habit.id}
                  className="bg-white rounded-lg shadow-md p-6"
                  style={{ borderLeft: `4px solid ${habit.color}` }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <span className="text-3xl">{habit.icon}</span>
                      <div>
                        <h3 className="text-xl font-semibold">{habit.name}</h3>
                        {habit.description && (
                          <p className="text-sm text-gray-600">{habit.description}</p>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={() => handleDeleteHabit(habit.id, habit.name)}
                      className="text-red-600 hover:text-red-700 text-sm"
                    >
                      Delete
                    </button>
                  </div>

                  {stats && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary-600">
                          {stats.completion_rate.toFixed(0)}%
                        </div>
                        <div className="text-xs text-gray-600">Completion</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                          {stats.current_streak}
                        </div>
                        <div className="text-xs text-gray-600">Current Streak</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">
                          {stats.longest_streak}
                        </div>
                        <div className="text-xs text-gray-600">Best Streak</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-700">
                          {stats.completed_days}/{stats.total_days}
                        </div>
                        <div className="text-xs text-gray-600">Days</div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })
        )}
      </div>
    </div>
  )
}

