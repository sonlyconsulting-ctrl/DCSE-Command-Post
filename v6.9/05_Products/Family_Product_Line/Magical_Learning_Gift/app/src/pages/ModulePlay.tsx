import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import { MODULES } from '../data/modules'

export default function ModulePlay() {
  const { moduleKey } = useParams<{ moduleKey: string }>()
  const navigate = useNavigate()
  const module = MODULES.find(m => m.key === moduleKey)

  if (!module) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <p style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</p>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', marginBottom: '16px' }}>
            Module not found
          </h1>
          <button
            onClick={() => navigate('/play')}
            style={{
              padding: '12px 28px',
              background: 'var(--color-primary)',
              color: '#fff',
              borderRadius: 'var(--radius-xl)',
              fontWeight: 700,
            }}
          >
            Back to Modules
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', background: `${module.color}08` }}>
      <Header variant="child" />

      <div className="container" style={{ padding: '32px 24px' }}>
        {/* Module Header */}
        <div
          style={{
            textAlign: 'center',
            padding: '40px 24px',
            background: `linear-gradient(135deg, ${module.color}20, ${module.color}05)`,
            borderRadius: 'var(--radius-lg)',
            marginBottom: '32px',
          }}
        >
          <span style={{ fontSize: '64px', display: 'block', marginBottom: '12px' }}>{module.emoji}</span>
          <h1
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.5rem, 3vw, 2rem)',
              color: module.color,
              marginBottom: '8px',
            }}
          >
            {module.title}
          </h1>
          <p style={{ color: 'var(--color-text-light)', maxWidth: '500px', margin: '0 auto' }}>
            {module.description}
          </p>
        </div>

        {/* Activities */}
        <h2
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.3rem',
            color: module.color,
            marginBottom: '20px',
            textAlign: 'center',
          }}
        >
          Activities
        </h2>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '16px',
            maxWidth: '900px',
            margin: '0 auto 40px',
          }}
        >
          {module.activities.map((activity, idx) => (
            <ActivityCard
              key={activity}
              activity={activity}
              index={idx}
              color={module.color}
            />
          ))}
        </div>

        {/* Interactive Demo */}
        <InteractiveDemo moduleKey={module.key} color={module.color} />
      </div>
    </div>
  )
}

function ActivityCard({ activity, index, color }: { activity: string; index: number; color: string }) {
  return (
    <div
      style={{
        padding: '20px',
        background: 'var(--color-surface)',
        borderRadius: 'var(--radius-md)',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        alignItems: 'center',
        gap: '14px',
        cursor: 'pointer',
        transition: 'transform 0.15s ease, box-shadow 0.15s ease',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-2px)'
        e.currentTarget.style.boxShadow = 'var(--shadow-md)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = 'var(--shadow-sm)'
      }}
    >
      <span
        style={{
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          background: `${color}20`,
          color,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 800,
          fontSize: '0.85rem',
          flexShrink: 0,
        }}
      >
        {index + 1}
      </span>
      <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{activity}</span>
    </div>
  )
}

function InteractiveDemo({ moduleKey, color }: { moduleKey: string; color: string }) {
  if (moduleKey === 'number-splash') return <NumberGame color={color} />
  if (moduleKey === 'letter-lagoon') return <LetterGame color={color} />
  if (moduleKey === 'color-shape') return <ShapeGame color={color} />
  if (moduleKey === 'memory-pool') return <MemoryGame color={color} />
  if (moduleKey === 'family-tree') return <FamilyDemo color={color} />
  if (moduleKey === 'storytime-cove') return <StoryDemo color={color} />
  return null
}

