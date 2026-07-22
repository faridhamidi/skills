import unittest

from profile_store import ProfileStore, update_profile


class ProfileStoreTests(unittest.TestCase):
    def test_updates_all_fields_when_storage_succeeds(self):
        store = ProfileStore({"name": "Ada", "email": "old@example.test"})

        update_profile(
            store,
            {"name": "Grace", "email": "new@example.test"},
        )

        self.assertEqual(
            store.snapshot(),
            {"name": "Grace", "email": "new@example.test"},
        )


if __name__ == "__main__":
    unittest.main()
