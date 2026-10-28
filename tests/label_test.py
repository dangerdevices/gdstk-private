#!/usr/bin/env python

# Copyright 2020 Lucas Heitzmann Gabrielli.
# This file is part of gdstk, distributed under the terms of the
# Boost Software License - Version 1.0.  See the accompanying
# LICENSE file or <http://www.boost.org/LICENSE_1_0.txt>

import pytest
import gdstk

def test_repetition():
    label = gdstk.Label("foo", (5, 7))
    assert label.repetition is None

    label.repetition = gdstk.Repetition(rows=1, columns=3, spacing=(1, 1))
    assert isinstance(label.repetition, gdstk.Repetition)

    _ = label.apply_repetition()
    assert label.repetition is None

