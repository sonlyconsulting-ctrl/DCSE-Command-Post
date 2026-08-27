import Header from '../components/Header'

export default function Privacy() {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />
      <div className="container" style={{ padding: '48px 24px', maxWidth: '720px' }}>
        <h1
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '2rem',
            color: 'var(--color-primary)',
            marginBottom: '32px',
          }}
        >
          Privacy &amp; Safety
        </h1>

        {SECTIONS.map(s => (
          <section key={s.title} style={{ marginBottom: '32px' }}>
            <h2 style={{ fontSize: '1.15rem', color: 'var(--color-text)', marginBottom: '12px' }}>
              {s.emoji} {s.title}
            </h2>
            <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {s.items.map((item, i) => (
                <li key={i} style={{ fontSize: '0.95rem', color: 'var(--color-text-light)', lineHeight: 1.6 }}>
                  {item}
                </li>
              ))}
            </ul>
          </section>
        ))}

        <div
          style={{
            padding: '24px',
            background: '#6BCB7715',
            borderRadius: 'var(--radius-md)',
            borderLeft: '4px solid #6BCB77',
          }}
        >
          <p style={{ fontWeight: 700, marginBottom: '8px' }}>Our Commitment</p>
          <p style={{ fontSize: '0.9rem', color: 'var(--color-text-light)', lineHeight: 1.6 }}>
            Magical Learning Gift is designed with children's safety as its highest priority.
            We do not serve ads, track behavior for third parties, or use child data for external model training.
            Guardians retain full control over all data, with export and deletion available at any time.
          </p>
        </div>
      </div>
    </div>
  )
}

const SECTIONS = [
  {
    emoji: '🔒',
    title: 'Data Collection',
    items: [
      'We collect only the minimum data needed to deliver the learning experience.',
      'Child profiles are created and managed exclusively by authorized guardians.',
      'No behavioral tracking, advertising identifiers, or third-party analytics.',
      'No facial recognition, voiceprint identification, or location tracking.',
    ],
  },
  {
    emoji: '🛡️',
    title: 'Guardian Control',
    items: [
      'Guardians control all content, module access, session limits, and privacy settings.',
      'Children cannot create accounts or share content without guardian authorization.',
      'All family media (photos, names, voice clips) requires explicit guardian approval.',
      'Support access is time-bound, logged, and revocable.',
    ],
  },
  {
    emoji: '📤',
    title: 'Data Rights',
    items: [
      'Full data export available in JSON and PDF formats.',
      'Deletion requests processed promptly for all child data.',
      'No data retention beyond guardian-specified policies.',
      'No data sharing with third parties for any purpose without explicit authorization.',
    ],
  },
  {
    emoji: '🚫',
    title: 'Prohibited Practices',
    items: [
      'No manipulative engagement mechanics (streaks, loss aversion, shame).',
      'No public leaderboards or child-to-child messaging.',
      'No autonomous purchases or social-media sharing by children.',
      'No developmental diagnoses inferred from app performance.',
      'No service-role credentials exposed in client code.',
    ],
  },
]
