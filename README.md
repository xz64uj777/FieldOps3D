# Field Ops 3D — Site Crew v0.9

Browser-first Three.js construction / field-operations simulator.

Improved modular fork of [Chatdemo](https://github.com/xz64uj777/Chatdemo) Field Ops.

**Play (after Pages deploy):** https://xz64uj777.github.io/FieldOps3D/

## Improvements vs Chatdemo monolith

| Area | Change |
|------|--------|
| Structure | CSS extracted; ES modules (`src/main.js`, `src/constants.js`, assembled `game.js`) |
| Mobile perf | Adaptive pixel ratio (1.5 touch / 1.8 desktop) |
| Options | Shadow quality Off / Low / High (persisted) |
| UX | Manual **Save** button; restart confirm (upstream) |
| Mobile chrome | Steer L/R + Lights hidden on narrow screens |
| Docs | Job thresholds & capacities in `src/constants.js` |
| Deploy | Pages workflow builds runtime from upstream + patches |

## How the runtime is built

`src/game.js` in git is a stub. On every push to `main`, Actions:

1. Fetches Chatdemo `index.html`
2. Extracts the module script
3. Applies v0.9 patches (pixel ratio, save button, shadow quality, menu hide)
4. Publishes `index.html` + `styles.css` + modules to GitHub Pages

## Controls

- Left joystick — drive / steer
- Right joystick (loader / excavator / crane) — boom / bucket / tools
- **LOAD / USE** — load, transfer, dump, accept contracts
- **MACHINE** — cycle equipment
- Yellow contract board — jobs
- **Save** — force local save

## Machines

1. D7 Dozer — grade
2. Wheel Loader — stockpile → truck
3. Dump Truck — haul / pave
4. Mobile Crane — bridge decks
5. Excavator — dig

## Layout

```
index.html                 # HUD + shell (v0.9 controls)
styles.css                 # extracted + mobile polish
src/main.js                # entry
src/constants.js           # documented thresholds
src/game.js                # stub; full file from CI
.github/workflows/pages.yml
```

## Local

```bash
# After a successful Actions run, download the Pages artifact,
# or re-run the Python build step from pages.yml against Chatdemo.
npx serve site
```

Three.js loads from jsDelivr on first run.

## License

Prototype — free to use and modify.
