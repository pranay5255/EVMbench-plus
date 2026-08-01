from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_ocr_jsonl import main, validate_ocr_jsonl  # noqa: E402


PDF_SHA256 = "a" * 64


def make_record(page_number: int, source_page_count: int = 2) -> dict:
    ocr_text = f"<PAGE><|det|>text [0, 0, 1, 1]<|/det|>page {page_number}"
    duplicated = {
        "created_at": "2026-01-01T00:00:00Z",
        "ocr_backend": "test",
        "ocr_endpoint_version": "v1",
        "ocr_model": "test-model",
        "ocr_model_version": "1",
        "ocr_text": ocr_text,
        "page_image_sha256": f"{page_number:064x}",
        "page_number": page_number,
        "pdf_id": "pdf_test",
        "raw_response_ref": f"page-{page_number}",
        "source_bucket": "test-bucket",
        "source_filename": "test.pdf",
        "source_page_count": source_page_count,
        "source_pdf_sha256": PDF_SHA256,
        "source_rel_path": "reports/test.pdf",
    }
    return {
        **duplicated,
        "raw_record": {**duplicated, "source_abs_path": "/evidence/test.pdf"},
        "schema_version": "evmbench_task_creation.ocr_page.v1",
        "text_length": len(ocr_text),
    }


def write_jsonl(path: Path, records: list[dict]) -> str:
    content = "".join(
        json.dumps(record, ensure_ascii=False) + "\n" for record in records
    )
    path.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class ValidateOcrJsonlTests(unittest.TestCase):
    def test_valid_export_passes_all_records_and_expectations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pages.jsonl"
            digest = write_jsonl(path, [make_record(1), make_record(2)])

            report = validate_ocr_jsonl(
                path,
                expected_sha256=digest,
                expected_record_count=2,
                expected_pdf_id="pdf_test",
                expected_source_page_count=2,
                expected_source_pdf_sha256=PDF_SHA256,
            )

            self.assertEqual(
                report["schema_version"],
                "ocr_to_evmbench_harbor.ocr_validation.v1",
            )
            self.assertTrue(report["summary"]["ok"])
            self.assertEqual(report["summary"]["record_count"], 2)
            self.assertEqual(report["summary"]["valid_record_count"], 2)
            self.assertTrue(
                report["summary"]["all_expected_page_records_passed"]
            )
            self.assertTrue(report["input"]["unchanged"])
            self.assertEqual(
                report["summary"]["failed_record_check_count"],
                0,
            )

    def test_detects_record_and_global_contract_violations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pages.jsonl"
            first = make_record(1)
            second = make_record(3)
            second["page_image_sha256"] = "not-a-hash"
            second["text_length"] += 1
            second["raw_record"]["page_number"] = True
            del second["source_rel_path"]
            write_jsonl(path, [first, second])

            report = validate_ocr_jsonl(
                path,
                expected_record_count=2,
                expected_pdf_id="pdf_test",
                expected_source_page_count=2,
                expected_source_pdf_sha256=PDF_SHA256,
            )

            self.assertFalse(report["summary"]["ok"])
            failed_global = set(report["summary"]["failed_global_check_ids"])
            self.assertIn("pages.exact_coverage", failed_global)
            failed_record = set(report["records"][1]["failed_check_ids"])
            self.assertIn(
                "record.required_field.source_rel_path",
                failed_record,
            )
            self.assertIn("record.page_image_sha256_hex64", failed_record)
            self.assertIn("record.text_length_matches", failed_record)
            self.assertIn(
                "record.raw_duplicate_exact.page_number",
                failed_record,
            )

    def test_cli_writes_json_and_text_reports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "pages.jsonl"
            json_report = root / "report.json"
            text_report = root / "report.txt"
            digest = write_jsonl(
                input_path,
                [make_record(1), make_record(2)],
            )

            return_code = main(
                [
                    str(input_path),
                    "--json-report",
                    str(json_report),
                    "--text-report",
                    str(text_report),
                    "--expected-sha256",
                    digest,
                    "--expected-record-count",
                    "2",
                    "--expected-pdf-id",
                    "pdf_test",
                    "--expected-source-page-count",
                    "2",
                    "--expected-source-pdf-sha256",
                    PDF_SHA256,
                ]
            )

            self.assertEqual(return_code, 0)
            self.assertTrue(json.loads(json_report.read_text())["summary"]["ok"])
            self.assertIn("result: PASS", text_report.read_text())


if __name__ == "__main__":
    unittest.main()
