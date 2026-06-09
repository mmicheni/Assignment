"""
kbs_crop_disease.py
-------------------
Crop Disease Diagnosis Knowledge-Based System
APT 3020 – Quiz 1

All-in-one file: knowledge base, inference engine,
explanation facility, and test cases.

Usage:
  python kbs_crop_disease.py            # interactive mode
  python kbs_crop_disease.py --test     # run all test cases
"""

import sys

# ═══════════════════════════════════════════════════════════════
# PART A: KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════

# ── Static Facts ────────────────────────────────────────────────
STATIC_FACTS = {
    "yellow_leaves_indicates":        ["nitrogen_deficiency", "mosaic_virus", "root_rot"],
    "brown_spots_indicates":          ["leaf_blight", "cercospora_leaf_spot", "bacterial_spot"],
    "wilting_indicates":              ["root_rot", "fusarium_wilt", "drought_stress"],
    "white_powder_indicates":         ["powdery_mildew"],
    "black_lesions_indicates":        ["anthracnose", "black_rot"],
    "stunted_growth_indicates":       ["nutrient_deficiency", "mosaic_virus", "nematode_infection"],
    "leaf_curl_indicates":            ["mosaic_virus", "aphid_infestation", "drought_stress"],
    "water_soaked_lesions_indicates": ["late_blight", "bacterial_spot"],

    "treatments": {
        "powdery_mildew":       "Apply sulfur-based fungicide; improve air circulation; avoid overhead irrigation.",
        "late_blight":          "Apply copper-based fungicide immediately; remove infected tissue; avoid wet foliage.",
        "mosaic_virus":         "Remove and destroy infected plants; control aphid vectors; use virus-resistant seeds.",
        "nitrogen_deficiency":  "Apply nitrogen-rich fertilizer (urea or DAP); incorporate organic compost.",
        "root_rot":             "Improve drainage; reduce watering; apply Trichoderma-based bio-fungicide.",
        "fusarium_wilt":        "Solarize soil; use resistant varieties; apply Bacillus subtilis biocontrol.",
        "leaf_blight":          "Apply mancozeb or chlorothalonil fungicide; practice crop rotation.",
        "cercospora_leaf_spot": "Apply azoxystrobin fungicide; remove infected leaves; maintain plant spacing.",
        "bacterial_spot":       "Apply copper bactericide; avoid overhead watering; use disease-free seeds.",
        "anthracnose":          "Apply mancozeb fungicide; destroy infected debris; use resistant cultivars.",
        "drought_stress":       "Irrigate promptly; apply mulch to retain moisture; use drought-tolerant varieties.",
        "nutrient_deficiency":  "Conduct soil test; apply balanced NPK fertilizer; correct soil pH if needed.",
        "aphid_infestation":    "Apply insecticidal soap or neem oil; introduce natural predators (ladybugs).",
        "black_rot":            "Remove infected parts; apply copper fungicide; practice 2-year crop rotation.",
        "nematode_infection":   "Apply nematicides; solarize soil; incorporate marigold as a trap crop.",
    },

    "severity_levels": {
        "low":    "Affects <20% of plant",
        "medium": "Affects 20–50% of plant",
        "high":   "Affects >50% of plant or multiple plants",
    },

    "crops_susceptible_to_powdery_mildew":    ["wheat", "barley", "cucumber", "squash"],
    "crops_susceptible_to_late_blight":       ["tomato", "potato"],
    "crops_susceptible_to_mosaic_virus":      ["tomato", "pepper", "bean", "cucumber"],
    "crops_susceptible_to_root_rot":          ["maize", "soybean", "bean", "tomato"],
    "crops_susceptible_to_fusarium_wilt":     ["tomato", "banana", "cotton", "melon"],
    "crops_susceptible_to_leaf_blight":       ["maize", "rice", "wheat", "sorghum"],
    "crops_susceptible_to_bacterial_spot":    ["tomato", "pepper"],
    "crops_susceptible_to_anthracnose":       ["mango", "bean", "pepper", "cucumber"],
    "crops_susceptible_to_nematode_infection":["tomato", "carrot", "banana", "pepper"],
}

