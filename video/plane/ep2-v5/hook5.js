      // B0 frame 0 = EP.1 v4b's last place: the ทะเลลด beach at eerie dusk, the smoke behind the far karst (820, 650); คิว big in front, pointing at it
      add("hook", { set: "tideBeach", setOpts: { id: "h0", view: "sea", time: "eerie", sea: 0, boats: 0, fish: 0, people: 0, seed: 7 }, dark: 0.02, light: { from: "left", rim: "#ffc890", rimOp: 0.9, shade: "#141a2a", shadeOp: 0.25, cast: { len: 0.6, op: 0.3 }, vol: false },
        grade: { top: "#ff8a5a", bottom: "#2a2050", op: 0.18 }, blur: { fg: 6 },
        cam: { keys: [{ t: 0, ...fr(640, 1000, 1.15, 540, 900) }, { t: D("hook"), glide: D("hook"), ...fr(680, 960, 1.24, 540, 900) }] }, captions: caps("hook"),
        actors: [A("kiw", 420, 1500, 1.6, [T("idle", "wide", "o"), T("cock", "wide", "o", 0.5), T("pointF", "wide", "o", 0.72)])],
        fx(tl, id, t0, L) { Tide.sea(tl, "h0", t0, D("hook"), {});
          put(L.sky, `<linearGradient id="h0-dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a6a"/><stop offset=".6" stop-color="#c87a6a"/><stop offset="1" stop-color="#f2b080"/></linearGradient><rect x="-2000" y="-1400" width="5200" height="2050" fill="url(#h0-dk)"/><circle cx="260" cy="640" r="260" fill="#fff0c8" opacity=".35"/><circle cx="260" cy="640" r="66" fill="#fff6e0"/>`);
          put(L.sky, `${Isle.plume("h0p", 830, 655, 620, { lean: 0.32, sunX: 260, n: 20 })}<g>${Plane.puffMk("h0c", 820, 650, 14, "dark", 70)}</g><circle cx="830" cy="655" r="40" fill="#ff7a2a" opacity=".8" filter="url(#plBlur14)"/>`);
          Plane.puffs(tl, "h0c", t0 - 3, D("hook") + 3.5, 14, { dx: 80, dy: -560, per: 2.0, op: 0.95 }); life(tl, t0, D("hook")); } });
