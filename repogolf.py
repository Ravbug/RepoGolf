from itertools import count
from pathlib import Path
import glob
import os
import json
import sys

outfile = Path('output.json')

fns = ""

def countFiles(path,extensions):
    files = (p.resolve() for p in Path(path).glob("**/*") if p.suffix in extensions)
    numfiles = 0
    totalSize = 0
    for f in files:
        numfiles+=1
        totalSize += os.path.getsize(f)
    return numfiles, totalSize

def addToRecord(name,count,size,extensions):
    data = ""
    with open(outfile,"r") as f:
        data = json.load(f)
    
    with open(outfile,"w") as f:
        data[name] = {"count":count,"size":size,"ext":", ".join(extensions)}
        json.dump(data,f)

def downloadGithub(name):
    os.system(f"curl -L \"https://github.com/{name}/archive/refs/heads/master.zip\" -o archive.zip && unzip archive.zip > /dev/null && rm archive.zip")

def simpleGithub(account,name,exts,branch="master"):
    downloadGithub(f"{account}/{name}")
    fcount, fsize = countFiles(f"{name}-{branch}",exts)
    os.system(f"rm -rf {name}-{branch}")
    addToRecord(name,fcount,fsize,exts)


# ================================= Sizing functions ==========================================


def doRavEngine():
    simpleGithub("Ravbug","RavEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake"})

def doGodot():
    simpleGithub("godotengine","godot",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh"})

def doRust():
    simpleGithub("rust-lang","rust",{".sh",".rs",".rust",".toml"})

def doWebkit():
    simpleGithub("WebKit","WebKit",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl"},"main")

def doUE5():
    simpleGithub("EpicGames","UnrealEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".metal"},"release")

def doLinux():
    os.system("curl \"https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.9.tar.xz\" -o archive.xz && unxz -v archive.xz && tar xvf archive")
    exts = {".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".asm", "makefile"}
    fcount, fsize = countFiles("linux-5.16.9",exts)
    addToRecord("linux",fcount,fsize,exts)
    os.system(f"rm -rf archive linux-5.16.9")

# create output file if it does not exist
if not outfile.exists():
    with open(outfile,"w+") as f:
        outfile.write_text("{}")

def doAll():
    for fn in fns.values():
        fn()

fns = {
    "RavEngine" : doRavEngine,
    "Godot" : doGodot,
    "Rust" : doRust,
    "WebKit" : doWebkit,
    #"Unreal" : doUE5,
    "Linux" : doLinux,
    "all" : doAll
}
fn = ""
try:
    fn = fns[sys.argv[1]]
except KeyError:
    print(f"{sys.argv[1]}: not a known codebase. Known codebases:")
    for name in fns:
        print(name)
    exit(1)

fn()
