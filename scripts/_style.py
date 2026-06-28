"""
_style.py — 図の共通スタイル（日本語フォント設定など）

各図スクリプトの先頭で:
    import matplotlib
    matplotlib.use("Agg")
    from _style import setup_japanese_font
    setup_japanese_font()
として使う。日本語フォントが無い環境では警告のみで継続（豆腐になるが落ちない）。
"""
from __future__ import annotations

_JP_CANDIDATES = [
    "Hiragino Sans",            # macOS
    "Hiragino Maru Gothic Pro",
    "YuGothic",
    "Yu Gothic",
    "Noto Sans CJK JP",         # Linux
    "IPAexGothic",
    "Arial Unicode MS",
    "AppleGothic",
]


def setup_japanese_font() -> str | None:
    """利用可能な日本語フォントを1つ選んで設定。選んだ名前を返す（無ければ None）。"""
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    available = {f.name for f in fm.fontManager.ttflist}
    chosen = next((c for c in _JP_CANDIDATES if c in available), None)
    if chosen:
        plt.rcParams["font.family"] = chosen
    else:
        print("[warn] 日本語フォントが見つかりません。ラベルが豆腐になる可能性があります。")
    plt.rcParams["axes.unicode_minus"] = False   # マイナス記号の文字化け防止
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["savefig.bbox"] = "tight"
    return chosen
