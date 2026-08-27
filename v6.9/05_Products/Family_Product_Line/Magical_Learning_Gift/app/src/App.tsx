import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import GuardianDashboard from './pages/GuardianDashboard'
import PlayHome from './pages/PlayHome'
import ModulePlay from './pages/ModulePlay'
import Privacy from './pages/Privacy'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/guardian/dashboard" element={<GuardianDashboard />} />
      <Route path="/play" element={<PlayHome />} />
      <Route path="/play/module/:moduleKey" element={<ModulePlay />} />
      <Route path="/privacy" element={<Privacy />} />
    </Routes>
  )
}

export default App
