import fs from 'node:fs';
import * as PELibrary from 'pe-library';
import * as ResEdit from 'resedit';

const [inputPath, outputPath, version] = process.argv.slice(2);
if (!inputPath || !outputPath || !/^\d+\.\d+\.\d+$/.test(version || '')) {
  throw new Error('Usage: node update-version.mjs INPUT.exe OUTPUT.exe X.Y.Z');
}
const [major, minor, patch] = version.split('.').map(Number);
const exe = PELibrary.NtExecutable.from(fs.readFileSync(inputPath));
const resources = PELibrary.NtExecutableResource.from(exe);
const versions = ResEdit.Resource.VersionInfo.fromEntries(resources.entries);
if (versions.length !== 1) throw new Error(`Expected one VERSIONINFO resource, got ${versions.length}`);
const info = versions[0];
info.setFileVersion(major, minor, patch, 0, 1033);
info.setProductVersion(major, minor, patch, 0, 1033);
info.setStringValues(
  { lang: 1033, codepage: 1200 },
  {
    FileDescription: 'Автономный справочник и конструктор цепочек аудиоплагинов',
    ProductName: 'Plugin Navigator',
    InternalName: 'Plugin_Navigator_Full',
    OriginalFilename: `Plugin_Navigator_Full_v${version}_Windows_x64.exe`,
    SpecialBuild: `Plugin_Navigator_Full v${version}`,
  },
);
info.outputToResourceEntries(resources.entries);
resources.outputResource(exe);
fs.writeFileSync(outputPath, Buffer.from(exe.generate()));
