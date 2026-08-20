import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ToastProvider } from './context/ToastContext'
import Navbar from './components/layout/Navbar'
import { ProtectedRoute, AdminRoute, GuestRoute } from './components/layout/RouteGuards'

import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import MatchDetail from './pages/MatchDetail'
import MyBets from './pages/MyBets'
import Ranking from './pages/Ranking'
import TeamStats from './pages/TeamStats'
import Profile from './pages/Profile'
import NotFound from './pages/NotFound'

import AdminLayout from './pages/admin/AdminLayout'
import AdminMatches from './pages/admin/AdminMatches'
import AdminMatchBets from './pages/admin/AdminMatchBets'
import AdminUsers from './pages/admin/AdminUsers'
import AdminReports from './pages/admin/AdminReports'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <div className="app-shell">
            <Navbar />

            <Routes>
              <Route element={<GuestRoute />}>
                <Route path="/login" element={<Login />} />
                <Route path="/cadastro" element={<Signup />} />
              </Route>

              <Route element={<ProtectedRoute />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/partidas/:id" element={<MatchDetail />} />
                <Route path="/minhas-apostas" element={<MyBets />} />
                <Route path="/ranking" element={<Ranking />} />
                <Route path="/selecoes" element={<TeamStats />} />
                <Route path="/perfil" element={<Profile />} />
              </Route>

              <Route element={<AdminRoute />}>
                <Route path="/admin" element={<AdminLayout />}>
                  <Route index element={<AdminMatches />} />
                  <Route path="usuarios" element={<AdminUsers />} />
                  <Route path="relatorios" element={<AdminReports />} />
                </Route>
                <Route path="/admin/partidas/:id/apostas" element={<AdminMatchBets />} />
              </Route>

              <Route path="*" element={<NotFound />} />
            </Routes>

            <footer className="footer">PalpiteCopa · Projeto Futuro Digital · Copa do Mundo 2026</footer>
          </div>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}