# ── Rules ────────────────────────────────────────────────────────
# Each rule: id, name, condition (lambda on facts dict),
#            conclusion key, explanation string
RULES = [
    {
        "id": "R01", "name": "Powdery Mildew Detection",
        "condition":   lambda f: f.get("white_powder_on_leaves") and f.get("dry_weather"),
        "conclusion":  "powdery_mildew",
        "explanation": "R01: White powder on leaves AND dry weather → Powdery Mildew.",
    },
    {
        "id": "R02", "name": "Late Blight Detection",
        "condition":   lambda f: f.get("water_soaked_lesions") and f.get("cool_wet_weather") and f.get("brown_spots"),
        "conclusion":  "late_blight",
        "explanation": "R02: Water-soaked lesions AND cool/wet weather AND brown spots → Late Blight.",
    },
    {
        "id": "R03", "name": "Mosaic Virus Detection",
        "condition":   lambda f: f.get("yellow_leaves") and f.get("leaf_curl") and f.get("stunted_growth"),
        "conclusion":  "mosaic_virus",
        "explanation": "R03: Yellow leaves AND leaf curl AND stunted growth → Mosaic Virus.",
    },
    {
        "id": "R04", "name": "Nitrogen Deficiency Detection",
        "condition":   lambda f: f.get("yellow_leaves") and f.get("pale_green_lower_leaves") and not f.get("wilting"),
        "conclusion":  "nitrogen_deficiency",
        "explanation": "R04: Yellow leaves AND pale lower leaves AND NO wilting → Nitrogen Deficiency.",
    },
    {
        "id": "R05", "name": "Root Rot Detection",
        "condition":   lambda f: f.get("wilting") and f.get("yellow_leaves") and f.get("overwatering"),
        "conclusion":  "root_rot",
        "explanation": "R05: Wilting AND yellow leaves AND overwatering history → Root Rot.",
    },
    {
        "id": "R06", "name": "Fusarium Wilt Detection",
        "condition":   lambda f: f.get("wilting") and f.get("brown_vascular_tissue") and not f.get("overwatering"),
        "conclusion":  "fusarium_wilt",
        "explanation": "R06: Wilting AND brown vascular tissue AND NO overwatering → Fusarium Wilt.",
    },
    {
        "id": "R07", "name": "Leaf Blight Detection",
        "condition":   lambda f: f.get("brown_spots") and f.get("lesions_with_yellow_halo") and f.get("humid_weather"),
        "conclusion":  "leaf_blight",
        "explanation": "R07: Brown spots AND yellow halo AND humid weather → Leaf Blight.",
    },
    {
        "id": "R08", "name": "Cercospora Leaf Spot Detection",
        "condition":   lambda f: f.get("brown_spots") and f.get("circular_spots") and not f.get("humid_weather"),
        "conclusion":  "cercospora_leaf_spot",
        "explanation": "R08: Circular brown spots WITHOUT humidity → Cercospora Leaf Spot.",
    },
    {
        "id": "R09", "name": "Bacterial Spot Detection",
        "condition":   lambda f: f.get("water_soaked_lesions") and f.get("brown_spots") and not f.get("cool_wet_weather"),
        "conclusion":  "bacterial_spot",
        "explanation": "R09: Water-soaked lesions AND brown spots in warm weather → Bacterial Spot.",
    },
    {
        "id": "R10", "name": "Anthracnose Detection",
        "condition":   lambda f: f.get("black_lesions") and f.get("sunken_spots") and f.get("humid_weather"),
        "conclusion":  "anthracnose",
        "explanation": "R10: Black sunken spots AND humid weather → Anthracnose.",
    },
    {
        "id": "R11", "name": "Drought Stress Detection",
        "condition":   lambda f: (f.get("wilting") and f.get("leaf_curl")
                                  and f.get("dry_weather") and not f.get("yellow_leaves")),
        "conclusion":  "drought_stress",
        "explanation": "R11: Wilting AND leaf curl AND dry weather AND NO yellowing → Drought Stress.",
    },
    {
        "id": "R12", "name": "General Nutrient Deficiency",
        "condition":   lambda f: f.get("stunted_growth") and f.get("pale_green_lower_leaves") and not f.get("yellow_leaves"),
        "conclusion":  "nutrient_deficiency",
        "explanation": "R12: Stunted growth AND pale lower leaves (no yellowing) → Nutrient Deficiency.",
    },
    {
        "id": "R13", "name": "Aphid Infestation Detection",
        "condition":   lambda f: f.get("leaf_curl") and f.get("sticky_residue") and f.get("visible_insects"),
        "conclusion":  "aphid_infestation",
        "explanation": "R13: Leaf curl AND sticky residue AND visible insects → Aphid Infestation.",
    },
    {
        "id": "R14", "name": "Black Rot Detection",
        "condition":   lambda f: f.get("black_lesions") and f.get("yellow_leaves") and not f.get("humid_weather"),
        "conclusion":  "black_rot",
        "explanation": "R14: Black lesions AND yellow leaves in dry conditions → Black Rot.",
    },
    {
        "id": "R15", "name": "Nematode Infection Detection",
        "condition":   lambda f: f.get("stunted_growth") and f.get("root_galls") and f.get("wilting"),
        "conclusion":  "nematode_infection",
        "explanation": "R15: Stunted growth AND root galls AND wilting → Nematode Infection.",
    },
    # ── Chained / Multi-step Rules ───────────────────────────────
    {
        "id": "R16", "name": "Severity Escalation (Chained)",
        "condition":   lambda f: f.get("severity") == "high" and f.get("multiple_plants_affected"),
        "conclusion":  "immediate_expert_consultation",
        "explanation": "R16 [Chained]: High severity AND multiple plants → Immediate expert consultation.",
    },
    {
        "id": "R17", "name": "Virus-Vector Link (Chained)",
        "condition":   lambda f: (f.get("aphid_infestation_confirmed")
                                  and f.get("yellow_leaves") and f.get("leaf_curl")),
        "conclusion":  "mosaic_virus",
        "explanation": "R17 [Chained]: Confirmed aphids + viral symptoms → Mosaic Virus via vector pathway.",
    },
]

