# Skills - Starter Template

This file defines modular skills for the starter template.

Each skill:
- Performs exactly one responsibility
- Uses explicit trigger phrases
- Produces structured output
- Includes validation guardrails
- Does not overlap with other skills

Skills are reusable capabilities.
Agents reference skills.
Skills do not define agents.

---

## 1. financial-data-parser

### Metadata

name: financial-data-parser  
description: Extracts, sanitizes, and validates structured financial data from CSV or XLSX files.  
triggers:
- parse financial data
- extract spreadsheet metrics
- process financial csv

### Instructions

1. Locate the specified `.csv` or `.xlsx` file.
2. Remove empty rows and normalize column headers.
3. Validate the dataset against a predefined schema.
4. Convert cleaned data into structured JSON.
5. Produce a structured artifact.

### Guardrails

- Do not assume missing values.
- Explicitly report schema violations.
- Do not perform business decision logic.

### Output Format (JSON)

{
  "status": "success | failure",
  "row_count": 0,
  "columns": [],
  "validation_summary": {
    "schema_valid": true,
    "missing_fields": []
  },
  "data": []
}

---

## 2. logic-sanity-check

### Metadata

name: logic-sanity-check  
description: Validates computed metrics and detects logical inconsistencies.  
triggers:
- run sanity check
- validate metrics
- check logical consistency

### Instructions

1. Accept structured input data.
2. Validate numeric ranges and boundaries.
3. Check for null or undefined critical fields.
4. Identify obvious inconsistencies.
5. Produce structured validation artifact.

### Guardrails

- Do not modify input data.
- Do not auto-correct invalid values.
- Fail explicitly if validation rules fail.

### Output Format (JSON)

{
  "status": "pass | fail",
  "errors": [],
  "warnings": [],
  "validated_fields": []
}

---

## 3. artifact-verifier

### Metadata

name: artifact-verifier  
description: Ensures agent outputs follow structured artifact requirements.  
triggers:
- verify artifact
- validate output structure

### Instructions

1. Inspect the provided artifact.
2. Confirm required keys are present.
3. Validate schema consistency.
4. Ensure no free-form reasoning is used as final output.
5. Produce structured validation result.

### Guardrails

- Do not modify artifact content.
- Fail clearly if required fields are missing.

### Output Format (JSON)

{
  "status": "valid | invalid",
  "missing_keys": [],
  "schema_issues": []
}

---

## Design Notes

- Keep skills narrow.
- Avoid combining responsibilities.
- Add new skills only when capability boundaries require it.
- Always enforce structured artifacts.
