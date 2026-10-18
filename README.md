# Field Ops 3D — Site Crew v0.9

Browser-first Three.js construction / field-operations simulator.

Improved modular fork of the Chatdemo Field Ops prototype.

**Play (after Pages deploy):** https://xz64uj777.github.io/FieldOps3D/

## What improved vs Chatdemo monolith

| Area | Change |
|------|--------|
| Structure | CSS extracted; ES modules (`src/main.js` → `src/game.js` + `src/constants.js`) |
| Mobile perf | Adaptive pixel ratio (1.5 on touch, 1.8 desktop) |
| Options | Shadow quality: Off / Low / High (persisted) |
| UX | Manual **Save** button; restart already confirms |
| Mobile chrome | Steer L/R + Lights hidden on narrow screens (still usable via joystick) |
| Docs | Documented job thresholds & capacities in `src/constants.js` |
| Deploy | Clean GitHub Pages workflow for static multi-file site |

Still a prototype. Gameplay logic remains in one module for stability; further splits (machines / jobs / controls) are straightforward next steps using the constants file.

## Controls

- Left joystick — drive / steer  
- Right joystick (loader / excavator / crane) — boom, bucket, tools  
- **LOAD / USE** — load aggregate, transfer to truck, dump at road, accept contracts  
- **MACHINE** — cycle equipment  
- Contract board (yellow) — accept / advance jobs  
- Progress auto-saves locally; use **Save** to force a write  

## Machines

1. D7 Dozer — grade road  
2. Wheel Loader — fill bucket from stockpile, dump into truck  
3. Dump Truck — haul aggregate, pave sections  
4. Mobile Crane — place bridge decks  
5. Excavator — foundation / flood-control dig  

## Repo layout

```
index.html          # shell + HUD markup
styles.css          # all UI styles
src/main.js         # entry
src/game.js         # runtime (Three.js scene, machines, jobs, controls)
src/constants.js    # shared thresholds for future refactors
.github/workflows/pages.yml
```

## Local run

Any static server from the repo root (modules require HTTP):

```bash
npx serve .
# or: python3 -m http.server 8080
```

Open the printed URL. Three.js loads from jsDelivr (network needed on first load).

## License

Prototype source — use and modify freely for your projects.
