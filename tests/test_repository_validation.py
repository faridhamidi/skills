from pathlib import Path
import tempfile
import textwrap
import unittest

from scripts.validate_repository import validate_repository


class RepositoryValidationTests(unittest.TestCase):
    def make_repository(self, root: Path) -> Path:
        skill = root / "skills/example-skill"
        (skill / "agents").mkdir(parents=True)
        (skill / "references").mkdir()
        (root / "README.md").write_text(
            "| [`example-skill`](skills/example-skill/) | Example. |\n"
            "Install from https://example.test/skills/tree/main/skills/remote-skill.\n"
        )
        (skill / "SKILL.md").write_text(
            textwrap.dedent(
                """\
                ---
                name: example-skill
                description: Use when an example skill is required.
                ---

                # Example Skill

                Read [the guide](references/guide.md#specific-section).
                """
            )
        )
        (skill / "references/guide.md").write_text(
            "# Guide\n\n## Specific section\n"
        )
        (skill / "agents/openai.yaml").write_text(
            textwrap.dedent(
                """\
                interface:
                  display_name: "Example Skill"
                  short_description: "Apply the example skill when required"
                  default_prompt: "Use $example-skill to handle this example."
                """
            )
        )
        return root

    def validate_fixture(self, mutate=None):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repository(Path(temporary))
            if mutate:
                mutate(root)
            return validate_repository(root)

    def test_accepts_a_complete_repository(self):
        self.assertEqual(self.validate_fixture(), [])

    def test_rejects_broken_markdown_targets_and_anchors(self):
        def mutate(root):
            guide = root / "skills/example-skill/references/guide.md"
            guide.write_text(
                "# Guide\n\n[missing](missing.md)\n"
                "[bad anchor](../SKILL.md#not-a-heading)\n"
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("missing.md" in error for error in errors))
        self.assertTrue(any("not-a-heading" in error for error in errors))

    def test_rejects_reference_style_links_to_missing_targets(self):
        def mutate(root):
            guide = root / "skills/example-skill/references/guide.md"
            guide.write_text("# Guide\n\nRead [the missing guide][missing].\n\n[missing]: absent.md\n")

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("absent.md" in error for error in errors))

    def test_rejects_links_that_escape_the_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            root = self.make_repository(temporary_path / "repository")
            outside = temporary_path / "outside.md"
            outside.write_text("# Outside\n")
            skill = root / "skills/example-skill/SKILL.md"
            skill.write_text(skill.read_text() + "\n[outside](../../../outside.md)\n")

            errors = validate_repository(root)

        self.assertTrue(any("outside repository" in error for error in errors))

    def test_rejects_skill_links_that_escape_the_distributable_package(self):
        def mutate(root):
            (root / "shared.md").write_text("# Shared\n")
            skill = root / "skills/example-skill/SKILL.md"
            skill.write_text(skill.read_text() + "\n[shared](../../shared.md)\n")

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("outside skill package" in error for error in errors))

    def test_rejects_invalid_skill_metadata(self):
        def mutate(root):
            skill = root / "skills/example-skill/SKILL.md"
            skill.write_text("---\nname: wrong-name\ndescription: \n---\n")

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("must match directory" in error for error in errors))
        self.assertTrue(any("description" in error for error in errors))

    def test_rejects_readme_registry_drift(self):
        errors = self.validate_fixture(
            lambda root: (root / "README.md").write_text(
                "# No registry\n\nSee [the skill](skills/example-skill/).\n"
            )
        )

        self.assertTrue(any("README registry" in error for error in errors))

    def test_rejects_readme_registry_label_target_mismatch(self):
        def mutate(root):
            readme = root / "README.md"
            readme.write_text(
                "| [`wrong-label`](skills/example-skill/) | Example. |\n"
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("label" in error and "example-skill" in error for error in errors))

    def test_rejects_steering_copy_drift(self):
        def mutate(root):
            assets = root / "skills/example-skill/assets"
            assets.mkdir()
            (assets / "steering.md").write_text("canonical\n")
            (assets / "AGENTS.md").write_text("different\n")
            (assets / "CLAUDE.md").write_text("canonical\n")

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("steering copies differ" in error for error in errors))

    def test_rejects_missing_or_inconsistent_openai_metadata(self):
        def mutate(root):
            metadata = root / "skills/example-skill/agents/openai.yaml"
            metadata.write_text(
                'interface:\n  display_name: "Example"\n'
                '  short_description: "Too short"\n'
                '  default_prompt: "Use this skill."\n'
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("short_description" in error for error in errors))
        self.assertTrue(any("$example-skill" in error for error in errors))

    def test_rejects_claims_linking_to_absent_examples_or_scripts(self):
        def mutate(root):
            guide = root / "skills/example-skill/references/guide.md"
            guide.write_text(
                guide.read_text()
                + "\nThe ../examples/witness.py executable witness runs in CI.\n"
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("examples/witness.py" in error for error in errors))

    def test_ignores_artifact_paths_inside_external_urls(self):
        def mutate(root):
            guide = root / "skills/example-skill/references/guide.md"
            guide.write_text(
                guide.read_text()
                + "\nSee https://example.test/examples/witness.py for the upstream witness.\n"
            )

        self.assertEqual(self.validate_fixture(mutate), [])

    def test_rejects_openai_keys_outside_interface_mapping(self):
        def mutate(root):
            metadata = root / "skills/example-skill/agents/openai.yaml"
            metadata.write_text(
                'not_interface:\n'
                '  display_name: "Example Skill"\n'
                '  short_description: "Apply the example skill when required"\n'
                '  default_prompt: "Use $example-skill to handle this example."\n'
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("interface mapping" in error for error in errors))

    def test_rejects_malformed_openai_yaml(self):
        def mutate(root):
            metadata = root / "skills/example-skill/agents/openai.yaml"
            metadata.write_text(
                'interface:\n'
                '  display_name: "Example Skill"\n'
                '  short_description: "Apply the example skill when required"\n'
                '  default_prompt: "Use $example-skill to handle this example."\n'
                '  invalid yaml !\n'
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("malformed" in error for error in errors))

    def test_rejects_invalid_openai_quoted_scalars(self):
        def mutate(root):
            metadata = root / "skills/example-skill/agents/openai.yaml"
            metadata.write_text(
                'interface:\n'
                '  display_name: "Bad \\q escape"\n'
                '  short_description: "Apply the example skill when required"\n'
                '  default_prompt: "Use $example-skill to handle this example."\n'
            )

        errors = self.validate_fixture(mutate)

        self.assertTrue(any("malformed" in error for error in errors))

    def test_missing_skills_directory_returns_diagnostics(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("# Empty repository\n")

            errors = validate_repository(root)

        self.assertTrue(any("skill directory is missing" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
