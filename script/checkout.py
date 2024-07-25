#! /usr/bin/env python3

import common, os, re, subprocess, sys, zipfile
import platform

def zip_dir(path, output=None):
    output = output or os.path.basename(path) + '.zip'
    zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(path):
        relative_root = '' if root == path else root.replace(path, '') + os.sep
        for filename in files:
            zip.write(os.path.join(root, filename), relative_root + filename)
    zip.close()


def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

  version = common.version()

  parser = common.create_parser(True)
  args = parser.parse_args()

  # Clone depot_tools
  if not os.path.exists("depot_tools"):
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "depot_tools"])

  # Clone Skia
  match = re.match('(m\\d+)(?:-([0-9a-f]+)(?:-([1-9][0-9]*))?)?', args.version)
  if not match:
    raise Exception('Expected --version "m<ver>-<sha>", got "' + args.version + '"')

  commit = match.group(2)
  iteration = match.group(3)

  if os.path.exists("skia"):
    print("> Fetching")
    os.chdir("skia")
    subprocess.check_call(["git", "reset", "--hard"])
    subprocess.check_call(["git", "clean", "-d", "-f"])
    subprocess.check_call(["git", "fetch", "origin"])
  else:
    print("> Cloning")
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://github.com/google/skia.git", "--quiet"])
    os.chdir("skia")
    subprocess.check_call(["git", "fetch", "origin"])

  # Checkout commit
  print("> Checking out", commit)
  subprocess.check_call(["git", "-c", "advice.detachedHead=false", "checkout", commit])

  # git deps
  print("> Running tools/git-sync-deps")
  if 'windows' == common.host():
    env = os.environ.copy()
    env['PYTHONHTTPSVERIFY']='0'
    subprocess.check_call(["python3", "tools/git-sync-deps"], env=env)
  else:
    subprocess.check_call(["python3", "tools/git-sync-deps"])

  # fetch ninja
  print("> Fetching ninja")
  subprocess.check_call(["python3", "bin/fetch-ninja"])

  if 'Linux' == platform.system():
    dist = 'Skia-' + version + '-' + 'src' + '.zip'
    print('> Writing', dist)

    skia_path = os.getcwd()
    print('> Creating', skia_path)
    os.chdir(os.pardir)
    zip_dir(skia_path, dist)
    os.chdir("skia")
  
  return 0

if __name__ == '__main__':
  sys.exit(main())
