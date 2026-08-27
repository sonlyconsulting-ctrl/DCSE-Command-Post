import { useState } from 'react'
import Header from '../components/Header'
import { MODULES } from '../data/modules'

type Tab = 'overview' | 'children' | 'modules' | 'progress' | 'settings'

export default function GuardianDashboard() {
  const [tab, setTab] = useState<Tab>('overview')

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)' }}>
      <Header variant="guardian" />

      <div className="container" style={{ padding: '32px 24px' }}>
        <div style={{ marginBottom: '32px' }}>
          <h1
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.5rem, 3vw, 2rem)',
              color: 'var(--color-primary)',
              marginBottom: '4px',
            }}
          >
            Guardian Dashboard
          </h1>
          <p style={{ color: 'var(--color-text-light)' }}>
            Manage child profiles, modules, content, and privacy settings.
          </p>
        </div>

        {/* Tabs */}
        <div
          style={{
            display: 'flex',
            gap: '4px',
            marginBottom: '32px',
            borderBottom: '2px solid var(--color-border)',
            overflowX: 'auto',
          }}
        >
          {TABS.map(t => (
            <button
              key={t.key}
              onClick={() => setTab(t.key as Tab)}
              style={{
                padding: '12px 20px',
                fontWeight: 700,
                fontSize: '0.9rem',
                background: 'none',
                color: tab === t.key ? 'var(--color-primary)' : 'var(--color-text-light)',
                borderBottom: tab === t.key ? '3px solid var(--color-primary)' : '3px solid transparent',
                whiteSpace: 'nowrap',
                transition: 'color 0.15s',
              }}
            >
              {t.emoji} {t.label}
            </button>
          ))}
        </div>

        {tab === 'overview' && <OverviewPanel />}
        {tab === 'children' && <ChildrenPanel />}
        {tab === 'modules' && <ModulesPanel />}
        {tab === 'progress' && <ProgressPanel />}
        {tab === 'settings' && <SettingsPanel />}
      </div>
    </div>
  )
}

const TABS = [
  { key: 'overview', label: 'Overview', emoji: '📋' },
  { key: 'children', label: 'Children', emoji: '👶' },
  { key: 'modules', label: 'Modules', emoji: '📚' },
  { key: 'progress', label: 'Progress', emoji: '📊' },
  { key: 'settings', label: 'Settings', emoji: '⚙️' },
]

function Card({ children, title, style }: { children: React.ReactNode; title?: string; style?: React.CSSProperties }) {
  return (
    <div
      style={{
        background: 'var(--color-surface)',
        borderRadius: 'var(--radius-md)',
        boxShadow: 'var(--shadow-sm)',
        padding: '24px',
        ...style,
      }}
    >
      {title && (
        <h3 style={{ fontSize: '1rem', marginBottom: '16px', color: 'var(--color-text)' }}>{title}</h3>
      )}
      {children}
    </div>
  )
}

function StatTile({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div
      style={{
        padding: '20px',
        background: `${color}10`,
        borderRadius: 'var(--radius-md)',
        borderLeft: `4px solid ${color}`,
        textAlign: 'center',
      }}
    >
      <p style={{ fontSize: '1.8rem', fontWeight: 800, color }}>{value}</p>
      <p style={{ fontSize: '0.8rem', color: 'var(--color-text-light)', fontWeight: 600 }}>{label}</p>
    </div>
  )
}

function OverviewPanel() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
          gap: '16px',
        }}
      >
        <StatTile label="Active Children" value="2" color="#6BCB77" />
        <StatTile label="Modules Assigned" value="4" color="#4D96FF" />
        <StatTile label="Activities Completed" value="47" color="#C77DFF" />
        <StatTile label="Total Time (hrs)" value="12.5" color="#FF8B4D" />
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
          gap: '24px',
        }}
      >
        <Card title="Recent Sessions">
          {DEMO_SESSIONS.map((s, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '10px 0',
                borderBottom: i < DEMO_SESSIONS.length - 1 ? '1px solid var(--color-border)' : 'none',
              }}
            >
              <div>
                <p style={{ fontWeight: 700, fontSize: '0.9rem' }}>{s.child}</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--color-text-light)' }}>{s.module}</p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <p style={{ fontSize: '0.8rem', fontWeight: 600 }}>{s.duration}</p>
                <p style={{ fontSize: '0.75rem', color: 'var(--color-text-light)' }}>{s.date}</p>
              </div>
            </div>
          ))}
        </Card>

        <Card title="Notifications">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <NoticeItem
              emoji="🎉"
              text="Emma completed all Unicorn Letter Lagoon activities for Band A!"
              time="2 hours ago"
            />
            <NoticeItem
              emoji="📸"
              text="3 new family photos pending approval for Family Tree Adventure."
              time="Yesterday"
            />
            <NoticeItem
              emoji="⏱️"
              text="Liam's daily session limit reached (45 min)."
              time="Yesterday"
            />
          </div>
        </Card>
      </div>
    </div>
  )
}

function NoticeItem({ emoji, text, time }: { emoji: string; text: string; time: string }) {
  return (
    <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
      <span style={{ fontSize: '20px', flexShrink: 0 }}>{emoji}</span>
      <div>
        <p style={{ fontSize: '0.85rem', lineHeight: 1.5 }}>{text}</p>
        <p style={{ fontSize: '0.75rem', color: 'var(--color-text-light)' }}>{time}</p>
      </div>
    </div>
  )
}

