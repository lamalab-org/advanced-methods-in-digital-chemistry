/* A three-point teaching example. No data or code is fetched from a server. */
(function (root) {
  'use strict';
  const inputs = [-1, 0, 1];
  const targets = [0.2, 1, 0.2];
  function kernel(x, z, gamma) { return Math.exp(-gamma * (x - z) ** 2); }
  function fit(gamma, alpha) {
    if (!(gamma > 0 && alpha > 0)) throw new Error('Positive gamma and alpha required');
    // Solve (K + alpha I)a = y with partial pivoting; alpha uses the
    // sum-of-squared-errors convention, as in sklearn.kernel_ridge.KernelRidge.
    const rows = inputs.map((x, i) => [
      ...inputs.map((z, j) => kernel(x, z, gamma) + (i === j ? alpha : 0)), targets[i]
    ]);
    for (let j = 0; j < 3; j++) {
      let pivot = j;
      for (let i = j + 1; i < 3; i++) if (Math.abs(rows[i][j]) > Math.abs(rows[pivot][j])) pivot = i;
      [rows[j], rows[pivot]] = [rows[pivot], rows[j]];
      const scale = rows[j][j];
      for (let k = j; k < 4; k++) rows[j][k] /= scale;
      for (let i = 0; i < 3; i++) {
        if (i === j) continue;
        const factor = rows[i][j];
        for (let k = j; k < 4; k++) rows[i][k] -= factor * rows[j][k];
      }
    }
    return rows.map(row => row[3]);
  }
  function contributions(x, gamma, weights) {
    return inputs.map((z, i) => weights[i] * kernel(x, z, gamma));
  }
  function predict(x, gamma, weights) {
    return contributions(x, gamma, weights).reduce((a, b) => a + b, 0);
  }
  const api = { inputs, targets, kernel, fit, contributions, predict };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.KernelExample = api;
})(globalThis);
