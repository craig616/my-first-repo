/* ---------- Sound: small, warm, synthesised cues (original, inspired by the feel of deduction games) ---------- */
let ctx = null, on = true, master = null;
function audio() {
  if (!on) return null;
  if (!ctx) {
    const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
    ctx = new AC(); master = ctx.createGain(); master.gain.value = 0.55;
    // A soft echo gives the sounds a little room, like a quiet study.
    const d = ctx.createDelay(); d.delayTime.value = 0.13; const fb = ctx.createGain(); fb.gain.value = 0.22; const wet = ctx.createGain(); wet.gain.value = 0.25;
    master.connect(ctx.destination); master.connect(d); d.connect(fb); fb.connect(d); d.connect(wet); wet.connect(ctx.destination);
  }
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}
function tone(freq, t0, dur, type = 'sine', vol = 0.3, bend = 0) {
  const c = audio(); if (!c) return;
  const o = c.createOscillator(), g = c.createGain();
  o.type = type; o.frequency.setValueAtTime(freq, c.currentTime + t0);
  if (bend) o.frequency.exponentialRampToValueAtTime(freq * bend, c.currentTime + t0 + dur);
  g.gain.setValueAtTime(0.0001, c.currentTime + t0);
  g.gain.exponentialRampToValueAtTime(vol, c.currentTime + t0 + 0.008);
  g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + t0 + dur);
  o.connect(g); g.connect(master); o.start(c.currentTime + t0); o.stop(c.currentTime + t0 + dur + 0.02);
}
function noise(t0, dur, freq, vol = 0.25, q = 1.2) {
  const c = audio(); if (!c) return;
  const len = Math.max(1, Math.floor(c.sampleRate * dur)), buf = c.createBuffer(1, len, c.sampleRate), data = buf.getChannelData(0);
  for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 3);
  const s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain();
  s.buffer = buf; f.type = 'bandpass'; f.frequency.value = freq; f.Q.value = q; g.gain.value = vol;
  s.connect(f); f.connect(g); g.connect(master); s.start(c.currentTime + t0);
}
// A sustained sine "bell" with optional pitch scoop, slow attack, held body and gentle tremolo.
function bell(freq, t0, dur, vol = 0.1, o = {}) {
  const c = audio(); if (!c) return;
  const t = c.currentTime + t0, osc = c.createOscillator(), g = c.createGain();
  osc.frequency.setValueAtTime(freq * (o.scoop || 1), t);
  if (o.scoop) osc.frequency.exponentialRampToValueAtTime(freq, t + 0.015);
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(vol, t + (o.attack || 0.006));
  if (o.hold) g.gain.exponentialRampToValueAtTime(vol * 0.5, t + o.hold);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  let out = g;
  if (o.trem) {
    const lfo = c.createOscillator(), depth = c.createGain(); out = c.createGain();
    lfo.frequency.value = o.trem; depth.gain.value = 0.3; out.gain.value = 0.7;
    lfo.connect(depth); depth.connect(out.gain); g.connect(out); lfo.start(t); lfo.stop(t + dur + 0.05);
  }
  osc.connect(g); out.connect(master); osc.start(t); osc.stop(t + dur + 0.05);
}
const sfx = {
  // select a blank: soft "pop" — tiny click plus a fast falling glide (~1.7 kHz to ~340 Hz in 70 ms)
  open()  { noise(0, 0.018, 3000, 0.10, 0.7); tone(1700, 0, 0.07, 'sine', 0.07, 0.2); },
  // place a word: a faint high tick and a small, lower seated pop (slightly varied each time)
  place() { const p = 0.96 + Math.random() * 0.08;
            noise(0, 0.012, 6500 * p, 0.06, 1.0); tone(900 * p, 0, 0.05, 'sine', 0.08, 0.45); tone(330 * p, 0.004, 0.09, 'triangle', 0.07, 0.9); },
  // swap a word: the pop in reverse, a short rising glide as the word lifts out
  lift()  { noise(0, 0.012, 2400, 0.05, 0.8); tone(380, 0, 0.06, 'sine', 0.06, 2.8); },
  // story complete: like a "correct" cue — strike click, bright ~1.2 kHz ping, then a warm B4 body that swells and shimmers
  ready() { noise(0, 0.02, 4000, 0.07, 0.6);
            bell(1200, 0, 0.9, 0.045, { scoop: 0.93 }); bell(950, 0.12, 0.35, 0.022);
            bell(493.88, 0, 1.2, 0.11, { attack: 0.08, hold: 0.4, trem: 11 }); bell(987.77, 0, 0.5, 0.03, { attack: 0.06 }); },
  // saved: a short, soft version of the solved fanfare — same ping, then a rolled E minor chord with tremolo and a high glint (~1.4 s)
  save()  { noise(0, 0.02, 4000, 0.06, 0.6);
            bell(1200, 0, 1.0, 0.04, { scoop: 0.93 }); bell(844, 0, 0.6, 0.03);
            [329.63, 392, 493.88].forEach((f, i) => bell(f, 0.06 + i * 0.07, 1.35 - i * 0.07, 0.07, { attack: 0.12, hold: 0.6, trem: 9 }));
            bell(1568, 0.25, 0.8, 0.014); },
  toggle(onNow) { tone(onNow ? 880 : 440, 0, 0.08, 'sine', 0.08); }
};
