from typing import List, Optional
from math import atan2, degrees

from ...domain.abstracts.movement import Foot
from .general import Visualiser, Figura, Panel


class PositionOnlyAsciiVisualiser(Visualiser):
    """
    Prints the positions of the steps in ASCII.
    Cannot show rotation.
    """

    def _makeSimpleGrid(self, width: int, height: int) -> List[List[None]]:  # Indexable as [x][y], i.e. the nested lists are columns with the leftmost element the bottommost element.
        return [[None for _ in range(height)] for _ in range(width)]

    def _gridToString(self, grid: List[List[Optional[str]]]) -> str:
        s = ""
        for y in range(len(grid[0])):
            row_y = ""
            for x in range(len(grid)):
                row_y += grid[x][y] or " "
                row_y += "|"
            row_y = row_y[:-1]
            row_y += "\n"
            s = row_y + s  # Reverse-order concatenation
        return s

    def _footToString(self, foot: Foot) -> str:
        if foot == Foot.LeaderLeft:
            return "L"
        elif foot == Foot.LeaderRight:
            return "R"
        else:
            return None

    def _vectorToString(self, x: float, y: float) -> str:
        arrows = ["🡒", "🡕", "🡑", "🡔", "🡐", "🡗", "🡓", "🡖"]  # https://stackoverflow.com/a/74089712/9352077

        angle = degrees(atan2(y, x))
        angle = round(angle if angle >= 0 else angle + 360)
        return arrows[angle // 45]

    def _render(self, figure: Figura) -> List[Panel]:
        panels = []

        gridspec, starting_feet = self._normaliseGrid(figure)
        width, height = gridspec.width, gridspec.height

        previous_feet = starting_feet
        for count, (feet, checkpoint) in enumerate(zip(self._simulate(figure, base=starting_feet), figure.checkpoints)):
            if checkpoint.hidden:
                previous_feet = feet
                continue

            grid = self._makeSimpleGrid(width, height)

            # Step 1: Visualise feet.
            for foot, position in feet.items():
                grid[position.x][position.y] = self._footToString(foot)

            # Step 2: Visualise history.
            for foot, step in checkpoint.steps_since_previous:
                start_x = previous_feet[foot].x
                start_y = previous_feet[foot].y
                delta_x = feet[foot].x - start_x
                delta_y = feet[foot].y - start_y
                if delta_x or delta_y and not grid[start_x][start_y]:
                    grid[start_x][start_y] = self._vectorToString(delta_x, delta_y)

            # Step 3: Print out.
            panels.append(Panel(self._gridToString(grid), count))

            previous_feet = feet

        return panels

    def _concatenate(self, panels: List[Panel]) -> str:
        rendered_width = len(panels[0].rendered.splitlines()[0])

        lines = [panel.rendered.splitlines(keepends=False) for panel in panels]  # [panel1_line1, panel1_line2, ...]  [panel2_line1, ...]
        for panellines, panel in zip(lines, panels):
            panellines.append("-"*rendered_width)
            panellines.append(" "*(rendered_width//2) + str(panel.count) + " "*(rendered_width//2))

        result = ""
        for lines_to_concatenate in zip(*lines):
            result += "        ".join(lines_to_concatenate) + "\n"
        return result
