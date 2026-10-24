# Accessibility

Use native HTML wherever possible. Static sites generally do not need JavaScript or ARIA libraries for basic accessibility.

- Use semantic landmarks such as `<header>`, `<nav>`, `<main>`, and `<footer>`, with a logical heading order and a descriptive page `<title>`.
- Write link text that describes the destination; avoid repeated vague labels such as “click here.”
- Give informative images meaningful `alt` text and decorative images `alt=""`.
- Associate each form control with a visible `<label>` and provide understandable error messages.
- Make links, buttons, and menus usable by keyboard. Keep focus indicators visible; do not remove outlines without an accessible replacement.
- Ensure text has sufficient contrast and remains readable when zoomed or viewed on narrow screens.

Prefer native `<button>` and `<a>` elements over clickable `<div>` elements. Test representative pages using only a keyboard and, when practical, a screen reader.
