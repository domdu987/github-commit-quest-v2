// Regenerate mapsdata.js (only needed to add countries or change the box):
//   mkdir geo-nm && cd geo-nm && npm init -y && npm i world-atlas@2.0.2 topojson-client@3.1.0 d3-geo@3.1.1 && cd ..
//   GEO_NM=$PWD/geo-nm node make_mapsdata.mjs
// Emit maps-data.js: Thailand + neighbours as SVG paths (Natural Earth 1:50m via world-atlas), plus the Mercator constants
// so lon/lat can be projected at runtime the same way.
import { createRequire } from "module";
import fs from "fs";
const NM = "" + (process.env.GEO_NM || "./geo-nm") + "";
const require = createRequire(NM + "/package.json");
const topo = require("topojson-client");
const d3 = await import(NM + "/node_modules/d3-geo/src/index.js");
const world = JSON.parse(fs.readFileSync(NM + "/node_modules/world-atlas/countries-50m.json", "utf8"));
const fc = topo.feature(world, world.objects.countries);
const pick = (id) => fc.features.find((f) => f.id === id);
const TH = pick("764");
const W = 900, H = 1300;
const proj = d3.geoMercator().fitExtent([[70, 50], [W - 70, H - 50]], TH);
const path = d3.geoPath(proj).digits(1);
const nb = {};
for (const [k, id] of Object.entries({ laos: "418", cambodia: "116", myanmar: "104", malaysia: "458", vietnam: "704", china: "156" })) nb[k] = path(pick(id));
const [tx, ty] = proj.translate(), k = proj.scale();
const merc = (lon, lat) => { const l = lon * Math.PI / 180, p = lat * Math.PI / 180; return [tx + k * l, ty - k * Math.log(Math.tan(Math.PI / 4 + p / 2))]; };
console.log("check bkk", proj([100.52, 13.75]), merc(100.52, 13.75));
const js = "// Generated from Natural Earth 1:50m (public domain) via world-atlas 2.0.2: Thailand and neighbours, Mercator in a 900x1300 box.\n" +
  "window.MAPDATA = window.MAPDATA || {};\nwindow.MAPDATA.th = " + JSON.stringify({ W, H, k: +k.toFixed(4), tx: +tx.toFixed(3), ty: +ty.toFixed(3), th: path(TH), nb }) + ";\n";
fs.writeFileSync("mapsdata.js", js);
console.log("bytes", js.length);
