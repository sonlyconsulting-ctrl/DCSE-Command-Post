import Header from '../components/Header'
import ModuleCard from '../components/ModuleCard'
import { MODULES } from '../data/modules'

export default function PlayHome() {
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, #F0EDFF 0%, #FFF5F7 100%)' }}>
      <Header variant="child" />

      <div className="container" style={{ padding: '48px 24px' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <p style={{ fontSize: '48px', marginBottom: '8px' }}>✨</p>
          <h1
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.8rem, 4vw, 2.5rem)',
              color: 'var(--color-primary)',
              marginBottom: '8px',
            }}
          >
            Choose Your Adventure!
          </h1>
          <p style={{ color: 'var(--color-text-light)', fontSize: '1.1rem' }}>
            Pick a module to start learning and playing.
          </p>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '24px',
            maxWidth: '900px',
            margin: '0 auto',
          }}
        >
          {MODULES.map(m => (
            <ModuleCard key={m.key} module={m} variant="play" />
          ))}
        </div>
      </div>
    </div>
  )
}
