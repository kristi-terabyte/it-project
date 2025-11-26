"""
Generate a simple Kanban board image using matplotlib.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLUMNS = {
    "Backlog": ["KAN-01 Ініціалізація", "KAN-02 CLI", "KAN-03 GUI"],
    "In Progress": ["KAN-04 Тести", "KAN-05 Документація"],
    "Review": ["KAN-06 PR GUI"],
    "Done": ["KAN-07 Kanban", "KAN-08 PDF", "KAN-09 Коміти", "KAN-10 Скріни"],
}

COLORS = ["#bfdbfe", "#c4b5fd", "#bbf7d0", "#fed7aa"]


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    output = base_dir / "screenshots" / "kanban_board.png"
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    width = 1 / len(COLUMNS)
    for idx, (column, tasks) in enumerate(COLUMNS.items()):
        x0 = idx * width
        rect = Rectangle(
            (x0, 0),
            width,
            1,
            linewidth=2,
            edgecolor="#1f2937",
            facecolor=COLORS[idx % len(COLORS)],
        )
        ax.add_patch(rect)
        ax.text(
            x0 + width / 2,
            0.95,
            column,
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
            color="#0f172a",
        )
        y = 0.85
        for task in tasks:
            ax.text(
                x0 + width / 2,
                y,
                f"• {task}",
                ha="center",
                va="top",
                fontsize=10,
                color="#111827",
            )
            y -= 0.12

    plt.tight_layout()
    plt.savefig(output, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Kanban board saved to {output}")


if __name__ == "__main__":
    main()

