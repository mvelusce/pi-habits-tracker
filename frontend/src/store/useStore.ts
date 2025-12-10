import { create } from 'zustand'
import { LifestyleFactor, LifestyleFactorEntry, MoodEntry } from '../lib/api'

interface Store {
  lifestyleFactors: LifestyleFactor[]
  lifestyleFactorEntries: LifestyleFactorEntry[]
  moodEntries: MoodEntry[]
  selectedDate: Date
  
  setLifestyleFactors: (lifestyleFactors: LifestyleFactor[]) => void
  setLifestyleFactorEntries: (entries: LifestyleFactorEntry[]) => void
  setMoodEntries: (entries: MoodEntry[]) => void
  setSelectedDate: (date: Date) => void
  
  addLifestyleFactor: (lifestyleFactor: LifestyleFactor) => void
  updateLifestyleFactor: (id: number, lifestyleFactor: Partial<LifestyleFactor>) => void
  removeLifestyleFactor: (id: number) => void
  
  addLifestyleFactorEntry: (entry: LifestyleFactorEntry) => void
  updateLifestyleFactorEntry: (id: number, entry: Partial<LifestyleFactorEntry>) => void
  
  addMoodEntry: (entry: MoodEntry) => void
  updateMoodEntry: (id: number, entry: Partial<MoodEntry>) => void
  removeMoodEntry: (id: number) => void
}

export const useStore = create<Store>((set) => ({
  lifestyleFactors: [],
  lifestyleFactorEntries: [],
  moodEntries: [],
  selectedDate: new Date(),
  
  setLifestyleFactors: (lifestyleFactors) => set({ lifestyleFactors }),
  setLifestyleFactorEntries: (entries) => set({ lifestyleFactorEntries: entries }),
  setMoodEntries: (entries) => set({ moodEntries: entries }),
  setSelectedDate: (date) => set({ selectedDate: date }),
  
  addLifestyleFactor: (lifestyleFactor) => set((state) => ({ lifestyleFactors: [...state.lifestyleFactors, lifestyleFactor] })),
  updateLifestyleFactor: (id, lifestyleFactorUpdate) => set((state) => ({
    lifestyleFactors: state.lifestyleFactors.map((lf) => lf.id === id ? { ...lf, ...lifestyleFactorUpdate } : lf)
  })),
  removeLifestyleFactor: (id) => set((state) => ({
    lifestyleFactors: state.lifestyleFactors.filter((lf) => lf.id !== id)
  })),
  
  addLifestyleFactorEntry: (entry) => set((state) => {
    const existing = state.lifestyleFactorEntries.findIndex(
      (e) => e.lifestyle_factor_id === entry.lifestyle_factor_id && e.date === entry.date
    )
    if (existing >= 0) {
      const newEntries = [...state.lifestyleFactorEntries]
      newEntries[existing] = entry
      return { lifestyleFactorEntries: newEntries }
    }
    return { lifestyleFactorEntries: [...state.lifestyleFactorEntries, entry] }
  }),
  updateLifestyleFactorEntry: (id, entryUpdate) => set((state) => ({
    lifestyleFactorEntries: state.lifestyleFactorEntries.map((e) => e.id === id ? { ...e, ...entryUpdate } : e)
  })),
  
  addMoodEntry: (entry) => set((state) => ({ moodEntries: [...state.moodEntries, entry] })),
  updateMoodEntry: (id, entryUpdate) => set((state) => ({
    moodEntries: state.moodEntries.map((e) => e.id === id ? { ...e, ...entryUpdate } : e)
  })),
  removeMoodEntry: (id) => set((state) => ({
    moodEntries: state.moodEntries.filter((e) => e.id !== id)
  })),
}))

