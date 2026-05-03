const { spawnSync } = require('node:child_process');
const path = require('node:path');

const benchmarkScript = path.join(__dirname, 'benchmark.py');
const repeat = '100';

const jobs = [
  {
    tool: 'playwright',
    profile: 'baseline',
    command: 'npm run test:playwright:baseline'
  },
  {
    tool: 'playwright',
    profile: 'ui-heavy',
    command: 'npm run test:playwright:ui-heavy'
  },
  {
    tool: 'playwright',
    profile: 'cpu-heavy',
    command: 'npm run test:playwright:cpu-heavy'
  },
  {
    tool: 'playwright',
    profile: 'ram-heavy',
    command: 'npm run test:playwright:ram-heavy'
  },
  {
    tool: 'cypress',
    profile: 'baseline',
    command: 'npm run test:cypress:baseline'
  },
  {
    tool: 'cypress',
    profile: 'ui-heavy',
    command: 'npm run test:cypress:ui-heavy'
  },
  {
    tool: 'cypress',
    profile: 'cpu-heavy',
    command: 'npm run test:cypress:cpu-heavy'
  },
  {
    tool: 'cypress',
    profile: 'ram-heavy',
    command: 'npm run test:cypress:ram-heavy'
  }
];

for (const job of jobs) {
  console.log(`\n[benchmark:all] Starting ${job.tool}/${job.profile}...`);
  const result = spawnSync('python', [
    benchmarkScript,
    '--tool',
    job.tool,
    '--profile',
    job.profile,
    '--command',
    job.command,
    '--repeat',
    repeat
  ], {
    stdio: 'inherit',
    shell: false,
    env: process.env
  });

  const exitCode = result.status ?? 1;
  if (exitCode !== 0) {
    process.exit(exitCode);
  }
}
