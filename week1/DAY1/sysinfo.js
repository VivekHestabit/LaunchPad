import os from "os";
import { getDiskInfo } from "node-disk-info";
import { gateway4async } from "default-gateway";
import { exec } from "child_process";

async function main() {
  console.log("=== SYSTEM INFO ===");

  // Hostname
  console.log("Hostname:", os.hostname());

  // Disk space
  try {
    const disks = await getDiskInfo();
    const disk = disks[0]; // first mounted disk
    const freeGB = (disk.available / (1024 ** 3)).toFixed(2);
    console.log("Available Disk Space (GB):", freeGB);
  } catch (err) {
    console.error("Disk error:", err);
  }

  // Default Gateway
  try {
    const gw = await gateway4async();
    console.log("Default Gateway:", gw.gateway);
  } catch (err) {
    console.error("Gateway error:", err);
  }

  // Open ports (top 5)
  exec("lsof -i -P -n | grep LISTEN | head -5", (err, stdout) => {
    if (err) return console.error("Ports error:", err);
    console.log("Open Ports (top 5):\n", stdout);
  });

  // Logged-in users
  exec("sudo who | wc -l", (err, stdout) => {
    if (err) return console.error("Users error:", err);
    console.log("Logged-in users count:", stdout.trim());
  });
}

export { main };

// Auto-run if called directly (optional)
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
