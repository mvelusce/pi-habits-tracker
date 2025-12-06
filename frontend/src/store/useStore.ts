import { create } from 'zustand'
import { Habit, HabitEntry, MoodEntry } from '../lib/api'

interface Store {
  habits: Habit[]
  habitEntries: HabitEntry[]
  moodEntries: MoodEntry[]
  selectedDate: Date
  
  setHabits: (habits: Habit[]) => void
  setHabitEntries: (entries: HabitEntry[]) => void
  setMoodEntries: (entries: MoodEntry[]) => void
  setSelectedDate: (date: Date) => void
  
  addHabit: (habit: Habit) => void
  updateHabit: (id: number, habit: Partial<Habit>) => void
  removeHabit: (id: number) => void
  
  addHabitEntry: (entry: HabitEntry) => void
  updateHabitEntry: (id: number, entry: Partial<HabitEntry>) => void
  
  addMoodEntry: (entry: MoodEntry) => void
  updateMoodEntry: (id: number, entry: Partial<MoodEntry>) => void
  removeMoodEntry: (id: number) => void
}

export const useStore = create<Store>((set) => ({
  habits: [],
  habitEntries: [],
  moodEntries: [],
  selectedDate: new Date(),
  
  setHabits: (habits) => set({ habits }),
  setHabitEntries: (entries) => set({ habitEntries: entries }),
  setMoodEntries: (entries) => set({ moodEntries: entries }),
  setSelectedDate: (date) => set({ selectedDate: date }),
  
  addHabit: (habit) => set((state) => ({ habits: [...state.habits, habit] })),
  updateHabit: (id, habitUpdate) => set((state) => ({
    habits: state.habits.map((h) => h.id === id ? { ...h, ...habitUpdate } : h)
  })),
  removeHabit: (id) => set((state) => ({
    habits: state.habits.filter((h) => h.id !== id)
  })),
  
  addHabitEntry: (entry) => set((state) => {
    const existing = state.habitEntries.findIndex(
      (e) => e.habit_id === entry.habit_id && e.date === entry.date
    )
    if (existing >= 0) {
      const newEntries = [...state.habitEntries]
      newEntries[existing] = entry
      return { habitEntries: newEntries }
    }
    return { habitEntries: [...state.habitEntries, entry] }
  }),
  updateHabitEntry: (id, entryUpdate) => set((state) => ({
    habitEntries: state.habitEntries.map((e) => e.id === id ? { ...e, ...entryUpdate } : e)
  })),
  
  addMoodEntry: (entry) => set((state) => ({ moodEntries: [...state.moodEntries, entry] })),
  updateMoodEntry: (id, entryUpdate) => set((state) => ({
    moodEntries: state.moodEntries.map((e) => e.id === id ? { ...e, ...entryUpdate } : e)
  })),
  removeMoodEntry: (id) => set((state) => ({
    moodEntries: state.moodEntries.filter((e) => e.id !== id)
  })),
}))