function NumberGame({ color }: { color: string }) {
  const [target] = useState(() => Math.floor(Math.random() * 8) + 2)
  const [selected, setSelected] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)

  const items = Array.from({ length: target }, (_, i) => i)
  const options = [target - 1, target, target + 1].sort(() => Math.random() - 0.5)

  const handleSelect = (n: number) => {
    setSelected(n)
    setShowResult(true)
  }

  return (
    <DemoWrapper title="Try It: Count the Stars!" color={color}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '40px', letterSpacing: '8px', marginBottom: '24px' }}>
          {items.map((_, i) => (
            <span key={i} role="img" aria-label="star">⭐</span>
          ))}
        </div>
        <p style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
          How many stars do you see?
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          {options.map(n => (
            <button
              key={n}
              onClick={() => handleSelect(n)}
              disabled={showResult}
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                fontSize: '1.5rem',
                fontWeight: 800,
                background: selected === n
                  ? n === target ? '#6BCB77' : '#FF6584'
                  : `${color}15`,
                color: selected === n ? '#fff' : color,
                border: `3px solid ${selected === n ? (n === target ? '#6BCB77' : '#FF6584') : color + '30'}`,
                transition: 'all 0.2s',
              }}
            >
              {n}
            </button>
          ))}
        </div>
        {showResult && (
          <p style={{ marginTop: '16px', fontSize: '1.2rem', fontWeight: 700, color: selected === target ? '#6BCB77' : '#FF6584' }}>
            {selected === target ? '🎉 Correct! Great counting!' : `Almost! There are ${target} stars. Try again!`}
          </p>
        )}
        {showResult && (
          <button
            onClick={() => { setSelected(null); setShowResult(false); window.location.reload() }}
            style={{ marginTop: '12px', padding: '8px 24px', background: color, color: '#fff', borderRadius: '20px', fontWeight: 700 }}
          >
            Play Again
          </button>
        )}
      </div>
    </DemoWrapper>
  )
}

function LetterGame({ color }: { color: string }) {
  const [current] = useState(() => {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return letters[Math.floor(Math.random() * letters.length)]
  })
  const [selected, setSelected] = useState<string | null>(null)

  const lower = current.toLowerCase()
  const distractors = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    .filter(l => l !== lower)
    .sort(() => Math.random() - 0.5)
    .slice(0, 3)

  const options = [...distractors, lower].sort(() => Math.random() - 0.5)

  return (
    <DemoWrapper title="Try It: Match the Letter!" color={color}>
      <div style={{ textAlign: 'center' }}>
        <p
          style={{
            fontSize: '72px',
            fontFamily: 'var(--font-display)',
            color,
            marginBottom: '16px',
          }}
        >
          {current}
        </p>
        <p style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px' }}>
          Find the lowercase match:
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          {options.map(l => (
            <button
              key={l}
              onClick={() => setSelected(l)}
              style={{
                width: '64px',
                height: '64px',
                borderRadius: 'var(--radius-md)',
                fontSize: '1.8rem',
                fontFamily: 'var(--font-display)',
                background: selected === l
                  ? l === lower ? '#6BCB77' : '#FF6584'
                  : `${color}15`,
                color: selected === l ? '#fff' : color,
                border: `3px solid ${selected === l ? (l === lower ? '#6BCB77' : '#FF6584') : color + '30'}`,
                transition: 'all 0.2s',
              }}
            >
              {l}
            </button>
          ))}
        </div>
        {selected && (
          <p style={{ marginTop: '16px', fontSize: '1.2rem', fontWeight: 700, color: selected === lower ? '#6BCB77' : '#FF6584' }}>
            {selected === lower ? '🦄 Perfect match!' : `Not quite! "${current}" matches "${lower}".`}
          </p>
        )}
      </div>
    </DemoWrapper>
  )
}

