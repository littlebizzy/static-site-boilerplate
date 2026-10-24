# Images

Store site images in `assets/` so `build.py` copies them to `public/assets/`.

- **Formats:** Use JPEG for photographs, PNG for images needing lossless detail or transparency, SVG for icons and illustrations, and WebP when smaller files are useful and supported by your workflow.
- **Names and alt text:** Use descriptive filenames and meaningful `alt` text for informative images. Use `alt=""` for purely decorative images.
- **Dimensions:** Set `width` and `height` to reserve space and prevent layout shifts; CSS can still make images responsive.
- **Loading:** Add `loading="lazy"` for images below the fold. Do not lazy-load the main hero image; consider `fetchpriority="high"` if it is the page's primary image.
- **Responsive images:** Use `srcset` and `sizes` when you have multiple image widths available. Compress images before publishing without visibly degrading them.

```html
<img
  src="/assets/photo-800.jpg"
  srcset="/assets/photo-400.jpg 400w, /assets/photo-800.jpg 800w"
  sizes="(max-width: 600px) 100vw, 800px"
  width="800"
  height="500"
  alt="A descriptive explanation of the image"
  loading="lazy"
>
```

Only reference image variants that actually exist in `assets/`.
