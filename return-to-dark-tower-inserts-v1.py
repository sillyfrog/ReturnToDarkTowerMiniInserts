#!/usr/bin/env python3
from copy import deepcopy
from pprint import pprint
from solid import *
from solid.utils import *
import pathlib
import math

FLOOR = 1.0

RIVER_FIRE_THICK = 8

CORNER_R = 2

TEXT_H = 0.4

CONTAINER_H = 64

TALLEST_H = 34

TOKENS_HEIGHT = CONTAINER_H - TALLEST_H - FLOOR


def base(width, depth, height, corner_r=CORNER_R):
    corners = [
        [+corner_r, +corner_r],
        [width - corner_r, +corner_r],
        [width - corner_r, depth - corner_r],
        [+corner_r, depth - corner_r],
    ]
    spheres = []
    for corner in corners:
        spheres.append(translate([corner[0], corner[1], corner_r])(sphere(r=corner_r)))
        spheres.append(
            translate([corner[0], corner[1], height - corner_r])(sphere(r=corner_r))
        )
    # for corner
    return hull()(*spheres)


SPORE_D = 17
SPORE_W = 66
SPORE_H = 24

SIEGE_TREES_W = 39
SIEGE_TREES_D = 16
SIEGE_TREES_H = 33

DUNGEON_W = 32
DUNGEON_D = 18
DUNGEON_H = 41

VIRTUE_4_D = 9
VIRTUE_3_D = 7
VIRTUE_W = 71
VIRTUE_H = 32

BASE_H = 20
BASE_DIA = 28.5


ALL_END_STEPS = [
    [0, 0],
    [45, 24],
    [52, 44],
    [54, 64],
    [58, 120],
    [62, 145],
    [66, 197],
]
TOP_END_D = 97
TOP_END_W = 58 - RIVER_FIRE_THICK + ALL_END_STEPS[-1][1]


def spore_trees():
    H = SIEGE_TREES_H / 2 + FLOOR

    steps = remove_river_fire_high(ALL_END_STEPS[:5])
    steps[-1][1] = SPORE_W + CORNER_R * 2
    steps[-1][0] = steps[-2][0]

    o = rendersection(steps, H, desc="Trees")

    o -= translate([-SPORE_D - CORNER_R, CORNER_R, H - SPORE_H / 2 - 3])(
        cube([SPORE_D, SPORE_W, SPORE_H])
    ).set_modifier("")

    o -= translate([-3 - SPORE_D - CORNER_R, SIEGE_TREES_W + CORNER_R + 1, H - TEXT_H])(
        rotate([0, 0, 90])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "SPORE",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="left",
                )
            )
        )
    )

    o -= translate([-steps[1][0] + CORNER_R, CORNER_R, FLOOR])(
        cube([SIEGE_TREES_D, SIEGE_TREES_W, SIEGE_TREES_H])
    ).set_modifier("")

    txt_move = 3
    siege_txt = translate([+txt_move, 0, 0])(
        rotate([0, 0, -90])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "SIEGE",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="right",
                )
            )
        )
    )
    siege_txt += translate([-txt_move, 0, 0])(
        rotate([0, 0, -90])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "TREES",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="right",
                )
            )
        )
    )

    o -= translate(
        [
            -steps[1][0] + CORNER_R + SIEGE_TREES_D / 2 - 3,
            SIEGE_TREES_W + CORNER_R + 1,
            H - TEXT_H,
        ]
    )(siege_txt)

    return o


def virtue():
    H = VIRTUE_H / 2 + FLOOR

    steps = remove_river_fire_high(ALL_END_STEPS[3:6])
    steps[0][1] = SPORE_W + CORNER_R * 2

    o = rendersection(steps, H)

    y = steps[0][1]
    w = steps[0][0]
    spacing = (w - CORNER_R / 2 - 4 * VIRTUE_3_D - VIRTUE_4_D) / 4
    d = steps[-1][1] - y
    offset = CORNER_R
    virtues = [VIRTUE_4_D] + [VIRTUE_3_D] * 4
    for virtue_d in virtues:
        o -= translate([-virtue_d - offset, d / 2 + y - VIRTUE_W / 2, FLOOR])(
            cube([virtue_d, VIRTUE_W, VIRTUE_H])
        ).set_modifier("")

        o -= translate([-virtue_d / 2 - offset, d / 2 + y, FLOOR - TEXT_H])(
            rotate([0, 0, 90])(
                linear_extrude(TEXT_H + 1)(
                    text(
                        "VIRTUE",
                        size=4,
                        font="Gloucester MT Extra Condensed:style=Regular",
                        # // font="Times New Roman:style=Bold",
                        valign="center",
                        halign="center",
                    )
                )
            )
        ).set_modifier("")
        offset += virtue_d + spacing

    return o


