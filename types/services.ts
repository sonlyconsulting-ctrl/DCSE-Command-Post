/** Types for content/sc-services.json. Confidence values reflect the registry. */
export type ServiceConfidence = 'DRAFT' | 'CONFIRMED';

export type ServiceProductCode = 'SC' | 'SS' | 'TSL' | 'CTJ' | 'MI';

export interface ServicesRegistryMeta {
  artifact_type: string;
  registry_id: string;
  version: string;
  source_authority: string;
  extraction_sources: string[];
  status: string;
  created_at: string;
  updated_at?: string;
  changelog?: string;
  pricing_note: string;
}

export interface ServiceBrandPalette {
  deep_navy: string;
  gold: string;
  electric_green: string;
  silver: string;
}

export interface ServiceBrandLogo {
  type: string;
  description: string;
  animation: string;
}

export interface ServiceBrand {
  name: string;
  code: string;
  tagline: string;
  posture: string;
  public_brand_rule: string;
  palette: ServiceBrandPalette;
  logo: ServiceBrandLogo;
  cta_primary: string;
  cta_secondary: string;
  prohibited_pronouns: string[];
  prohibited_punctuation: string[];
}

export interface ServiceCapability {
  title: string;
  input: string;
  output: string;
  domain: string;
}

export interface ServiceUniqueSection {
  type: string;
  features: string[];
}

export interface ServicePricingTier {
  tier: number;
  name: string;
  price: string;
  confidence: ServiceConfidence;
  badge?: string;
  features?: string[];
  billing?: string;
  note?: string;
}

export interface ServiceProgram {
  name: string;
  tagline: string;
  price?: string;
  price_range?: string;
  confidence: ServiceConfidence;
}

export interface ServiceIndividualProducts {
  price_range: string;
  examples: string[];
  note: string;
  confidence: ServiceConfidence;
}

export interface ServiceCoinEconomy {
  pick_correct: number;
  pick_incorrect: number;
  daily_login: number;
  weekly_streak: number;
  signup_bonus: number | 'TBD';
  membership_multiplier: number | 'TBD';
}

export type SportCategory =
  | 'NFL'
  | 'NBA'
  | 'MLB'
  | 'NHL'
  | 'NCAA'
  | 'High School Football'
  | 'High School Basketball';

export interface FavoriteTeam {
  id: string;
  name: string;
  shortName: string;
  sport: SportCategory;
  leagueOrConference: string;
  region: string;
  color?: string;
  seedOrRank?: string;
  websiteUrl?: string;
}

export interface TeamScoreOutcome {
  gameId: string;
  opponent: string;
  teamScore: number;
  opponentScore: number;
  date: string;
  outcome: 'W' | 'L' | 'T';
  detail?: string;
}

export interface TeamScheduledGame {
  gameId: string;
  opponent: string;
  gameTime: string;
  date: string;
  venue: string;
  broadcast?: string;
  isHome: boolean;
  odds?: string;
  liveLookUrl?: string;
  teamWebsiteUrl?: string;
}

export interface TeamActivityAlert {
  id: string;
  timestamp: string;
  headline: string;
  detail: string;
  badge: 'SCORE' | 'SCHEDULE' | 'ROSTER' | 'RADIUS_ALERT';
}

export interface TeamTrackerRecord {
  team: FavoriteTeam;
  recentScore: TeamScoreOutcome;
  upcomingGame: TeamScheduledGame;
  activityUpdate: TeamActivityAlert;
}

export interface ServiceFavoriteTeamsConfig {
  max_selections: number;
  supported_sports: SportCategory[];
  activity_tracking_fields: string[];
  selection_rule: string;
}

export interface ServiceProduct {
  code: ServiceProductCode;
  name: string;
  parent_brand: string;
  motto: string;
  hero: string;
  description: string;
  description_short?: string;
  capabilities: ServiceCapability[];
  unique_section: ServiceUniqueSection;
  sections: string[];
  pricing_tiers: ServicePricingTier[];
  personas?: string[];
  programs?: ServiceProgram[];
  individual_products?: ServiceIndividualProducts;
  coin_economy?: ServiceCoinEconomy;
  favorite_teams_config?: ServiceFavoriteTeamsConfig;
}

export interface ServiceKnownPrices {
  tsl_lounge_vip_monthly: string;
  gyto_assessment: string;
  gyto_foundations_ctj: string;
  gyto_strategic_analyst: string;
  ss_individual_products: string;
}

export interface ServicesRegistry {
  _meta: ServicesRegistryMeta;
  brand: ServiceBrand;
  products: ServiceProduct[];
  known_prices: ServiceKnownPrices;
  open_decisions: string[];
}
