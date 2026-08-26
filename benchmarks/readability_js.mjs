import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";
import { pathToFileURL } from "node:url";


const environment = path.resolve(process.argv[2]);
const require = createRequire(pathToFileURL(path.join(environment, "package.json")));
const { Readability } = require("@mozilla/readability");
const { JSDOM, VirtualConsole } = require("jsdom");

const virtualConsole = new VirtualConsole();
virtualConsole.on("jsdomError", error => {
  if (error.type !== "css parsing") {
    process.stderr.write(error.stack + "\n");
  }
});

const lines = readline.createInterface({ input: process.stdin });
for await (const line of lines) {
  try {
    const request = JSON.parse(line);
    const dom = new JSDOM(request.source, {
      url: request.url,
      virtualConsole,
    });
    const article = new Readability(dom.window.document).parse();
    process.stdout.write(JSON.stringify({ content: article.content }) + "\n");
    dom.window.close();
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: error.stack }) + "\n");
  }
}