def quest_base_dungeon():
    HEIGHT = max(DUNGEON_H / 2, BASE_H) + FLOOR

    steps = ALL_END_STEPS[-2:]
    # steps = ALL_END_STEPS[-2:]
    x = -steps[-1][0]
    y = steps[-2][1]
    w = steps[1][0]
    d = steps[1][1] - steps[0][1]

    o = rendersection(steps, HEIGHT)

    bases = up(FLOOR)(cylinder(d=BASE_DIA, h=100))
    o -= translate([-BASE_DIA / 2, CORNER_R + BASE_DIA / 2 + y, 0])(bases)
    o -= translate([0, CORNER_R + BASE_DIA / 2 + y, -10])(bases)

    o -= translate([-BASE_DIA / 2 - 5, CORNER_R + BASE_DIA / 2 + y, FLOOR - TEXT_H])(
        rotate([0, 0, 90])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "BASES",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="center",
                )
            )
        )
    ).set_modifier("")

    tower_cut_w = w - CORNER_R * 2
    tower_cut_d = d - CORNER_R * 2 - BASE_DIA - 1
    o -= translate([-CORNER_R - tower_cut_w, CORNER_R * 1 + y + BASE_DIA + 1, FLOOR])(
        cube([tower_cut_w, tower_cut_d, 100])
    ).set_modifier("")

    o -= translate(
        [
            -CORNER_R - tower_cut_w / 2,
            CORNER_R * 1 + y + BASE_DIA + 1 + tower_cut_d / 2,
            FLOOR - TEXT_H,
        ]
    )(
        rotate([0, 0, 180])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "TOWERS",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="center",
                )
            )
        )
    )

    tower_cut_w = w - CORNER_R - BASE_DIA / 3
    tower_cut_d = d - CORNER_R * 3 - DUNGEON_D
    tower_cut = translate(
        [-tower_cut_w - BASE_DIA / 3, CORNER_R * 2 + y + DUNGEON_D, FLOOR]
    )(cube([tower_cut_w, tower_cut_d, 100])).set_modifier("")
    o -= tower_cut

    # Add a curve matching base on the tower edge
    curve = cylinder(d=BASE_DIA + CORNER_R * 2, h=HEIGHT - FLOOR) - cylinder(
        d=BASE_DIA, h=1000
    )
    # Keep just the required section
    curve = translate([-BASE_DIA / 2, CORNER_R + BASE_DIA / 2 + y, FLOOR])(curve)
    curve = intersection()(curve, tower_cut).set_modifier("")
    o += curve

    o -= translate([x + CORNER_R, y + CORNER_R, FLOOR])(
        cube([DUNGEON_W, DUNGEON_D, DUNGEON_H])
    ).set_modifier("")

    o -= translate(
        [
            x + CORNER_R + DUNGEON_W / 2,
            y + CORNER_R + DUNGEON_D / 2,
            FLOOR - TEXT_H,
        ]
    )(
        rotate([0, 0, 0])(
            linear_extrude(TEXT_H + 1)(
                text(
                    "DUNGN",
                    size=5,
                    font="Gloucester MT Extra Condensed:style=Regular",
                    # // font="Times New Roman:style=Bold",
                    valign="center",
                    halign="center",
                )
            )
        )
    )
    return o


