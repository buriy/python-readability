import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";
import { pathToFileURL } from "node:url";


const environment = path.resolve(process.argv[2]);
const require = createRequire(pathToFileURL(path.join(environment, "package.json")));
const { parseHTML } = require("linkedom");
const modulePath = path.join(environment, "node_modules", "defuddle", "dist", "node.js");
const { Defuddle } = await import(pathToFileURL(modulePath));

const lines = readline.createInterface({ input: process.stdin });
for await (const line of lines) {
  try {
    const request = JSON.parse(line);
    const { document } = parseHTML(request.source);
    const result = await Defuddle(document, request.url, { useAsync: false });
    process.stdout.write(JSON.stringify({ content: result.content }) + "\n");
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: error.stack }) + "\n");
  }
}
