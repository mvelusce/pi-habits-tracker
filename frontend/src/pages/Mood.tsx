import { useEffect, useState } from 'react'
import { moodApi, MoodEntry } from '../lib/api'
import { formatDate, formatDisplayDate, getMoodEmoji } from '../lib/utils'
import MoodPicker from '../components/MoodPicker'
import { Smile } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Mood() {
  const [loading, setLoading] = useState(true)
  const [recentEntries, setRecentEntries] = useState<MoodEntry[]>([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    mood_score: 5,
    energy_level: 5,
    stress_level: 5,
    notes: '',
    tags: ''
  })

  useEffect(() => {
    loadMoodEntries()
  }, [])

  const loadMoodEntries = async () => {
    try {
      setLoading(true)
      const response = await moodApi.getAll(undefined, undefined, 30)
      setRecentEntries(response.data)
    } catch (error) {
      console.error('Error loading mood entries:', error)
      toast.error('Failed to load mood entries')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await moodApi.create({
        date: formatDate(new Date()),
        mood_score: formData.mood_score,
        energy_level: formData.energy_level,
        stress_level: formData.stress_level,
        notes: formData.notes || undefined,
        tags: formData.tags || undefined
      })

      setRecentEntries([response.data, ...recentEntries])
      setFormData({
        mood_score: 5,
        energy_level: 5,
        stress_level: 5,
        notes: '',
        tags: ''
      })
      setShowForm(false)
      toast.success('Mood logged successfully! 😊')
    } catch (error) {
      console.error('Error creating mood entry:', error)
      toast.error('Failed to log mood')
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this mood entry?')) {
      return
    }

    try {
      await moodApi.delete(id)
      setRecentEntries(recentEntries.filter(e => e.id !== id))
      toast.success('Mood entry deleted')
    } catch (error) {
      console.error('Error deleting mood entry:', error)
      toast.error('Failed to delete mood entry')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const todayEntries = recentEntries.filter(e => e.date === formatDate(new Date()))
  const averageToday = todayEntries.length > 0
    ? todayEntries.reduce((sum, e) => sum + e.mood_score, 0) / todayEntries.length
    : null

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Mood Tracker</h1>
        <Smile className="text-primary-600" size={28} />
      </div>

      {/* Today's Summary */}
      {averageToday !== null && (
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg shadow-md p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-1">Today's Mood</h2>
              <p className="text-3xl font-bold">{averageToday.toFixed(1)}/10</p>
              <p className="text-sm text-purple-100 mt-1">{todayEntries.length} check-in(s)</p>
            </div>
            <div className="text-6xl">{getMoodEmoji(Math.round(averageToday))}</div>
          </div>
        </div>
      )}

      {/* Log Mood Button */}
      {!showForm && (
        <button
          onClick={() => setShowForm(true)}
          className="w-full bg-primary-600 text-white py-4 rounded-lg hover:bg-primary-700 font-semibold text-lg shadow-md"
        >
          + Log Your Mood
        </button>
      )}

      {/* Mood Entry Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <h3 className="text-xl font-semibold">How are you feeling?</h3>

          <MoodPicker
            value={formData.mood_score}
            onChange={(value) => setFormData({ ...formData, mood_score: value })}
            label="Overall Mood"
          />

          <MoodPicker
            value={formData.energy_level}
            onChange={(value) => setFormData({ ...formData, energy_level: value })}
            label="Energy Level"
          />

          <MoodPicker
            value={formData.stress_level}
            onChange={(value) => setFormData({ ...formData, stress_level: value })}
            label="Stress Level"
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes (Optional)
            </label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="What's on your mind?"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tags (Optional)
            </label>
            <input
              type="text"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="work, exercise, social..."
            />
          </div>

          <div className="flex space-x-3">
            <button
              type="submit"
              className="flex-1 bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 font-semibold"
            >
              Save Mood
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg hover:bg-gray-300 font-semibold"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Recent Entries */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Check-ins</h2>
        
        {recentEntries.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
            <p>No mood entries yet. Log your first one!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {recentEntries.map((entry) => (
              <div key={entry.id} className="bg-white rounded-lg shadow-md p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl">{getMoodEmoji(entry.mood_score)}</span>
                    <div>
                      <p className="font-semibold text-lg">{entry.mood_score}/10</p>
                      <p className="text-sm text-gray-600">
                        {formatDisplayDate(entry.date)} • {new Date(entry.time).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(entry.id)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Delete
                  </button>
                </div>

                {(entry.energy_level || entry.stress_level) && (
                  <div className="flex space-x-4 text-sm text-gray-600 mb-2">
                    {entry.energy_level && (
                      <span>⚡ Energy: {entry.energy_level}/10</span>
                    )}
                    {entry.stress_level && (
                      <span>😰 Stress: {entry.stress_level}/10</span>
                    )}
                  </div>
                )}

                {entry.notes && (
                  <p className="text-gray-700 bg-gray-50 p-2 rounded mt-2">
                    {entry.notes}
                  </p>
                )}

                {entry.tags && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {entry.tags.split(',').map((tag, i) => (
                      <span
                        key={i}
                        className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs"
                      >
                        {tag.trim()}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

