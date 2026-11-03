# Week 10 static illustrations

These three still diagrams appear on PowerPoint slides 30–32. They contain no animation.

- [Array conditions and one matching event](01_array_match.png)
- [The first update and the repeat](02_repeated_set.png)
- [The expected state in an update filter](03_expected_state.png)

The diagrams show selected fields from the Week 10 notebook. The write examples retain the complete test filter, including `test_record: True` and `course_fixture: "cst4714"`. The initial test record has no `assignee_id` field.

The editable [Manim source](week10_stills.py) uses Manim Community 0.22 and the Helvetica Neue and Menlo fonts. Render stills with:

```sh
manim -s -r 2240,960 --disable_caching --media_dir build week10_stills.py ArrayMatchStill RepeatedSetStill ExpectedStateStill
```

Each scene only adds objects. It does not play animations. The PNGs are 2240 × 960 pixels. Use the course's instructional-content license for the illustrations and its code license for the Python source.
