"""
test_runner.py
--------------
Automated test cases for the Crop Disease Diagnosis KBS.
Run via: python main.py --test
"""

from main import run_test_case

# ─────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────

TEST_CASES = [
    {
        "name": "TC01 – Powdery Mildew (Cucumber)",
        "crop": "cucumber",
        "facts": {
            "white_powder_on_leaves":  True,
            "dry_weather":             True,
            "yellow_leaves":           False,
            "brown_spots":             False,
            "wilting":                 False,
            "stunted_growth":          False,
            "leaf_curl":               False,
            "water_soaked_lesions":    False,
            "black_lesions":           False,
            "overwatering":            False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "pale_green_lower_leaves": False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "multiple_plants_affected":False,
            "severity":                "medium",
        },
        "expected": ["powdery_mildew"],
    },
    {
        "name": "TC02 – Late Blight (Tomato)",
        "crop": "tomato",
        "facts": {
            "water_soaked_lesions":    True,
            "cool_wet_weather":        True,
            "brown_spots":             True,
            "white_powder_on_leaves":  False,
            "dry_weather":             False,
            "yellow_leaves":           False,
            "wilting":                 False,
            "stunted_growth":          False,
            "leaf_curl":               False,
            "black_lesions":           False,
            "overwatering":            False,
            "humid_weather":           False,
            "pale_green_lower_leaves": False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "multiple_plants_affected":True,
            "severity":                "high",
        },
        "expected": ["late_blight", "immediate_expert_consultation"],
    },
    {
        "name": "TC03 – Mosaic Virus (Pepper)",
        "crop": "pepper",
        "facts": {
            "yellow_leaves":           True,
            "leaf_curl":               True,
            "stunted_growth":          True,
            "white_powder_on_leaves":  False,
            "dry_weather":             False,
            "brown_spots":             False,
            "wilting":                 False,
            "water_soaked_lesions":    False,
            "black_lesions":           False,
            "overwatering":            False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "pale_green_lower_leaves": False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "multiple_plants_affected":False,
            "severity":                "medium",
        },
        "expected": ["mosaic_virus"],
    },
    {
        "name": "TC04 – Nitrogen Deficiency (Maize)",
        "crop": "maize",
        "facts": {
            "yellow_leaves":           True,
            "pale_green_lower_leaves": True,
            "wilting":                 False,
            "white_powder_on_leaves":  False,
            "dry_weather":             False,
            "brown_spots":             False,
            "stunted_growth":          False,
            "leaf_curl":               False,
            "water_soaked_lesions":    False,
            "black_lesions":           False,
            "overwatering":            False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "multiple_plants_affected":False,
            "severity":                "low",
        },
        "expected": ["nitrogen_deficiency"],
    },
    {
        "name": "TC05 – Root Rot (Tomato)",
        "crop": "tomato",
        "facts": {
            "wilting":                 True,
            "yellow_leaves":           True,
            "overwatering":            True,
            "white_powder_on_leaves":  False,
            "dry_weather":             False,
            "brown_spots":             False,
            "stunted_growth":          False,
            "leaf_curl":               False,
            "water_soaked_lesions":    False,
            "black_lesions":           False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "pale_green_lower_leaves": False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "multiple_plants_affected":False,
            "severity":                "medium",
        },
        "expected": ["root_rot"],
    },
    {
        "name": "TC06 – Aphid Infestation + Mosaic Virus (Multi-step chaining)",
        "crop": "bean",
        "facts": {
            "leaf_curl":               True,
            "sticky_residue":          True,
            "visible_insects":         True,
            "yellow_leaves":           True,
            "stunted_growth":          True,
            "white_powder_on_leaves":  False,
            "dry_weather":             False,
            "brown_spots":             False,
            "wilting":                 False,
            "water_soaked_lesions":    False,
            "black_lesions":           False,
            "overwatering":            False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "pale_green_lower_leaves": False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "multiple_plants_affected":True,
            "severity":                "high",
        },
        "expected": ["aphid_infestation", "mosaic_virus", "immediate_expert_consultation"],
    },
    {
        "name": "TC07 – No Disease (Healthy Crop)",
        "crop": "wheat",
        "facts": {
            "yellow_leaves":           False,
            "brown_spots":             False,
            "white_powder_on_leaves":  False,
            "black_lesions":           False,
            "water_soaked_lesions":    False,
            "leaf_curl":               False,
            "pale_green_lower_leaves": False,
            "lesions_with_yellow_halo":False,
            "circular_spots":          False,
            "sunken_spots":            False,
            "sticky_residue":          False,
            "visible_insects":         False,
            "wilting":                 False,
            "stunted_growth":          False,
            "brown_vascular_tissue":   False,
            "root_galls":              False,
            "dry_weather":             False,
            "cool_wet_weather":        False,
            "humid_weather":           False,
            "overwatering":            False,
            "multiple_plants_affected":False,
            "severity":                "low",
        },
        "expected": [],
    },
]


def run_all_tests():
    """Run all test cases and print a summary table."""
    print("\n" + "█" * 60)
    print("         AUTOMATED TEST SUITE – ALL TEST CASES")
    print("█" * 60)

    from main import run_test_case
    from main import InferenceEngine

    results = []
    for tc in TEST_CASES:
        engine = InferenceEngine(tc["facts"])
        actual = engine.run()
        passed = sorted(actual) == sorted(tc["expected"])
        results.append({
            "name":     tc["name"],
            "expected": tc["expected"],
            "actual":   actual,
            "passed":   passed,
        })
        run_test_case(tc["facts"], tc["crop"], tc["name"])

    # Summary
    print("\n" + "═" * 60)
    print("  TEST SUMMARY")
    print("═" * 60)
    for r in results:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"\n  {status} | {r['name']}")
        print(f"         Expected : {r['expected']}")
        print(f"         Got      : {r['actual']}")

    total  = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n  Result: {passed}/{total} tests passed")
    print("═" * 60)


if __name__ == "__main__":
    run_all_tests()