function ShapeGame({ color }: { color: string }) {
  const shapes = [
    { name: 'Circle', emoji: '🔴', svg: 'circle' },
    { name: 'Square', emoji: '🟦', svg: 'square' },
    { name: 'Triangle', emoji: '🔺', svg: 'triangle' },
    { name: 'Star', emoji: '⭐', svg: 'star' },
  ]
  const [targetIdx] = useState(() => Math.floor(Math.random() * shapes.length))
  const [selected, setSelected] = useState<number | null>(null)

  return (
    <DemoWrapper title="Try It: Find the Shape!" color={color}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px' }}>
          Tap the <strong>{shapes[targetIdx].name}</strong>!
        </p>
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
          {shapes.map((s, i) => (
            <button
              key={s.name}
              onClick={() => setSelected(i)}
              style={{
                width: '80px',
                height: '80px',
                borderRadius: s.svg === 'circle' ? '50%' : 'var(--radius-md)',
                fontSize: '36px',
                background: selected === i
                  ? i === targetIdx ? '#6BCB7730' : '#FF658430'
                  : `${color}10`,
                border: `3px solid ${selected === i ? (i === targetIdx ? '#6BCB77' : '#FF6584') : color + '20'}`,
                transition: 'all 0.2s',
              }}
            >
              {s.emoji}
            </button>
          ))}
        </div>
        {selected !== null && (
          <p style={{ marginTop: '16px', fontSize: '1.2rem', fontWeight: 700, color: selected === targetIdx ? '#6BCB77' : '#FF6584' }}>
            {selected === targetIdx ? '🌻 You found it!' : `That's a ${shapes[selected].name}. Look for the ${shapes[targetIdx].name}!`}
          </p>
        )}
      </div>
    </DemoWrapper>
  )
}

function MemoryGame({ color }: { color: string }) {
  const emojis = ['🐶', '🐱', '🐰', '🦊', '🐸', '🐵']
  const [cards] = useState(() => {
    const pairs = emojis.slice(0, 4)
    return [...pairs, ...pairs].sort(() => Math.random() - 0.5)
  })
  const [flipped, setFlipped] = useState<number[]>([])
  const [matched, setMatched] = useState<number[]>([])

  const handleFlip = (idx: number) => {
    if (flipped.length === 2 || flipped.includes(idx) || matched.includes(idx)) return
    const next = [...flipped, idx]
    setFlipped(next)
    if (next.length === 2) {
      if (cards[next[0]] === cards[next[1]]) {
        setMatched(prev => [...prev, next[0], next[1]])
        setFlipped([])
      } else {
        setTimeout(() => setFlipped([]), 800)
      }
    }
  }

  return (
    <DemoWrapper title="Try It: Memory Match!" color={color}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: '0.95rem', color: 'var(--color-text-light)', marginBottom: '16px' }}>
          Find all matching pairs!
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 64px)', gap: '8px', justifyContent: 'center' }}>
          {cards.map((emoji, i) => {
            const isVisible = flipped.includes(i) || matched.includes(i)
            return (
              <button
                key={i}
                onClick={() => handleFlip(i)}
                aria-label={isVisible ? emoji : 'Hidden card'}
                style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '28px',
                  background: matched.includes(i) ? '#6BCB7720' : isVisible ? `${color}15` : color,
                  border: `2px solid ${matched.includes(i) ? '#6BCB77' : color + '40'}`,
                  transition: 'all 0.2s',
                  color: isVisible ? 'inherit' : color,
                }}
              >
                {isVisible ? emoji : '?'}
              </button>
            )
          })}
        </div>
        {matched.length === cards.length && (
          <p style={{ marginTop: '16px', fontSize: '1.2rem', fontWeight: 700, color: '#6BCB77' }}>
            🫧 Amazing memory! You found them all!
          </p>
        )}
      </div>
    </DemoWrapper>
  )
}

