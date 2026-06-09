# Crop Disease Diagnosis Knowledge-Based System
### APT 3020 – Quiz 1 | Knowledge-Based Systems

---

## Problem Being Solved

Smallholder farmers and agronomists often lack immediate access to expert knowledge when crop diseases appear. This KBS simulates an agricultural expert system that accepts observed symptoms and environmental conditions, applies forward-chaining inference over a rule base, and produces a diagnosis with treatment recommendations and full reasoning explanation.

**Domain:** Crop Disease Diagnosis  
**Language:** Python 3.10+  
**Paradigm:** Rule-Based Expert System with Forward-Chaining Inference

---

## Repository Structure

```
kbs-assignment/
├── README.md               ← This file
├── main.py                 ← Entry point: inference engine + UI + explanation facility
├── knowledge_base.py       ← Facts, rules, frames (knowledge representation)
├── test_runner.py          ← Automated test cases
├── test_cases.md           ← Documented test results
├── diagrams/
│   └── semantic_network.png ← Part D: Semantic network diagram
└── screenshots/            ← Sample output screenshots
```

---

## Facts Used (15+)

Stored in `STATIC_FACTS` in `knowledge_base.py`:

| # | Fact |
|---|------|
| F01 | Yellow leaves may indicate nitrogen deficiency, mosaic virus, or root rot |
| F02 | Brown spots may indicate leaf blight, cercospora leaf spot, or bacterial spot |
| F03 | Wilting may indicate root rot, fusarium wilt, or drought stress |
| F04 | White powder on leaves indicates powdery mildew |
| F05 | Black lesions indicate anthracnose or black rot |
| F06 | Stunted growth indicates nutrient deficiency, mosaic virus, or nematode infection |
| F07 | Leaf curl indicates mosaic virus, aphid infestation, or drought stress |
| F08 | Water-soaked lesions indicate late blight or bacterial spot |
| F09 | Treatment for powdery mildew: sulfur-based fungicide |
| F10 | Treatment for late blight: copper-based fungicide (urgent) |
| F11 | Treatment for mosaic virus: remove infected plants, control aphid vectors |
| F12 | Treatment for nitrogen deficiency: apply urea or DAP fertilizer |
| F13 | Treatment for root rot: improve drainage, apply Trichoderma bio-fungicide |
| F14 | Tomato and potato are susceptible to late blight |
| F15 | Wheat, barley, cucumber, squash are susceptible to powdery mildew |
| F16 | Aphids are vectors for mosaic virus transmission |
| F17 | Severity levels: Low (<20%), Medium (20–50%), High (>50%) |
| F18 | Fusarium wilt is identified by brown vascular tissue when stem is cut |
| F19 | Root galls are a key indicator of nematode infection |
| F20 | Nematode management includes soil solarization and marigold trap crops |

---

## Rules Used (17)

Defined in `RULES` list in `knowledge_base.py`:

| ID  | Rule Name | Condition | Conclusion |
|-----|-----------|-----------|------------|
| R01 | Powdery Mildew Detection | white_powder + dry_weather | powdery_mildew |
| R02 | Late Blight Detection | water_soaked_lesions + cool_wet_weather + brown_spots | late_blight |
| R03 | Mosaic Virus Detection | yellow_leaves + leaf_curl + stunted_growth | mosaic_virus |
| R04 | Nitrogen Deficiency | yellow_leaves + pale_lower_leaves + NOT wilting | nitrogen_deficiency |
| R05 | Root Rot Detection | wilting + yellow_leaves + overwatering | root_rot |
| R06 | Fusarium Wilt Detection | wilting + brown_vascular_tissue + NOT overwatering | fusarium_wilt |
| R07 | Leaf Blight Detection | brown_spots + yellow_halo + humid_weather | leaf_blight |
| R08 | Cercospora Leaf Spot | brown_spots + circular_spots + NOT humid_weather | cercospora_leaf_spot |
| R09 | Bacterial Spot Detection | water_soaked_lesions + brown_spots + NOT cool_wet | bacterial_spot |
| R10 | Anthracnose Detection | black_lesions + sunken_spots + humid_weather | anthracnose |
| R11 | Drought Stress Detection | wilting + leaf_curl + dry_weather + NOT yellow_leaves | drought_stress |
| R12 | General Nutrient Deficiency | stunted_growth + pale_lower_leaves + NOT yellow | nutrient_deficiency |
| R13 | Aphid Infestation | leaf_curl + sticky_residue + visible_insects | aphid_infestation |
| R14 | Black Rot Detection | black_lesions + yellow_leaves + NOT humid | black_rot |
| R15 | Nematode Infection | stunted_growth + root_galls + wilting | nematode_infection |
| R16 | Severity Escalation (Chained) | severity==high + multiple_plants_affected | immediate_expert_consultation |
| R17 | Virus-Vector Link (Chained) | aphid_infestation_confirmed + yellow_leaves + leaf_curl | mosaic_virus |

