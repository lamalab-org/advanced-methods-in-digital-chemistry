# Course visual identity

The course borrows the warm red (`#A43830`, hover `#8A2E27`), white background,
thin rules, JetBrains Mono typography, and lab mark from [lamalab.org](https://lamalab.org/),
inspected on 27 October 2026. Long explanations retain proportional system text;
headings, navigation, and code carry the monospaced style. Chemical notation and
capitalisation are preserved.

- `lamalab-logo.png`: unchanged lab mark from <https://lamalab.org/png-file.png>.
- `fonts/JetBrainsMono-Regular.woff2` and `fonts/JetBrainsMono-Bold.woff2`:
  [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono/tree/master/fonts/webfonts),
  distributed with its [SIL Open Font License](fonts/OFL.txt).
- `lamalab.scss`: Quarto/Bootstrap colour and font settings.
- `lamalab.css`: shared local font declarations and colour tokens.
- `course.css`: reading, navigation, small-screen, and print styles.
- `activities.css`: matching typography and controls for the interactive examples;
  plot colours continue to encode their existing scientific distinctions.

The fonts and logo are hosted with the course. The private instructor book copies
these shared assets during its local pre-render step, so both books use the same
source styling without publishing instructor material.