function FamilyDemo({ color }: { color: string }) {
  const members = [
    { name: 'Grandma Rose', role: 'Grandmother', emoji: '👵' },
    { name: 'Dad', role: 'Parent', emoji: '👨' },
    { name: 'Mom', role: 'Parent', emoji: '👩' },
    { name: 'You', role: 'Child', emoji: '🧒' },
    { name: 'Baby Sam', role: 'Sibling', emoji: '👶' },
  ]

  return (
    <DemoWrapper title="Try It: Meet the Family!" color={color}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: '0.95rem', color: 'var(--color-text-light)', marginBottom: '24px' }}>
          Every family is unique and special. Here is an example family tree:
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center' }}>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <FamilyMember {...members[0]} color={color} />
          </div>
          <div style={{ width: '2px', height: '20px', background: `${color}40` }} />
          <div style={{ display: 'flex', gap: '32px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <FamilyMember {...members[1]} color={color} />
            <FamilyMember {...members[2]} color={color} />
          </div>
          <div style={{ width: '2px', height: '20px', background: `${color}40` }} />
          <div style={{ display: 'flex', gap: '32px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <FamilyMember {...members[3]} color={color} />
            <FamilyMember {...members[4]} color={color} />
          </div>
        </div>
      </div>
    </DemoWrapper>
  )
}

function FamilyMember({ name, role, emoji, color }: { name: string; role: string; emoji: string; color: string }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          background: `${color}15`,
          border: `2px solid ${color}40`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '28px',
          margin: '0 auto 6px',
        }}
      >
        {emoji}
      </div>
      <p style={{ fontWeight: 700, fontSize: '0.85rem' }}>{name}</p>
      <p style={{ fontSize: '0.75rem', color: 'var(--color-text-light)' }}>{role}</p>
    </div>
  )
}

function StoryDemo({ color }: { color: string }) {
  const [step, setStep] = useState(0)
  const story = [
    { text: 'Once upon a time, a little fox found a glowing lantern in the forest.', emoji: '🦊' },
    { text: 'The lantern was warm and hummed a gentle song.', emoji: '🏮' },
    { text: '"I wonder who lost this?" the fox thought.', emoji: '💭' },
    { text: 'The fox followed tiny paw prints in the snow...', emoji: '🐾' },
    { text: 'And found a baby owl shivering by a tree!', emoji: '🦉' },
    { text: '"Here, this will keep you warm," said the fox. And they became the best of friends.', emoji: '💛' },
  ]

  return (
    <DemoWrapper title="Try It: A Little Story" color={color}>
      <div style={{ textAlign: 'center', maxWidth: '480px', margin: '0 auto' }}>
        <p style={{ fontSize: '48px', marginBottom: '12px' }}>{story[step].emoji}</p>
        <p style={{ fontSize: '1.1rem', lineHeight: 1.7, fontWeight: 600, marginBottom: '24px', minHeight: '60px' }}>
          {story[step].text}
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <button
            onClick={() => setStep(Math.max(0, step - 1))}
            disabled={step === 0}
            style={{
              padding: '10px 24px',
              borderRadius: '20px',
              background: step === 0 ? 'var(--color-border)' : `${color}15`,
              color: step === 0 ? 'var(--color-text-light)' : color,
              fontWeight: 700,
            }}
          >
            Back
          </button>
          <span style={{ padding: '10px 0', fontSize: '0.85rem', color: 'var(--color-text-light)' }}>
            {step + 1} / {story.length}
          </span>
          <button
            onClick={() => setStep(Math.min(story.length - 1, step + 1))}
            disabled={step === story.length - 1}
            style={{
              padding: '10px 24px',
              borderRadius: '20px',
              background: step === story.length - 1 ? 'var(--color-border)' : color,
              color: '#fff',
              fontWeight: 700,
            }}
          >
            Next
          </button>
        </div>
        {step === story.length - 1 && (
          <p style={{ marginTop: '16px', fontSize: '1.1rem', fontWeight: 700, color: '#6BCB77' }}>
            📚 The End! What a wonderful story!
          </p>
        )}
      </div>
    </DemoWrapper>
  )
}

function DemoWrapper({ title, color, children }: { title: string; color: string; children: React.ReactNode }) {
  return (
    <div
      style={{
        padding: '32px 24px',
        background: 'var(--color-surface)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)',
        maxWidth: '700px',
        margin: '0 auto',
        border: `2px solid ${color}20`,
      }}
    >
      <h3
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.15rem',
          color,
          textAlign: 'center',
          marginBottom: '24px',
        }}
      >
        {title}
      </h3>
      {children}
    </div>
  )
}
