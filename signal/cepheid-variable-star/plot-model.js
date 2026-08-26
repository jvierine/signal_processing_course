export function tilePeriodicModel(rawTimes, modelTimes, modelValues, period, maxPoints = 12000) {
  if (!rawTimes.length || modelTimes.length < 2 || modelTimes.length !== modelValues.length || !(period > 0)) {
    return { time: [], value: [] };
  }

  const start = Math.min(...rawTimes);
  const end = Math.max(...rawTimes);
  const firstCycle = Math.floor((start - modelTimes[0]) / period);
  const lastCycle = Math.ceil((end - modelTimes[0]) / period);
  const closesPeriod = Math.abs(modelTimes[modelTimes.length - 1] - modelTimes[0] - period) < period * 1e-9;
  const sampleCount = closesPeriod ? modelTimes.length - 1 : modelTimes.length;
  const time = [];
  const value = [];

  for (let cycle = firstCycle; cycle <= lastCycle; cycle += 1) {
    for (let index = 0; index < sampleCount; index += 1) {
      const repeatedTime = cycle * period + modelTimes[index];
      if (repeatedTime < start || repeatedTime > end) continue;
      time.push(repeatedTime);
      value.push(modelValues[index]);
    }
  }
  if (time.length > maxPoints) {
    const stride = Math.ceil(time.length / maxPoints);
    return {
      time: time.filter((_, index) => index % stride === 0),
      value: value.filter((_, index) => index % stride === 0),
    };
  }
  return { time, value };
}
