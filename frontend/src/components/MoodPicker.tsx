import { getMoodEmoji } from '../lib/utils'

interface MoodPickerProps {
  value: number
  onChange: (value: number) => void
  label?: string
}

export default function MoodPicker({ value, onChange, label = "How are you feeling?" }: MoodPickerProps) {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <span className="text-4xl">{getMoodEmoji(value)}</span>
          <span className="text-2xl font-bold text-primary-600">{value}/10</span>
        </div>
        
        <input
          type="range"
          min="1"
          max="10"
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          className="w-full h-3 bg-gradient-to-r from-red-400 via-yellow-400 to-green-400 rounded-lg appearance-none cursor-pointer"
          style={{
            accentColor: value >= 7 ? '#10b981' : value >= 4 ? '#fbbf24' : '#ef4444'
          }}
        />
        
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>Very Bad</span>
          <span>Neutral</span>
          <span>Excellent</span>
        </div>
      </div>
    </div>
  )
}

