'use strict';
const fs = require('fs');
const path = require('path');

// Local checkpoint store. Monday is the source of truth for STATUS; this file holds
// per-item pipeline checkpoints (so a crashed run resumes) and the rolling fingerprint
// list the structural-variation gate compares against.
class Store {
  constructor(dir) {
    this.dir = dir;
    this.file = path.join(dir, 'state.json');
    this.data = { items: {}, fingerprints: [], lastRun: null };
    this._load();
  }
  _load() {
    try { this.data = JSON.parse(fs.readFileSync(this.file, 'utf8')); }
    catch { /* fresh */ }
    if (!this.data.items) this.data.items = {};
    if (!this.data.fingerprints) this.data.fingerprints = [];
  }
  save() {
    fs.mkdirSync(this.dir, { recursive: true });
    fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2));
  }
  item(id) {
    if (!this.data.items[id]) this.data.items[id] = { id, stage: 'new', checkpoints: {} };
    return this.data.items[id];
  }
  setStage(id, stage, payload) {
    const it = this.item(id);
    it.stage = stage;
    if (payload) it.checkpoints[stage] = payload;
    return it;
  }
  clearItem(id) { delete this.data.items[id]; }
  // rolling window of the last N draft fingerprints (for the variation gate)
  recentFingerprints(n = 25) { return this.data.fingerprints.slice(-n); }
  pushFingerprint(fp) {
    this.data.fingerprints.push(fp);
    if (this.data.fingerprints.length > 200) this.data.fingerprints = this.data.fingerprints.slice(-200);
  }
}

module.exports = { Store };
