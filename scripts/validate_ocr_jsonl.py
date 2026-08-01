#!/usr/bin/env python3
"""Validate one preserved evmbench_task_creation OCR JSONL export.

The validator is deliberately read-only with respect to the source JSONL. It
hashes the input before and after validation and can write both machine-readable
and reviewer-readable reports outside a candidate directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


OCR_SCHEMA_VERSION = "evmbench_task_creation.ocr_page.v1"
REPORT_SCHEMA_VERSION = "ocr_to_evmbench_harbor.ocr_validation.v1"
HEX_64_RE = re.compile(r"^[0-9a-fA-F]{64}$")

REQUIRED_TOP_LEVEL_FIELDS = (
    "created_at",
    "ocr_backend",
    "ocr_endpoint_version",
    "ocr_model",
    "ocr_model_version",
    "ocr_text",
    "page_image_sha256",
    "page_number",
    "pdf_id",
    "raw_record",
    "raw_response_ref",
    "schema_version",
    "source_bucket",
    "source_filename",
    "source_page_count",
    "source_pdf_sha256",
    "source_rel_path",
    "text_length",
)

DUPLICATED_RAW_FIELDS = (
    "created_at",
    "ocr_backend",
    "ocr_endpoint_version",
    "ocr_model",
    "ocr_model_version",
    "ocr_text",
    "page_image_sha256",
    "page_number",
    "pdf_id",
    "raw_response_ref",
    "source_bucket",
    "source_filename",
    "source_page_count",
    "source_pdf_sha256",
    "source_rel_path",
)

CONSISTENT_ACROSS_RECORDS_FIELDS = (
    "pdf_id",
    "source_bucket",
    "source_filename",
    "source_rel_path",
    "source_page_count",
    "source_pdf_sha256",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def same_type_and_value(left: Any, right: Any) -> bool:
    return type(left) is type(right) and left == right


def typed_json(value: Any) -> dict[str, Any]:
    return {"type": type(value).__name__, "value": value}


def unique_typed_values(values: Sequence[Any]) -> list[Any]:
    unique: list[Any] = []
    for value in values:
        if not any(same_type_and_value(value, prior) for prior in unique):
            unique.append(value)
    return unique


def check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    **details: Any,
) -> None:
    entry: dict[str, Any] = {"id": check_id, "passed": bool(passed)}
    if details:
        entry["details"] = details
    checks.append(entry)


def failed_check_ids(checks: Sequence[dict[str, Any]]) -> list[str]:
    return [str(item["id"]) for item in checks if not item["passed"]]


def validate_record_line(line: str, line_number: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "line_number": line_number,
        "page_number": None,
        "checks": [],
        "valid": False,
    }
    checks = result["checks"]

    nonempty = bool(line.strip())
    check(checks, "line.nonempty", nonempty)
    if not nonempty:
        result["failed_check_ids"] = failed_check_ids(checks)
        return result

    try:
        parsed = json.loads(line)
    except json.JSONDecodeError as exc:
        check(
            checks,
            "line.valid_json",
            False,
            error=exc.msg,
            column=exc.colno,
        )
        result["failed_check_ids"] = failed_check_ids(checks)
        return result

    check(checks, "line.valid_json", True)
    is_object = isinstance(parsed, dict)
    check(checks, "record.is_object", is_object, actual_type=type(parsed).__name__)
    if not is_object:
        result["failed_check_ids"] = failed_check_ids(checks)
        return result

    result["_record"] = parsed
    result["page_number"] = parsed.get("page_number")

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        check(
            checks,
            f"record.required_field.{field}",
            field in parsed,
        )

    check(
        checks,
        "record.schema_version",
        parsed.get("schema_version") == OCR_SCHEMA_VERSION,
        expected=OCR_SCHEMA_VERSION,
        actual=parsed.get("schema_version"),
    )

    page_number = parsed.get("page_number")
    check(
        checks,
        "record.page_number_positive_integer",
        is_plain_int(page_number) and page_number > 0,
        actual=typed_json(page_number),
    )

    source_page_count = parsed.get("source_page_count")
    check(
        checks,
        "record.source_page_count_positive_integer",
        is_plain_int(source_page_count) and source_page_count > 0,
        actual=typed_json(source_page_count),
    )

    source_pdf_sha256 = parsed.get("source_pdf_sha256")
    check(
        checks,
        "record.source_pdf_sha256_hex64",
        isinstance(source_pdf_sha256, str)
        and HEX_64_RE.fullmatch(source_pdf_sha256) is not None,
        actual=typed_json(source_pdf_sha256),
    )

    page_image_sha256 = parsed.get("page_image_sha256")
    check(
        checks,
        "record.page_image_sha256_hex64",
        isinstance(page_image_sha256, str)
        and HEX_64_RE.fullmatch(page_image_sha256) is not None,
        actual=typed_json(page_image_sha256),
    )

    ocr_text = parsed.get("ocr_text")
    ocr_text_is_string = isinstance(ocr_text, str)
    check(
        checks,
        "record.ocr_text_string",
        ocr_text_is_string,
        actual_type=type(ocr_text).__name__,
    )
    check(
        checks,
        "record.ocr_text_page_marker",
        ocr_text_is_string and ocr_text.startswith("<PAGE>"),
    )

    text_length = parsed.get("text_length")
    check(
        checks,
        "record.text_length_matches",
        ocr_text_is_string
        and is_plain_int(text_length)
        and text_length == len(ocr_text),
        declared=typed_json(text_length),
        actual=len(ocr_text) if ocr_text_is_string else None,
    )

    raw_record = parsed.get("raw_record")
    raw_record_is_object = isinstance(raw_record, dict)
    check(
        checks,
        "record.raw_record_object",
        raw_record_is_object,
        actual_type=type(raw_record).__name__,
    )

    for field in DUPLICATED_RAW_FIELDS:
        top_present = field in parsed
        raw_present = raw_record_is_object and field in raw_record
        matches = (
            top_present
            and raw_present
            and same_type_and_value(parsed[field], raw_record[field])
        )
        details: dict[str, Any] = {
            "top_level_present": top_present,
            "raw_record_present": raw_present,
        }
        if top_present:
            details["top_level"] = typed_json(parsed[field])
        if raw_present:
            details["raw_record"] = typed_json(raw_record[field])
        check(
            checks,
            f"record.raw_duplicate_exact.{field}",
            matches,
            **details,
        )

    return result


def validate_ocr_jsonl(
    input_path: Path,
    *,
    expected_sha256: str | None = None,
    expected_record_count: int | None = None,
    expected_pdf_id: str | None = None,
    expected_source_page_count: int | None = None,
    expected_source_pdf_sha256: str | None = None,
) -> dict[str, Any]:
    resolved_path = input_path.resolve(strict=True)
    started_at = utc_now()
    input_sha256_before = sha256_file(resolved_path)
    input_size_bytes = resolved_path.stat().st_size

    with resolved_path.open("r", encoding="utf-8", newline="") as handle:
        lines = handle.read().splitlines()

    record_results = [
        validate_record_line(line, line_number)
        for line_number, line in enumerate(lines, start=1)
    ]
    parsed_records = [
        item["_record"] for item in record_results if "_record" in item
    ]

    global_checks: list[dict[str, Any]] = []
    check(
        global_checks,
        "file.nonempty",
        input_size_bytes > 0 and len(lines) > 0,
        size_bytes=input_size_bytes,
        line_count=len(lines),
    )
    check(
        global_checks,
        "file.every_line_json_object",
        len(parsed_records) == len(lines),
        parsed_object_count=len(parsed_records),
        line_count=len(lines),
    )

    if expected_sha256 is not None:
        check(
            global_checks,
            "file.expected_sha256",
            input_sha256_before == expected_sha256.lower(),
            expected=expected_sha256.lower(),
            actual=input_sha256_before,
        )

    if expected_record_count is not None:
        check(
            global_checks,
            "file.expected_record_count",
            len(lines) == expected_record_count,
            expected=expected_record_count,
            actual=len(lines),
        )

    page_numbers = [
        record.get("page_number")
        for record in parsed_records
        if is_plain_int(record.get("page_number"))
    ]
    all_pages_positive_integers = (
        len(page_numbers) == len(parsed_records)
        and all(page_number > 0 for page_number in page_numbers)
    )
    check(
        global_checks,
        "pages.all_positive_integers",
        all_pages_positive_integers,
        page_numbers=page_numbers,
    )
    check(
        global_checks,
        "pages.strictly_increasing",
        all_pages_positive_integers
        and all(
            earlier < later
            for earlier, later in zip(page_numbers, page_numbers[1:])
        ),
        page_numbers=page_numbers,
    )
    check(
        global_checks,
        "pages.unique",
        len(page_numbers) == len(set(page_numbers)),
        page_numbers=page_numbers,
    )

    consistent_values: dict[str, Any] = {}
    for field in CONSISTENT_ACROSS_RECORDS_FIELDS:
        values = [record[field] for record in parsed_records if field in record]
        unique = unique_typed_values(values)
        consistent = len(values) == len(parsed_records) and len(unique) == 1
        if consistent:
            consistent_values[field] = unique[0]
        check(
            global_checks,
            f"records.consistent.{field}",
            consistent,
            observed=[typed_json(value) for value in unique],
            records_with_field=len(values),
            record_count=len(parsed_records),
        )

    unique_pdf_ids = unique_typed_values(
        [record["pdf_id"] for record in parsed_records if "pdf_id" in record]
    )
    check(
        global_checks,
        "records.exactly_one_pdf_id",
        len(unique_pdf_ids) == 1
        and len(parsed_records) > 0
        and all("pdf_id" in record for record in parsed_records),
        observed=[typed_json(value) for value in unique_pdf_ids],
    )

    source_page_count = consistent_values.get("source_page_count")
    page_coverage_expected = (
        list(range(1, source_page_count + 1))
        if is_plain_int(source_page_count) and source_page_count > 0
        else None
    )
    check(
        global_checks,
        "pages.exact_coverage",
        page_coverage_expected is not None and page_numbers == page_coverage_expected,
        expected=page_coverage_expected,
        actual=page_numbers,
    )

    if expected_pdf_id is not None:
        check(
            global_checks,
            "records.expected_pdf_id",
            consistent_values.get("pdf_id") == expected_pdf_id,
            expected=expected_pdf_id,
            actual=consistent_values.get("pdf_id"),
        )

    if expected_source_page_count is not None:
        check(
            global_checks,
            "records.expected_source_page_count",
            consistent_values.get("source_page_count")
            == expected_source_page_count,
            expected=expected_source_page_count,
            actual=consistent_values.get("source_page_count"),
        )

    if expected_source_pdf_sha256 is not None:
        check(
            global_checks,
            "records.expected_source_pdf_sha256",
            consistent_values.get("source_pdf_sha256")
            == expected_source_pdf_sha256.lower(),
            expected=expected_source_pdf_sha256.lower(),
            actual=consistent_values.get("source_pdf_sha256"),
        )

    for item in record_results:
        record = item.pop("_record", None)
        if record is not None:
            expected_page_number = item["line_number"]
            check(
                item["checks"],
                "record.page_matches_export_position",
                record.get("page_number") == expected_page_number,
                expected=expected_page_number,
                actual=record.get("page_number"),
            )
            for field in CONSISTENT_ACROSS_RECORDS_FIELDS:
                baseline = consistent_values.get(field)
                passed = (
                    field in record
                    and field in consistent_values
                    and same_type_and_value(record[field], baseline)
                )
                check(
                    item["checks"],
                    f"record.matches_consistent_value.{field}",
                    passed,
                    baseline=typed_json(baseline),
                    actual=typed_json(record.get(field)),
                )

        item["failed_check_ids"] = failed_check_ids(item["checks"])
        item["valid"] = len(item["failed_check_ids"]) == 0

    input_sha256_after = sha256_file(resolved_path)
    check(
        global_checks,
        "file.unchanged_during_validation",
        input_sha256_after == input_sha256_before,
        before=input_sha256_before,
        after=input_sha256_after,
    )

    valid_record_count = sum(bool(item["valid"]) for item in record_results)
    failed_global_check_ids = failed_check_ids(global_checks)
    record_check_count = sum(len(item["checks"]) for item in record_results)
    failed_record_check_count = sum(
        len(item["failed_check_ids"]) for item in record_results
    )
    ok = (
        not failed_global_check_ids
        and valid_record_count == len(record_results)
        and len(record_results) > 0
    )

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "validation_started_at": started_at,
        "validation_finished_at": utc_now(),
        "input": {
            "path": str(resolved_path),
            "size_bytes": input_size_bytes,
            "sha256_before": input_sha256_before,
            "sha256_after": input_sha256_after,
            "unchanged": input_sha256_before == input_sha256_after,
        },
        "contract": {
            "ocr_schema_version": OCR_SCHEMA_VERSION,
            "required_top_level_fields": list(REQUIRED_TOP_LEVEL_FIELDS),
            "duplicated_raw_fields": list(DUPLICATED_RAW_FIELDS),
            "consistent_across_records_fields": list(
                CONSISTENT_ACROSS_RECORDS_FIELDS
            ),
            "ocr_text_page_marker": "<PAGE>",
        },
        "expectations": {
            "sha256": expected_sha256,
            "record_count": expected_record_count,
            "pdf_id": expected_pdf_id,
            "source_page_count": expected_source_page_count,
            "source_pdf_sha256": expected_source_pdf_sha256,
        },
        "summary": {
            "ok": ok,
            "record_count": len(record_results),
            "valid_record_count": valid_record_count,
            "invalid_record_count": len(record_results) - valid_record_count,
            "all_expected_page_records_passed": (
                expected_record_count is not None
                and len(record_results) == expected_record_count
                and valid_record_count == expected_record_count
            ),
            "page_numbers": page_numbers,
            "source_page_count": consistent_values.get("source_page_count"),
            "pdf_id": consistent_values.get("pdf_id"),
            "source_pdf_sha256": consistent_values.get("source_pdf_sha256"),
            "global_check_count": len(global_checks),
            "failed_global_check_count": len(failed_global_check_ids),
            "failed_global_check_ids": failed_global_check_ids,
            "record_check_count": record_check_count,
            "failed_record_check_count": failed_record_check_count,
        },
        "global_checks": global_checks,
        "records": record_results,
    }


def render_text_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    input_info = report["input"]
    lines = [
        "P2 OCR JSONL VALIDATION",
        "",
        f"result: {'PASS' if summary['ok'] else 'FAIL'}",
        f"input: {input_info['path']}",
        f"sha256_before: {input_info['sha256_before']}",
        f"sha256_after: {input_info['sha256_after']}",
        f"input_unchanged: {str(input_info['unchanged']).lower()}",
        f"record_count: {summary['record_count']}",
        f"valid_record_count: {summary['valid_record_count']}",
        f"invalid_record_count: {summary['invalid_record_count']}",
        "all_expected_page_records_passed: "
        f"{str(summary['all_expected_page_records_passed']).lower()}",
        f"pdf_id: {summary['pdf_id']}",
        f"source_page_count: {summary['source_page_count']}",
        f"source_pdf_sha256: {summary['source_pdf_sha256']}",
        f"page_numbers: {summary['page_numbers']}",
        f"global_checks: {summary['global_check_count']}",
        f"failed_global_checks: {summary['failed_global_check_count']}",
        f"record_checks: {summary['record_check_count']}",
        f"failed_record_checks: {summary['failed_record_check_count']}",
        "",
        "FAILED CHECKS",
    ]
    failures: list[str] = []
    failures.extend(
        f"global: {check_id}"
        for check_id in summary["failed_global_check_ids"]
    )
    for record in report["records"]:
        failures.extend(
            f"line {record['line_number']}: {check_id}"
            for check_id in record["failed_check_ids"]
        )
    lines.extend(failures or ["none"])
    lines.append("")
    return "\n".join(lines)


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Preserved OCR JSONL path.")
    parser.add_argument("--json-report", type=Path, required=True)
    parser.add_argument("--text-report", type=Path, required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--expected-record-count", type=int)
    parser.add_argument("--expected-pdf-id")
    parser.add_argument("--expected-source-page-count", type=int)
    parser.add_argument("--expected-source-pdf-sha256")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = validate_ocr_jsonl(
        args.input,
        expected_sha256=args.expected_sha256,
        expected_record_count=args.expected_record_count,
        expected_pdf_id=args.expected_pdf_id,
        expected_source_page_count=args.expected_source_page_count,
        expected_source_pdf_sha256=args.expected_source_pdf_sha256,
    )
    write_report(
        args.json_report,
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
    )
    write_report(args.text_report, render_text_report(report))
    return 0 if report["summary"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
