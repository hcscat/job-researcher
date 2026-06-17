import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from job_harvest.config import build_queries, load_config
from job_harvest.search import normalize_url


class ConfigTest(unittest.TestCase):
    def test_load_config_and_build_queries(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config_path.write_text(
                """
output_dir: "./output"
criteria:
  roles:
    - "백엔드 개발자"
  keywords:
    - "Python"
    - "FastAPI"
  locations:
    - "서울"
  extra_terms:
    - "채용"
search:
  sites:
    - saramin
  ai_provider: external_command
ai:
  auth_mode: external_command
  external_command: "python scripts/enrich.py"
preprocessing:
  dedupe_strategy: company_title_location
integrations:
  harness_config:
    enabled: true
""".strip(),
                encoding="utf-8",
            )

            config = load_config(config_path)
            self.assertEqual(config.search.sites, ["saramin"])
            self.assertEqual(
                build_queries(config.criteria, []),
                ["백엔드 개발자 Python FastAPI 서울 채용"],
            )
            self.assertEqual(config.search.ai_provider, "external_command")
            self.assertEqual(config.ai.auth_mode, "external_command")
            self.assertEqual(config.ai.external_command, "python scripts/enrich.py")
            self.assertEqual(config.preprocessing.dedupe_strategy, "company_title_location")
            self.assertEqual(config.integrations.harness_config, {"enabled": True})

    def test_normalize_url_strips_blind_and_linkedin_queries(self) -> None:
        self.assertEqual(
            normalize_url(
                "https://www.linkedin.com/jobs/view/1234567890/?position=1&pageNum=0&trackingId=abc"
            ),
            "https://www.linkedin.com/jobs/view/1234567890",
        )
        self.assertEqual(
            normalize_url(
                "https://kr.linkedin.com/jobs/view/1234567890?position=2&pageNum=3&refId=abc"
            ),
            "https://www.linkedin.com/jobs/view/1234567890",
        )
        self.assertEqual(
            normalize_url(
                "https://www.teamblind.com/jobs/7890?searchKeyword=backend&page=3"
            ),
            "https://www.teamblind.com/jobs/7890",
        )
        self.assertEqual(
            normalize_url(
                "https://www.jobkorea.co.kr/Recruit/GI_Read/48906383?Oem_Code=C1&logpath=1&stext=backend&listno=21&sc=552"
            ),
            "https://www.jobkorea.co.kr/Recruit/GI_Read/48906383",
        )
        self.assertEqual(
            normalize_url("https://www.rocketpunch.com/jobs?jobId=123&tracking=abc"),
            "https://www.rocketpunch.com/jobs?jobId=123",
        )


if __name__ == "__main__":
    unittest.main()
