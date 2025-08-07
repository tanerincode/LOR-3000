from pathlib import Path

from oven.loader import load_prompts_from_file


def test_load_prompts_from_yaml(tmp_path: Path) -> None:
    content = (
        "support_agent:\n"
        "  system: |\n"
        "    You are a helpful support agent.\n"
        "  version: v1\n"
        "  description: Default support agent\n"
    )
    p = tmp_path / "prompts.yaml"
    p.write_text(content, encoding="utf-8")
    prompts = load_prompts_from_file(p)
    assert "support_agent" in prompts
    assert prompts["support_agent"].system.startswith("You are a helpful")

