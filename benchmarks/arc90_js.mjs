import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";
import vm from "node:vm";
import { pathToFileURL } from "node:url";


const environment = path.resolve(process.argv[2]);
const require = createRequire(pathToFileURL(path.join(environment, "package.json")));
const { JSDOM, VirtualConsole } = require("jsdom");
const sourcePath = path.join(environment, "readability.js");
const readabilityScript = new vm.Script(fs.readFileSync(sourcePath, "utf8"), {
  filename: sourcePath,
});

const virtualConsole = new VirtualConsole();
virtualConsole.on("jsdomError", error => {
  if (error.type !== "css parsing") {
    process.stderr.write(error.stack + "\n");
  }
});

const lines = readline.createInterface({ input: process.stdin });
for await (const line of lines) {
  let dom;
  try {
    const request = JSON.parse(line);
    dom = new JSDOM(request.source, {
      url: request.url,
      runScripts: "outside-only",
      virtualConsole,
    });
    const window = dom.window;
    window.readConvertLinksToFootnotes = false;
    window.readStyle = "style-novel";
    window.readSize = "size-medium";
    window.readMargin = "margin-wide";
    window.scrollTo = () => {};
    for (const stylesheet of window.document.styleSheets) {
      if (stylesheet.href === undefined) {
        Object.defineProperty(stylesheet, "href", { value: null });
      }
    }
    readabilityScript.runInContext(dom.getInternalVMContext());
    const article = window.document.querySelector("#readability-content");
    process.stdout.write(JSON.stringify({ content: article.innerHTML }) + "\n");
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: error.stack }) + "\n");
  } finally {
    dom?.window.close();
  }
}
