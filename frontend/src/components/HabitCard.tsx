import { useState } from 'react'
import { Habit, HabitEntry } from '../lib/api'
import { Check, Edit2, Trash2 } from 'lucide-react'

interface HabitCardProps {
  habit: Habit
  entry?: HabitEntry
  onToggle: (completed: boolean) => void
  onEdit: () => void
  onDelete: () => void
}

export default function HabitCard({ habit, entry, onToggle, onEdit, onDelete }: HabitCardProps) {
  const [showMenu, setShowMenu] = useState(false)
  const isCompleted = entry?.completed || false

  return (
    <div
      className="relative bg-white rounded-lg shadow-md p-4 transition-all hover:shadow-lg"
      style={{ borderLeft: `4px solid ${habit.color}` }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3 flex-1">
          <button
            onClick={() => onToggle(!isCompleted)}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
              isCompleted
                ? 'bg-primary-500 text-white scale-110'
                : 'border-2 border-gray-300 hover:border-primary-500'
            }`}
          >
            {isCompleted ? <Check size={24} /> : habit.icon || '✓'}
          </button>
          
          <div className="flex-1">
            <h3 className={`font-semibold text-lg ${isCompleted ? 'line-through text-gray-500' : ''}`}>
              {habit.name}
            </h3>
            {habit.description && (
              <p className="text-sm text-gray-600">{habit.description}</p>
            )}
          </div>
        </div>

        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-2 hover:bg-gray-100 rounded"
          >
            ⋮
          </button>
          
          {showMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 z-10">
              <button
                onClick={() => {
                  onEdit()
                  setShowMenu(false)
                }}
                className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center space-x-2"
              >
                <Edit2 size={16} />
                <span>Edit</span>
              </button>
              <button
                onClick={() => {
                  onDelete()
                  setShowMenu(false)
                }}
                className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center space-x-2 text-red-600"
              >
                <Trash2 size={16} />
                <span>Delete</span>
              </button>
            </div>
          )}
        </div>
      </div>
      
      {isCompleted && entry?.notes && (
        <div className="mt-2 text-sm text-gray-600 bg-gray-50 p-2 rounded">
          💭 {entry.notes}
        </div>
      )}
    </div>
  )
}

