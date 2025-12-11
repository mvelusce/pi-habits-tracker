import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { api } from '../lib/api'

interface AuthContextType {
  isAuthenticated: boolean
  isLoading: boolean
  setupComplete: boolean
  login: (username: string, password: string) => Promise<void>
  register: (username: string, password: string) => Promise<void>
  logout: () => void
  checkSetup: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [setupComplete, setSetupComplete] = useState(false)

  const checkSetup = async () => {
    try {
      const response = await api.get('/api/auth/check-setup')
      setSetupComplete(response.data.setup_complete)
    } catch (error) {
      console.error('Error checking setup:', error)
    }
  }

  const checkAuth = async () => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      setIsAuthenticated(false)
      setIsLoading(false)
      return
    }

    try {
      // Verify token is still valid
      await api.get('/api/auth/me')
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Token validation failed:', error)
      localStorage.removeItem('auth_token')
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    const init = async () => {
      await checkSetup()
      await checkAuth()
    }
    init()
  }, [])

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', { username, password })
      const { access_token } = response.data
      localStorage.setItem('auth_token', access_token)
      setIsAuthenticated(true)
      setSetupComplete(true)
    } catch (error: any) {
      console.error('Login failed:', error)
      throw new Error(error.response?.data?.detail || 'Login failed')
    }
  }

  const register = async (username: string, password: string) => {
    try {
      await api.post('/api/auth/register', { username, password })
      // After registration, log in automatically
      await login(username, password)
    } catch (error: any) {
      console.error('Registration failed:', error)
      throw new Error(error.response?.data?.detail || 'Registration failed')
    }
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isLoading,
        setupComplete,
        login,
        register,
        logout,
        checkSetup,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

