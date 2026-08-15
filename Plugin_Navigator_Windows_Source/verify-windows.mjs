import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import * as asar from '@electron/asar';
import * as PELibrary from 'pe-library';
import * as ResEdit from 'resedit';

const [exePath, htmlPath, version] = process.argv.slice(2);
if (!exePath || !htmlPath || !version) throw new Error('Usage: node verify-windows.mjs APP.exe APP.html X.Y.Z');
const binary = fs.readFileSync(exePath);
const exe = PELibrary.NtExecutable.from(binary);
const resources = PELibrary.NtExecutableResource.from(exe);
const payload = resources.entries.find(entry => entry.type === 10 && entry.id === 'NEUTRALINOJS_RESOURCES_NEU');
if (!payload) throw new Error('Embedded NEUTRALINOJS_RESOURCES_NEU was not found');
const temp = path.join(os.tmpdir(), `plugin-navigator-${process.pid}.neu`);
try {
  fs.writeFileSync(temp, Buffer.from(payload.bin));
  const embedded = asar.extractFile(temp, 'resources/index.html');
  const expected = fs.readFileSync(htmlPath);
  if (!Buffer.from(embedded).equals(expected)) throw new Error('Embedded HTML differs from release HTML');
  const config = JSON.parse(Buffer.from(asar.extractFile(temp, 'neutralino.config.json')).toString('utf8'));
  if (config.version !== version) throw new Error(`Embedded config version is ${config.version}, expected ${version}`);
  if (config.applicationName !== 'Plugin Navigator' || config.defaultMode !== 'window') {
    throw new Error('Embedded config does not start Plugin Navigator in window mode');
  }
  if (config.documentRoot !== '/resources/' || config.url !== '/' || config.enableServer !== true) {
    throw new Error('Embedded config points to the wrong document root');
  }
} finally {
  fs.rmSync(temp, { force: true });
}
const versions = ResEdit.Resource.VersionInfo.fromEntries(resources.entries);
if (versions.length !== 1) throw new Error('VERSIONINFO verification failed');
const strings = versions[0].getStringValues({ lang: 1033, codepage: 1200 });
if (strings.ProductVersion !== `${version}.0` || strings.FileVersion !== `${version}.0`) {
  throw new Error(`Wrong Windows metadata: ${strings.FileVersion} / ${strings.ProductVersion}`);
}
console.log(JSON.stringify({ status: 'PASS', version, embeddedConfig: true, documentRoot: '/resources/', embeddedBytes: fs.statSync(htmlPath).size }));
