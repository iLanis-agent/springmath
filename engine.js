// Spring Math engine: straight-line (ideal) spring arithmetic. Force at a compression, stored energy, compression for a force, and two springs combined. Exact integers on tenths, results rounded half up.
function _t(t, err, lo, hi) { // decimal text with at most one place -> tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,5})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _RATE = "the spring rate must be from 0.1 to 1000 N/mm with at most one decimal place";
var _RATE2 = "the second spring rate must be from 0.1 to 1000 N/mm with at most one decimal place";
var _MM = "the compression must be from 0.1 to 1000 mm with at most one decimal place";
var _FORCE = "the force must be from 0.1 to 10000 N with at most one decimal place";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _k(t) { return _t(t, _RATE, 1, 10000); }
function _x(t) { return _t(t, _MM, 1, 10000); }

function forceTruth(rate, mm) {
  var k = _k(rate), x = _x(mm);
  return "A spring rated " + _dec(k, 1) + " N/mm pushes back with " + _dec(k * x, 2) + " N when it is compressed " + _dec(x, 1) + " mm.";
}
function energyTruth(rate, mm) {
  var k = _k(rate), x = _x(mm);
  return "Compressed " + _dec(x, 1) + " mm, a spring rated " + _dec(k, 1) + " N/mm stores " + _dec(_hu(k * x * x, 20), 2) + " mJ.";
}
function travelTruth(rate, force) {
  var k = _k(rate), f = _t(force, _FORCE, 1, 100000);
  return "To push back with " + _dec(f, 1) + " N, a spring rated " + _dec(k, 1) + " N/mm is compressed " + _dec(_hu(f * 100, k), 2) + " mm.";
}
function pairTruth(rate, rate2) {
  var a = _k(rate), b = _t(rate2, _RATE2, 1, 10000);
  return "Two springs rated " + _dec(a, 1) + " and " + _dec(b, 1) + " N/mm add up to " + _dec(a + b, 1) + " N/mm side by side, and give " + _dec(_hu(a * b * 10, a + b), 2) + " N/mm end to end.";
}
