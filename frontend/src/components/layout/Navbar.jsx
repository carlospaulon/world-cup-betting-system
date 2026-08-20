import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { formatPoints } from '../../utils/format'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand">
          <span className="brand-mark">PC</span>
          <span className="brand-name">Palpite<span>Copa</span></span>
        </div>

        <nav className="nav-links">
          <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Partidas</NavLink>
          <NavLink to="/minhas-apostas" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Minhas apostas</NavLink>
          <NavLink to="/ranking" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Ranking</NavLink>
          <NavLink to="/selecoes" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Seleções</NavLink>
          <NavLink to="/perfil" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Perfil</NavLink>
          {user.is_admin && (
            <NavLink to="/admin" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>Admin</NavLink>
          )}
        </nav>

        <div className="nav-user">
          <span className="nav-points">{formatPoints(user.points)} pts</span>
          <button className="btn btn-ghost btn-sm" onClick={handleLogout}>Sair</button>
        </div>
      </div>
    </header>
  )
}
