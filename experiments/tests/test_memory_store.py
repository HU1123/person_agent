"""长期记忆：JSON 持久化。"""

from lib.memory_store import MemoryStore


def test_save_and_load_fact(tmp_path):
    store = MemoryStore(tmp_path / "store.json")
    store.save_fact("name", "小明")
    assert store.load_all() == {"name": "小明"}


def test_format_for_prompt_includes_facts(tmp_path):
    store = MemoryStore(tmp_path / "store.json")
    store.save_fact("city", "北京")
    text = store.format_for_prompt()
    assert "city" in text
    assert "北京" in text


def test_format_for_prompt_empty_when_no_facts(tmp_path):
    store = MemoryStore(tmp_path / "store.json")
    assert store.format_for_prompt() == ""
