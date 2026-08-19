import { NavLink, Outlet } from 'react-router-dom'

export default function AdminLayout() {
  return (
    <div className="container page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Painel administrativo</p>
          <h1 className="h1">Administração</h1>
        </div>
      </div>

      <div className="tabs">
        <NavLink to="/admin" end className={({ isActive }) => `tab-btn${isActive ? ' active' : ''}`}>Partidas</NavLink>
        <NavLink to="/admin/usuarios" className={({ isActive }) => `tab-btn${isActive ? ' active' : ''}`}>Usuários</NavLink>
        <NavLink to="/admin/relatorios" className={({ isActive }) => `tab-btn${isActive ? ' active' : ''}`}>Estatísticas &amp; relatórios</NavLink>
      </div>

      <Outlet />
    </div>
  )
}
