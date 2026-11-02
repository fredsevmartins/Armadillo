// Development-only syntax validation; dependencies are installed outside the project.
import { readFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

if (!process.argv[2]) throw new Error('Usage: node scripts/check_mermaid.mjs NODE_MODULES_DIRECTORY');
const modules = resolve(process.argv[2]);
const { JSDOM } = await import(pathToFileURL(resolve(modules, 'jsdom/lib/api.js')).href);
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import(pathToFileURL(resolve(modules, 'mermaid/dist/mermaid.core.mjs')).href);
mermaid.initialize({ startOnLoad: false });
const diagrams = resolve(dirname(fileURLToPath(import.meta.url)), '../docs/diagrams');
const names = readdirSync(diagrams).filter(name => name.endsWith('.mmd')).sort();
for (const name of names) {
  await mermaid.parse(readFileSync(resolve(diagrams, name), 'utf8'));
  process.stdout.write(`PASS ${name}\n`);
}
process.stdout.write(`PASS: ${names.length} Mermaid sources; syntax only, not browser rendering\n`);
