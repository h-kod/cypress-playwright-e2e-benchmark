const { spawn, spawnSync } = require('node:child_process');
const path = require('node:path');

delete process.env.ELECTRON_RUN_AS_NODE;

function waitForServer(url, timeoutMs = 30000) {
  const startedAt = Date.now();

  return new Promise((resolve, reject) => {
    const probe = async () => {
      try {
        const response = await fetch(url, { method: 'GET' });
        if (response.ok) {
          resolve();
          return;
        }
      } catch (error) {
        // Keep retrying until the server is ready or the timeout is hit.
      }

      if (Date.now() - startedAt >= timeoutMs) {
        reject(new Error(`Timed out waiting for ${url}`));
        return;
      }

      setTimeout(probe, 500);
    };

    probe();
  });
}

async function main() {
  const serverScript = path.join(__dirname, 'static-server.js');
  const serverProcess = spawn(process.execPath, [serverScript], {
    stdio: 'ignore',
    shell: false,
    env: process.env
  });

  const shutdownServer = () => {
    if (!serverProcess.killed) {
      serverProcess.kill();
    }
  };

  process.on('exit', shutdownServer);
  process.on('SIGINT', () => {
    shutdownServer();
    process.exit(130);
  });
  process.on('SIGTERM', () => {
    shutdownServer();
    process.exit(143);
  });

  try {
    await waitForServer('http://127.0.0.1:5500/');

    const result = process.platform === 'win32'
      ? spawnSync('cmd.exe', ['/d', '/s', '/c', 'npx cypress run --browser electron'], {
          stdio: 'inherit',
          shell: false,
          env: process.env
        })
      : spawnSync('npx', ['cypress', 'run', '--browser', 'electron'], {
          stdio: 'inherit',
          shell: false,
          env: process.env
        });

    process.exitCode = result.status ?? 1;
  } finally {
    shutdownServer();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
