import { useState, useMemo } from 'react';
import type {
  SportCategory,
  FavoriteTeam,
  TeamScoreOutcome,
  TeamScheduledGame,
  TeamActivityAlert,
  TeamTrackerRecord,
} from '../../types/services';

export interface TeamTrackerProps {
  initialSelectedIds?: string[];
  maxSelections?: number;
  teamsRegistry?: FavoriteTeam[];
  trackerRegistry?: Record<string, TeamTrackerRecord>;
  onSelectionChange?: (selectedTeams: FavoriteTeam[]) => void;
  className?: string;
}

/** Comprehensive registry of selectable teams across all supported athletic tiers. */
export const DEFAULT_TEAMS_REGISTRY: FavoriteTeam[] = [
  // NFL
  {
    id: 'nfl-kc',
    name: 'Kansas City Chiefs',
    shortName: 'Chiefs',
    sport: 'NFL',
    leagueOrConference: 'AFC West',
    region: 'Kansas City, MO',
    seedOrRank: 'AFC #1',
    color: '#E31837',
  },
  {
    id: 'nfl-sf',
    name: 'San Francisco 49ers',
    shortName: '49ers',
    sport: 'NFL',
    leagueOrConference: 'NFC West',
    region: 'Santa Clara, CA',
    seedOrRank: 'NFC #2',
    color: '#AA0000',
  },
  {
    id: 'nfl-bal',
    name: 'Baltimore Ravens',
    shortName: 'Ravens',
    sport: 'NFL',
    leagueOrConference: 'AFC North',
    region: 'Baltimore, MD',
    seedOrRank: 'AFC #2',
    color: '#241773',
  },
  {
    id: 'nfl-det',
    name: 'Detroit Lions',
    shortName: 'Lions',
    sport: 'NFL',
    leagueOrConference: 'NFC North',
    region: 'Detroit, MI',
    seedOrRank: 'NFC #1',
    color: '#0076B6',
  },
  {
    id: 'nfl-phi',
    name: 'Philadelphia Eagles',
    shortName: 'Eagles',
    sport: 'NFL',
    leagueOrConference: 'NFC East',
    region: 'Philadelphia, PA',
    seedOrRank: 'NFC #3',
    color: '#004C54',
  },

  // NBA
  {
    id: 'nba-bos',
    name: 'Boston Celtics',
    shortName: 'Celtics',
    sport: 'NBA',
    leagueOrConference: 'Eastern Conference',
    region: 'Boston, MA',
    seedOrRank: 'East #1',
    color: '#007A33',
  },
  {
    id: 'nba-den',
    name: 'Denver Nuggets',
    shortName: 'Nuggets',
    sport: 'NBA',
    leagueOrConference: 'Western Conference',
    region: 'Denver, CO',
    seedOrRank: 'West #2',
    color: '#0E2240',
  },
  {
    id: 'nba-lal',
    name: 'Los Angeles Lakers',
    shortName: 'Lakers',
    sport: 'NBA',
    leagueOrConference: 'Western Conference',
    region: 'Los Angeles, CA',
    seedOrRank: 'West #7',
    color: '#552583',
  },
  {
    id: 'nba-nyk',
    name: 'New York Knicks',
    shortName: 'Knicks',
    sport: 'NBA',
    leagueOrConference: 'Eastern Conference',
    region: 'New York, NY',
    seedOrRank: 'East #2',
    color: '#006BB6',
  },

  // MLB
  {
    id: 'mlb-nyy',
    name: 'New York Yankees',
    shortName: 'Yankees',
    sport: 'MLB',
    leagueOrConference: 'AL East',
    region: 'Bronx, NY',
    seedOrRank: 'AL East #1',
    color: '#003087',
  },
  {
    id: 'mlb-lad',
    name: 'Los Angeles Dodgers',
    shortName: 'Dodgers',
    sport: 'MLB',
    leagueOrConference: 'NL West',
    region: 'Los Angeles, CA',
    seedOrRank: 'NL West #1',
    color: '#005A9C',
  },
  {
    id: 'mlb-atl',
    name: 'Atlanta Braves',
    shortName: 'Braves',
    sport: 'MLB',
    leagueOrConference: 'NL East',
    region: 'Atlanta, GA',
    seedOrRank: 'NL East #2',
    color: '#CE1141',
  },
  {
    id: 'mlb-bal',
    name: 'Baltimore Orioles',
    shortName: 'Orioles',
    sport: 'MLB',
    leagueOrConference: 'AL East',
    region: 'Baltimore, MD',
    seedOrRank: 'AL East #2',
    color: '#DF4601',
  },

  // NHL
  {
    id: 'nhl-fla',
    name: 'Florida Panthers',
    shortName: 'Panthers',
    sport: 'NHL',
    leagueOrConference: 'Atlantic Division',
    region: 'Sunrise, FL',
    seedOrRank: 'Atlantic #1',
    color: '#041E42',
  },
  {
    id: 'nhl-edm',
    name: 'Edmonton Oilers',
    shortName: 'Oilers',
    sport: 'NHL',
    leagueOrConference: 'Pacific Division',
    region: 'Edmonton, AB',
    seedOrRank: 'Pacific #2',
    color: '#FF4C00',
  },
  {
    id: 'nhl-nyr',
    name: 'New York Rangers',
    shortName: 'Rangers',
    sport: 'NHL',
    leagueOrConference: 'Metropolitan Division',
    region: 'New York, NY',
    seedOrRank: 'Metro #1',
    color: '#0038A8',
  },
  {
    id: 'nhl-dal',
    name: 'Dallas Stars',
    shortName: 'Stars',
    sport: 'NHL',
    leagueOrConference: 'Central Division',
    region: 'Dallas, TX',
    seedOrRank: 'Central #1',
    color: '#006847',
  },

  // NCAA
  {
    id: 'ncaa-uga',
    name: 'Georgia Bulldogs',
    shortName: 'Bulldogs',
    sport: 'NCAA',
    leagueOrConference: 'SEC (Football/Basketball)',
    region: 'Athens, GA',
    seedOrRank: 'AP #2',
    color: '#BA0C2F',
  },
  {
    id: 'ncaa-tex',
    name: 'Texas Longhorns',
    shortName: 'Longhorns',
    sport: 'NCAA',
    leagueOrConference: 'SEC (Football/Basketball)',
    region: 'Austin, TX',
    seedOrRank: 'AP #1',
    color: '#BF5700',
  },
  {
    id: 'ncaa-osu',
    name: 'Ohio State Buckeyes',
    shortName: 'Buckeyes',
    sport: 'NCAA',
    leagueOrConference: 'Big Ten',
    region: 'Columbus, OH',
    seedOrRank: 'AP #3',
    color: '#BB0000',
  },
  {
    id: 'ncaa-uconn',
    name: 'UConn Huskies',
    shortName: 'Huskies',
    sport: 'NCAA',
    leagueOrConference: 'Big East (Basketball)',
    region: 'Storrs, CT',
    seedOrRank: 'NCAA Champ #1',
    color: '#000E2F',
  },
  {
    id: 'ncaa-duke',
    name: 'Duke Blue Devils',
    shortName: 'Blue Devils',
    sport: 'NCAA',
    leagueOrConference: 'ACC (Basketball)',
    region: 'Durham, NC',
    seedOrRank: 'AP #7',
    color: '#003087',
  },

  // High School Football
  {
    id: 'hsfb-mater-dei',
    name: 'Mater Dei Monarchs',
    shortName: 'Mater Dei',
    sport: 'High School Football',
    leagueOrConference: 'Trinity League (CIF-SS)',
    region: 'Santa Ana, CA',
    seedOrRank: 'National #1',
    color: '#CE1126',
  },
  {
    id: 'hsfb-duncanville',
    name: 'Duncanville Panthers',
    shortName: 'Duncanville',
    sport: 'High School Football',
    leagueOrConference: 'UIL 6A Division 1 (District 11-6A)',
    region: 'Duncanville, TX',
    seedOrRank: 'National #3',
    color: '#003366',
  },
  {
    id: 'hsfb-st-john-bosco',
    name: 'St. John Bosco Braves',
    shortName: 'Bosco',
    sport: 'High School Football',
    leagueOrConference: 'Trinity League (CIF-SS)',
    region: 'Bellflower, CA',
    seedOrRank: 'National #2',
    color: '#002D62',
  },
  {
    id: 'hsfb-north-shore',
    name: 'North Shore Mustangs',
    shortName: 'North Shore',
    sport: 'High School Football',
    leagueOrConference: 'UIL 6A Division 1 (District 23-6A)',
    region: 'Houston, TX',
    seedOrRank: 'Texas Top 5',
    color: '#8B0000',
  },
  {
    id: 'hsfb-buford',
    name: 'Buford Wolves',
    shortName: 'Buford',
    sport: 'High School Football',
    leagueOrConference: 'GHSA Class 7A (Region 8-7A)',
    region: 'Buford, GA',
    seedOrRank: 'Georgia #1',
    color: '#005A36',
  },

  // High School Basketball
  {
    id: 'hsbb-montverde',
    name: 'Montverde Academy Eagles',
    shortName: 'Montverde',
    sport: 'High School Basketball',
    leagueOrConference: 'National Interscholastic (NIBC)',
    region: 'Montverde, FL',
    seedOrRank: 'National #1',
    color: '#552583',
  },
  {
    id: 'hsbb-paul-vi',
    name: 'Paul VI Panthers',
    shortName: 'Paul VI',
    sport: 'High School Basketball',
    leagueOrConference: 'Washington Catholic Athletic (WCAC)',
    region: 'Chantilly, VA',
    seedOrRank: 'National #2',
    color: '#000000',
  },
  {
    id: 'hsbb-columbus',
    name: 'Columbus Explorers',
    shortName: 'Columbus',
    sport: 'High School Basketball',
    leagueOrConference: 'FHSAA Class 7A',
    region: 'Miami, FL',
    seedOrRank: 'Florida #1',
    color: '#003366',
  },
  {
    id: 'hsbb-sierra-canyon',
    name: 'Sierra Canyon Trailblazers',
    shortName: 'Sierra Canyon',
    sport: 'High School Basketball',
    leagueOrConference: 'Mission League (CIF-SS)',
    region: 'Chatsworth, CA',
    seedOrRank: 'California Top 5',
    color: '#002B49',
  },
];

