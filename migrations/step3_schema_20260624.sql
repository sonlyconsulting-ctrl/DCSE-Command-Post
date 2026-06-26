-- SQL Item 1 — routing_log
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE routing_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  record_id TEXT NOT NULL,
  record_type TEXT NOT NULL,
  routed_to TEXT NOT NULL,
  review_type TEXT NOT NULL,
  packet_json JSONB NOT NULL,
  routed_at TIMESTAMPTZ DEFAULT now(),
  lane TEXT NOT NULL CHECK (lane IN ('SC', 'SS', 'DCSE')),
  resolved BOOLEAN DEFAULT false,
  resolution_note TEXT
);

ALTER TABLE routing_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY routing_log_dcs_admin ON routing_log
  FOR ALL
  TO authenticated
  USING (auth.jwt() ->> 'role' = 'dcs_admin')
  WITH CHECK (auth.jwt() ->> 'role' = 'dcs_admin');

CREATE POLICY routing_log_no_anon ON routing_log
  FOR ALL
  TO anon
  USING (false);

-- SQL Item 2 — RAG Vectors Table
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS ps_schema;

CREATE TABLE ps_schema.rag_vectors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT NOT NULL,
  embedding vector(384) NOT NULL,
  metadata JSONB,
  source_label TEXT,
  lane TEXT DEFAULT 'PS' NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE ps_schema.rag_vectors ENABLE ROW LEVEL SECURITY;

CREATE POLICY ps_rag_dcs_only ON ps_schema.rag_vectors
  FOR ALL
  TO authenticated
  USING (auth.jwt() ->> 'role' = 'dcs_admin')
  WITH CHECK (auth.jwt() ->> 'role' = 'dcs_admin');

CREATE POLICY ps_rag_no_anon ON ps_schema.rag_vectors
  FOR ALL
  TO anon
  USING (false);

CREATE TABLE dcse_rag_vectors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT NOT NULL,
  embedding vector(384) NOT NULL,
  metadata JSONB,
  source_label TEXT NOT NULL,
  source_display TEXT,
  lane TEXT NOT NULL CHECK (lane IN ('SC', 'SS', 'DCSE')),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX ON dcse_rag_vectors
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

ALTER TABLE dcse_rag_vectors ENABLE ROW LEVEL SECURITY;

CREATE POLICY rag_dcs_admin ON dcse_rag_vectors
  FOR ALL TO authenticated
  USING (auth.jwt() ->> 'role' = 'dcs_admin')
  WITH CHECK (auth.jwt() ->> 'role' = 'dcs_admin');

CREATE POLICY rag_operator_lane ON dcse_rag_vectors
  FOR SELECT TO authenticated
  USING (
    lane IN ('SC', 'SS', 'DCSE')
    AND auth.jwt() ->> 'role' IN ('dcs_admin', 'operator', 'cto_reviewer')
  );

CREATE POLICY rag_no_anon ON dcse_rag_vectors
  FOR ALL TO anon
  USING (false);
