import fs from 'fs/promises';
import { performance } from 'perf_hooks';

// Read command-line arguments
const args = process.argv.slice(2);
console.log('Arguments passed:', args);

async function processFile(filename) {
  const start = performance.now();
  const content = await fs.readFile(filename, 'utf-8');

  const lines = content.split('\n').length;
  const words = content.split(/\s+/).filter(Boolean).length;
  const chars = content.length;

  const end = performance.now();
  const memoryMB = process.memoryUsage().heapUsed / (1024 * 1024);

  return {
    file: filename,
    lines,
    words,
    chars,
    executionTimeMs: Math.round(end - start),
    memoryMB: parseFloat(memoryMB.toFixed(2)),
  };
}

const files = [];
const uniqueFiles = [];
for (let i = 0; i < args.length; i += 2) {
  const flag = args[i];
  const file = args[i + 1];
  if (['--lines', '--words', '--chars'].includes(flag)) {
    files.push(file);
  }
  if (flag === '--unique') {
    uniqueFiles.push(file);
  }
}

async function main() {
  const results = await Promise.all(files.map(processFile));
  console.log(results);

  // 2. Unique file processing
  const uniqueOutputs = await Promise.all(uniqueFiles.map(removeDuplicates));

  uniqueOutputs.forEach((path) => {
    console.log('Unique file written to:', path);
  });

  // 3. Save performance log
  const logData = {
    timestamp: new Date().toISOString(),
    stats: results,
    uniqueOutputs,
  };

  const logPath = `logs/performance-${Date.now()}.json`;
  await fs.writeFile(logPath, JSON.stringify(logData, null, 2));

  console.log('Performance log saved to:', logPath);
}

main();

async function removeDuplicates(filename) {
  const content = await fs.readFile(filename, 'utf-8');

  // Remove duplicate lines:
  const uniqueLines = [...new Set(content.split('\n'))].join('\n');

  // Ensure output folder exists
  await fs.mkdir('output', { recursive: true });

  // Write to output/unique-<filename>
  const outputPath = `output/unique-${filename}`;
  await fs.writeFile(outputPath, uniqueLines);

  return outputPath; // so we can log it
}
