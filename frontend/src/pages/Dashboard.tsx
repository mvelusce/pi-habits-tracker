import { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import { habitsApi, habitEntriesApi, moodApi } from '../lib/api'
import { formatDate, formatDisplayDate, getMoodEmoji } from '../lib/utils'
import HabitCard from '../components/HabitCard'
import { Calendar, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { habits, setHabits, habitEntries, setHabitEntries, selectedDate, setSelectedDate } = useStore()
  const [loading, setLoading] = useState(true)
  const [todayMood, setTodayMood] = useState<number | null>(null)

  useEffect(() => {
    loadData()
  }, [selectedDate])

  const loadData = async () => {
    try {
      setLoading(true)
      const [habitsRes, entriesRes, moodRes] = await Promise.all([
        habitsApi.getAll(),
        habitEntriesApi.getByDate(formatDate(selectedDate)),
        moodApi.getByDate(formatDate(selectedDate))
      ])
      
      setHabits(habitsRes.data)
      setHabitEntries(entriesRes.data)
      
      if (moodRes.data.length > 0) {
        const avgMood = moodRes.data.reduce((sum, m) => sum + m.mood_score, 0) / moodRes.data.length
        setTodayMood(Math.round(avgMood))
      } else {
        setTodayMood(null)
      }
    } catch (error) {
      console.error('Error loading data:', error)
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleHabit = async (habitId: number, completed: boolean) => {
    try {
      const response = await habitEntriesApi.create({
        habit_id: habitId,
        date: formatDate(selectedDate),
        completed
      })
      
      const existing = habitEntries.findIndex(
        e => e.habit_id === habitId && e.date === formatDate(selectedDate)
      )
      
      if (existing >= 0) {
        const newEntries = [...habitEntries]
        newEntries[existing] = response.data
        setHabitEntries(newEntries)
      } else {
        setHabitEntries([...habitEntries, response.data])
      }
      
      toast.success(completed ? 'Habit completed! 🎉' : 'Habit unchecked')
    } catch (error) {
      console.error('Error toggling habit:', error)
      toast.error('Failed to update habit')
    }
  }

  const changeDate = (days: number) => {
    const newDate = new Date(selectedDate)
    newDate.setDate(newDate.getDate() + days)
    setSelectedDate(newDate)
  }

  const isToday = formatDate(selectedDate) === formatDate(new Date())
  const completedCount = habitEntries.filter(e => e.completed).length
  const totalCount = habits.filter(h => h.is_active).length
  const completionRate = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Date Selector */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center justify-between">
          <button
            onClick={() => changeDate(-1)}
            className="p-2 hover:bg-gray-100 rounded-lg text-gray-800 font-semibold text-xl"
          >
            ←
          </button>
          
          <div className="flex items-center space-x-2">
            <Calendar className="text-primary-600" size={20} />
            <span className="text-lg font-semibold text-gray-800">
              {isToday ? 'Today' : formatDisplayDate(selectedDate)}
            </span>
          </div>
          
          <button
            onClick={() => changeDate(1)}
            className="p-2 hover:bg-gray-100 rounded-lg text-gray-800 font-semibold text-xl disabled:text-gray-400"
            disabled={isToday}
          >
            →
          </button>
        </div>
        
        {!isToday && (
          <button
            onClick={() => setSelectedDate(new Date())}
            className="w-full mt-2 text-sm text-primary-600 hover:text-primary-700"
          >
            Back to Today
          </button>
        )}
      </div>

      {/* Stats Card */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg shadow-md p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">
              {completedCount} / {totalCount}
            </h2>
            <p className="text-primary-100">Habits Completed</p>
          </div>
          <div className="text-5xl">
            {completionRate === 100 ? '🌟' : completionRate >= 75 ? '🔥' : completionRate >= 50 ? '💪' : '🌱'}
          </div>
        </div>
        
        <div className="bg-white/20 rounded-full h-3 overflow-hidden">
          <div
            className="bg-white h-full transition-all duration-500"
            style={{ width: `${completionRate}%` }}
          />
        </div>
        
        <div className="mt-2 flex items-center justify-between text-sm text-primary-100">
          <span>{completionRate}% Complete</span>
          {todayMood && (
            <span className="flex items-center space-x-1">
              <span>Mood:</span>
              <span className="text-2xl">{getMoodEmoji(todayMood)}</span>
              <span>{todayMood}/10</span>
            </span>
          )}
        </div>
      </div>

      {/* Habits List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">Your Habits</h2>
          <TrendingUp className="text-primary-600" size={24} />
        </div>
        
        {habits.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-500 mb-4">No habits yet. Create your first habit!</p>
            <a
              href="/habits"
              className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700"
            >
              Create Habit
            </a>
          </div>
        ) : (
          <div className="space-y-3">
            {habits
              .filter(h => h.is_active)
              .map(habit => {
                const entry = habitEntries.find(
                  e => e.habit_id === habit.id && e.date === formatDate(selectedDate)
                )
                
                return (
                  <HabitCard
                    key={habit.id}
                    habit={habit}
                    entry={entry}
                    onToggle={(completed) => handleToggleHabit(habit.id, completed)}
                    onEdit={() => {/* Navigate to edit */}}
                    onDelete={() => {/* Handle delete */}}
                  />
                )
              })}
          </div>
        )}
      </div>
    </div>
  )
}

