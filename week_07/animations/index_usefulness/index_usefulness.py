"""An original, captioned CST4714 animation. No database timings are simulated.

Render: uv run manim -qh --fps 30 index_usefulness.py IndexUsefulness
Prose/visuals: CC BY-NC-SA 4.0; original code: MIT. Atilio Barreda, 2026.
"""
from manim import *

config.background_color = "#F7F8FA"
config.frame_width = 16
config.frame_height = 9

INK = "#17212D"
MUTED = "#536373"
BLUE = "#3565E8"
PURPLE = "#A83CCE"
GREEN = "#167A65"
AMBER = "#A96012"
LINE = "#CAD3DE"
WHITE_BG = "#FFFFFF"

PEOPLE = [
    (101, "Ada", "Kim"), (102, "Atilio", "Barreda"),
    (103, "Lina", "Ortiz"), (104, "Noah", "Chen"),
    (105, "Maya", "Barreda"), (106, "Omar", "Singh"),
]


def label(text, size=26, color=INK, **kwargs):
    return Text(text, font="Arial", font_size=size, color=color, **kwargs)


def fit_text(text, size=26, width=13.8, color=INK):
    mob = label(text, size=size, color=color, line_spacing=1.15)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def panel(width, height, color=LINE, fill=WHITE_BG):
    return RoundedRectangle(width=width, height=height, corner_radius=0.12,
                            stroke_color=color, stroke_width=1.4,
                            fill_color=fill, fill_opacity=1)


def users_table(center=LEFT * 3.65 + DOWN * 0.30):
    width, row_h = 6.0, 0.53
    grid = VGroup()
    rows = []
    contents = []
    headers = ["id", "fname", "lname"]
    xs = [-2.33, -0.65, 1.65]
    for i, vals in enumerate([headers] + [list(map(str, row)) for row in PEOPLE]):
        box = Rectangle(width=width, height=row_h, stroke_color=LINE, stroke_width=1,
                        fill_color="#EBEFF5" if i == 0 else WHITE_BG, fill_opacity=1)
        box.move_to([0, 1.59 - i * row_h, 0])
        row = VGroup(box)
        txts = VGroup()
        for x, value in zip(xs, vals):
            t = label(value, size=23 if i else 22, color=MUTED if i == 0 else INK)
            t.move_to([x, box.get_y(), 0])
            txts.add(t)
        row.add(txts)
        grid.add(row)
        if i:
            rows.append(box)
            contents.append(txts)
    title = label("users  ·  table", size=27).next_to(grid, UP, buff=0.24)
    all_mobs = VGroup(title, grid).move_to(center)
    return all_mobs, rows, contents


def lastname_index(center=RIGHT * 4.2 + DOWN * 0.40):
    entries = sorted([(person[2], i) for i, person in enumerate(PEOPLE)])
    rows = []
    texts = []
    group = VGroup()
    for j, (name, slot) in enumerate(entries):
        box = panel(4.35, 0.53, color=PURPLE).move_to([0, 1.0 - j * 0.59, 0])
        text = label(f"{name}   →   location {slot + 1}", size=22)
        text.move_to(box)
        group.add(VGroup(box, text))
        rows.append(box)
        texts.append(text)
    heading = label("users_lname_idx", size=27, color=PURPLE).next_to(group, UP, buff=0.20)
    sub = label("ordered keys + row locations", size=18, color=MUTED).next_to(group, DOWN, buff=0.18)
    group = VGroup(heading, group, sub).move_to(center)
    return group, rows, texts, entries


