"""
knowledge_base.py
-----------------
Crop Disease Diagnosis Knowledge-Based System
Contains: facts, rules, conclusions, and frame representations.
"""

# ─────────────────────────────────────────────
# STATIC FACTS (domain knowledge - always true)
# ─────────────────────────────────────────────
STATIC_FACTS = {
    # Symptom → possible disease mapping (supporting rules)
    "yellow_leaves_indicates": ["nitrogen_deficiency", "mosaic_virus", "root_rot"],
    "brown_spots_indicates":   ["leaf_blight", "cercospora_leaf_spot", "bacterial_spot"],
    "wilting_indicates":       ["root_rot", "fusarium_wilt", "drought_stress"],
    "white_powder_indicates":  ["powdery_mildew"],
    "black_lesions_indicates": ["anthracnose", "black_rot"],
    "stunted_growth_indicates":["nutrient_deficiency", "mosaic_virus", "nematode_infection"],
    "leaf_curl_indicates":     ["mosaic_virus", "aphid_infestation", "drought_stress"],
    "water_soaked_lesions_indicates": ["late_blight", "bacterial_spot"],

    # Disease → treatment mapping
    "treatments": {
        "powdery_mildew":      "Apply sulfur-based fungicide; improve air circulation; avoid overhead irrigation.",
        "late_blight":         "Apply copper-based fungicide immediately; remove infected tissue; avoid wet foliage.",
        "mosaic_virus":        "Remove and destroy infected plants; control aphid vectors; use virus-resistant seeds.",
        "nitrogen_deficiency": "Apply nitrogen-rich fertilizer (urea or DAP); incorporate organic compost.",
        "root_rot":            "Improve drainage; reduce watering; apply Trichoderma-based bio-fungicide.",
        "fusarium_wilt":       "Solarize soil; use resistant varieties; apply biocontrol agents like Bacillus subtilis.",
        "leaf_blight":         "Apply mancozeb or chlorothalonil fungicide; practice crop rotation.",
        "cercospora_leaf_spot":"Apply fungicide (azoxystrobin); remove infected leaves; maintain plant spacing.",
        "bacterial_spot":      "Apply copper bactericide; avoid overhead watering; use certified disease-free seeds.",
        "anthracnose":         "Apply mancozeb fungicide; destroy infected debris; use resistant cultivars.",
        "drought_stress":      "Irrigate promptly; apply mulch to retain soil moisture; use drought-tolerant varieties.",
        "nutrient_deficiency": "Conduct soil test; apply balanced NPK fertilizer; correct soil pH if needed.",
        "aphid_infestation":   "Apply insecticidal soap or neem oil; introduce natural predators (ladybugs).",
        "black_rot":           "Remove infected plant parts; apply copper fungicide; practice 2-year crop rotation.",
        "nematode_infection":  "Apply nematicides; solarize soil; incorporate marigold as a trap crop.",
    },

    # Severity thresholds
    "severity_levels": {
        "low":    "Affects <20% of plant",
        "medium": "Affects 20-50% of plant",
        "high":   "Affects >50% of plant or multiple plants",
    },

    # Crop susceptibility facts
    "crops_susceptible_to_powdery_mildew":   ["wheat", "barley", "cucumber", "squash"],
    "crops_susceptible_to_late_blight":      ["tomato", "potato"],
    "crops_susceptible_to_mosaic_virus":     ["tomato", "pepper", "bean", "cucumber"],
    "crops_susceptible_to_root_rot":         ["maize", "soybean", "bean", "tomato"],
    "crops_susceptible_to_fusarium_wilt":    ["tomato", "banana", "cotton", "melon"],
    "crops_susceptible_to_leaf_blight":      ["maize", "rice", "wheat", "sorghum"],
    "crops_susceptible_to_bacterial_spot":   ["tomato", "pepper"],
    "crops_susceptible_to_anthracnose":      ["mango", "bean", "pepper", "cucumber"],
    "crops_susceptible_to_nematode_infection":["tomato", "carrot", "banana", "pepper"],
}

