from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from windows_ops_toolkit.docx_integrity import check_docx
from windows_ops_toolkit.docx_report import build_report


def test_build_report_and_check_integrity(tmp_path):
    output = tmp_path / "report.docx"
    build_report(
        {
            "title": "Demo",
            "sections": [
                {
                    "title": "Summary",
                    "paragraphs": ["Hello"],
                    "table": [["A", "B"], ["1", "2"]],
                }
            ],
        },
        output,
    )

    result = check_docx(output)
    assert result["ok"] is True
    assert result["paragraph_count"] >= 2
    assert result["table_count"] == 1
