# MCP Presentation (Manim)

This project contains an **animated presentation built with Manim and Manim Slides**.

## Installation

Install the required dependencies:

```bash
pip install manim manim-slides PyQt6
```

## Render the Presentation

Render the presentation using Manim:

```bash
manim render main.py MCPPresentation -ql
```

Options:

* `-ql` → quick low quality (fast rendering)
* `-qm` → medium quality
* `-qh` → high quality

## Run the Slides

After rendering, start the presentation:

```bash
manim-slides present MCPPresentation
```

## Controls

| Key       | Action            |
| --------- | ----------------- |
| → / Space | Next slide        |
| ←         | Previous slide    |
| F         | Fullscreen        |
| Q         | Quit presentation |

## Project Structure

```
project/
│
├── main.py          # Manim presentation code
├── media/           # Generated videos and images
└── README.md
```
