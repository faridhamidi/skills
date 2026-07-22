import json
from pathlib import Path
import shutil
import sys
import tempfile
import textwrap
import unittest

from evals.ptm_eval.case import Case
from evals.ptm_eval.runner import run_trial
from evals.ptm_eval.validation import snapshot_tree, validate_artifact


REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = REPO_ROOT / "evals/cases/ptm-retry-recovery.json"
FIXTURE = REPO_ROOT / "evals/fixtures/retry-recovery"


class CaseTests(unittest.TestCase):
    def test_loads_paths_inside_repository(self):
        case = Case.load(CASE_PATH, REPO_ROOT)

        self.assertEqual(case.id, "ptm-retry-recovery")
        self.assertEqual(case.fixture, FIXTURE)
        self.assertTrue(case.oracle.is_file())

    def test_rejects_fixture_path_outside_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            case_path = Path(temporary) / "case.json"
            case_path.write_text(
                json.dumps(
                    {
                        "id": "escape",
                        "fixture": "../outside",
                        "prompt": "x",
                        "project_test_command": ["true"],
                        "oracle": "evals/oracles/retry_recovery_oracle.py",
                        "failure_token": "fail_on_attempts",
                    }
                )
            )

            with self.assertRaises(ValueError):
                Case.load(case_path, REPO_ROOT)


class ValidationTests(unittest.TestCase):
    def test_baseline_passes_public_tests_and_fails_hidden_oracle(self):
        case = Case.load(CASE_PATH, REPO_ROOT)

        result = validate_artifact(case, FIXTURE, FIXTURE)

        self.assertTrue(result["project_tests"]["passed"])
        self.assertFalse(result["hidden_oracle"]["passed"])
        self.assertEqual(result["changed_files"], [])
        self.assertEqual(result["new_tests"], [])

    def test_detects_fault_injection_and_exactly_one_tag_per_new_test(self):
        case = Case.load(CASE_PATH, REPO_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "artifact"
            shutil.copytree(FIXTURE, artifact)
            (artifact / "tests/test_recovery.py").write_text(
                textwrap.dedent(
                    '''
                    import unittest
                    from profile_store import ProfileStore

                    class RecoveryTests(unittest.TestCase):
                        # Falsifies: permanent failures can leave partial state.
                        def test_permanent_failure(self):
                            store = ProfileStore({}, fail_on_attempts={1})
                            self.assertEqual(store.snapshot(), {})
                    '''
                )
            )

            result = validate_artifact(case, FIXTURE, artifact)

        self.assertEqual(result["new_tests"], ["tests/test_recovery.py::test_permanent_failure"])
        self.assertTrue(result["fault_injection_present"])
        self.assertTrue(result["intent_tags"]["passed"])

    def test_does_not_count_intent_phrase_inside_test_body_as_declaration(self):
        case = Case.load(CASE_PATH, REPO_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "artifact"
            shutil.copytree(FIXTURE, artifact)
            (artifact / "tests/test_recovery.py").write_text(
                textwrap.dedent(
                    '''
                    import unittest
                    from profile_store import ProfileStore

                    class RecoveryTests(unittest.TestCase):
                        def test_permanent_failure(self):
                            message = "Falsifies: this is only test data"
                            store = ProfileStore({}, fail_on_attempts={1})
                            self.assertTrue(message)
                    '''
                )
            )

            result = validate_artifact(case, FIXTURE, artifact)

        self.assertFalse(result["intent_tags"]["passed"])
        self.assertEqual(
            result["intent_tags"]["counts"],
            {"tests/test_recovery.py::test_permanent_failure": 0},
        )


class RunnerTests(unittest.TestCase):
    def test_fake_agent_run_preserves_evidence_and_condition(self):
        case = Case.load(CASE_PATH, REPO_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            fake_agent = temporary_path / "fake_agent.py"
            fake_agent.write_text(
                textwrap.dedent(
                    '''
                    from pathlib import Path
                    import sys

                    workspace = Path(sys.argv[1])
                    marker = workspace / "agent-ran.txt"
                    marker.write_text("ran")
                    '''
                )
            )
            output = temporary_path / "results"

            result = run_trial(
                case=case,
                condition="treatment",
                output_dir=output,
                repo_root=REPO_ROOT,
                command_template=[sys.executable, str(fake_agent), "{workspace}"],
                timeout=10,
            )

            result_dir = Path(result["result_dir"])
            self.assertEqual(result["condition"], "treatment")
            self.assertEqual(result["agent"]["returncode"], 0)
            self.assertTrue((result_dir / "artifact/agent-ran.txt").is_file())
            self.assertTrue((result_dir / "result.json").is_file())
            self.assertFalse((result_dir / "codex-home").exists())

    def test_rejects_unknown_condition(self):
        case = Case.load(CASE_PATH, REPO_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                run_trial(
                    case=case,
                    condition="maybe",
                    output_dir=Path(temporary),
                    repo_root=REPO_ROOT,
                    command_template=["true"],
                )


if __name__ == "__main__":
    unittest.main()
