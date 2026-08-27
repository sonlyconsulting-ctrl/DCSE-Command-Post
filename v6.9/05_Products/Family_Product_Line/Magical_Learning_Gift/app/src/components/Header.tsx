import { useNavigate, useLocation } from 'react-router-dom'

interface Props {
  variant?: 'default' | 'guardian' | 'child'
}

export default function Header({ variant = 'default' }: Props) {
  const navigate = useNavigate()
  const location = useLocation()

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <header
      style={{
        background: variant === 'child'
          ? 'linear-gradient(135deg, #6C63FF 0%, #C77DFF 100%)'
          : 'var(--color-surface)',
        borderBottom: variant === 'child' ? 'none' : '1px solid var(--color-border)',
        padding: '0 24px',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        boxShadow: 'var(--shadow-sm)',
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '64px',
        }}
      >
        <button
          onClick={() => navigate('/')}
          aria-label="Go to home page"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            background: 'none',
            padding: '4px',
          }}
        >
          <span style={{ fontSize: '28px' }}>✨</span>
          <span
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '1.2rem',
              color: variant === 'child' ? '#fff' : 'var(--color-primary)',
            }}
          >
            Magical Learning Gift
          </span>
        </button>

        <nav style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          {variant !== 'child' && (
            <>
              <NavButton
                label="Home"
                onClick={() => navigate('/')}
                active={location.pathname === '/'}
              />
              <NavButton
                label="Guardian"
                onClick={() => navigate('/guardian/dashboard')}
                active={isActive('/guardian')}
              />
              <NavButton
                label="Play"
                onClick={() => navigate('/play')}
                active={isActive('/play')}
                highlight
              />
            </>
          )}
          {variant === 'child' && (
            <NavButton
              label="Back to Modules"
              onClick={() => navigate('/play')}
              active={false}
              light
            />
          )}
        </nav>
      </div>
    </header>
  )
}

function NavButton({
  label,
  onClick,
  active,
  highlight,
  light,
}: {
  label: string
  onClick: () => void
  active: boolean
  highlight?: boolean
  light?: boolean
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '8px 16px',
        borderRadius: 'var(--radius-sm)',
        fontSize: '0.9rem',
        fontWeight: 700,
        background: highlight
          ? 'var(--color-primary)'
          : active
            ? 'var(--color-primary)12'
            : 'transparent',
        color: light
          ? '#fff'
          : highlight
            ? '#fff'
            : active
              ? 'var(--color-primary)'
              : 'var(--color-text-light)',
        border: light ? '2px solid rgba(255,255,255,0.5)' : 'none',
        transition: 'background 0.15s ease',
      }}
    >
      {label}
    </button>
  )
}