class IndexUsefulness(Scene):
    """Readable without audio; designed for instructor narration or pausing."""

    def construct(self):
        self.timeline = []
        self.caption_track = []
        self.introduction()
        self.scan()
        self.build_index()
        self.lookup()
        self.every_row()
        self.selectivity()
        self.wrong_column()
        self.upkeep()
        self.verify()

    def chapter(self, number, title):
        if self.caption_track and 'end' not in self.caption_track[-1]:
            self.caption_track[-1]['end'] = round(self.renderer.time, 3)
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        self.timeline.append((round(self.renderer.time, 2), title))
        eyebrow = label(f"CST4714  /  DATABASE ADMINISTRATION     {number}", size=17, color=BLUE)
        eyebrow.to_corner(UL, buff=0.55)
        heading = fit_text(title, size=39).next_to(eyebrow, DOWN, buff=0.28).align_to(eyebrow, LEFT)
        rule = Line(LEFT * 7.4 + UP * 2.95, RIGHT * 7.4 + UP * 2.95, color=LINE)
        foot = label("Schematic illustration · not a benchmark", size=16, color=MUTED)
        foot.to_corner(DR, buff=0.30)
        self.play(FadeIn(eyebrow), FadeIn(heading), Create(rule), FadeIn(foot), run_time=0.45)
        self.caption_mob = None

    def caption(self, text, color=INK):
        if self.caption_track and 'end' not in self.caption_track[-1]:
            self.caption_track[-1]['end'] = round(self.renderer.time, 3)
        new = fit_text(text, size=27, width=14.2, color=color).move_to(DOWN * 3.2)
        if self.caption_mob is None:
            self.play(FadeIn(new), run_time=0.35)
        else:
            self.play(ReplacementTransform(self.caption_mob, new), run_time=0.35)
        self.caption_mob = new
        self.caption_track.append({'start': round(self.renderer.time, 3), 'text': text})

    def query(self, text):
        t = Text(text, font="Menlo", font_size=23, color=INK, line_spacing=1.05)
        if t.width > 13.5:
            t.scale_to_fit_width(13.5)
        box = panel(14.5, max(0.65, t.height + 0.25)).move_to(UP * 2.35)
        t.move_to(box)
        self.play(FadeIn(box), Write(t), run_time=0.75)
        return VGroup(box, t)

    def introduction(self):
        self.chapter("01", "When does an index help?")
        table = panel(4.5, 2.2).move_to(LEFT * 3.7)
        table_label = label("users", size=42).move_to(table)
        idx = panel(4.5, 2.2, PURPLE).move_to(RIGHT * 3.7)
        idx_label = label("index on lname", size=35, color=PURPLE).move_to(idx)
        arrow = Arrow(idx.get_left(), table.get_right(), color=PURPLE, buff=0.2)
        self.play(FadeIn(table), Write(table_label), FadeIn(idx), Write(idx_label), GrowArrow(arrow), run_time=1.0)
        self.caption("An index gives PostgreSQL another way to find rows.\nWhether it helps depends on the query and the data.")
        self.wait(4)

    def scan(self):
        self.chapter("02", "Without a matching index: inspect the table")
        self.query("SELECT * FROM users WHERE lname = 'Barreda';")
        table, rows, _ = users_table()
        self.play(FadeIn(table), run_time=0.55)
        description = fit_text("Sequential scan\n\nCheck each row's lname.\nReturn every match.", size=30, width=6)
        description.move_to(RIGHT * 3.7 + UP * 0.4)
        self.play(FadeIn(description), run_time=0.4)
        self.caption("The table is not ordered by last name.")
        cursor = SurroundingRectangle(rows[0], buff=0.02, color=BLUE, stroke_width=3)
        self.play(Create(cursor), run_time=0.3)
        for i, row in enumerate(rows):
            if i:
                self.play(cursor.animate.move_to(row), run_time=0.45)
            if i in [1, 4]:
                self.play(row.animate.set_fill("#EFE0F7", opacity=1), run_time=0.35)
            self.wait(0.35)
        self.caption("Two rows match. Finding the first one does not end the scan.")
        self.wait(3)

    def build_index(self):
        self.chapter("03", "Build a separate structure for last names")
        self.query("CREATE INDEX users_lname_idx ON users (lname);")
        table, rows, contents = users_table()
        idx, idx_rows, idx_text, entries = lastname_index()
        self.play(FadeIn(table), run_time=0.5)
        self.play(FadeIn(idx[0]), FadeIn(idx[2]), *[Create(r) for r in idx_rows], run_time=0.7)
        for j, (_, slot) in enumerate(entries):
            self.play(TransformFromCopy(contents[slot][2], idx_text[j]), run_time=0.42)
        self.caption("The B-tree keeps ordered keys and row locations.\nCreating it does not reorder the table.")
        self.wait(4)

    def lookup(self):
        self.chapter("04", "One possible plan: look up, then fetch")
        self.query("SELECT * FROM users WHERE lname = 'Barreda';")
        table, rows, _ = users_table()
        idx, idx_rows, _, _ = lastname_index()
        self.play(FadeIn(table), FadeIn(idx), run_time=0.6)
        self.caption("A B-tree uses guide keys to find the matching key range.")
        guide = panel(2.0, 0.5, PURPLE).move_to(RIGHT * 0.65 + UP * 0.8)
        guide_text = label("guide keys", size=18, color=PURPLE).move_to(guide)
        path = Arrow(guide.get_right(), idx_rows[0].get_left(), buff=0.05, color=PURPLE)
        self.play(FadeIn(guide), FadeIn(guide_text), GrowArrow(path), run_time=0.4)
        self.play(Indicate(idx_rows[0], color=PURPLE), Indicate(idx_rows[1], color=PURPLE), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(guide), FadeOut(guide_text), FadeOut(path), run_time=0.3)
        self.caption("The index finds two locations. SELECT * also needs fname and id,\nso this plan fetches the complete rows from the table.")
        arrows = VGroup()
        for j, slot in [(0, 1), (1, 4)]:
            arrow = Arrow(idx_rows[j].get_left(), rows[slot].get_right(), color=PURPLE,
                          buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.12)
            arrows.add(arrow)
            self.play(idx_rows[j].animate.set_fill("#EFE0F7", opacity=1),
                      GrowArrow(arrow), rows[slot].animate.set_fill("#EFE0F7", opacity=1), run_time=0.8)
        self.wait(3)
        self.caption("Same matching rows; another route.\nFor just six rows, PostgreSQL may still choose a sequential scan.")
        self.wait(4)

    def every_row(self):
        self.chapter("05", "No WHERE clause: every row is still needed")
        self.query("SELECT * FROM users;")
        table, rows, _ = users_table()
        idx, _, _, _ = lastname_index()
        self.play(FadeIn(table), FadeIn(idx), run_time=0.5)
        self.play(idx.animate.set_opacity(0.25), run_time=0.5)
        self.caption("This query asks for all columns of all rows.\nThe lname index cannot eliminate rows from that request.")
        for row in rows:
            self.play(row.animate.set_fill("#DCE7FE", opacity=1), run_time=0.35)
        self.wait(2)
        self.caption("Reading the table directly is often cheaper than\nwalking an index and fetching every table row.")
        self.wait(4)

    def selectivity(self):
        self.chapter("06", "How much of the table must PostgreSQL visit?")
        small_label = label("Small table", size=30).move_to(LEFT * 4.25 + UP * 2.1)
        large_label = label("Larger table, few matches", size=30).move_to(RIGHT * 2.75 + UP * 2.1)
        page = panel(2.65, 2.3).move_to(LEFT * 4.25 + UP * 0.25)
        tiny_rows = VGroup(*[Line(LEFT * 1.05, RIGHT * 1.05, color=LINE) for _ in range(8)])
        tiny_rows.arrange(DOWN, buff=0.2).move_to(page)
        small_caption = label("All rows fit on one page", size=21, color=MUTED).next_to(page, DOWN, buff=0.3)
        pages = VGroup(*[Square(side_length=0.45, stroke_color=LINE, stroke_width=1,
                                fill_color=WHITE_BG, fill_opacity=1) for _ in range(64)])
        pages.arrange_in_grid(rows=8, cols=8, buff=0.07).move_to(RIGHT * 2.75 + DOWN * 0.20)
        self.play(FadeIn(small_label), FadeIn(large_label), FadeIn(page), FadeIn(tiny_rows),
                  FadeIn(small_caption), FadeIn(pages), run_time=0.8)
        self.caption("PostgreSQL reads table pages. On a tiny table,\na direct scan can cost less than an index lookup plus row fetches.")
        self.play(page.animate.set_fill("#DCE7FE", opacity=1), run_time=0.8)
        self.wait(3)
        self.caption("If a matching index lets a query visit only a few table pages,\nit can avoid much of the scan. These boxes are illustrative pages.")
        self.play(pages[11].animate.set_fill(PURPLE, opacity=0.6),
                  pages[52].animate.set_fill(PURPLE, opacity=0.6), run_time=1)
        self.wait(3.5)
        new_label = label("Many matches across most pages", size=28).move_to(large_label)
        self.play(ReplacementTransform(large_label, new_label), run_time=0.5)
        self.play(LaggedStart(*[p.animate.set_fill(PURPLE, opacity=0.45) for i,p in enumerate(pages) if i < 56], lag_ratio=0.025), run_time=2)
        self.caption("When matches spread across most pages, index-driven row fetches\nmay add work. A sequential scan or bitmap plan may cost less.")
        self.wait(4)

    def wrong_column(self):
        self.chapter("07", "The indexed column must fit the search")
        self.query("SELECT * FROM users WHERE lname = 'Barreda';")
        bad = panel(6.1, 2.0).move_to(LEFT * 3.55)
        good = panel(6.1, 2.0, PURPLE).move_to(RIGHT * 3.55)
        bad_text = label("ON users (fname)\nFirst names", size=29).move_to(bad)
        good_text = label("ON users (lname)\nLast names", size=29, color=PURPLE).move_to(good)
        self.play(FadeIn(bad), FadeIn(good), Write(bad_text), Write(good_text), run_time=0.8)
        self.caption("A first-name index does not directly locate a last-name match.\nThe ON users (lname) definition determines the indexed column.")
        self.wait(4)
        self.play(Indicate(good, color=PURPLE), run_time=0.8)
        self.caption("users_lname_idx is a helpful name.\nThe index name itself does not control which column it searches.")
        self.wait(3)

    def upkeep(self):
        self.chapter("08", "An index has a storage and maintenance cost")
        table = panel(4.4, 2.0).move_to(LEFT * 3.6)
        idx = panel(4.4, 2.0, PURPLE).move_to(RIGHT * 3.6)
        t = label("users table", size=31).move_to(table)
        i = label("lname index", size=31, color=PURPLE).move_to(idx)
        insert = label("Insert a new user:  Zoe Zhou", size=32).move_to(UP * 2)
        self.play(FadeIn(table), FadeIn(idx), Write(t), Write(i), Write(insert), run_time=0.8)
        row = label("new row", size=23, color=BLUE).move_to(LEFT * 3.6 + DOWN * 1.7)
        key = label("new key + location", size=23, color=PURPLE).move_to(RIGHT * 3.6 + DOWN * 1.7)
        self.play(TransformFromCopy(insert, row), TransformFromCopy(insert, key), run_time=1.2)
        self.caption("The insert maintains both structures.\nDeletes and changes to indexed values also require index work.")
        self.wait(4)
        self.caption("Keep an index when its benefit to the workload\nis worth its extra storage and maintenance.")
        self.wait(3)

    def verify(self):
        self.chapter("09", "An index is an option. Check the chosen plan.")
        code = Text("EXPLAIN (ANALYZE, BUFFERS)\nSELECT * FROM users\nWHERE lname = 'Barreda';", font="Menlo", font_size=29, color=INK,
                    line_spacing=1.2).move_to(UP * 1.2)
        self.play(Write(code), run_time=1.3)
        note = label("ANALYZE executes this SELECT.", size=23, color=BLUE).next_to(code, DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        outcomes = label("Seq Scan     ·     Index Scan     ·     Bitmap Heap Scan", size=27, color=PURPLE).move_to(DOWN * 0.8)
        self.play(FadeIn(outcomes), run_time=0.6)
        self.caption("Compare actual plan, rows, and buffers before and after.\nKeep the query and data the same; confirm the same results.")
        self.wait(4)
        self.caption("PostgreSQL chooses a plan using estimated costs.\nAn unchanged sequential scan can be a sensible result.")
        self.wait(4)
        import json
        from pathlib import Path
        Path(config.media_dir).mkdir(parents=True, exist_ok=True)
        (Path(config.media_dir) / "chapters.json").write_text(json.dumps(self.timeline, indent=2) + "\n")
        self.caption_track[-1]['end'] = round(self.renderer.time, 3)
        (Path(config.media_dir) / "captions.json").write_text(json.dumps(self.caption_track, indent=2) + "\n")
