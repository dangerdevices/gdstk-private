#!/usr/bin/env python

# Copyright 2020 Lucas Heitzmann Gabrielli.
# This file is part of gdstk, distributed under the terms of the
# Boost Software License - Version 1.0.  See the accompanying
# LICENSE file or <http://www.boost.org/LICENSE_1_0.txt>

import pytest
import gdstk


def test_inside():
    ring = gdstk.ellipse((0, 0), 1, inner_radius=0.5, tolerance=1e-3)
    circle = gdstk.ellipse((0, 0), 0.5, tolerance=1e-3)

    points = [(0, 0), (0.2, 0), (-0.1, -0.8), (0.9, 0.7), (-0.4, 0.4)]
    truth_ring = tuple(0.25 <= p[0] ** 2 + p[1] ** 2 <= 1 for p in points)
    truth_circle = tuple(p[0] ** 2 + p[1] ** 2 <= 0.25 for p in points)

    assert ring.contain(*points) == truth_ring
    assert ring.contain_all(*points) == all(truth_ring)
    assert ring.contain_any(*points) == any(truth_ring)

    assert circle.contain(*points) == truth_circle
    assert circle.contain_all(*points) == all(truth_circle)
    assert circle.contain_any(*points) == any(truth_circle)

    assert gdstk.inside(points, [ring, circle]) == tuple(
        r or c for r, c in zip(truth_ring, truth_circle)
    )
    assert gdstk.all_inside(points, [ring, circle]) == all(
        [r or c for r, c in zip(truth_ring, truth_circle)]
    )
    assert gdstk.any_inside(points, [ring, circle]) == any(
        [r or c for r, c in zip(truth_ring, truth_circle)]
    )

    polys = [gdstk.rectangle((0, 0), (10, 10)), gdstk.rectangle((10, 0), (20, 10))]
    for pts, _any, _all in (
        ([(1, 1), (-1, -1)], True, False),
        ([(2, 2), (-2, 2), (2, -2)], True, False),
        ([(5, 5), (10, 5)], True, True),
        ([(-1, -1), (-2, -2)], False, False),
        ([(2, 3)], True, True),
    ):
        assert gdstk.any_inside(pts, polys) == _any
        assert gdstk.all_inside(pts, polys) == _all


def test_references_short():
    c1 = gdstk.Cell("c1")
    c1.add(gdstk.rectangle((0, 0), (5, 5), layer=1))

    r1 = gdstk.Reference(c1, origin=(0, 0))
    r2 = gdstk.Reference(c1, origin=(2, 2))
    r3 = gdstk.Reference(c1, origin=(10, 10))

    assert gdstk.references_short(r1, r2)
    assert not gdstk.references_short(r1, r2, layers=())
    assert not gdstk.references_short(r1, r3)
    assert not gdstk.references_short(r2, r3)

    c2 = gdstk.Cell("c2")
    c2.add(
        gdstk.rectangle((10, 10), (20, 20), layer=1),
        gdstk.rectangle((-5, -5), (5, 5), layer=2),
    )

    r4 = gdstk.Reference(c2, origin=(0, 0))
    r5 = gdstk.Reference(c2, origin=(-7, -7))

    assert not gdstk.references_short(r1, r4)
    assert gdstk.references_short(r1, r5)
    assert not gdstk.references_short(r1, r5, layers=((2, 0),))
