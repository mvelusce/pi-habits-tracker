import { create } from 'zustand'
import { LifestyleFactor, LifestyleFactorEntry, WellbeingMetricEntry } from '../lib/api'

interface Store {
  lifestyleFactors: LifestyleFactor[]
  lifestyleFactorEntries: LifestyleFactorEntry[]
  wellbeingMetricEntries: WellbeingMetricEntry[]
  selectedDate: Date
  
  setLifestyleFactors: (lifestyleFactors: LifestyleFactor[]) => void
  setLifestyleFactorEntries: (entries: LifestyleFactorEntry[]) => void
  setWellbeingMetricEntries: (entries: WellbeingMetricEntry[]) => void
  setSelectedDate: (date: Date) => void
  
  addLifestyleFactor: (lifestyleFactor: LifestyleFactor) => void
  updateLifestyleFactor: (id: number, lifestyleFactor: Partial<LifestyleFactor>) => void
  removeLifestyleFactor: (id: number) => void
  
  addLifestyleFactorEntry: (entry: LifestyleFactorEntry) => void
  updateLifestyleFactorEntry: (id: number, entry: Partial<LifestyleFactorEntry>) => void
  
  addWellbeingMetricEntry: (entry: WellbeingMetricEntry) => void
  updateWellbeingMetricEntry: (id: number, entry: Partial<WellbeingMetricEntry>) => void
  removeWellbeingMetricEntry: (id: number) => void
}

export const useStore = create<Store>((set) => ({
  lifestyleFactors: [],
  lifestyleFactorEntries: [],
  wellbeingMetricEntries: [],
  selectedDate: new Date(),
  
  setLifestyleFactors: (lifestyleFactors) => set({ lifestyleFactors }),
  setLifestyleFactorEntries: (entries) => set({ lifestyleFactorEntries: entries }),
  setWellbeingMetricEntries: (entries) => set({ wellbeingMetricEntries: entries }),
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
  
  addWellbeingMetricEntry: (entry) => set((state) => ({ wellbeingMetricEntries: [...state.wellbeingMetricEntries, entry] })),
  updateWellbeingMetricEntry: (id, entryUpdate) => set((state) => ({
    wellbeingMetricEntries: state.wellbeingMetricEntries.map((e) => e.id === id ? { ...e, ...entryUpdate } : e)
  })),
  removeWellbeingMetricEntry: (id) => set((state) => ({
    wellbeingMetricEntries: state.wellbeingMetricEntries.filter((e) => e.id !== id)
  })),
}))

