import importlib.util
from pathlib import Path
import sys
import unittest


ARTIFACT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None


def load_module(artifact):
    module_path = Path(artifact).resolve() / "profile_store.py"
    spec = importlib.util.spec_from_file_location("evaluated_profile_store", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RetryRecoveryOracle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ARTIFACT is None:
            raise ValueError("usage: retry_recovery_oracle.py <artifact>")
        cls.subject = load_module(ARTIFACT)

    def test_transient_failure_commits_complete_update(self):
        store = self.subject.ProfileStore(
            {"name": "Ada", "email": "old@example.test"},
            fail_on_attempts={1},
        )

        self.subject.update_profile(
            store,
            {"name": "Grace", "email": "new@example.test"},
            attempts=2,
        )

        self.assertEqual(
            store.snapshot(),
            {"name": "Grace", "email": "new@example.test"},
        )

    def test_permanent_failure_preserves_original_profile(self):
        original = {"name": "Ada", "email": "old@example.test"}
        store = self.subject.ProfileStore(original, fail_on_attempts={1, 2})

        with self.assertRaises(self.subject.StorageFailure):
            self.subject.update_profile(
                store,
                {"name": "Grace", "email": "new@example.test"},
                attempts=2,
            )

        self.assertEqual(store.snapshot(), original)


if __name__ == "__main__":
    sys.argv = [sys.argv[0]]
    unittest.main(verbosity=2)