# ── Frame Representation (Part D) ───────────────────────────────
FRAMES = {
    "powdery_mildew": {
        "class":      "FungalDisease",
        "name":       "Powdery Mildew",
        "pathogen":   "Erysiphe spp. (Fungus)",
        "symptoms":   ["white powdery coating", "distorted leaves", "premature leaf drop"],
        "conditions": ["dry weather", "moderate temperatures", "poor air circulation"],
        "crops":      ["wheat", "barley", "cucumber", "squash"],
        "severity":   "medium",
        "contagious": True,
        "treatment":  STATIC_FACTS["treatments"]["powdery_mildew"],
        "prevention": "Use resistant varieties; ensure adequate plant spacing.",
    },
    "late_blight": {
        "class":      "OomyceteDisease",
        "name":       "Late Blight",
        "pathogen":   "Phytophthora infestans",
        "symptoms":   ["water-soaked lesions", "brown spots", "white mold underside", "rapid plant death"],
        "conditions": ["cool temperatures 10–20°C", "high humidity", "wet weather"],
        "crops":      ["tomato", "potato"],
        "severity":   "high",
        "contagious": True,
        "treatment":  STATIC_FACTS["treatments"]["late_blight"],
        "prevention": "Avoid overhead irrigation; use certified disease-free seed tubers.",
    },
    "mosaic_virus": {
        "class":      "ViralDisease",
        "name":       "Mosaic Virus",
        "pathogen":   "Tobamovirus / CMV (Virus)",
        "symptoms":   ["yellow mosaic pattern", "leaf curl", "stunted growth", "mottled appearance"],
        "conditions": ["aphid vectors present", "infected seed or tools"],
        "crops":      ["tomato", "pepper", "bean", "cucumber"],
        "severity":   "high",
        "contagious": True,
        "treatment":  STATIC_FACTS["treatments"]["mosaic_virus"],
        "prevention": "Use virus-indexed seeds; control aphids; disinfect tools.",
    },
    "nitrogen_deficiency": {
        "class":      "NutrientDisorder",
        "name":       "Nitrogen Deficiency",
        "pathogen":   "None (abiotic)",
        "symptoms":   ["yellowing from older leaves", "pale green coloration", "reduced growth"],
        "conditions": ["low soil nitrogen", "poor organic matter", "waterlogged soils"],
        "crops":      ["all crops"],
        "severity":   "medium",
        "contagious": False,
        "treatment":  STATIC_FACTS["treatments"]["nitrogen_deficiency"],
        "prevention": "Regular soil testing; adequate fertilization plan.",
    },
    "root_rot": {
        "class":      "FungalDisease",
        "name":       "Root Rot",
        "pathogen":   "Pythium / Rhizoctonia spp.",
        "symptoms":   ["wilting", "yellow leaves", "dark/mushy roots", "poor growth"],
        "conditions": ["overwatering", "poor drainage", "compacted soils"],
        "crops":      ["maize", "soybean", "bean", "tomato"],
        "severity":   "high",
        "contagious": False,
        "treatment":  STATIC_FACTS["treatments"]["root_rot"],
        "prevention": "Ensure well-drained soil; avoid overwatering; use raised beds.",
    },
}


