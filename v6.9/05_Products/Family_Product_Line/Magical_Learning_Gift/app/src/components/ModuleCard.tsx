import { useNavigate } from 'react-router-dom'
import type { LearningModule } from '../data/modules'

interface Props {
  module: LearningModule
  variant?: 'landing' | 'play'
}

export default function ModuleCard({ module, variant = 'landing' }: Props) {
  const navigate = useNavigate()
  const isPlay = variant === 'play'

  return (
    <button
      onClick={() => navigate(`/play/module/${module.key}`)}
      aria-label={`Open ${module.title}`}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: isPlay ? '16px' : '12px',
        padding: isPlay ? '32px 24px' : '24px 20px',
        background: 'var(--color-surface)',
        border: `3px solid ${module.color}30`,
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        cursor: 'pointer',
        width: '100%',
        textAlign: 'center',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-4px)'
        e.currentTarget.style.boxShadow = 'var(--shadow-md)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = 'var(--shadow-sm)'
      }}
    >
      <span
        style={{
          fontSize: isPlay ? '64px' : '48px',
          lineHeight: 1,
          display: 'block',
        }}
        role="img"
        aria-hidden="true"
      >
        {module.emoji}
      </span>
      <div>
        <h3
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: isPlay ? '1.25rem' : '1.1rem',
            color: module.color,
            marginBottom: '4px',
          }}
        >
          {module.title}
        </h3>
        <p
          style={{
            fontSize: '0.85rem',
            color: 'var(--color-text-light)',
            fontWeight: 600,
          }}
        >
          {module.category}
        </p>
      </div>
      {!isPlay && (
        <p
          style={{
            fontSize: '0.85rem',
            color: 'var(--color-text-light)',
            lineHeight: 1.5,
          }}
        >
          {module.description}
        </p>
      )}
    </button>
  )
}