/** Live-style tracking dataset showing scores, game times, and radius alerts. */
export const DEFAULT_TRACKER_REGISTRY: Record<string, TeamTrackerRecord> = {
  'nfl-kc': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'nfl-kc')!,
    recentScore: {
      gameId: 'nfl-kc-w6',
      opponent: 'San Francisco 49ers',
      teamScore: 28,
      opponentScore: 18,
      date: 'Oct 20, 2026',
      outcome: 'W',
      detail: 'Fourth quarter ground drive closed out victory on the road.',
    },
    upcomingGame: {
      gameId: 'nfl-kc-w7',
      opponent: 'Denver Broncos',
      gameTime: '4:25 PM EDT',
      date: 'Sunday, Oct 26',
      venue: 'GEHA Field at Arrowhead Stadium',
      broadcast: 'CBS / Paramount+',
      isHome: true,
    },
    activityUpdate: {
      id: 'act-kc-1',
      timestamp: '2 hours ago',
      headline: 'Roster Activation: Starting Cornerback Cleared',
      detail: 'Defense returns to full health ahead of division matchup.',
      badge: 'ROSTER',
    },
  },
  'nba-bos': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'nba-bos')!,
    recentScore: {
      gameId: 'nba-bos-g1',
      opponent: 'New York Knicks',
      teamScore: 132,
      opponentScore: 109,
      date: 'Oct 22, 2026',
      outcome: 'W',
      detail: 'Tied NBA record with 29 made three-point field goals in opener.',
    },
    upcomingGame: {
      gameId: 'nba-bos-g2',
      opponent: 'Milwaukee Bucks',
      gameTime: '7:30 PM EDT',
      date: 'Monday, Oct 27',
      venue: 'TD Garden',
      broadcast: 'TNT / Max',
      isHome: true,
    },
    activityUpdate: {
      id: 'act-bos-1',
      timestamp: '4 hours ago',
      headline: 'Championship Banner Raised at TD Garden',
      detail: 'Lounge members celebrated the season launch with pick bonus multipliers.',
      badge: 'RADIUS_ALERT',
    },
  },
  'mlb-nyy': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'mlb-nyy')!,
    recentScore: {
      gameId: 'mlb-nyy-alcs5',
      opponent: 'Cleveland Guardians',
      teamScore: 5,
      opponentScore: 2,
      date: 'Oct 19, 2026',
      outcome: 'W',
      detail: 'Tenth-inning 3-run home run clinched American League pennant.',
    },
    upcomingGame: {
      gameId: 'mlb-nyy-ws1',
      opponent: 'Los Angeles Dodgers',
      gameTime: '8:08 PM EDT',
      date: 'Friday, Oct 24',
      venue: 'Dodger Stadium',
      broadcast: 'FOX Sports',
      isHome: false,
    },
    activityUpdate: {
      id: 'act-nyy-1',
      timestamp: '1 day ago',
      headline: 'World Series Starting Pitcher Confirmed',
      detail: 'Ace starter tabbed for Game 1 start on national broadcast.',
      badge: 'SCHEDULE',
    },
  },
  'ncaa-uga': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'ncaa-uga')!,
    recentScore: {
      gameId: 'ncaa-uga-w8',
      opponent: 'Texas Longhorns',
      teamScore: 30,
      opponentScore: 15,
      date: 'Oct 19, 2026',
      outcome: 'W',
      detail: 'Dominant first-half defensive performance in Austin road showdown.',
    },
    upcomingGame: {
      gameId: 'ncaa-uga-w9',
      opponent: 'Florida Gators',
      gameTime: '3:30 PM EDT',
      date: 'Saturday, Nov 1',
      venue: 'EverBank Stadium, Jacksonville',
      broadcast: 'ABC / ESPN+',
      isHome: false,
    },
    activityUpdate: {
      id: 'act-uga-1',
      timestamp: '3 hours ago',
      headline: 'SEC Defensive Player of the Week Awarded',
      detail: 'Defensive front recorded 7 sacks and 3 turnovers in ranked victory.',
      badge: 'SCORE',
    },
  },
  'hsfb-mater-dei': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'hsfb-mater-dei')!,
    recentScore: {
      gameId: 'hsfb-md-w8',
      opponent: 'JSerra Catholic Lions',
      teamScore: 41,
      opponentScore: 17,
      date: 'Oct 18, 2026',
      outcome: 'W',
      detail: 'Trinity League matchup secured another undefeated regular season week.',
    },
    upcomingGame: {
      gameId: 'hsfb-md-w9',
      opponent: 'St. John Bosco Braves',
      gameTime: '7:00 PM PDT',
      date: 'Friday, Oct 24',
      venue: 'Santa Ana Stadium',
      broadcast: 'Bally Sports SoCal / NFHS Network',
      isHome: true,
    },
    activityUpdate: {
      id: 'act-md-1',
      timestamp: '5 hours ago',
      headline: 'Rivalry Clash: Sold-Out Radius Event',
      detail: 'National #1 vs. National #2 showdown previewed on Lounge Feed.',
      badge: 'RADIUS_ALERT',
    },
  },
  'nfl-sf': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'nfl-sf')!,
    recentScore: {
      gameId: 'nfl-sf-w6',
      opponent: 'Kansas City Chiefs',
      teamScore: 18,
      opponentScore: 28,
      date: 'Oct 20, 2026',
      outcome: 'L',
      detail: 'Turnovers in red zone halted second-half comeback bid.',
    },
    upcomingGame: {
      gameId: 'nfl-sf-w7',
      opponent: 'Dallas Cowboys',
      gameTime: '8:20 PM EDT',
      date: 'Sunday, Oct 26',
      venue: "Levi's Stadium",
      broadcast: 'NBC / Peacock',
      isHome: true,
    },
    activityUpdate: {
      id: 'act-sf-1',
      timestamp: '1 hour ago',
      headline: 'Sunday Night Football Matchup Announced',
      detail: 'Prime-time showdown draws heavy Lounge pick activity.',
      badge: 'SCHEDULE',
    },
  },
  'nhl-fla': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'nhl-fla')!,
    recentScore: {
      gameId: 'nhl-fla-g4',
      opponent: 'Vegas Golden Knights',
      teamScore: 4,
      opponentScore: 3,
      date: 'Oct 19, 2026',
      outcome: 'W',
      detail: 'Overtime game-winner tallied at Amerant Bank Arena.',
    },
    upcomingGame: {
      gameId: 'nhl-fla-g5',
      opponent: 'New York Rangers',
      gameTime: '7:00 PM EDT',
      date: 'Thursday, Oct 24',
      venue: 'Madison Square Garden',
      broadcast: 'ESPN / ESPN+',
      isHome: false,
    },
    activityUpdate: {
      id: 'act-fla-1',
      timestamp: '6 hours ago',
      headline: 'Power Play Efficiency Climbs to 28.5%',
      detail: 'Special teams unit converts two goals in road swing.',
      badge: 'SCORE',
    },
  },
  'hsbb-montverde': {
    team: DEFAULT_TEAMS_REGISTRY.find((t) => t.id === 'hsbb-montverde')!,
    recentScore: {
      gameId: 'hsbb-mv-pre1',
      opponent: 'IMG Academy Ascenders',
      teamScore: 84,
      opponentScore: 68,
      date: 'Oct 17, 2026',
      outcome: 'W',
      detail: 'Preseason showcase victory featured balanced double-digit scoring.',
    },
    upcomingGame: {
      gameId: 'hsbb-mv-open',
      opponent: 'Oak Hill Academy Warriors',
      gameTime: '6:30 PM EDT',
      date: 'Saturday, Nov 8',
      venue: 'Nest Center, Montverde, FL',
      broadcast: 'ESPNU / Lounge Stream',
      isHome: true,
    },
    activityUpdate: {
      id: 'act-mv-1',
      timestamp: '8 hours ago',
      headline: 'NIBC Schedule Officially Released',
      detail: 'National championship defense begins with 12 televised contests.',
      badge: 'SCHEDULE',
    },
  },
};

