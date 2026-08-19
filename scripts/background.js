/* ==========================================================================
   Animated graph-traversal background.

   Ported from the `Component extends DCLogic` class in the Claude Design
   canvas "Josh Beira - Portfolio v2.dc.html". The graph construction, the
   Dijkstra and BFS traversals and the reveal -> path -> hold -> fade phase
   machine are unchanged; only the React plumbing (props/setState/render)
   has been replaced with constructor options and direct DOM updates.
   ========================================================================== */

(function () {
  'use strict';

  var DEFAULTS = {
    graphMode: 'lattice',          // 'lattice' (dijkstra) | 'wavefront' (bfs)
    animationPresence: 30,         // 0-100, how present the graph is against the ground
    accent: '#7ED9C4'
  };

  var TAIL = 46;                   // segments kept "hot" behind the traversal head

  var NOTES = {
    lattice: 'bg: dijkstra, weighted lattice',
    wavefront: 'bg: breadth-first search'
  };

  function GraphBackground(canvas, options) {
    this.props = Object.assign({}, DEFAULTS, options || {});
    this.canvasEl = canvas;
    this.ctx = canvas.getContext('2d');
    this._mode = null;
    this.raf = 0;
    this.rzT = 0;

    this.motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    this.reduced = this.motionQuery.matches;

    this.tick = this.tick.bind(this);
    this.onResize = this.onResize.bind(this);
    this.onVisibility = this.onVisibility.bind(this);
    this.onMotionChange = this.onMotionChange.bind(this);
  }

  /* --- lifecycle ---------------------------------------------------------- */

  GraphBackground.prototype.start = function () {
    if (!this.ctx) return;
    this.resize();
    this.rebuild();
    this._sig = this.sig();
    this.last = performance.now();
    this.play();

    window.addEventListener('resize', this.onResize);
    document.addEventListener('visibilitychange', this.onVisibility);
    if (this.motionQuery.addEventListener) {
      this.motionQuery.addEventListener('change', this.onMotionChange);
    }
  };

  GraphBackground.prototype.play = function () {
    if (this.raf) return;
    this.last = performance.now();
    this.raf = requestAnimationFrame(this.tick);
  };

  GraphBackground.prototype.pause = function () {
    cancelAnimationFrame(this.raf);
    this.raf = 0;
  };

  GraphBackground.prototype.destroy = function () {
    clearTimeout(this.rzT);
    this.pause();
    window.removeEventListener('resize', this.onResize);
    document.removeEventListener('visibilitychange', this.onVisibility);
    if (this.motionQuery.removeEventListener) {
      this.motionQuery.removeEventListener('change', this.onMotionChange);
    }
  };

  // Mobile browsers fire resize when the address bar collapses; a width-only
  // guard keeps the traversal from restarting while the user scrolls.
  GraphBackground.prototype.onResize = function () {
    var self = this;
    if (!this.ctx) return;
    clearTimeout(this.rzT);
    this.rzT = setTimeout(function () {
      var prevW = self.w;
      self.resize();
      if (Math.abs(self.w - prevW) > 1) self.rebuild();
    }, 180);
  };

  // A backgrounded tab should not burn battery on a decoration.
  GraphBackground.prototype.onVisibility = function () {
    if (document.hidden) this.pause();
    else this.play();
  };

  GraphBackground.prototype.onMotionChange = function (e) {
    this.reduced = e.matches;
  };

  /* --- state -------------------------------------------------------------- */

  Object.defineProperty(GraphBackground.prototype, 'mode', {
    get: function () { return this._mode || this.props.graphMode || 'lattice'; }
  });

  Object.defineProperty(GraphBackground.prototype, 'presence', {
    get: function () {
      var p = this.props.animationPresence;
      return (p === undefined || p === null ? 30 : p) / 100;
    }
  });

  Object.defineProperty(GraphBackground.prototype, 'accent', {
    get: function () { return this.props.accent || '#7ED9C4'; }
  });

  GraphBackground.prototype.sig = function () {
    return [this.mode, this.presence, this.accent].join('|');
  };

  // Stands in for setState + componentDidUpdate: rebuild only when the
  // mode/presence/accent signature actually changed.
  GraphBackground.prototype.setMode = function (mode) {
    this._mode = mode;
    if (!this.ctx) return;
    var s = this.sig();
    if (s !== this._sig) { this._sig = s; this.rebuild(); }
  };

  GraphBackground.prototype.resize = function () {
    var c = this.canvasEl;
    if (!c || !this.ctx) return;
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    this.w = c.clientWidth || window.innerWidth;
    this.h = c.clientHeight || window.innerHeight;
    c.width = Math.round(this.w * dpr);
    c.height = Math.round(this.h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  GraphBackground.prototype.rebuild = function () {
    if (!this.ctx) return;
    var g = this.mode === 'wavefront' ? this.buildScatter() : this.buildLattice();
    this.nodes = g.nodes;
    this.edges = g.edges;
    var plan = this.mode === 'wavefront' ? this.bfs(g) : this.dijkstra(g);
    this.order = plan.order;
    this.path = plan.path || null;
    this.cursor = 0;
    this.pathCursor = 0;
    this.phase = 'reveal';
    this.phaseT = 0;
    this.alpha = 1;
  };

  /* --- graph construction ------------------------------------------------- */

  GraphBackground.prototype.buildScatter = function () {
    var step = this.w < 640 ? 62 : 82;
    var cols = Math.ceil(this.w / step) + 2;
    var rows = Math.ceil(this.h / step) + 2;
    var nodes = [], id = [];
    for (var r = 0; r < rows; r++) {
      id[r] = [];
      for (var c = 0; c < cols; c++) {
        id[r][c] = nodes.length;
        nodes.push({
          x: (c - 0.5) * step + (Math.random() - 0.5) * step * 0.78,
          y: (r - 0.5) * step + (Math.random() - 0.5) * step * 0.78
        });
      }
    }
    var edges = [], adj = nodes.map(function () { return []; });
    var link = function (a, b) {
      var n1 = nodes[a], n2 = nodes[b];
      var d = Math.hypot(n1.x - n2.x, n1.y - n2.y);
      if (d > step * 1.6) return;
      var e = edges.length;
      edges.push({ a: a, b: b, w: d });
      adj[a].push({ to: b, e: e, w: d });
      adj[b].push({ to: a, e: e, w: d });
    };
    for (var r2 = 0; r2 < rows; r2++) for (var c2 = 0; c2 < cols; c2++) {
      var a = id[r2][c2];
      if (c2 + 1 < cols) link(a, id[r2][c2 + 1]);
      if (r2 + 1 < rows) link(a, id[r2 + 1][c2]);
      if (r2 + 1 < rows && c2 + 1 < cols && Math.random() < 0.42) link(a, id[r2 + 1][c2 + 1]);
      if (r2 + 1 < rows && c2 > 0 && Math.random() < 0.42) link(a, id[r2 + 1][c2 - 1]);
    }
    return {
      nodes: nodes,
      edges: edges,
      adj: adj,
      start: this.nearest(nodes, this.w * (0.1 + Math.random() * 0.8), this.h * (0.1 + Math.random() * 0.8))
    };
  };

  GraphBackground.prototype.buildLattice = function () {
    var step = this.w < 640 ? 58 : 76;
    var cols = Math.ceil(this.w / step) + 2;
    var rows = Math.ceil(this.h / step) + 2;
    var nodes = [], id = [];
    for (var r = 0; r < rows; r++) {
      id[r] = [];
      for (var c = 0; c < cols; c++) {
        id[r][c] = nodes.length;
        nodes.push({
          x: (c - 0.5) * step + (Math.random() - 0.5) * 9,
          y: (r - 0.5) * step + (Math.random() - 0.5) * 9
        });
      }
    }
    var edges = [], adj = nodes.map(function () { return []; });
    var link = function (a, b) {
      var n1 = nodes[a], n2 = nodes[b];
      var w = Math.hypot(n1.x - n2.x, n1.y - n2.y) * (0.35 + Math.random() * 1.9);
      var e = edges.length;
      edges.push({ a: a, b: b, w: w });
      adj[a].push({ to: b, e: e, w: w });
      adj[b].push({ to: a, e: e, w: w });
    };
    for (var r2 = 0; r2 < rows; r2++) for (var c2 = 0; c2 < cols; c2++) {
      if (c2 + 1 < cols) link(id[r2][c2], id[r2][c2 + 1]);
      if (r2 + 1 < rows) link(id[r2][c2], id[r2 + 1][c2]);
    }
    var start = this.nearest(nodes, this.w * 0.04, this.h * (0.15 + Math.random() * 0.7));
    var goal = this.nearest(nodes, this.w * 0.96, this.h * (0.15 + Math.random() * 0.7));
    return { nodes: nodes, edges: edges, adj: adj, start: start, goal: goal };
  };

  GraphBackground.prototype.nearest = function (nodes, x, y) {
    var best = 0, bd = Infinity;
    for (var i = 0; i < nodes.length; i++) {
      var d = (nodes[i].x - x) * (nodes[i].x - x) + (nodes[i].y - y) * (nodes[i].y - y);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  };

  /* --- traversals --------------------------------------------------------- */

  GraphBackground.prototype.bfs = function (g) {
    var seen = new Uint8Array(g.nodes.length);
    var q = [g.start];
    var order = [{ e: -1, n: g.start }];
    seen[g.start] = 1;
    for (var i = 0; i < q.length; i++) {
      var cur = q[i];
      var nb = g.adj[cur].slice().sort(function () { return Math.random() - 0.5; });
      for (var k = 0; k < nb.length; k++) {
        if (!seen[nb[k].to]) {
          seen[nb[k].to] = 1;
          q.push(nb[k].to);
          order.push({ e: nb[k].e, n: nb[k].to });
        }
      }
    }
    return { order: order };
  };

  GraphBackground.prototype.dijkstra = function (g) {
    var n = g.nodes.length;
    var dist = new Float64Array(n).fill(Infinity);
    var done = new Uint8Array(n);
    var prevN = new Int32Array(n).fill(-1);
    var prevE = new Int32Array(n).fill(-1);
    dist[g.start] = 0;
    var order = [{ e: -1, n: g.start }];
    for (var it = 0; it < n; it++) {
      var u = -1, bd = Infinity;
      for (var i = 0; i < n; i++) if (!done[i] && dist[i] < bd) { bd = dist[i]; u = i; }
      if (u < 0) break;
      done[u] = 1;
      if (u !== g.start) order.push({ e: prevE[u], n: u });
      var nb = g.adj[u];
      for (var k = 0; k < nb.length; k++) {
        var v = nb[k].to, nd = dist[u] + nb[k].w;
        if (nd < dist[v]) { dist[v] = nd; prevN[v] = u; prevE[v] = nb[k].e; }
      }
    }
    var path = [];
    var cur = g.goal;
    while (cur >= 0 && cur !== g.start) {
      if (prevE[cur] < 0) break;
      path.push(prevE[cur]);
      cur = prevN[cur];
    }
    path.reverse();
    return { order: order, path: path };
  };

  /* --- drawing ------------------------------------------------------------ */

  GraphBackground.prototype.rgba = function (hex, a) {
    var h = String(hex).replace('#', '');
    var v = h.length === 3 ? h.split('').map(function (x) { return x + x; }).join('') : h;
    var n = parseInt(v, 16);
    return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
  };

  GraphBackground.prototype.tick = function (t) {
    this.raf = requestAnimationFrame(this.tick);
    var dt = Math.min(0.05, (t - this.last) / 1000);
    this.last = t;
    if (!this.ctx || !this.order) return;
    var speed = this.reduced ? this.order.length : 68;

    if (this.phase === 'reveal') {
      this.cursor += speed * dt;
      if (this.cursor >= this.order.length) {
        this.cursor = this.order.length;
        this.phase = this.path && this.path.length ? 'path' : 'hold';
        this.phaseT = 0;
      }
    } else if (this.phase === 'path') {
      this.pathCursor += 26 * dt;
      if (this.pathCursor >= this.path.length) {
        this.pathCursor = this.path.length;
        this.phase = 'hold';
        this.phaseT = 0;
      }
    } else if (this.phase === 'hold') {
      this.phaseT += dt;
      if (this.phaseT > 2.4) { this.phase = 'fade'; this.phaseT = 0; }
    } else {
      this.phaseT += dt;
      this.alpha = Math.max(0, 1 - this.phaseT / 1.5);
      if (this.phaseT > 1.6) { this.rebuild(); return; }
    }
    this.draw();
  };

  GraphBackground.prototype.draw = function () {
    var ctx = this.ctx, p = this.presence, A = this.alpha;
    var faint = (0.05 + 0.3 * p) * A;
    var hot = (0.2 + 0.7 * p) * A;
    var nodeA = (0.07 + 0.34 * p) * A;
    var ink = '233,228,217';
    var i, e, ed, a, b, k, nd;

    ctx.clearRect(0, 0, this.w, this.h);

    var cur = this.cursor;
    var lim = Math.min(this.order.length, Math.floor(cur));

    // settled edges
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(' + ink + ',' + faint + ')';
    ctx.beginPath();
    for (i = 0; i < lim; i++) {
      e = this.order[i].e;
      if (e < 0) continue;
      if (cur - i < TAIL) continue;
      ed = this.edges[e]; a = this.nodes[ed.a]; b = this.nodes[ed.b];
      ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
    }
    ctx.stroke();

    // hot tail behind the traversal head
    ctx.lineWidth = 1.25;
    for (i = Math.max(0, lim - TAIL); i < lim; i++) {
      e = this.order[i].e;
      if (e < 0) continue;
      k = 1 - (cur - i) / TAIL;
      ed = this.edges[e]; a = this.nodes[ed.a]; b = this.nodes[ed.b];
      ctx.strokeStyle = this.rgba(this.accent, hot * k * k);
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }

    // settled nodes
    ctx.fillStyle = 'rgba(' + ink + ',' + nodeA + ')';
    for (i = 0; i < lim; i++) {
      if (cur - i < TAIL) continue;
      nd = this.nodes[this.order[i].n];
      ctx.beginPath(); ctx.arc(nd.x, nd.y, 1.2, 0, 6.2832); ctx.fill();
    }

    // hot nodes
    for (i = Math.max(0, lim - TAIL); i < lim; i++) {
      k = 1 - (cur - i) / TAIL;
      nd = this.nodes[this.order[i].n];
      ctx.fillStyle = this.rgba(this.accent, Math.min(1, hot * (0.4 + k)));
      ctx.beginPath(); ctx.arc(nd.x, nd.y, 1.3 + 1.7 * k, 0, 6.2832); ctx.fill();
    }

    // shortest path (dijkstra mode only)
    if (this.path && this.pathCursor > 0) {
      var pl = Math.min(this.path.length, Math.floor(this.pathCursor));
      ctx.lineWidth = 1.75;
      ctx.lineCap = 'round';
      ctx.strokeStyle = this.rgba(this.accent, Math.min(0.9, (0.3 + 0.65 * p) * A));
      ctx.beginPath();
      for (i = 0; i < pl; i++) {
        ed = this.edges[this.path[i]]; a = this.nodes[ed.a]; b = this.nodes[ed.b];
        ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
      }
      ctx.stroke();
      ctx.lineWidth = 1;
    }
  };

  /* --- wiring ------------------------------------------------------------- */

  function init() {
    var canvas = document.getElementById('bg');
    if (!canvas || !canvas.getContext) return;

    var bg = new GraphBackground(canvas);
    var buttons = Array.prototype.slice.call(document.querySelectorAll('[data-bg-mode]'));
    var note = document.getElementById('bg-note');

    function sync() {
      var mode = bg.mode;
      buttons.forEach(function (btn) {
        var on = btn.getAttribute('data-bg-mode') === mode;
        btn.classList.toggle('is-on', on);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      if (note && NOTES[mode]) note.textContent = NOTES[mode];
    }

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        bg.setMode(btn.getAttribute('data-bg-mode'));
        sync();
      });
    });

    sync();
    bg.start();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
