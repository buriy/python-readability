import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";
import { pathToFileURL } from "node:url";


process.noDeprecation = true;
const environment = path.resolve(process.argv[2]);
const require = createRequire(pathToFileURL(path.join(environment, "package.json")));
const Parser = require("@postlight/parser");

const lines = readline.createInterface({ input: process.stdin });
for await (const line of lines) {
  try {
    const request = JSON.parse(line);
    const result = await Parser.parse(request.url, {
      html: request.source,
      fetchAllPages: false,
    });
    process.stdout.write(JSON.stringify({ content: result.content }) + "\n");
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: error.stack }) + "\n");
  }
}
