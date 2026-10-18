#!/usr/bin/env python3
"""Build site/ from Chatdemo upstream + v0.9 patches."""
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITE_SRC = SITE / "src"


def main() -> None:
    SITE_SRC.mkdir(parents=True, exist_ok=True)

    # Copy local shell assets
    (SITE / "styles.css").write_text((ROOT / "styles.css").read_text(encoding="utf-8"), encoding="utf-8")
    (SITE_SRC / "main.js").write_text((ROOT / "src" / "main.js").read_text(encoding="utf-8"), encoding="utf-8")
    (SITE_SRC / "constants.js").write_text((ROOT / "src" / "constants.js").read_text(encoding="utf-8"), encoding="utf-8")
    (SITE / "index.html").write_text((ROOT / "index.html").read_text(encoding="utf-8"), encoding="utf-8")

    url = "https://raw.githubusercontent.com/xz64uj777/Chatdemo/main/index.html"
    html = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")

    script_m = re.search(r'<script type="module">([\s\S]*?)</script>', html)
    if not script_m:
        raise SystemExit("Could not find <script type=module> in Chatdemo index.html")
    script = script_m.group(1)

    # Drop trailing non-module script / HTML if present inside the capture
    if "</script>" in script:
        script = script.split("</script>")[0]

    # Adaptive pixel ratio
    old_pr = "renderer.setPixelRatio(Math.min(devicePixelRatio,1.8));"
    new_pr = (
        "const MAX_PR=window.matchMedia('(pointer:coarse)').matches?1.5:1.8;"
        "renderer.setPixelRatio(Math.min(devicePixelRatio,MAX_PR));"
    )
    if old_pr in script:
        script = script.replace(old_pr, new_pr)

    # Manual save button hook
    restart = (
        "$('restart').onclick=()=>{if(!confirm('Restart construction from the beginning? "
        "This resets all contract objectives, vehicle positions and loads, money, fuel, and "
        "saved site progress on this device.'))return;try{localStorage.removeItem('fieldOps3dSave')}"
        "catch(e){}location.reload()};"
    )
    if "manualSave" not in script and restart in script:
        script = script.replace(
            restart,
            restart + "\nconst _ms=$('manualSave');if(_ms)_ms.onclick=()=>saveGame(false);",
        )

    # Shadow quality control
    if "setupShadowQuality" not in script:
        shadow = """
(function setupShadowQuality(){
  const sel=$('shadowQuality');
  if(!sel)return;
  const apply=()=>{
    const v=sel.value;
    if(v==='off'){renderer.shadowMap.enabled=false;sun.castShadow=false;}
    else if(v==='low'){renderer.shadowMap.enabled=true;sun.castShadow=true;sun.shadow.mapSize.set(512,512);}
    else{renderer.shadowMap.enabled=true;sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);}
    renderer.shadowMap.needsUpdate=true;
    try{localStorage.setItem('fieldOps3dShadow',v)}catch(e){}
  };
  try{const s=localStorage.getItem('fieldOps3dShadow');if(s)sel.value=s}catch(e){}
  sel.addEventListener('change',apply);apply();
})();
"""
        if "animate();" in script:
            script = script.replace("animate();", shadow + "\nanimate();", 1)
        else:
            script += shadow

    # Hide menus on start
    if "hideMenusOnStart" not in script:
        script += """
(function hideMenusOnStart(){
  const run = () => {
    ['machinePicker','optionsMenu','machineGuide'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.remove('open');
    });
    document.body.classList.add('panels-hidden');
    const hideButton = document.getElementById('panelHide');
    if (hideButton) hideButton.textContent = '+ SHOW MENUS';
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
"""

    out = SITE_SRC / "game.js"
    out.write_text(script, encoding="utf-8")
    print(f"Wrote {out} ({len(script)} bytes)")

    for needle, path in [
        ("three@0.160.0", out),
        ("Field Ops 3D", SITE / "index.html"),
        ("manualSave", SITE / "index.html"),
        ("shadowQuality", SITE / "index.html"),
    ]:
        text = path.read_text(encoding="utf-8")
        if needle not in text:
            raise SystemExit(f"Validation failed: {needle!r} missing in {path}")

    print("Build OK")


if __name__ == "__main__":
    main()
