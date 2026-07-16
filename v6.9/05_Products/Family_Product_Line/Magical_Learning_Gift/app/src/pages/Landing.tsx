import { useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import ModuleCard from '../components/ModuleCard'
import { MODULES } from '../data/modules'

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />

      {/* Hero */}
      <section
        style={{
          background: 'linear-gradient(135deg, #6C63FF 0%, #C77DFF 50%, #FF85A1 100%)',
          padding: '80px 24px',
          textAlign: 'center',
          color: '#fff',
        }}
      >
        <div className="container">
          <p style={{ fontSize: '64px', marginBottom: '16px' }}>✨</p>
          <h1
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(2rem, 5vw, 3.5rem)',
              marginBottom: '16px',
            }}
          >
            Magical Learning Gift
          </h1>
          <p
            style={{
              fontSize: 'clamp(1rem, 2.5vw, 1.25rem)',
              maxWidth: '640px',
              margin: '0 auto 32px',
              opacity: 0.95,
              lineHeight: 1.6,
            }}
          >
            A personalized, guardian-controlled learning experience that turns
            family knowledge, academics, and discovery into a magical gift
            for children ages 4-12.
          </p>
          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => navigate('/play')}
              style={{
                padding: '16px 36px',
                borderRadius: 'var(--radius-xl)',
                background: '#fff',
                color: 'var(--color-primary)',
                fontWeight: 800,
                fontSize: '1.1rem',
                boxShadow: 'var(--shadow-md)',
                transition: 'transform 0.15s ease',
              }}
              onMouseEnter={e => (e.currentTarget.style.transform = 'scale(1.05)')}
              onMouseLeave={e => (e.currentTarget.style.transform = 'scale(1)')}
            >
              Start Exploring
            </button>
            <button
              onClick={() => navigate('/guardian/dashboard')}
              style={{
                padding: '16px 36px',
                borderRadius: 'var(--radius-xl)',
                background: 'rgba(255,255,255,0.2)',
                color: '#fff',
                fontWeight: 700,
                fontSize: '1.1rem',
                border: '2px solid rgba(255,255,255,0.5)',
                transition: 'background 0.15s ease',
              }}
              onMouseEnter={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.3)')}
              onMouseLeave={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.2)')}
            >
              Guardian Dashboard
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section style={{ padding: '64px 24px' }}>
        <div className="container">
          <h2
            style={{
              textAlign: 'center',
              fontSize: 'clamp(1.5rem, 3vw, 2rem)',
              color: 'var(--color-primary)',
              marginBottom: '12px',
            }}
          >
            Built for Families
          </h2>
          <p
            style={{
              textAlign: 'center',
              color: 'var(--color-text-light)',
              maxWidth: '600px',
              margin: '0 auto 48px',
              fontSize: '1.05rem',
            }}
          >
            Every feature designed with child safety, guardian control,
            and personalized learning at its core.
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '24px',
              marginBottom: '64px',
            }}
          >
            {FEATURES.map(f => (
              <div
                key={f.title}
                style={{
                  padding: '28px 24px',
                  background: 'var(--color-surface)',
                  borderRadius: 'var(--radius-md)',
                  boxShadow: 'var(--shadow-sm)',
                  textAlign: 'center',
                }}
              >
                <span style={{ fontSize: '36px', display: 'block', marginBottom: '12px' }}>
                  {f.emoji}
                </span>
                <h3 style={{ fontSize: '1.1rem', marginBottom: '8px', color: 'var(--color-text)' }}>
                  {f.title}
                </h3>
                <p style={{ fontSize: '0.9rem', color: 'var(--color-text-light)', lineHeight: 1.6 }}>
                  {f.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Modules Preview */}
      <section style={{ padding: '64px 24px', background: '#F4F2FF' }}>
        <div className="container">
          <h2
            style={{
              textAlign: 'center',
              fontSize: 'clamp(1.5rem, 3vw, 2rem)',
              color: 'var(--color-primary)',
              marginBottom: '12px',
            }}
          >
            Six Learning Modules
          </h2>
          <p
            style={{
              textAlign: 'center',
              color: 'var(--color-text-light)',
              maxWidth: '600px',
              margin: '0 auto 48px',
              fontSize: '1.05rem',
            }}
          >
            From literacy and numeracy to family identity and creative storytelling.
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '20px',
            }}
          >
            {MODULES.map(m => (
              <ModuleCard key={m.key} module={m} />
            ))}
          </div>
        </div>
      </section>

      {/* Age Bands */}
      <section style={{ padding: '64px 24px' }}>
        <div className="container">
          <h2
            style={{
              textAlign: 'center',
              fontSize: 'clamp(1.5rem, 3vw, 2rem)',
              color: 'var(--color-primary)',
              marginBottom: '48px',
            }}
          >
            Adaptive Age Bands
          </h2>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '20px',
            }}
          >
            {AGE_BANDS.map(b => (
              <div
                key={b.label}
                style={{
                  padding: '24px',
                  background: 'var(--color-surface)',
                  borderRadius: 'var(--radius-md)',
                  boxShadow: 'var(--shadow-sm)',
                  borderLeft: `4px solid ${b.color}`,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                  <span
                    style={{
                      background: b.color,
                      color: '#fff',
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '0.9rem',
                    }}
                  >
                    {b.band}
                  </span>
                  <h3 style={{ fontSize: '1.05rem' }}>{b.label}</h3>
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--color-text-light)', marginBottom: '4px' }}>
                  Ages {b.range}
                </p>
                <p style={{ fontSize: '0.85rem', color: 'var(--color-text-light)' }}>
                  {b.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          background: 'var(--color-text)',
          color: 'rgba(255,255,255,0.7)',
          padding: '48px 24px',
          textAlign: 'center',
        }}
      >
        <div className="container">
          <p style={{ fontFamily: 'var(--font-display)', color: '#fff', fontSize: '1.1rem', marginBottom: '8px' }}>
            ✨ Magical Learning Gift
          </p>
          <p style={{ fontSize: '0.85rem', marginBottom: '16px' }}>
            A DCSE Family Product Line experience by Sonly Consulting
          </p>
          <div style={{ display: 'flex', gap: '24px', justifyContent: 'center', fontSize: '0.85rem' }}>
            <a href="/privacy" style={{ color: 'rgba(255,255,255,0.7)' }}>Privacy</a>
            <a href="/guardian/dashboard" style={{ color: 'rgba(255,255,255,0.7)' }}>Guardian Access</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

const FEATURES = [
  {
    emoji: '🛡️',
    title: 'Guardian Controlled',
    desc: 'Parents and guardians manage every aspect: content, difficulty, session limits, and privacy settings.',
  },
  {
    emoji: '🎁',
    title: 'Giftable Experience',
    desc: 'Purchase and gift a personalized learning journey for birthdays, holidays, or any special occasion.',
  },
  {
    emoji: '🌈',
    title: 'Inclusive Families',
    desc: 'Supports diverse family structures — adoptive, blended, chosen, and extended families are all welcome.',
  },
  {
    emoji: '🔒',
    title: 'Privacy First',
    desc: 'No tracking, no ads, no social sharing. Family data stays private with full export and deletion rights.',
  },
  {
    emoji: '♿',
    title: 'Accessible Design',
    desc: 'Reduced-motion support, keyboard navigation, audio instructions, and color-independent visual cues.',
  },
  {
    emoji: '📊',
    title: 'Progress Insights',
    desc: 'Clear distinction between observed activity and derived suggestions — no developmental diagnoses.',
  },
]

const AGE_BANDS = [
  { band: 'A', label: 'Explorer', range: '4-5', color: '#6BCB77', desc: 'Large targets, narration-first, short sessions' },
  { band: 'B', label: 'Builder', range: '6-7', color: '#4D96FF', desc: 'Simple instructions, matching, sequencing' },
  { band: 'C', label: 'Pathfinder', range: '8-9', color: '#FFD93D', desc: 'Multi-step tasks, memory challenges' },
  { band: 'D', label: 'Creator', range: '10-12', color: '#C77DFF', desc: 'More autonomy, reflection prompts' },
]
