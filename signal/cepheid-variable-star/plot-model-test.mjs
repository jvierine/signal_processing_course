import assert from "node:assert/strict";
import { tilePeriodicModel } from "./plot-model.js";

const result = tilePeriodicModel([2.5, 8.5], [0, 1, 2, 3, 4], [0, 10, 20, 30, 40], 4);
assert.deepEqual(result.time, [3, 4, 5, 6, 7, 8]);
assert.deepEqual(result.value, [30, 0, 10, 20, 30, 0]);

const bounded = tilePeriodicModel([0, 100], [0, 0.5, 1], [0, 1, 0], 1, 30);
assert.ok(bounded.time.length <= 30);
assert.equal(tilePeriodicModel([], [0, 1], [0, 1], 1).time.length, 0);

console.log("Cepheid periodic-model plotting tests passed");
