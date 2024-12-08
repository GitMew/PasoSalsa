from typing import List, Union, Optional

from math import cos, sin, radians, atan2, degrees

from .general import Visualiser, Panel, GridSpec, Visualisable, WhichPerson
from ...domain.instances.movement import InPlace
from ...domain.abstracts.simulation import AbsoluteFootState, NamedFoot, _StepVisitor
from ...domain.abstracts.movement import *


class TikzVisualiser(Visualiser):
    """
    Prints the positions of the steps as TikZ code.
    """

    def __init__(self, which: WhichPerson, panels_per_row: int=3, loop_count_after: Optional[int]=None, show_count_0: bool=False,
                 do_colour: bool=True, rotate_everything_by: int=0):
        super().__init__(which=which, panels_per_row=panels_per_row, loop_count_after=loop_count_after, show_count_0=show_count_0, rotate_everything_by=rotate_everything_by)
        self._do_colour = do_colour

    def _render(self, pattern_or_figura: Visualisable) -> List[Panel]:
        gridspec, previous_feet, feet_and_steps = self._getRenderDetails(pattern_or_figura)

        panels = []
        width, height = gridspec.width, gridspec.height
        for count, (states, steps) in enumerate(feet_and_steps, start=1):
            if all(step is None for step in steps.values()):  # Pause == nobody moved.
                previous_feet = states
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
            for foot, position in states.items():
                panel_string += r"    \node" + f"[salsa-foot{self._footToNodeStyle(foot)},rotate={position.rotation-90}] at " + self._positionToMatrixCoordinate(position, gridspec) + " {" + self._footToString(foot) + "};\n"

            # Step 3: Visualise history.
            for foot, step in steps.items():
                style = self._footToArrowStyle(foot)

                start = previous_feet[foot]
                end   = states[foot]
                start_still_occupied = any(current.isSamePlace(start) for current in states.values())
                if not start.isSamePlace(end):
                    if isinstance(step, Move):  # TODO: It's quite difficult to know the trajectory of a foot given just its start and end pose. Possibly needs user disambiguation.
                        panel_string += r"    \draw[salsa-arrow" + style + "] " + self._positionToMatrixCoordinate(start, gridspec, anchor_center=not start_still_occupied) + " to " + self._positionToMatrixCoordinate(end, gridspec) + ";\n"
                    else:  # We assume that feet are always tangent to the arc of their movement. This means that when a foot moves and rotates, we can deduce which side of the movement line the foot's arc was based on whether it rotated clockwise (left of the line, higher degrees) or counterclockwise (right of the line, lower degrees).
                        if isinstance(step, MoveThenTurn):
                            manhattan_distance = abs(step.move.forward) + abs(step.move.rightward)
                            foot_rotation_sign = (-1)**(step.turn.degrees < 0)
                        elif isinstance(step, TurnThenMove):
                            manhattan_distance = abs(step.move.forward) + abs(step.move.rightward)
                            foot_rotation_sign = (-1)**(step.turn.degrees < 0)
                        else:
                            raise NotImplementedError

                        # Get movement line
                        delta_x = end.x - start.x
                        delta_y = end.y - start.y
                        movement_angle = degrees(atan2(delta_y, delta_x))
                        movement_angle = movement_angle if movement_angle >= 0 else movement_angle + 360

                        bending_angle = movement_angle - foot_rotation_sign*90
                        if abs(step.turn.degrees) > 180 or (abs(step.turn.degrees) > 135 and manhattan_distance <= 4):  # For highly rotating turns OR for quite rotating turns that are very tight, have an entry/exit away from the movement line.
                            out_angle = bending_angle
                            in_angle  = bending_angle + foot_rotation_sign*45
                            looseness = 2
                        else:  # For smaller turns, have the arc be 45° off the movement line.
                            out_angle = bending_angle + foot_rotation_sign*45
                            in_angle  = bending_angle - foot_rotation_sign*45
                            looseness = 1

                        panel_string += r"    \draw[salsa-arrow" + style + "] " + self._positionToMatrixCoordinate(start, gridspec, anchor_center=not start_still_occupied) + f" to[out={round(out_angle,3)},in={round(in_angle,3)},looseness={looseness}] " + self._positionToMatrixCoordinate(end, gridspec) + ";\n"
                elif step == InPlace:
                    panel_string += r"    \node[salsa-encircle" + style + "] at " + self._positionToMatrixCoordinate(start, gridspec) + r" {\filler};" + "\n"
                elif start.rotation != end.rotation:
                    assert isinstance(step, Turn)
                    start_angle = start.rotation
                    end_angle   = start_angle + step.degrees
                    panel_string += r"    \draw[salsa-arrow" + style + "] ($" + self._positionToMatrixCoordinate(start, gridspec) + "+" + f"({round(cos(radians(start_angle)),3)}em,{round(sin(radians(start_angle)),3)}em)" + f"$) arc[start angle={start_angle},end angle={end_angle},radius=1em];\n"

            panel_string += r"\end{tikzpicture}"
            panels.append(Panel(rendered=panel_string, count=count))

            previous_feet = states

        return panels

    def _concatenate(self, panels: List[Panel]) -> str:
        n = self._panels_per_row
        result = r"\begin{longtable}{" + "c"*n + "}\n"

        for i in range((len(panels)-1)//n + 1):
            subpanels = panels[n*i:n*(i+1)]
            result += "\n&\n".join(p.rendered for p in subpanels)
            result += r"\\[-1.75em]" + "\n"
            result += r"\bfseries " + r" & \bfseries ".join(str(p.count) for p in subpanels) + r" \\" + "\n"

        result += r"\end{longtable}"
        return result

    def _positionToMatrixCoordinate(self, position: AbsoluteFootState, gridspec: GridSpec, anchor_center: bool=False) -> str:
        return f"(m-{gridspec.height-1-position.y+2}-{position.x+2}" + ".center"*anchor_center + ")"

    def _footToString(self, foot: NamedFoot) -> str:
        if foot == NamedFoot.LeaderLeft:
            return "L"
        elif foot == NamedFoot.LeaderRight:
            return "R"
        elif foot == NamedFoot.FollowerLeft:
            return "L"
        elif foot == NamedFoot.FollowerRight:
            return "R"
        else:
            raise NotImplementedError

    def _footToNodeStyle(self, foot: NamedFoot) -> str:
        if self._do_colour:
            if foot in {NamedFoot.LeaderLeft, NamedFoot.LeaderRight}:
                return ",salsa-foot-leader"
            elif foot in {NamedFoot.FollowerLeft, NamedFoot.FollowerRight}:
                return ",salsa-foot-follower"
            else:
                raise NotImplementedError
        else:
            return ""

    def _footToArrowStyle(self, foot: NamedFoot) -> str:
        if self._do_colour:
            if foot in {NamedFoot.LeaderLeft, NamedFoot.LeaderRight}:
                return ",salsa-arrow-leader"
            elif foot in {NamedFoot.FollowerLeft, NamedFoot.FollowerRight}:
                return ",salsa-arrow-follower"
            else:
                raise NotImplementedError
        else:
            return ""

    def preamble(self) -> str:
        return r"""
\usepackage{longtable}        
\setlength{\tabcolsep}{-0.75em}

\usepackage[dvipsnames]{xcolor}

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
\tikzstyle{salsa-gridline}=[black!35]
\tikzstyle{salsa-encircle}=[draw, circle, inner sep=1pt]
\tikzstyle{salsa-arrow}=[-latex, black, line width=0.75pt]
\tikzstyle{salsa-foot}=[]

\newcommand{\filler}{\phantom{M}}

% Person-specific styling
\tikzstyle{salsa-foot-leader}=[RoyalBlue]
\tikzstyle{salsa-arrow-leader}=[RoyalBlue]
\tikzstyle{salsa-foot-follower}=[BrickRed]
\tikzstyle{salsa-arrow-follower}=[BrickRed]
        """


class StepToTikz(_StepVisitor):
    """
    TODO: In-place arrows when dealing with any kind of Turn.
    """

    def visit_Move(self, step: Move):
        pass

    def visit_Turn(self, step: Turn):
        pass

    def visit_MoveThenTurn(self, step: MoveThenTurn):
        pass

    def visit_TurnThenMove(self, step: TurnThenMove):
        pass
