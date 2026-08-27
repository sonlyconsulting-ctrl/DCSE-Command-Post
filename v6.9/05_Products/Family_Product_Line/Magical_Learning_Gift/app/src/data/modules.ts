export interface LearningModule {
  key: string
  title: string
  category: string
  emoji: string
  color: string
  description: string
  ageBands: string
  activities: string[]
}

export const MODULES: LearningModule[] = [
  {
    key: 'family-tree',
    title: 'My Family Tree Adventure',
    category: 'Family & Identity',
    emoji: '🌳',
    color: '#6BCB77',
    description: 'Explore family roles, names, relationships, and inclusive family structures through interactive activities.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Match a name to a relationship',
      'Build a family tree',
      'Who is related to whom?',
      'Photo-to-name matching',
      'Family story cards',
      'People who care for me',
    ],
  },
  {
    key: 'number-splash',
    title: 'Rainbow Number Splash',
    category: 'Numeracy',
    emoji: '🌈',
    color: '#4D96FF',
    description: 'Number recognition, counting, comparison, sequences, and simple operations with colorful visuals.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Count objects',
      'Match numeral to quantity',
      'Complete a sequence',
      'More, less, or equal',
      'Early addition and subtraction',
      'Pattern recognition',
    ],
  },
  {
    key: 'letter-lagoon',
    title: 'Unicorn Letter Lagoon',
    category: 'Literacy',
    emoji: '🦄',
    color: '#C77DFF',
    description: 'Letter recognition, sound association, word beginnings, spelling, and reading confidence builders.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Uppercase/lowercase matching',
      'Letter sounds',
      'Beginning sounds',
      'Build a word',
      'Name recognition',
      'Read-along cards',
    ],
  },
  {
    key: 'color-shape',
    title: 'Color and Shape Garden',
    category: 'Visual Learning',
    emoji: '🌻',
    color: '#FFD93D',
    description: 'Color, shape, size, sorting, grouping, and spatial reasoning in a vibrant garden setting.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Match colors',
      'Identify shapes',
      'Sort by size or attribute',
      'Complete visual patterns',
      'Find the different item',
      'Build a picture from shapes',
    ],
  },
  {
    key: 'memory-pool',
    title: 'Magical Memory Pool',
    category: 'Memory & Recall',
    emoji: '🫧',
    color: '#FF8B4D',
    description: 'Working memory, recognition, sequencing, and recall through enchanting pool-themed challenges.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Card matching',
      'Remember the sequence',
      'What changed?',
      'Picture recall',
      'Sound recall',
      'Family-photo memory sets',
    ],
  },
  {
    key: 'storytime-cove',
    title: 'Storytime Cove',
    category: 'Social-Emotional',
    emoji: '📚',
    color: '#FF85A1',
    description: 'Listening, sequencing, emotional vocabulary, comprehension, and creativity through stories.',
    ageBands: 'A-D (Ages 4-12)',
    activities: [
      'Read-along stories',
      'Put events in order',
      'Choose how a character feels',
      'Predict what happens next',
      'Retell the story',
      'Build a simple story',
    ],
  },
]