# ═══════════════════════════════════════════════════════════════
# PART B: INFERENCE ENGINE
# ═══════════════════════════════════════════════════════════════

class InferenceEngine:
    """
    Forward-chaining inference engine.
    Evaluates rules against working memory (user-supplied facts),
    fires matched rules, adds conclusions back to working memory
    (enabling multi-step chaining), and records every step.
    """

    def __init__(self, facts: dict):
        self.working_memory  = dict(facts)   # mutable copy
        self.fired_rules     = []            # rules that matched
        self.conclusions     = []            # final diagnoses
        self.reasoning_chain = []            # full trace

    def run(self) -> list:
        """Execute forward-chaining until fixed-point (no new rules fire)."""
        changed   = True
        iteration = 0

        while changed:
            changed    = False
            iteration += 1
            self.reasoning_chain.append(f"\n── Inference Iteration {iteration} ──")

            for rule in RULES:
                if rule["id"] in [r["id"] for r in self.fired_rules]:
                    continue  # already fired

                try:
                    if rule["condition"](self.working_memory):
                        conclusion = rule["conclusion"]
                        self.fired_rules.append(rule)
                        self.reasoning_chain.append(f"  ✔ {rule['id']} fired  → {conclusion}")
                        self.reasoning_chain.append(f"     {rule['explanation']}")

                        if conclusion not in self.conclusions:
                            self.conclusions.append(conclusion)
                            # Feed conclusion back → enables chained rules
                            self.working_memory[conclusion + "_confirmed"] = True
                            changed = True
                    else:
                        self.reasoning_chain.append(f"  ✘ {rule['id']} not satisfied")

                except Exception as e:
                    self.reasoning_chain.append(f"  ⚠ {rule['id']} error: {e}")

        return self.conclusions


# ═══════════════════════════════════════════════════════════════
# PART C: EXPLANATION FACILITY
# ═══════════════════════════════════════════════════════════════