# ─────────────────────────────────────────────
# RULES
# Each rule: condition function + conclusion key + explanation string
# ─────────────────────────────────────────────
RULES = [
    {
        "id": "R01",
        "name": "Powdery Mildew Detection",
        "condition": lambda f: f.get("white_powder_on_leaves") and f.get("dry_weather"),
        "conclusion": "powdery_mildew",
        "explanation": "R01: White powder on leaves AND dry weather → Powdery Mildew confirmed.",
    },
    {
        "id": "R02",
        "name": "Late Blight Detection",
        "condition": lambda f: f.get("water_soaked_lesions") and f.get("cool_wet_weather") and f.get("brown_spots"),
        "conclusion": "late_blight",
        "explanation": "R02: Water-soaked lesions AND cool/wet weather AND brown spots → Late Blight confirmed.",
    },
    {
        "id": "R03",
        "name": "Mosaic Virus Detection",
        "condition": lambda f: f.get("yellow_leaves") and f.get("leaf_curl") and f.get("stunted_growth"),
        "conclusion": "mosaic_virus",
        "explanation": "R03: Yellow leaves AND leaf curl AND stunted growth → Mosaic Virus confirmed.",
    },
    {
        "id": "R04",
        "name": "Nitrogen Deficiency Detection",
        "condition": lambda f: f.get("yellow_leaves") and f.get("pale_green_lower_leaves") and not f.get("wilting"),
        "conclusion": "nitrogen_deficiency",
        "explanation": "R04: Yellow leaves AND pale lower leaves AND no wilting → Nitrogen Deficiency.",
    },
    {
        "id": "R05",
        "name": "Root Rot Detection",
        "condition": lambda f: f.get("wilting") and f.get("yellow_leaves") and f.get("overwatering"),
        "conclusion": "root_rot",
        "explanation": "R05: Wilting AND yellow leaves AND history of overwatering → Root Rot.",
    },
    {
        "id": "R06",
        "name": "Fusarium Wilt Detection",
        "condition": lambda f: f.get("wilting") and f.get("brown_vascular_tissue") and not f.get("overwatering"),
        "conclusion": "fusarium_wilt",
        "explanation": "R06: Wilting AND brown vascular tissue AND no overwatering → Fusarium Wilt.",
    },
    {
        "id": "R07",
        "name": "Leaf Blight Detection",
        "condition": lambda f: f.get("brown_spots") and f.get("lesions_with_yellow_halo") and f.get("humid_weather"),
        "conclusion": "leaf_blight",
        "explanation": "R07: Brown spots AND yellow halo AND humid weather → Leaf Blight.",
    },
    {
        "id": "R08",
        "name": "Cercospora Leaf Spot Detection",
        "condition": lambda f: f.get("brown_spots") and f.get("circular_spots") and not f.get("humid_weather"),
        "conclusion": "cercospora_leaf_spot",
        "explanation": "R08: Brown circular spots without humidity → Cercospora Leaf Spot.",
    },
    {
        "id": "R09",
        "name": "Bacterial Spot Detection",
        "condition": lambda f: f.get("water_soaked_lesions") and f.get("brown_spots") and not f.get("cool_wet_weather"),
        "conclusion": "bacterial_spot",
        "explanation": "R09: Water-soaked lesions AND brown spots in warm weather → Bacterial Spot.",
    },
    {
        "id": "R10",
        "name": "Anthracnose Detection",
        "condition": lambda f: f.get("black_lesions") and f.get("sunken_spots") and f.get("humid_weather"),
        "conclusion": "anthracnose",
        "explanation": "R10: Black sunken spots AND humid weather → Anthracnose.",
    },
    {
        "id": "R11",
        "name": "Drought Stress Detection",
        "condition": lambda f: f.get("wilting") and f.get("leaf_curl") and f.get("dry_weather") and not f.get("yellow_leaves"),
        "conclusion": "drought_stress",
        "explanation": "R11: Wilting AND leaf curl AND dry weather AND no yellowing → Drought Stress.",
    },
    {
        "id": "R12",
        "name": "General Nutrient Deficiency",
        "condition": lambda f: f.get("stunted_growth") and f.get("pale_green_lower_leaves") and not f.get("yellow_leaves"),
        "conclusion": "nutrient_deficiency",
        "explanation": "R12: Stunted growth AND pale lower leaves (no yellowing) → General Nutrient Deficiency.",
    },
    {
        "id": "R13",
        "name": "Aphid Infestation Detection",
        "condition": lambda f: f.get("leaf_curl") and f.get("sticky_residue") and f.get("visible_insects"),
        "conclusion": "aphid_infestation",
        "explanation": "R13: Leaf curl AND sticky residue AND visible insects → Aphid Infestation.",
    },
    {
        "id": "R14",
        "name": "Black Rot Detection",
        "condition": lambda f: f.get("black_lesions") and f.get("yellow_leaves") and not f.get("humid_weather"),
        "conclusion": "black_rot",
        "explanation": "R14: Black lesions AND yellow leaves in dry weather → Black Rot.",
    },
    {
        "id": "R15",
        "name": "Nematode Infection Detection",
        "condition": lambda f: f.get("stunted_growth") and f.get("root_galls") and f.get("wilting"),
        "conclusion": "nematode_infection",
        "explanation": "R15: Stunted growth AND root galls AND wilting → Nematode Infection.",
    },
    # Multi-step chained rules
    {
        "id": "R16",
        "name": "Severe Disease Escalation",
        "condition": lambda f: f.get("severity") == "high" and f.get("multiple_plants_affected"),
        "conclusion": "immediate_expert_consultation",
        "explanation": "R16 (Chained): High severity AND multiple plants affected → Immediate expert consultation required.",
    },
    {
        "id": "R17",
        "name": "Virus-Vector Link",
        "condition": lambda f: f.get("aphid_infestation_confirmed") and f.get("yellow_leaves") and f.get("leaf_curl"),
        "conclusion": "mosaic_virus",
        "explanation": "R17 (Chained): Confirmed aphid infestation with viral symptoms → Mosaic Virus via vector.",
    },
]

