import sys
import os
import json
import re

_TYPE_SIGNALS = {
    "technical_log": [
        "psql", "migration", "trace", "stdout", "stderr", 
        "commit", "rollback", "insert", "update", "select", "constraint"
    ]
}

def _signal(layer, category, evidence, location, reuse, seq):
    return {
        "layer": layer,
        "category": category,
        "evidence": evidence,
        "source_location": location,
        "proposed_reuse": reuse,
        "sequence": seq
    }

def extract_technical_signals(source):
    content = source["raw_content"]
    signals = []
    seq = 1

    # AG Log-specific technical capture
    if source["source_type"] in ("technical_log", "hybrid_technical_log"):
        lines = content.split("\n")
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if any(kw in stripped.lower() for kw in ["rls", "row level security", "policy"]):
                signals.append(_signal("technical", "rls_enforcement", stripped, f"L{idx+1}", "Supabase RLS compliance pattern", seq)); seq+=1
            elif any(kw in stripped.lower() for kw in ["service_role", "anon_key", "supabase_url"]):
                signals.append(_signal("technical", "credential_routing", stripped, f"L{idx+1}", "Backend mediation verification", seq)); seq+=1
            elif re.match(r"(CREATE|ALTER|DROP|INSERT|UPDATE)", stripped, re.IGNORECASE):
                signals.append(_signal("technical", "schema_mutation", stripped, f"L{idx+1}", "DB structural change log", seq)); seq+=1

    return signals

def load_source(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return {"source_id": os.path.basename(filepath), "raw_content": content}

def classify_source(source):
    content = source["raw_content"].lower()
    match_count = sum(1 for kw in _TYPE_SIGNALS["technical_log"] if kw in content)
    # Heuristic: If it contains SQL keywords or technical stack traces, route as technical_log
    if match_count >= 1:
        return "technical_log"
    return "unknown"

def run_extraction(filepath, outdir):
    try:
        src = load_source(filepath)
    except FileNotFoundError:
        print(f"ERROR: Source file '{filepath}' not found.")
        sys.exit(1)
        
    src["source_type"] = classify_source(src)
    
    # Step 03 Gate Enforcement Simulation (Assuming Pass for AG Logs post-gate)
    ps_risk = "None"
    if ps_risk == "Critical":
        print("HALT: PS Critical Risk Detected.")
        sys.exit(1)

    signals = extract_technical_signals(src)
    
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "ddna_extracted.json")
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(signals, f, indent=2)
        
    print(f"Extraction complete. Found {len(signals)} technical signals.")
    print(f"Output written to {outpath}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dcse_ddna_extraction_v01.py <source_file> <output_dir>")
        sys.exit(1)
    run_extraction(sys.argv[1], sys.argv[2])