class ExplanationFacility:
    """Prints diagnosis results, treatments, frame details, and full reasoning trace."""

    @staticmethod
    def explain(engine: InferenceEngine, crop: str = "Unknown"):
        print("\n" + "═" * 62)
        print("        CROP DISEASE DIAGNOSIS – RESULTS")
        print("═" * 62)

        if not engine.conclusions:
            print("\n✅ No disease or stress detected based on provided symptoms.")
            print("   Monitor your crop and re-assess if symptoms develop.")
            return

        print(f"\nCrop    : {crop.upper()}")
        print(f"Symptoms: {sum(1 for v in engine.working_memory.values() if v is True)} active flags\n")

        for i, diagnosis in enumerate(engine.conclusions, 1):
            label = diagnosis.replace("_", " ").title()
            print(f"─── Diagnosis {i}: {label} ───")

            treatment = STATIC_FACTS["treatments"].get(diagnosis)
            if treatment:
                print(f"  💊 Treatment : {treatment}")
            elif diagnosis == "immediate_expert_consultation":
                print("  🚨 Action    : Contact your local agricultural extension officer immediately.")

            frame = FRAMES.get(diagnosis)
            if frame:
                print(f"  🦠 Pathogen  : {frame['pathogen']}")
                print(f"  📋 Symptoms  : {', '.join(frame['symptoms'])}")
                print(f"  ⚠  Severity  : {frame['severity'].upper()}")
                print(f"  🔄 Contagious: {'Yes – isolate affected plants' if frame['contagious'] else 'No'}")
                print(f"  🛡  Prevention: {frame['prevention']}")
            print()

        print("─── Reasoning Trace ───")
        for line in engine.reasoning_chain:
            print(line)

        print("\n─── Rules That Fired ───")
        if engine.fired_rules:
            for rule in engine.fired_rules:
                print(f"  [{rule['id']}] {rule['name']}")
        else:
            print("  None")

        print("\n" + "═" * 62)


# ═══════════════════════════════════════════════════════════════
# INTERACTIVE USER INPUT
# ═══════════════════════════════════════════════════════════════

def ask(question: str) -> bool:
    while True:
        ans = input(f"  {question} [y/n]: ").strip().lower()
        if ans in ("y", "yes"): return True
        if ans in ("n", "no"):  return False
        print("  Please enter y or n.")

def collect_facts_interactively() -> tuple:
    print("\n" + "═" * 62)
    print("   CROP DISEASE DIAGNOSIS KNOWLEDGE-BASED SYSTEM")
    print("         APT 3020 – Knowledge-Based Systems")
    print("═" * 62)
    print("\nAnswer each question with 'y' (yes) or 'n' (no).\n")

    crop = input("Enter crop name (e.g. tomato, maize, wheat): ").strip().lower() or "unknown"
    print()

    facts = {}

    print("── Visual Symptoms ──")
    facts["yellow_leaves"]            = ask("Are the leaves turning yellow?")
    facts["brown_spots"]              = ask("Are there brown spots on the leaves?")
    facts["white_powder_on_leaves"]   = ask("Is there white powdery coating on leaves?")
    facts["black_lesions"]            = ask("Are there black lesions or dark sunken spots?")
    facts["water_soaked_lesions"]     = ask("Are there water-soaked or greasy-looking lesions?")
    facts["leaf_curl"]                = ask("Are the leaves curling or distorting?")
    facts["pale_green_lower_leaves"]  = ask("Are the lower/older leaves pale green?")
    facts["lesions_with_yellow_halo"] = ask("Do brown spots have a yellow halo?")
    facts["circular_spots"]           = ask("Are the spots circular and well-defined?")
    facts["sunken_spots"]             = ask("Are spots sunken (depressed into tissue)?")
    facts["sticky_residue"]           = ask("Is there sticky residue (honeydew) on leaves?")
    facts["visible_insects"]          = ask("Can you see small insects on the plant?")

    print("\n── Structural & Systemic Symptoms ──")
    facts["wilting"]               = ask("Is the plant wilting despite adequate water?")
    facts["stunted_growth"]        = ask("Is the plant growing slower than expected?")
    facts["brown_vascular_tissue"] = ask("When you cut the stem, is the inner tissue brown?")
    facts["root_galls"]            = ask("Are there knots/galls on the roots?")

    print("\n── Environmental & Management Context ──")
    facts["dry_weather"]               = ask("Has the weather been hot and dry recently?")
    facts["cool_wet_weather"]          = ask("Has the weather been cool and wet/rainy?")
    facts["humid_weather"]             = ask("Is the weather generally humid?")
    facts["overwatering"]              = ask("Has the crop been heavily/frequently irrigated?")
    facts["multiple_plants_affected"]  = ask("Are multiple plants in the field showing symptoms?")

    print("\n── Severity Assessment ──")
    print("  How much of the plant is affected?")
    print("   1 = Low (<20%)   2 = Medium (20–50%)   3 = High (>50%)")
    while True:
        sev = input("  Enter 1, 2, or 3: ").strip()
        if sev == "1": facts["severity"] = "low";    break
        if sev == "2": facts["severity"] = "medium"; break
        if sev == "3": facts["severity"] = "high";   break
        print("  Please enter 1, 2, or 3.")

    return facts, crop