---

## How Inference Works

The system uses **forward-chaining** (data-driven) inference:

```
User provides symptom facts
        ↓
InferenceEngine loads facts into Working Memory
        ↓
Iterate over all rules:
   IF rule condition matches working memory facts → fire rule
   → Add conclusion to working memory (enables chaining)
   → Record rule in reasoning trace
        ↓
Repeat until no new rules fire (fixed-point)
        ↓
ExplanationFacility prints all conclusions + trace
```

**Multi-step chaining example (TC06):**
```
Symptoms: leaf_curl + sticky_residue + visible_insects + yellow_leaves + stunted_growth
    → R13 fires → aphid_infestation added to working memory
    → R03 fires → mosaic_virus added to working memory  
    → R17 fires → mosaic_virus re-confirmed via aphid vector pathway
    → R16 fires → immediate_expert_consultation (high severity + multiple plants)
```

**Negation-as-failure** is used in R04, R06, R08, R11, R12, R14 – the absence of a fact is a condition.

---

## Knowledge Representation – Frame Representation (Part D)

Five disease frames are defined in `FRAMES` in `knowledge_base.py`. Each frame captures:

| Slot | Description |
|------|-------------|
| `class` | Disease category (FungalDisease, ViralDisease, NutrientDisorder…) |
| `name` | Human-readable name |
| `pathogen` | Causative organism |
| `symptoms` | List of characteristic symptoms |
| `conditions` | Environmental conditions favouring the disease |
| `crops` | Susceptible crop types |
| `severity` | Typical severity level |
| `contagious` | Boolean – whether isolation is needed |
| `treatment` | Recommended treatment |
| `prevention` | Preventive measures |

**Diseases with frames:** Powdery Mildew, Late Blight, Mosaic Virus, Nitrogen Deficiency, Root Rot.

The semantic network diagram is in `diagrams/semantic_network.png`.

---

## Possible Conclusions / Recommendations (15)

1. `powdery_mildew`
2. `late_blight`
3. `mosaic_virus`
4. `nitrogen_deficiency`
5. `root_rot`
6. `fusarium_wilt`
7. `leaf_blight`
8. `cercospora_leaf_spot`
9. `bacterial_spot`
10. `anthracnose`
11. `drought_stress`
12. `nutrient_deficiency`
13. `aphid_infestation`
14. `black_rot`
15. `nematode_infection`
16. `immediate_expert_consultation` *(chained escalation)*

---

## How to Run the System

### Requirements
- Python 3.10 or higher
- No external dependencies for the KBS itself

```bash
# Clone the repository
git clone https://github.com/<your-username>/kbs-assignment.git
cd kbs-assignment

# Run interactive mode
python main.py

# Run all automated test cases
python test_runner.py
# or
python main.py --test
```

---

## Sample Output

```
══════════════════════════════════════════════════════════
         CROP DISEASE DIAGNOSIS – RESULTS
══════════════════════════════════════════════════════════

Crop: TOMATO
Symptoms analysed: 6 active symptom flags

─── Diagnosis 1: Late Blight ───
  💊 Treatment : Apply copper-based fungicide immediately; remove infected tissue.
  🦠 Pathogen  : Phytophthora infestans
  📋 Symptoms  : water-soaked lesions, brown spots, white mold on undersides
  ⚠  Severity  : HIGH
  🔄 Contagious: Yes – isolate affected plants
  🛡  Prevention: Avoid overhead irrigation; use certified disease-free seed tubers.

─── Diagnosis 2: Immediate Expert Consultation ───
  🚨 Action    : Contact your local agricultural extension officer immediately.

─── Reasoning Trace ───

── Inference Iteration 1 ──
  ✔ R02 fired → late_blight
     Reason: R02: Water-soaked lesions AND cool/wet weather AND brown spots → Late Blight confirmed.
  ✔ R16 fired → immediate_expert_consultation
     Reason: R16 (Chained): High severity AND multiple plants affected → Immediate expert consultation required.

─── Rules That Fired ───
  [R02] Late Blight Detection
  [R16] Severe Disease Escalation
```

---

## Testing

See `test_cases.md` for full documentation. Summary:

| Test | Crop | Diagnosis | Result |
|------|------|-----------|--------|
| TC01 | Cucumber | Powdery Mildew | ✅ PASS |
| TC02 | Tomato | Late Blight + Expert Alert | ✅ PASS |
| TC03 | Pepper | Mosaic Virus | ✅ PASS |
| TC04 | Maize | Nitrogen Deficiency | ✅ PASS |
| TC05 | Tomato | Root Rot | ✅ PASS |
| TC06 | Bean | Aphid + Mosaic Virus (chained) | ✅ PASS |
| TC07 | Wheat | No Disease | ✅ PASS |

**7/7 tests passed**