function ChildrenPanel() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
      {DEMO_CHILDREN.map(c => (
        <Card key={c.name}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                background: `${c.color}20`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '28px',
              }}
            >
              {c.avatar}
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem' }}>{c.name}</h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-text-light)' }}>
                Band {c.band} ({c.label}) &middot; Age {c.age}
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {c.modules.map(m => (
              <span
                key={m}
                style={{
                  padding: '4px 12px',
                  borderRadius: '20px',
                  background: `${c.color}15`,
                  color: c.color,
                  fontSize: '0.8rem',
                  fontWeight: 700,
                }}
              >
                {m}
              </span>
            ))}
          </div>
        </Card>
      ))}
      <Card style={{ border: '2px dashed var(--color-border)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <button
          style={{
            padding: '16px 32px',
            background: 'var(--color-primary)10',
            color: 'var(--color-primary)',
            borderRadius: 'var(--radius-md)',
            fontWeight: 700,
            fontSize: '0.95rem',
          }}
        >
          + Add Child Profile
        </button>
      </Card>
    </div>
  )
}

function ModulesPanel() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
      {MODULES.map(m => (
        <Card key={m.key}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
            <span style={{ fontSize: '32px' }}>{m.emoji}</span>
            <div>
              <h3 style={{ fontSize: '1rem', color: m.color }}>{m.title}</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--color-text-light)' }}>{m.category}</p>
            </div>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--color-text-light)', marginBottom: '12px' }}>
            {m.description}
          </p>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--color-text-light)' }}>
              {m.activities.length} activities
            </span>
            <span
              style={{
                padding: '4px 12px',
                borderRadius: '20px',
                background: '#6BCB7720',
                color: '#6BCB77',
                fontSize: '0.8rem',
                fontWeight: 700,
              }}
            >
              Active
            </span>
          </div>
        </Card>
      ))}
    </div>
  )
}

function ProgressPanel() {
  return (
    <div>
      <Card title="Activity Completion by Module" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {MODULES.map(m => {
            const pct = Math.floor(Math.random() * 60 + 20)
            return (
              <div key={m.key}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>
                    {m.emoji} {m.title}
                  </span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--color-text-light)' }}>{pct}%</span>
                </div>
                <div
                  style={{
                    height: '10px',
                    background: 'var(--color-border)',
                    borderRadius: '5px',
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      height: '100%',
                      width: `${pct}%`,
                      background: m.color,
                      borderRadius: '5px',
                      transition: 'width 0.5s ease',
                    }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </Card>

      <Card title="Skills Practiced">
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {SKILLS.map(s => (
            <span
              key={s}
              style={{
                padding: '6px 14px',
                borderRadius: '20px',
                background: 'var(--color-primary)10',
                color: 'var(--color-primary)',
                fontSize: '0.8rem',
                fontWeight: 600,
              }}
            >
              {s}
            </span>
          ))}
        </div>
      </Card>
    </div>
  )
}

function SettingsPanel() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px' }}>
      <Card title="Session Controls">
        <SettingRow label="Daily session limit" value="45 minutes" />
        <SettingRow label="Break reminders" value="Every 15 minutes" />
        <SettingRow label="Timed mode" value="Disabled" />
        <SettingRow label="Audio instructions" value="Enabled" />
        <SettingRow label="Reduced motion" value="System default" />
      </Card>
      <Card title="Privacy & Data">
        <SettingRow label="Data retention" value="Until deletion" />
        <SettingRow label="Public sharing" value="Disabled" />
        <SettingRow label="Export format" value="JSON + PDF" />
        <SettingRow label="Third-party tracking" value="None" />
        <button
          style={{
            marginTop: '16px',
            padding: '10px 20px',
            background: '#FF658415',
            color: '#FF6584',
            borderRadius: 'var(--radius-sm)',
            fontWeight: 700,
            fontSize: '0.85rem',
          }}
        >
          Request Data Export
        </button>
      </Card>
    </div>
  )
}

function SettingRow({ label, value }: { label: string; value: string }) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 0',
        borderBottom: '1px solid var(--color-border)',
      }}
    >
      <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{label}</span>
      <span style={{ fontSize: '0.85rem', color: 'var(--color-text-light)' }}>{value}</span>
    </div>
  )
}

const DEMO_SESSIONS = [
  { child: 'Emma', module: 'Unicorn Letter Lagoon', duration: '18 min', date: 'Today' },
  { child: 'Liam', module: 'Rainbow Number Splash', duration: '25 min', date: 'Today' },
  { child: 'Emma', module: 'Color and Shape Garden', duration: '12 min', date: 'Yesterday' },
  { child: 'Liam', module: 'Magical Memory Pool', duration: '30 min', date: 'Yesterday' },
]

const DEMO_CHILDREN = [
  { name: 'Emma', age: 5, band: 'A', label: 'Explorer', avatar: '🧒', color: '#FF85A1', modules: ['Letters', 'Colors', 'Family Tree'] },
  { name: 'Liam', age: 8, band: 'C', label: 'Pathfinder', avatar: '👦', color: '#4D96FF', modules: ['Numbers', 'Memory', 'Stories', 'Letters'] },
]

const SKILLS = [
  'Letter Recognition', 'Counting', 'Color Matching', 'Shape Identification',
  'Sequencing', 'Family Relationships', 'Story Comprehension', 'Visual Memory',
  'Pattern Recognition', 'Name Spelling', 'Phonics', 'Emotional Vocabulary',
]