# ═══════════════════════════════════════════════════════════════
# PART E: TEST CASES
# ═══════════════════════════════════════════════════════════════

TEST_CASES = [
    {
        "name": "TC01 – Powdery Mildew (Cucumber)",
        "crop": "cucumber",
        "expected": ["powdery_mildew"],
        "facts": {
            "white_powder_on_leaves": True,  "dry_weather": True,
            "yellow_leaves": False,           "brown_spots": False,
            "wilting": False,                 "stunted_growth": False,
            "leaf_curl": False,               "water_soaked_lesions": False,
            "black_lesions": False,           "overwatering": False,
            "cool_wet_weather": False,        "humid_weather": False,
            "pale_green_lower_leaves": False, "brown_vascular_tissue": False,
            "root_galls": False,              "lesions_with_yellow_halo": False,
            "circular_spots": False,          "sunken_spots": False,
            "sticky_residue": False,          "visible_insects": False,
            "multiple_plants_affected": False,"severity": "medium",
        },
    },
    {
        "name": "TC02 – Late Blight + Expert Alert (Tomato)",
        "crop": "tomato",
        "expected": ["late_blight", "immediate_expert_consultation"],
        "facts": {
            "water_soaked_lesions": True,     "cool_wet_weather": True,
            "brown_spots": True,              "multiple_plants_affected": True,
            "white_powder_on_leaves": False,  "dry_weather": False,
            "yellow_leaves": False,           "wilting": False,
            "stunted_growth": False,          "leaf_curl": False,
            "black_lesions": False,           "overwatering": False,
            "humid_weather": False,           "pale_green_lower_leaves": False,
            "brown_vascular_tissue": False,   "root_galls": False,
            "lesions_with_yellow_halo": False,"circular_spots": False,
            "sunken_spots": False,            "sticky_residue": False,
            "visible_insects": False,         "severity": "high",
        },
    },
    {
        "name": "TC03 – Mosaic Virus (Pepper)",
        "crop": "pepper",
        "expected": ["mosaic_virus"],
        "facts": {
            "yellow_leaves": True,            "leaf_curl": True,
            "stunted_growth": True,           "white_powder_on_leaves": False,
            "dry_weather": False,             "brown_spots": False,
            "wilting": False,                 "water_soaked_lesions": False,
            "black_lesions": False,           "overwatering": False,
            "cool_wet_weather": False,        "humid_weather": False,
            "pale_green_lower_leaves": False, "brown_vascular_tissue": False,
            "root_galls": False,              "lesions_with_yellow_halo": False,
            "circular_spots": False,          "sunken_spots": False,
            "sticky_residue": False,          "visible_insects": False,
            "multiple_plants_affected": False,"severity": "medium",
        },
    },
    {
        "name": "TC04 – Nitrogen Deficiency (Maize)",
        "crop": "maize",
        "expected": ["nitrogen_deficiency"],
        "facts": {
            "yellow_leaves": True,            "pale_green_lower_leaves": True,
            "wilting": False,                 "white_powder_on_leaves": False,
            "dry_weather": False,             "brown_spots": False,
            "stunted_growth": False,          "leaf_curl": False,
            "water_soaked_lesions": False,    "black_lesions": False,
            "overwatering": False,            "cool_wet_weather": False,
            "humid_weather": False,           "brown_vascular_tissue": False,
            "root_galls": False,              "lesions_with_yellow_halo": False,
            "circular_spots": False,          "sunken_spots": False,
            "sticky_residue": False,          "visible_insects": False,
            "multiple_plants_affected": False,"severity": "low",
        },
    },
    {
        "name": "TC05 – Root Rot (Tomato)",
        "crop": "tomato",
        "expected": ["root_rot"],
        "facts": {
            "wilting": True,                  "yellow_leaves": True,
            "overwatering": True,             "white_powder_on_leaves": False,
            "dry_weather": False,             "brown_spots": False,
            "stunted_growth": False,          "leaf_curl": False,
            "water_soaked_lesions": False,    "black_lesions": False,
            "cool_wet_weather": False,        "humid_weather": False,
            "pale_green_lower_leaves": False, "brown_vascular_tissue": False,
            "root_galls": False,              "lesions_with_yellow_halo": False,
            "circular_spots": False,          "sunken_spots": False,
            "sticky_residue": False,          "visible_insects": False,
            "multiple_plants_affected": False,"severity": "medium",
        },
    },
    {
        "name": "TC06 – Aphid + Mosaic Virus chain (Bean)",
        "crop": "bean",
        "expected": ["mosaic_virus", "aphid_infestation", "immediate_expert_consultation"],
        "facts": {
            "leaf_curl": True,                "sticky_residue": True,
            "visible_insects": True,          "yellow_leaves": True,
            "stunted_growth": True,           "multiple_plants_affected": True,
            "white_powder_on_leaves": False,  "dry_weather": False,
            "brown_spots": False,             "wilting": False,
            "water_soaked_lesions": False,    "black_lesions": False,
            "overwatering": False,            "cool_wet_weather": False,
            "humid_weather": False,           "pale_green_lower_leaves": False,
            "brown_vascular_tissue": False,   "root_galls": False,
            "lesions_with_yellow_halo": False,"circular_spots": False,
            "sunken_spots": False,            "severity": "high",
        },
    },
    {
        "name": "TC07 – No Disease (Healthy Wheat)",
        "crop": "wheat",
        "expected": [],
        "facts": {
            "yellow_leaves": False,           "brown_spots": False,
            "white_powder_on_leaves": False,  "black_lesions": False,
            "water_soaked_lesions": False,    "leaf_curl": False,
            "pale_green_lower_leaves": False, "lesions_with_yellow_halo": False,
            "circular_spots": False,          "sunken_spots": False,
            "sticky_residue": False,          "visible_insects": False,
            "wilting": False,                 "stunted_growth": False,
            "brown_vascular_tissue": False,   "root_galls": False,
            "dry_weather": False,             "cool_wet_weather": False,
            "humid_weather": False,           "overwatering": False,
            "multiple_plants_affected": False,"severity": "low",
        },
    },
]


