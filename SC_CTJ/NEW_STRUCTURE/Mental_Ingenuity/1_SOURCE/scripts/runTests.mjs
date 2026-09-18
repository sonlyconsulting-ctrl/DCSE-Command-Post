import { spawn } from "node:child_process";

function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: "inherit", shell: false });
    child.on("exit", (code) => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}`)));
  });
}

await run("npm", ["run", "build"]);
await run("npm", ["run", "build:test"]);
await run("npm", ["run", "test:production"]);

const preview = spawn("./node_modules/.bin/vite", ["preview", "--host", "127.0.0.1", "--port", "4173", "--outDir", "dist-test"], {
  stdio: "inherit",
  shell: false,
});

try {
  let ready = false;
  for (let i = 0; i < 60; i += 1) {
    try {
      const response = await fetch("http://127.0.0.1:4173");
      if (response.ok) { ready = true; break; }
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  if (!ready) throw new Error("test preview did not become ready");
  await run("npm", ["run", "test:e2e"]);
  await run("npm", ["run", "test:media"]);
  await run("npm", ["run", "brand-scan"]);
} finally {
  preview.kill("SIGTERM");
}