# ─────────────────────────────────────────────
# FRAME REPRESENTATION (Part D)
# ─────────────────────────────────────────────
FRAMES = {
    "powdery_mildew": {
        "class":       "FungalDisease",
        "name":        "Powdery Mildew",
        "pathogen":    "Erysiphe spp. (Fungus)",
        "symptoms":    ["white powdery coating", "distorted leaves", "premature leaf drop"],
        "conditions":  ["dry weather", "moderate temperatures", "poor air circulation"],
        "crops":       ["wheat", "barley", "cucumber", "squash"],
        "severity":    "medium",
        "contagious":  True,
        "treatment":   STATIC_FACTS["treatments"]["powdery_mildew"],
        "prevention":  "Use resistant varieties; ensure adequate plant spacing.",
    },
    "late_blight": {
        "class":       "OomyceteDisease",
        "name":        "Late Blight",
        "pathogen":    "Phytophthora infestans",
        "symptoms":    ["water-soaked lesions", "brown spots", "white mold on undersides", "rapid plant death"],
        "conditions":  ["cool temperatures (10-20°C)", "high humidity", "wet weather"],
        "crops":       ["tomato", "potato"],
        "severity":    "high",
        "contagious":  True,
        "treatment":   STATIC_FACTS["treatments"]["late_blight"],
        "prevention":  "Avoid overhead irrigation; use certified disease-free seed tubers.",
    },
    "mosaic_virus": {
        "class":       "ViralDisease",
        "name":        "Mosaic Virus",
        "pathogen":    "Tobamovirus / CMV (Virus)",
        "symptoms":    ["yellow mosaic pattern", "leaf curl", "stunted growth", "mottled appearance"],
        "conditions":  ["aphid vectors present", "infected seed or tools"],
        "crops":       ["tomato", "pepper", "bean", "cucumber"],
        "severity":    "high",
        "contagious":  True,
        "treatment":   STATIC_FACTS["treatments"]["mosaic_virus"],
        "prevention":  "Use virus-indexed seeds; control aphids; disinfect tools.",
    },
    "nitrogen_deficiency": {
        "class":       "NutrientDisorder",
        "name":        "Nitrogen Deficiency",
        "pathogen":    "None (abiotic)",
        "symptoms":    ["yellowing starting from older leaves", "pale green coloration", "reduced growth"],
        "conditions":  ["low soil nitrogen", "poor soil organic matter", "waterlogged soils"],
        "crops":       ["all crops"],
        "severity":    "medium",
        "contagious":  False,
        "treatment":   STATIC_FACTS["treatments"]["nitrogen_deficiency"],
        "prevention":  "Regular soil testing; adequate fertilization plan.",
    },
    "root_rot": {
        "class":       "FungalDisease",
        "name":        "Root Rot",
        "pathogen":    "Pythium / Rhizoctonia spp.",
        "symptoms":    ["wilting", "yellow leaves", "dark/mushy roots", "poor growth"],
        "conditions":  ["overwatering", "poor drainage", "compacted soils"],
        "crops":       ["maize", "soybean", "bean", "tomato"],
        "severity":    "high",
        "contagious":  False,
        "treatment":   STATIC_FACTS["treatments"]["root_rot"],
        "prevention":  "Ensure well-drained soil; avoid overwatering; use raised beds.",
    },
}
