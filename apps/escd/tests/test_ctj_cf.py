from apps.escd.runtime.ctj_cf import (
    CFState,
    action_modes_for,
    classify_request,
    correction_ddna_candidate,
    next_resolution_state,
    resolve_ctj_objects,
    should_escalate_to_user,
    start_ctj_cf,
)


def test_unified_alias_resolves_canonical_object():
    assert resolve_ctj_objects("Send me the CTJ Unified review link") == ["CTJ-UNIFIED"]


def test_unknown_does_not_escalate_while_enterprise_sources_remain():
    state = CFState("find Unified", resolution_state="UNKNOWN")
    assert should_escalate_to_user(state, retrievable_sources_remaining=True) is False


def test_searched_not_found_is_distinct_from_verified_absent():
    assert next_resolution_state("UNKNOWN", searched_all=True) == "SEARCHED_NOT_FOUND"
    assert next_resolution_state("UNKNOWN", affirmative_absence=True) == "VERIFIED_ABSENT"


def test_brand_generation_enters_generate_mode():
    classes = classify_request("Create a new Unified brand image from the approved CTJ identity")
    modes = action_modes_for(classes)
    assert "CREATE" in classes
    assert "BRAND_MEDIA" in classes
    assert "GENERATE" in modes


def test_sell_readiness_classifies_commerce_without_stopping_on_unknown():
    state = start_ctj_cf("What remains before CTJ Unified can sell through Stripe?")
    assert "CTJ-UNIFIED" in state.canonical_objects
    assert "COMMERCIALIZE" in state.request_classes
    assert state.resolution_state == "UNKNOWN"


def test_title_change_does_not_implicitly_promote():
    state = start_ctj_cf("Change the CTJ Unified title")
    assert "CTJ-UNIFIED" in state.canonical_objects
    assert "PROMOTE" not in state.action_modes


def test_dcs_correction_produces_candidate_not_doctrine():
    candidate = correction_ddna_candidate(
        "Asked DCS to provide an existing CTJ link",
        "Retrieve enterprise sources before asking me"
    )
    assert candidate["status"] == "CANDIDATE"
    assert candidate["authority"] == "DCS_EXPLICIT_CORRECTION"
    assert candidate["promotion"] == "REQUIRES_DEDUP_CONTRADICTION_VALIDATION"


def test_hard_gate_allows_escalation():
    state = CFState("release", hard_stop="release_promotion_gate")
    assert should_escalate_to_user(state, retrievable_sources_remaining=True) is True
