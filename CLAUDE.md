# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The marketing website for Órale – Authentic Mexican Flavor, a Mexican food business in Limerick, Ireland. It is served directly by GitHub Pages from this repo (`orale-authentic-mexican-flavor.github.io`) — there is no build step, bundler, package manager, or test suite. The entire site is `index.html`: a single self-contained HTML file with inline `<style>` and inline `<script>`, plus a handful of image assets and a PDF at the repo root.

## Reglas de trabajo — Órale

### Git y control de versiones
- NO crees ramas, NO hagas commits, NO hagas push, NI crees Pull Requests de forma
  automática. Realiza cualquier operación de git ÚNICAMENTE si yo lo pido de forma
  explícita en el momento.
- Al terminar los cambios, déjalos SIN commitear y avísame qué archivos modificaste.
  Yo reviso y decido cuándo commitear, crear la rama y el PR.
- Antes de cualquier operación de git (branch, add, commit, push, PR), pídeme
  confirmación explícita.
- master es la rama de producción (GitHub Pages publica desde ahí). Nunca hagas
  cambios directos ni operaciones de git sobre master sin mi confirmación.

### Verificación y pruebas
- NO levantes servidores locales (python -m http.server, npx serve, live-server, etc.)
  ni uses plugins o automatización de navegador (Chrome, Playwright, etc.) de forma
  proactiva.
- Puedes levantar el servidor a petición del usuario, pero primero pregunta y
  espera confirmación explícita antes de iniciarlo.
- Cuando el usuario pida explícitamente levantar el servidor y verificar
  funcionalidades, puedes usar automatización de navegador y herramientas
  relacionadas para hacer pruebas funcionales de lo levantado.
- Fuera de ese caso explícito, el usuario levanta el servidor y revisa los
  cambios manualmente cuando lo decide.
- Al terminar una tarea, describe qué archivos cambiaste y qué debe revisar el
  usuario, pero NO ejecutes pruebas por tu cuenta ni intentes verificar en
  ejecución salvo que el usuario lo haya solicitado explícitamente como se
  indica arriba.

### Estilo del sitio
- El sitio es bilingüe EN/ES con inglés por defecto (toggle data-en/data-es + LANG).
- Todo texto de interfaz nuevo debe ser bilingüe. Los nombres de platillos y de
  personas se mantienen en español en ambos idiomas.
- Respeta la paleta, tipografías, botones .btn, papel picado y favicon existentes.
- No dupliques los datos de platillos: viven solo en dishes-data.js.
- No rompas funcionalidad existente (menú, toggle, secciones, imágenes, video, QR).

## Development workflow

There are no build/lint/test commands — none exist in this repo. To work on the site:

- Edit `index.html` directly.
- Preview by opening the file in a browser, or serving the directory locally (e.g. `python -m http.server`) so relative asset paths (`hero-food.png`, `dish-pork-red-pozole.png`, etc.) resolve correctly.
- Changes go live on push to `master` via GitHub Pages — there is no CI/staging environment, so treat commits to `master` as production deploys.

## Architecture of `index.html`

Everything lives in one file, structured top to bottom as:

1. **`<style>` block** — CSS custom properties in `:root` define the brand palette (`--chile`, `--nopal`, `--cempasuchil`, `--talavera` — colors named after the Mexican flag/Talavera pottery motif) and typography (`Fraunces` for display, `DM Sans` for body). All component styles follow.
2. **Markup sections** in page order: nav → hero → `#order` → `#menu` → `#about` → `#refund` → `#contact` → footer. Decorative inline SVGs (papel picado bunting, sugar skull, cactus, mariachi motifs) are hand-drawn paths embedded directly in the HTML.
3. **`<script>` block** at the bottom drives two runtime concerns:
   - **Bilingual content (EN/ES)**: nearly every user-facing element carries `data-en` and `data-es` attributes holding the two language variants. `applyLang()` swaps `innerHTML` for every `[data-en]` element based on the `LANG` variable and re-renders the menu; the language toggle button (`#langBtn`) flips `LANG` and calls `applyLang()`. **When adding or editing any visible text, always set both `data-en` and `data-es`** (and keep the element's own text content in sync with the `data-en` value, since that's the initial render before JS runs).
   - **Menu data-driven rendering**: the `#menu` section is empty markup (`<div id="menuRoot">`) populated entirely from JS data. `CATS` defines menu categories in display order; `DISHES` is a flat array of dish objects (`cat`, `v` for vegan, `a` for allergen keys, optional `img`, and `en`/`es` sub-objects with `n`/`d` name/description). `ALLERGENS` maps allergen keys to bilingual labels. `renderMenu()` groups `DISHES` by `CATS` order and builds the dish grid, including allergen chips and the vegan badge. **To add/edit/remove a dish or category, edit the `CATS`/`DISHES`/`ALLERGENS` JS objects — do not hand-write dish markup.** Dish prices are intentionally not listed here (`€ —`); pricing lives on the delivery platforms, per the menu note.

## Content notes

- Allergen tagging follows the 14 EU/FSAI statutory allergens (see the `#about` safety box copy) — when adding a dish, set `a: [...]` accurately using the existing `ALLERGENS` keys (`gluten`, `milk`, `soy`, `sesame`, `nuts`, `peanuts`, `sulphites`); use `a: []` if none apply (renders "No statutory allergens declared").
- External links to keep in sync if the business changes them: Uber Eats / Deliveroo order links (currently placeholder `#`), WhatsApp (`https://wa.me/353899610776`), Instagram/Facebook (placeholder `#`, marked with `EDITAR` comments), Google Business Profile (placeholder `#`).
- The Refund Policy PDF (`Orale_Refund_Policy_V1.0.pdf`) is linked from both the `#refund` section and the footer via its absolute GitHub Pages URL — if the PDF filename changes, update both links.

## Estructura del repositorio

### /docs — Sitio web estático
Servido por GitHub Pages desde /docs/.
Configuración: Settings → Pages → Source → /docs.
No mover index.html fuera de /docs/.
Archivos principales: index.html, dish.html, dishes-data.js.

### /haccp — Documentos HACCP
Scripts de generación del Plan HACCP v1.3.
Ver instrucciones específicas en CLAUDE.md del repo HACCP.
No copiar config.js al repo — está en .gitignore.
No ejecutar npm install ni generar outputs sin autorización explícita.
