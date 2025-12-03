import fs from "fs";
const path = "./logs/day1-sysmetrics.json";

const metrics = {
  cpuUsage: process.cpuUsage(),
  resourceUsage: process.resourceUsage(),
  timestamp: new Date().toISOString()
};

fs.writeFileSync(path, JSON.stringify(metrics, null, 2));

console.log("Metrics saved to", path);

export default metrics; 
