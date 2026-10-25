# edoworks.github.io

**Retirement in progress (2026-10-25).** The owner has ended the Edoworks
website and product portfolio. This repository is being preserved in the
Foculoom archives before GitHub Pages and the source repository are removed.
The structure below describes the historical site.

Former public website for **Edoworks**.

- **Domain:** `edoworks.com` (historically served via GitHub Pages and Cloudflare DNS).
- **Surfaces:** landing (`index.html`), blog (`blog/index.html`), portfolio
  (`portfolio/index.html`), Rung project page (`rung/index.html`), and the
  qualification-stage NowNest pages (`nownest/`).
- **Build stamp:** every HTML page carries
  `<meta name="generator" content="Edoworks <version>">` and a
  `Built by Edoworks <version>.` footer per
  `.factory/standards/factory-stamp.md`.

## Brand architecture

- **Edoworks** = software engineering work (portfolio + blog at `edoworks.com`).
- **Foculoom LLC** = legal entity (corporate site at `foculoom.com`).

See `.factory/standards/factory-stamp.md` § Brand architecture.

## Local structure

```
edoworks.github.io/
├── CNAME            # edoworks.com (set after domain registration)
├── index.html       # landing (links to portfolio + blog)
├── blog/
│   └── index.html   # blog index
├── rung/
│   └── index.html   # static Rung distribution page
├── nownest/          # qualification, support, privacy, and terms pages
└── robots.txt
```

## Publishing

This is a GitHub Pages site. Publishing changes requires rendered-page review
and the public-link check.
