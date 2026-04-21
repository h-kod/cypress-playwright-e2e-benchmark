const { spawnSync } = require('node:child_process');

delete process.env.ELECTRON_RUN_AS_NODE;

const result = spawnSync('npx', ['cypress', 'run', '--browser', 'electron'], {
  stdio: 'inherit',
  shell: true,
  env: process.env
});

process.exit(result.status ?? 1);