const ALL_SPORTS_FILTER = 'ALL';

/**
 * TSL Multi-Sport Favorite Teams Selection & Activity Tracker.
 * Obeying v7.3 Governance: Zero database modifications, strictly typed, zero prohibited pronouns.
 */
export default function TeamTracker({
  initialSelectedIds = ['nfl-kc', 'nba-bos', 'mlb-nyy', 'ncaa-uga', 'hsfb-mater-dei'],
  maxSelections = 5,
  teamsRegistry = DEFAULT_TEAMS_REGISTRY,
  trackerRegistry = DEFAULT_TRACKER_REGISTRY,
  onSelectionChange,
  className = '',
}: TeamTrackerProps) {
  const [selectedIds, setSelectedIds] = useState<string[]>(initialSelectedIds.slice(0, maxSelections));
  const [selectedSport, setSelectedSport] = useState<string>(ALL_SPORTS_FILTER);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [alertNotice, setAlertNotice] = useState<string | null>(null);

  const sportsList: SportCategory[] = [
    'NFL',
    'NBA',
    'MLB',
    'NHL',
    'NCAA',
    'High School Football',
    'High School Basketball',
  ];

  // Filter selectable teams based on sport tab and search query
  const filteredTeams = useMemo(() => {
    return teamsRegistry.filter((team) => {
      const matchesSport = selectedSport === ALL_SPORTS_FILTER || team.sport === selectedSport;
      const q = searchQuery.trim().toLowerCase();
      const matchesQuery =
        q.length === 0 ||
        team.name.toLowerCase().includes(q) ||
        team.shortName.toLowerCase().includes(q) ||
        team.region.toLowerCase().includes(q) ||
        team.leagueOrConference.toLowerCase().includes(q);
      return matchesSport && matchesQuery;
    });
  }, [teamsRegistry, selectedSport, searchQuery]);

  // Selected teams full objects
  const selectedTeams = useMemo(() => {
    return selectedIds
      .map((id) => teamsRegistry.find((t) => t.id === id))
      .filter((t): t is FavoriteTeam => Boolean(t));
  }, [selectedIds, teamsRegistry]);

  // Toggle selection handler
  const handleToggleTeam = (teamId: string) => {
    if (selectedIds.includes(teamId)) {
      const next = selectedIds.filter((id) => id !== teamId);
      setSelectedIds(next);
      setAlertNotice(null);
      if (onSelectionChange) {
        const nextTeams = next
          .map((id) => teamsRegistry.find((t) => t.id === id))
          .filter((t): t is FavoriteTeam => Boolean(t));
        onSelectionChange(nextTeams);
      }
    } else {
      if (selectedIds.length >= maxSelections) {
        setAlertNotice(`Maximum selection limit reached (${maxSelections} teams). Deselect a team to add another.`);
        return;
      }
      const next = [...selectedIds, teamId];
      setSelectedIds(next);
      setAlertNotice(null);
      if (onSelectionChange) {
        const nextTeams = next
          .map((id) => teamsRegistry.find((t) => t.id === id))
          .filter((t): t is FavoriteTeam => Boolean(t));
        onSelectionChange(nextTeams);
      }
    }
  };

  const handleClearAll = () => {
    setSelectedIds([]);
    setAlertNotice(null);
    if (onSelectionChange) {
      onSelectionChange([]);
    }
  };

  return (
    <section className={`space-y-8 ${className}`} aria-label="TSL Favorite Teams and Activity Tracker">
      {/* Header Banner */}
      <div className="bg-[#112240] border-2 border-[#D4AF37]/50 rounded-2xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-[#D4AF37]/5 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-[#00875A]/20 text-[#00875A] border border-[#00875A]/40">
                TSL MULTI-SPORT FEATURE
              </span>
              <span className="text-xs font-mono text-[#D4AF37]">Up to {maxSelections} Favorite Teams</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
              Tedo&apos;s Sports Lounge: Multi-Sport Favorite Teams Tracker
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Curate up to {maxSelections} favorite athletic teams across NFL, NBA, MLB, NHL, NCAA, and High School Football/Basketball. Monitor real-time scores, upcoming game times, and radius community activity feeds from a single synchronized dashboard.
            </p>
          </div>

          {/* Quick Counter Card */}
          <div className="bg-[#0A192F] border border-slate-700 rounded-xl p-4 min-w-[220px] text-center space-y-1 shadow-lg">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
              Active Member Selections
            </span>
            <div className="text-3xl font-black text-[#D4AF37]">
              {selectedIds.length} <span className="text-base font-semibold text-slate-400">/ {maxSelections}</span>
            </div>
            <p className="text-[11px] text-slate-400">
              {maxSelections - selectedIds.length === 0
                ? 'Maximum capacity reached'
                : `${maxSelections - selectedIds.length} slot(s) remaining`}
            </p>
          </div>
        </div>

        {/* Selected Teams Ribbon */}
        <div className="mt-6 pt-6 border-t border-slate-800/80">
          <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00875A] animate-pulse" />
              Selected Teams:
            </span>
            {selectedIds.length > 0 && (
              <button
                type="button"
                onClick={handleClearAll}
                className="text-[11px] text-[#D4AF37] hover:underline font-semibold"
              >
                Clear All Selections
              </button>
            )}
          </div>

          {selectedTeams.length === 0 ? (
            <p className="text-xs text-slate-500 italic py-1">
              Zero teams selected. Use the directory below to choose up to {maxSelections} teams.
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {selectedTeams.map((team) => (
                <div
                  key={team.id}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0A192F] border border-[#D4AF37]/50 text-xs text-white shadow-sm"
                >
                  <span className="text-[9px] font-bold uppercase px-1.5 py-0.5 rounded bg-slate-800 text-[#D4AF37]">
                    {team.sport}
                  </span>
                  <span className="font-bold">{team.name}</span>
                  <button
                    type="button"
                    onClick={() => handleToggleTeam(team.id)}
                    className="text-slate-400 hover:text-red-400 text-sm font-black transition ml-1"
                    title={`Remove ${team.name}`}
                    aria-label={`Remove ${team.name}`}
                  >
                    &times;
                  </button>
                </div>
              ))}
            </div>
          )}

          {alertNotice && (
            <div className="mt-3 p-2.5 rounded-lg bg-red-950/40 border border-red-500/50 text-xs text-red-200">
              {alertNotice}
            </div>
          )}
        </div>
      </div>

      {/* ========================================================= */}
      {/* LIVE 5-TEAM ACTIVITY TRACKER DASHBOARD                    */}
      {/* ========================================================= */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-black text-white flex items-center gap-2">
            <span>5-Team Multi-Sport Activity Dashboard</span>
            <span className="text-xs font-normal text-slate-400 font-mono">
              (Synchronized Feed)
            </span>
          </h3>
          <span className="text-xs font-mono text-[#00875A] font-semibold">
            Status: ACTIVE
          </span>
        </div>

        {selectedTeams.length === 0 ? (
          <div className="bg-[#112240] border border-slate-700/80 rounded-xl p-8 text-center space-y-3">
            <div className="text-4xl text-slate-600">🏟️</div>
            <h4 className="text-base font-bold text-white">No Teams Currently Tracked</h4>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Select up to {maxSelections} teams in the selection directory below to populate real-time scores, upcoming schedules, and radius updates.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {selectedTeams.map((team) => {
              const tracker = trackerRegistry[team.id] || {
                team,
                recentScore: {
                  gameId: `${team.id}-recent`,
                  opponent: 'Regional Opponent',
                  teamScore: 0,
                  opponentScore: 0,
                  date: 'Scheduled',
                  outcome: 'T' as const,
                  detail: 'Game data compiling.',
                },
                upcomingGame: {
                  gameId: `${team.id}-next`,
                  opponent: 'Upcoming Matchup',
                  gameTime: 'TBD',
                  date: 'Upcoming',
                  venue: team.region,
                  broadcast: 'Lounge Regional Feed',
                  isHome: true,
                },
                activityUpdate: {
                  id: `act-${team.id}`,
                  timestamp: 'Just now',
                  headline: 'Roster Schedule Synced',
                  detail: 'Active tracking enabled for this program.',
                  badge: 'RADIUS_ALERT' as const,
                },
              };

              const { recentScore, upcomingGame, activityUpdate } = tracker;

              return (
                <article
                  key={team.id}
                  className="bg-[#112240] border-2 border-slate-700/90 hover:border-[#D4AF37] rounded-xl p-5 flex flex-col justify-between shadow-xl transition-all duration-200"
                >
                  <div className="space-y-4">
                    {/* Team Header */}
                    <div className="flex items-start justify-between gap-3 border-b border-slate-800 pb-3">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-[#0A192F] text-[#D4AF37] border border-[#D4AF37]/30">
                            {team.sport}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            {team.leagueOrConference}
                          </span>
                        </div>
                        <h4 className="text-lg font-black text-white">{team.name}</h4>
                        <span className="text-xs text-slate-400">{team.region}</span>
                      </div>
                      {team.seedOrRank && (
                        <span className="px-2.5 py-1 rounded bg-[#00875A]/20 text-[#00875A] border border-[#00875A]/40 text-[11px] font-bold whitespace-nowrap">
                          {team.seedOrRank}
                        </span>
                      )}
                    </div>

                    {/* Recent Score Module */}
                    <div className="bg-[#0A192F] border border-slate-800/80 rounded-lg p-3 space-y-1.5">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="text-slate-400 uppercase font-bold tracking-wider">
                          Recent Result
                        </span>
                        <span className="text-slate-500 font-mono text-[10px]">
                          {recentScore.date}
                        </span>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="text-sm font-bold text-white">
                          vs. {recentScore.opponent}
                        </div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-xs font-black ${
                              recentScore.outcome === 'W'
                                ? 'bg-[#00875A]/20 text-[#00875A] border border-[#00875A]/40'
                                : recentScore.outcome === 'L'
                                ? 'bg-red-950/40 text-red-400 border border-red-500/30'
                                : 'bg-amber-950/40 text-amber-400 border border-amber-500/30'
                            }`}
                          >
                            {recentScore.outcome}
                          </span>
                          <span className="text-sm font-black text-white font-mono">
                            {recentScore.teamScore} - {recentScore.opponentScore}
                          </span>
                        </div>
                      </div>

                      {recentScore.detail && (
                        <p className="text-[11px] text-slate-400 leading-snug">
                          {recentScore.detail}
                        </p>
                      )}
                    </div>

                    {/* Upcoming Matchup Module */}
                    <div className="bg-[#0A192F] border border-slate-800/80 rounded-lg p-3 space-y-1.5">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="text-[#D4AF37] uppercase font-bold tracking-wider">
                          Next Matchup
                        </span>
                        <span className="text-slate-400 font-mono text-[10px]">
                          {upcomingGame.date} • {upcomingGame.gameTime}
                        </span>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="text-sm font-bold text-white">
                          {upcomingGame.isHome ? 'vs.' : '@'} {upcomingGame.opponent}
                        </div>
                        {upcomingGame.broadcast && (
                          <span className="text-[10px] font-mono text-[#D4AF37] px-2 py-0.5 rounded bg-[#112240] border border-slate-700">
                            {upcomingGame.broadcast}
                          </span>
                        )}
                      </div>

                      <div className="text-[11px] text-slate-400 flex items-center gap-1.5">
                        <span className="text-slate-500">📍</span>
                        <span>{upcomingGame.venue}</span>
                      </div>
                    </div>

                    {/* Real-Time Activity Alert */}
                    <div className="p-3 rounded-lg bg-[#0E1E38] border border-slate-700/60 space-y-1">
                      <div className="flex items-center justify-between text-[10px]">
                        <span className="font-bold text-[#D4AF37] uppercase tracking-wider">
                          📢 Activity Feed ({activityUpdate.badge})
                        </span>
                        <span className="text-slate-500">{activityUpdate.timestamp}</span>
                      </div>
                      <div className="text-xs font-bold text-white">
                        {activityUpdate.headline}
                      </div>
                      <p className="text-[11px] text-slate-300 leading-snug">
                        {activityUpdate.detail}
                      </p>
                    </div>
                  </div>

                  <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs">
                    <span className="text-slate-400 text-[11px]">
                      Lounge Radius Tracking: <strong className="text-[#00875A]">ENABLED</strong>
                    </span>
                    <button
                      type="button"
                      onClick={() => handleToggleTeam(team.id)}
                      className="text-slate-400 hover:text-red-400 font-bold transition text-[11px]"
                    >
                      Remove from Tracker
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </div>

      {/* ========================================================= */}
      {/* INTERACTIVE MULTI-SPORT TEAM SELECTOR DIRECTORY           */}
      {/* ========================================================= */}
      <div className="bg-[#112240] border border-slate-700 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl">
        <div className="space-y-2">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span>Multi-Sport Team Directory</span>
                <span className="text-xs text-slate-400 font-normal">
                  ({filteredTeams.length} available)
                </span>
              </h3>
              <p className="text-xs text-slate-300">
                Filter by athletic tier or search by team, region, or conference. Click any team card to add or remove it from the 5-team tracker.
              </p>
            </div>

            {/* Search Input */}
            <div className="w-full sm:w-72">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search teams, cities, leagues..."
                className="w-full px-3.5 py-2 bg-[#0A192F] border border-slate-700 rounded-lg text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-[#D4AF37]"
              />
            </div>
          </div>

          {/* Sport Filter Tabs */}
          <div className="flex flex-wrap items-center gap-1.5 pt-2">
            <button
              type="button"
              onClick={() => setSelectedSport(ALL_SPORTS_FILTER)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                selectedSport === ALL_SPORTS_FILTER
                  ? 'bg-[#D4AF37] text-[#0A192F] shadow'
                  : 'bg-[#0A192F] text-slate-300 hover:text-white border border-slate-700'
              }`}
            >
              All Sports
            </button>
            {sportsList.map((sport) => (
              <button
                key={sport}
                type="button"
                onClick={() => setSelectedSport(sport)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                  selectedSport === sport
                    ? 'bg-[#D4AF37] text-[#0A192F] shadow'
                    : 'bg-[#0A192F] text-slate-300 hover:text-white border border-slate-700'
                }`}
              >
                {sport}
              </button>
            ))}
          </div>
        </div>

        {/* Team Selection Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredTeams.map((team) => {
            const isSelected = selectedIds.includes(team.id);
            const isAtMax = selectedIds.length >= maxSelections && !isSelected;

            return (
              <div
                key={team.id}
                onClick={() => handleToggleTeam(team.id)}
                className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 flex flex-col justify-between ${
                  isSelected
                    ? 'bg-[#0E254A] border-[#D4AF37] shadow-lg shadow-[#D4AF37]/10'
                    : isAtMax
                    ? 'bg-[#0A192F]/60 border-slate-800 opacity-60 hover:opacity-80'
                    : 'bg-[#0A192F] border-slate-800 hover:border-slate-600'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-[#D4AF37]">
                      {team.sport}
                    </span>
                    <span
                      className={`text-xs font-bold px-2 py-0.5 rounded ${
                        isSelected
                          ? 'bg-[#00875A] text-white'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {isSelected ? '✓ Tracked' : '+ Add'}
                    </span>
                  </div>

                  <div>
                    <h4 className="text-sm font-black text-white">{team.name}</h4>
                    <p className="text-[11px] text-slate-400">{team.region}</p>
                    <p className="text-[10px] text-slate-500 font-mono mt-0.5">
                      {team.leagueOrConference}
                    </p>
                  </div>
                </div>

                {team.seedOrRank && (
                  <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-[#00875A]">
                    {team.seedOrRank}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {filteredTeams.length === 0 && (
          <div className="text-center py-8 text-xs text-slate-500">
            No teams found matching current filters. Try resetting the search or selecting another sport.
          </div>
        )}
      </div>
    </section>
  );
}
