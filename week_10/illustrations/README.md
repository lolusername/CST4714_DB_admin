# Week 10 static illustrations

These four static diagrams were rendered with Manim. They appear in the main PowerPoint lesson and beside the matching explanations in Colab. They contain no animation.

- [Filter, project, and sort](04_filter_project_sort.png) — slide 12
- [Array conditions and one matching event](01_array_match.png) — slide 16
- [The first update and the repeat](02_repeated_set.png) — slide 19
- [The expected state in an update filter](03_expected_state.png) — slide 21

The diagrams show selected fields from the Week 10 notebook. The write examples retain the complete test filter, including `test_record: True` and `course_fixture: "cst4714"`. The initial test record has no `assignee_id` field.

The editable [Manim source](week10_stills.py) uses Manim Community 0.22 and the Helvetica Neue and Menlo fonts. Render stills with:

```sh
manim -s -r 2240,960 --disable_caching --media_dir build week10_stills.py ArrayMatchStill RepeatedSetStill ExpectedStateStill FilterProjectSortStill
```

Each scene only adds objects. It does not play animations. The PNGs are 2240 × 960 pixels. Use the course's instructional-content license for the illustrations and its code license for the Python source.

The filter/projection/sort illustration uses only tickets 1001, 1003, and 1006 from the six-ticket fixture. Its stages are conceptual, not a claim about a physical query execution plan. The status filter excludes resolved ticket 1003; projection keeps ticket ID and status, and descending ticket ID puts 1006 before 1001. The stored documents are unchanged.