def run_all_tests():
    print("\n" + "█" * 62)
    print("        AUTOMATED TEST SUITE – ALL TEST CASES")
    print("█" * 62)

    results = []
    for tc in TEST_CASES:
        print(f"\n{'▓' * 62}")
        print(f"  TEST: {tc['name']}  |  Crop: {tc['crop'].upper()}")
        print(f"{'▓' * 62}")

        engine = InferenceEngine(tc["facts"])
        actual = engine.run()
        ExplanationFacility.explain(engine, tc["crop"])

        passed = sorted(actual) == sorted(tc["expected"])
        results.append({"name": tc["name"], "expected": tc["expected"],
                         "actual": actual, "passed": passed})

    # Summary table
    print("\n" + "═" * 62)
    print("  TEST SUMMARY")
    print("═" * 62)
    for r in results:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"\n  {status}  {r['name']}")
        print(f"           Expected : {r['expected']}")
        print(f"           Got      : {r['actual']}")

    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n  Result: {passed_count}/{len(results)} tests passed")
    print("═" * 62)


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_all_tests()
        return

    # Interactive mode
    facts, crop = collect_facts_interactively()
    engine = InferenceEngine(facts)
    engine.run()
    ExplanationFacility.explain(engine, crop)

    print()
    again = input("Diagnose another crop? [y/n]: ").strip().lower()
    if again in ("y", "yes"):
        main()


if __name__ == "__main__":
    main()