def tokens():
    TOP_EXTRA_WIDTH = 2

    TOKEN_CORNER_R = 6

    def token_text(txt, steps):
        x = (steps[1][0]) / 2
        y = (steps[-1][1] + steps[0][1]) / 2
        return translate([-x, y, FLOOR - TEXT_H,])(
            rotate([0, 0, 0])(
                linear_extrude(TEXT_H + 1)(
                    text(
                        txt,
                        size=5,
                        font="Gloucester MT Extra Condensed:style=Regular",
                        valign="center",
                        halign="center",
                    )
                )
            )
        ).set_modifier("")

    steps = ALL_END_STEPS[:-1]
    o = rendersection(steps, TOKENS_HEIGHT)

    # Put a hard edge on this side for hte river of fire to rest on
    depth = steps[-1][1]
    lift_edge = translate([0, 0, TOKENS_HEIGHT - CORNER_R])(
        rotate([0, -90, 0])(cylinder(r=CORNER_R, h=CORNER_R))
    )
    river_lift_edges = []
    river_lift_edges.append(translate([0, CORNER_R + 5, 0])(lift_edge))
    river_lift_edges.append(translate([TOP_EXTRA_WIDTH, CORNER_R + 5, 0])(lift_edge))
    river_lift_edges.append(
        translate([-CORNER_R, CORNER_R + 5, CORNER_R])(sphere(r=CORNER_R))
    )

    river_lift_edges.append(translate([0, depth - CORNER_R - 5, 0])(lift_edge))
    river_lift_edges.append(
        translate([TOP_EXTRA_WIDTH, depth - CORNER_R - 5, 0])(lift_edge)
    )
    river_lift_edges.append(
        translate([-CORNER_R, depth - CORNER_R - 5, CORNER_R])(sphere(r=CORNER_R))
    )
    # o += lift_start
    o += hull()(*river_lift_edges)

    steps1 = deepcopy(steps[:3])
    o -= rendersection(steps1, 100, True, corner_r=TOKEN_CORNER_R).set_modifier("")
    o -= token_text("SPIRIT", steps1)

    steps2 = deepcopy(steps[2:5])
    steps2[0][1] -= CORNER_R
    steps2[-1][1] -= 40
    o -= rendersection(steps2, 100, True, corner_r=TOKEN_CORNER_R).set_modifier("")
    o -= token_text("SPIRIT", steps2)

    steps3 = deepcopy(steps[3:5])
    steps3[0][1] = steps2[-1][1] - CORNER_R
    steps3[-1][1] -= 6.5
    o -= rendersection(steps3, 100, True, corner_r=TOKEN_CORNER_R).set_modifier("")
    o -= token_text("WORRIOR", steps3)

    steps4 = deepcopy(steps[3:6])
    steps4[0][1] = steps3[-1][1] - CORNER_R
    o -= rendersection(steps4, 100, True, corner_r=TOKEN_CORNER_R).set_modifier("")
    o -= token_text("WORRIOR", steps4)

    return o


def rendersection(steps, height, do_hollow=False, desc=None, corner_r=CORNER_R):
    offset_y = 0
    final_y = steps[-1][1]
    parts = []
    last_y = steps[0][1]
    if do_hollow:
        offset_y -= CORNER_R
        z = FLOOR
        x = CORNER_R
        w = CORNER_R * 2
    else:
        z = 0
        x = 0
        w = 0

    total = 0
    for step_x, step_y in steps[1:]:
        extra = corner_r * 2
        if step_y == final_y:
            if do_hollow:
                extra = -CORNER_R * 2
            else:
                extra = 0
        parts.append(
            translate([-step_x + x, last_y - offset_y, z])(
                base(step_x - w, step_y - last_y + extra, height, corner_r)
            )
        )
        if desc:
            print(
                desc, (step_x - w), (step_y - last_y), (step_x - w) * (step_y - last_y)
            )
            total += (step_x - w) * (step_y - last_y)
        last_y = step_y

    if desc:
        print(desc, "Total:", total)
    return sum(parts)


def remove_river_fire(steps):
    ret = []
    for x, y in steps:
        if x > RIVER_FIRE_THICK:
            x -= RIVER_FIRE_THICK
        ret.append([x, y])
    return ret


def remove_river_fire_high(steps):
    THICK = RIVER_FIRE_THICK - 5
    ret = []
    for x, y in steps:
        if x > THICK:
            x -= THICK
        ret.append([x, y])
    return ret


def cos(angle):
    return math.cos(math.radians(angle))


def sin(angle):
    return math.sin(math.radians(angle))


def tan(angle):
    return math.tan(math.radians(angle))


def main():

    saveasscad(spore_trees(), "spore_trees")
    saveasscad(virtue(), "virtue")
    saveasscad(quest_base_dungeon(), "quest_base_dungeon")
    saveasscad(rotate([0, 0, 90])(tokens()), "tokens")
    # saveasscad(
    #     quest_base_dungeon()
    #     + translate([-RIVER_FIRE_THICK, 0, TOKENS_HEIGHT])(spore_trees() + virtue())
    #     + tokens(),
    #     "together",
    # )
    return


def saveasscad(obj, name):
    fn = pathlib.Path(__file__)
    outfn = fn.parent / (name + ".scad")
    scad_render_to_file(obj, outfn, file_header="$fn = 90;\n")


if __name__ == "__main__":
    main()
