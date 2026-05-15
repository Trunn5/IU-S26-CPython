#!/usr/bin/env node

function fibonacciIter(n) {
  const mod = 1000000007;
  let a = 0;
  let b = 1;
  for (let i = 0; i < n; i += 1) {
    const next = (a + b) % mod;
    a = b;
    b = next;
  }
  return a;
}

function primeCount(limit) {
  if (limit < 2) {
    return 0;
  }
  let count = 0;
  for (let n = 2; n <= limit; n += 1) {
    let isPrime = true;
    const root = Math.floor(Math.sqrt(n));
    for (let d = 2; d <= root; d += 1) {
      if (n % d === 0) {
        isPrime = false;
        break;
      }
    }
    if (isPrime) {
      count += 1;
    }
  }
  return count;
}

function matrixMul(size) {
  const a = Array.from({ length: size }, (_, i) =>
    Array.from({ length: size }, (_, j) => (i + j) % 10),
  );
  const b = Array.from({ length: size }, (_, i) =>
    Array.from({ length: size }, (_, j) => (i * j) % 7),
  );
  const c = Array.from({ length: size }, () => Array(size).fill(0));
  for (let i = 0; i < size; i += 1) {
    for (let k = 0; k < size; k += 1) {
      const aik = a[i][k];
      for (let j = 0; j < size; j += 1) {
        c[i][j] += aik * b[k][j];
      }
    }
  }
  return c[0][0];
}

function jsonRoundtrip(items) {
  const payload = [];
  for (let i = 0; i < items; i += 1) {
    payload.push({
      id: i,
      name: `user_${i}`,
      active: i % 2 === 0,
      score: i * 1.5,
      tags: [`tag_${i % 10}`, `group_${i % 5}`],
    });
  }
  const encoded = JSON.stringify(payload);
  const decoded = JSON.parse(encoded);
  return decoded.length;
}

const benchmarks = {
  fibonacci_iter: () => fibonacciIter(180000),
  prime_count: () => primeCount(20000),
  matrix_mul: () => matrixMul(120),
  json_roundtrip: () => jsonRoundtrip(20000),
};
let sink = 0;

function parseArg(name, defaultValue) {
  const fullName = `--${name}`;
  const idx = process.argv.indexOf(fullName);
  if (idx === -1 || idx + 1 >= process.argv.length) {
    return defaultValue;
  }
  return process.argv[idx + 1];
}

function runSingle(name, warmup, repeat) {
  const fn = benchmarks[name];
  if (!fn) {
    throw new Error(`Unknown benchmark: ${name}`);
  }

  for (let i = 0; i < warmup; i += 1) {
    sink ^= Number(fn()) | 0;
  }

  const times = [];
  const memories = [];
  for (let i = 0; i < repeat; i += 1) {
    const beforeMem = process.memoryUsage().heapUsed;
    const start = process.hrtime.bigint();
    sink ^= Number(fn()) | 0;
    const elapsedNs = process.hrtime.bigint() - start;
    const afterMem = process.memoryUsage().heapUsed;
    times.push(Number(elapsedNs) / 1e6);
    memories.push(Math.max(0, (afterMem - beforeMem) / 1024.0));
  }

  const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
  const avgMemory = memories.reduce((a, b) => a + b, 0) / memories.length;

  return {
    benchmark: name,
    time_ms: avgTime,
    memory_kb: avgMemory,
    sink,
  };
}

const benchmark = parseArg("benchmark", null);
const warmup = Number(parseArg("warmup", "5"));
const repeat = Number(parseArg("repeat", "7"));

if (!benchmark) {
  throw new Error("Missing --benchmark");
}

console.log(JSON.stringify(runSingle(benchmark, warmup, repeat)));
