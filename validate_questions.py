#!/usr/bin/env python3
"""
AI-103 Question Bank Validator
Usage: python3 validate_questions.py questions/ai103_questions.json
"""

import json
import sys

REQUIRED_FIELDS = ["tag", "type", "multi", "text", "options", "answer", "expl"]
VALID_TAGS = ["f", "s", "r", "c"]
VALID_TYPES = ["mcq", "code", "dragdrop"]
VALID_CODETYPES = ["complete", "bug"]

def validate(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    if not isinstance(data, list) or len(data) == 0:
        print("❌ JSON must be a non-empty array")
        sys.exit(1)

    errors = []
    warnings = []

    for i, q in enumerate(data):
        idx = f"Q{i+1}"

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in q:
                errors.append(f"{idx}: Missing required field '{field}'")

        if "type" not in q:
            continue

        # Tag
        if q.get("tag") not in VALID_TAGS:
            warnings.append(f"{idx}: Unknown tag '{q.get('tag')}' — expected one of {VALID_TAGS}")

        # Type
        if q["type"] not in VALID_TYPES:
            errors.append(f"{idx}: Invalid type '{q['type']}' — expected one of {VALID_TYPES}")

        # Options
        if "options" in q and (not isinstance(q["options"], list) or len(q["options"]) < 2):
            errors.append(f"{idx}: 'options' must be an array with at least 2 items")

        # Answer
        if "answer" in q:
            if not isinstance(q["answer"], list) or len(q["answer"]) == 0:
                errors.append(f"{idx}: 'answer' must be a non-empty array of indices")
            elif "options" in q:
                for a in q["answer"]:
                    if not isinstance(a, int) or a >= len(q["options"]):
                        errors.append(f"{idx}: Answer index {a} out of range (options has {len(q['options'])} items)")

        # Multi
        if q.get("multi") is True and "answer" in q and len(q.get("answer", [])) != 2:
            errors.append(f"{idx}: Select TWO question (multi=true) must have exactly 2 answer indices")

        # Code questions
        if q["type"] == "code":
            if "code" not in q:
                errors.append(f"{idx}: Code question missing 'code' field")
            if "codetype" not in q or q["codetype"] not in VALID_CODETYPES:
                errors.append(f"{idx}: Code question missing or invalid 'codetype' — expected 'complete' or 'bug'")
            if q.get("codetype") == "complete" and "code" in q and "___" not in q["code"]:
                warnings.append(f"{idx}: Complete-type code question has no blank (___) in code field")

        # Dragdrop questions
        if q["type"] == "dragdrop":
            for field in ["items", "slots", "correctMapping"]:
                if field not in q:
                    errors.append(f"{idx}: Dragdrop question missing '{field}' field")
            if all(f in q for f in ["items", "slots", "correctMapping"]):
                if len(q["items"]) != len(q["slots"]):
                    errors.append(f"{idx}: Dragdrop 'items' and 'slots' must be same length")
                if len(q["correctMapping"]) != len(q["slots"]):
                    errors.append(f"{idx}: Dragdrop 'correctMapping' length must match 'slots' length")
                if len(set(q["correctMapping"])) != len(q["correctMapping"]):
                    errors.append(f"{idx}: Dragdrop 'correctMapping' has duplicate item indices — each item maps to one slot only")

        # Explanation format
        if "expl" in q and not q["expl"].startswith("Correct answer:"):
            warnings.append(f"{idx}: Explanation should start with 'Correct answer: X — ...'")

    # Summary
    print(f"\n📊 Validation Summary")
    print(f"   Total questions: {len(data)}")
    print(f"   MCQ:      {sum(1 for q in data if q.get('type')=='mcq' and not q.get('multi'))}")
    print(f"   SelectTwo:{sum(1 for q in data if q.get('multi'))}")
    print(f"   Code:     {sum(1 for q in data if q.get('type')=='code')}")
    print(f"   DragDrop: {sum(1 for q in data if q.get('type')=='dragdrop')}")
    print(f"   Scenario: {sum(1 for q in data if q.get('scen'))}")
    print()

    if warnings:
        print(f"⚠️  {len(warnings)} warning(s):")
        for w in warnings[:10]:
            print(f"   {w}")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings)-10} more")
        print()

    if errors:
        print(f"❌ {len(errors)} error(s):")
        for e in errors[:20]:
            print(f"   {e}")
        if len(errors) > 20:
            print(f"   ... and {len(errors)-20} more")
        sys.exit(1)
    else:
        print(f"✅ All {len(data)} questions are valid!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_questions.py <path-to-questions.json>")
        sys.exit(1)
    validate(sys.argv[1])
