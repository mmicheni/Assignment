# Test Cases – Crop Disease Diagnosis KBS

## Overview
7 test cases were designed to cover: single-diagnosis scenarios, multi-diagnosis chaining, abiotic disorders, and the healthy-plant (no-disease) edge case.

---

## TC01 – Powdery Mildew (Cucumber)

**Inputs:**
- white_powder_on_leaves: ✅
- dry_weather: ✅
- All others: ❌

**Rules Fired:** R01  
**Expected Output:** `powdery_mildew`  
**Actual Output:** `powdery_mildew`  
**Result:** ✅ PASS  

**Treatment Given:**  
Apply sulfur-based fungicide; improve air circulation; avoid overhead irrigation.

---

## TC02 – Late Blight (Tomato)

**Inputs:**
- water_soaked_lesions: ✅
- cool_wet_weather: ✅
- brown_spots: ✅
- multiple_plants_affected: ✅
- severity: high

**Rules Fired:** R02, R16 (chained – severity escalation)  
**Expected Output:** `late_blight`, `immediate_expert_consultation`  
**Actual Output:** `late_blight`, `immediate_expert_consultation`  
**Result:** ✅ PASS  

**Demonstrates:** Multi-step chaining – R02 fires first, adds `late_blight` to working memory; R16 then evaluates `high severity + multiple plants` and fires independently.

---

## TC03 – Mosaic Virus (Pepper)

**Inputs:**
- yellow_leaves: ✅
- leaf_curl: ✅
- stunted_growth: ✅

**Rules Fired:** R03  
**Expected Output:** `mosaic_virus`  
**Actual Output:** `mosaic_virus`  
**Result:** ✅ PASS  

---

## TC04 – Nitrogen Deficiency (Maize)

**Inputs:**
- yellow_leaves: ✅
- pale_green_lower_leaves: ✅
- wilting: ❌ (critical distinguishing factor)

**Rules Fired:** R04  
**Expected Output:** `nitrogen_deficiency`  
**Actual Output:** `nitrogen_deficiency`  
**Result:** ✅ PASS  

**Note:** The absence of wilting is a negative condition used to distinguish this from Root Rot (R05), demonstrating negation-as-failure reasoning.

---

## TC05 – Root Rot (Tomato)

**Inputs:**
- wilting: ✅
- yellow_leaves: ✅
- overwatering: ✅

**Rules Fired:** R05  
**Expected Output:** `root_rot`  
**Actual Output:** `root_rot`  
**Result:** ✅ PASS  

---

## TC06 – Aphid Infestation + Mosaic Virus (Multi-Step Chaining – Bean)

**Inputs:**
- leaf_curl: ✅
- sticky_residue: ✅
- visible_insects: ✅
- yellow_leaves: ✅
- stunted_growth: ✅
- multiple_plants_affected: ✅
- severity: high

**Rules Fired:** R03, R13, R16, R17  
**Expected Output:** `aphid_infestation`, `mosaic_virus`, `immediate_expert_consultation`  
**Actual Output:** `mosaic_virus`, `aphid_infestation`, `immediate_expert_consultation`  
**Result:** ✅ PASS  

**Demonstrates 3-level chaining:**
1. R03 fires (yellow + leaf_curl + stunted → mosaic_virus)
2. R13 fires (leaf_curl + sticky + insects → aphid_infestation)
3. R16 fires (high severity + multiple plants → expert consultation)
4. R17 fires (aphid confirmed + viral symptoms → re-confirms mosaic_virus via vector pathway)

---

## TC07 – No Disease (Healthy Wheat)

**Inputs:** All symptom flags: ❌, severity: low

**Rules Fired:** None  
**Expected Output:** `[]` (empty)  
**Actual Output:** `[]`  
**Result:** ✅ PASS  

**Note:** Tests the system's ability to correctly output "no diagnosis" when no rules fire, avoiding false positives.

---

## Summary Table

| ID   | Crop     | Expected Diagnosis               | Result  |
|------|----------|----------------------------------|---------|
| TC01 | Cucumber | Powdery Mildew                   | ✅ PASS |
| TC02 | Tomato   | Late Blight + Expert Alert       | ✅ PASS |
| TC03 | Pepper   | Mosaic Virus                     | ✅ PASS |
| TC04 | Maize    | Nitrogen Deficiency              | ✅ PASS |
| TC05 | Tomato   | Root Rot                         | ✅ PASS |
| TC06 | Bean     | Aphid + Mosaic Virus + Alert     | ✅ PASS |
| TC07 | Wheat    | No Disease                       | ✅ PASS |

**7/7 tests passed (100%)**
