from typing import List, Optional

from .general import Visualiser, Figura, Panel, GridSpec
from ..abstraction.movement import Foot, FootPosition
from ..instances.movement import InPlace


class TikzVisualiser(Visualiser):
    """
    Prints the positions of the steps as TikZ code.
    """

    def render(self, figure: Figura) -> List[Panel]:
        gridspec, starting_feet = self._normaliseGrid(figure)
        width, height = gridspec.width, gridspec.height
        panels = []

        previous_feet = starting_feet
        for count, (feet, checkpoint) in enumerate(zip(self._simulate(figure, base=starting_feet), figure.checkpoints)):
            if checkpoint.hidden:
                previous_feet = feet
                continue

            # Step 1: Just the grid.
            panel_string = r"\begin{tikzpicture}" + "\n"
            panel_string += r"    \matrix[salsa-layout] (m) {" + "\n"
            panel_string += (r"        " + " & ".join([r"\filler"]*(width+2)) + r"\\" + "\n")*(height+2)
            panel_string += r"    };" + "\n"

            panel_string += r"    \foreach \currX [count=\prevX] in {" + ",".join(map(str,range(2,width+3))) + "} {\n"
            panel_string += r"        \draw[salsa-gridline] ($(m-1-\prevX.south)!0.5!(m-1-\currX.south)$) -- ($(m-" + f"{height+2}" + "-\prevX.north)!0.5!(m-" + f"{height+2}" + "-\currX.north)$);" + "\n"
            panel_string += r"    }" + "\n"
            panel_string += r"    \foreach \currY [count=\prevY] in {" + ",".join(map(str,range(2,height+3))) + "} {\n"
            panel_string += r"        \draw[salsa-gridline] ($(m-\prevY-1.east)!0.5!(m-\currY-1.east)$) -- ($(m-\prevY-" + f"{width+2}" + ".west)!0.5!(m-\currY-" + f"{width+2}" + ".west)$);" + "\n"
            panel_string += r"    }" + "\n"

            # Step 2: Visualise feet.
            for foot, position in feet.items():
                panel_string += r"    \node[rotate=" + str(position.rotation-90) + "] at " + self._positionToMatrixCoordinate(position, gridspec) + " {" + self._footToString(foot) + "};\n"

            # # Step 3: Visualise history.
            for foot, step in checkpoint.steps_since_previous:
                start = previous_feet[foot]
                end   = feet[foot]
                if not start.isSamePlace(end):
                    panel_string += r"    \draw[salsa-arrow] " + self._positionToMatrixCoordinate(start, gridspec, anchor_center=True) + " to " + self._positionToMatrixCoordinate(end, gridspec) + ";\n"
                elif step == InPlace:
                    panel_string += r"    \node[salsa-encircle] at " + self._positionToMatrixCoordinate(start, gridspec) + r"{\filler};" + "\n"

            panel_string += r"\end{tikzpicture}"
            panels.append(Panel(rendered=panel_string, count=count))

            previous_feet = feet

        return panels

    def concatenate(self, panels: List[Panel]) -> str:
        n = self._panels_per_row
        result = r"\begin{longtable}{" + "c"*n + "}\n"

        for i in range((len(panels)-1)//n + 1):
            subpanels = panels[n*i:n*(i+1)]
            result += "\n&\n".join(p.rendered for p in subpanels)
            result += r"\\[-1.75em]" + "\n"
            result += r"\bfseries " + r" & \bfseries ".join(str(p.count) for p in subpanels) + r" \\" + "\n"

        result += r"\end{longtable}"
        return result

    def _positionToMatrixCoordinate(self, position: FootPosition, gridspec: GridSpec, anchor_center: bool=False) -> str:
        return f"(m-{gridspec.height-1-position.y+2}-{position.x+2}" + ".center"*anchor_center + ")"

    def _footToString(self, foot: Foot) -> str:
        if foot == Foot.LeaderLeft:
            return "L"
        elif foot == Foot.LeaderRight:
            return "R"
        else:
            return None

    def preamble(self) -> str:
        return r"""
\usepackage{longtable}        
\setlength{\tabcolsep}{-0.75em}

\usepackage{tikz}
\usetikzlibrary{calc}
\usetikzlibrary{matrix}

\tikzstyle{salsa-layout}=[
    matrix of nodes, 
    nodes={
        circle, inner sep=1pt, anchor=center,
        % outer sep=0em  % outer sep sadly controls two things: the extent of the border cells past the node borders (which we want), AND the radius to which arrows attach.
    },
    column sep=1.5em,
    row sep=1.5em,
]
\tikzstyle{salsa-gridline}=[black!20]
\tikzstyle{salsa-encircle}=[draw, circle, inner sep=1pt]
\tikzstyle{salsa-arrow}=[-latex, black]

\newcommand{\filler}{\phantom{M}}
        """
