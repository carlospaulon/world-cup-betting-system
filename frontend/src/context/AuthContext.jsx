import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { getMe, loginUser, registerUser, extractErrorMessage } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadMe = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setLoading(false)
      return
    }
    try {
      const { data } = await getMe()
      setUser(data)
    } catch {
      localStorage.removeItem('access_token')
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadMe()
  }, [loadMe])

  const login = async (email, password) => {
    try {
      const { data } = await loginUser(email, password)
      localStorage.setItem('access_token', data.access_token)
      await loadMe()
      return { ok: true }
    } catch (err) {
      return { ok: false, message: extractErrorMessage(err) }
    }
  }

  const register = async (payload) => {
    try {
      await registerUser(payload)
      return { ok: true }
    } catch (err) {
      return { ok: false, message: extractErrorMessage(err) }
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  const refreshUser = () => loadMe()

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
