#!python3

from itertools import count
from pathlib import Path
import glob
import os
import json
import sys
from datetime import date

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
        data[name] = {"count":count,"size":size,"ext":", ".join(extensions),"date":f"{date.today()}"}
        pretty_json = json.dumps(data, indent=4, sort_keys=True)
        outfile.write_text(pretty_json)

def downloadGithub(name):
    os.system(f"curl -L \"https://github.com/{name}/archive/refs/heads/master.zip\" -o archive.zip ; unzip archive.zip > /dev/null ; rm archive.zip")

def simpleDirectory(dir,exts,name,nameOverride=None):
    if not Path(f"{dir}").exists():
        raise RuntimeError(f"Directory {dir} not found, either due to download error or bug")
    fcount, fsize = countFiles(dir,exts)
    os.system(f"rm -rf {dir}")
    addToRecord(name if not nameOverride else nameOverride,fcount,fsize,exts)

def simpleGithub(account,name,exts,branch="master",nameOverride=None,dirOverride=None):
    downloadGithub(f"{account}/{name}")
    simpleDirectory(f"{name}-{branch}" if not dirOverride else dirOverride,exts,name,nameOverride)


def simpleNPM(name,exts,nameOverride=None):
    os.mkdir("npm")
    os.chdir("npm")
    os.system(f"npm install {name} --production=false")
    os.chdir("..")
    simpleDirectory("npm",exts,name,nameOverride)

# ================================= Sizing functions ==========================================


def doRavEngine():
    simpleGithub("Ravbug","RavEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".mm",".m"})

def doGodot():
    simpleGithub("godotengine","godot",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh"})

def doRust():
    simpleGithub("rust-lang","rust",{".sh",".rs",".rust",".toml"})

def doWebkit():
    simpleGithub("WebKit","WebKit",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl"},"main")

def doUE5():
    simpleGithub("EpicGames","UnrealEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".metal"},"release")

def doLinux():
    os.system("curl \"https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.9.tar.xz\" -o archive.xz && unxz -v archive.xz && tar xvf archive > /dev/null")
    simpleDirectory("linux-5.16.9",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".asm", "makefile"}, "linux")

def doLLVM():
    os.system("curl -L \"https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-14.0.0.zip\" -o archive.zip && unzip archive.zip > /dev/null && rm archive.zip")
    simpleDirectory("llvm-project-llvmorg-14.0.0",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".asm", "makefile", ".ll", ".py", "CMakeLists.txt"}, "llvm-project")

def doBlender():
    os.system("git clone https://git.blender.org/blender.git --depth=1")
    simpleDirectory("blender",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".metal"},"Blender")

def doGCC():
    os.system("git clone git://gcc.gnu.org/git/gcc.git --depth=1")
    simpleDirectory("gcc",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake", ".asm", "makefile", ".ads", ".py", ".go", ".d", ".m", ".mm" ,".s", ".S", ".f90", "CMakeLists.txt"},"gcc")

def doSwift():
    simpleGithub("apple","Swift",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".swift", ".m", ".mm"},"main")

def doChromeProjs():
    os.system("git -c core.deltaBaseCacheLimit=2g clone https://chromium.googlesource.com/chromium/src.git --depth=1 --recurse-submodules")
    simpleDirectory("src",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl",".metal"},"Chromium-All")
    simpleDirectory("src/chromeos",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl",".metal"},"ChromeOS")
    os.system("rm -rf src")

def doFirefox():
    os.system("hg clone https://hg.mozilla.org/mozilla-central/")
    simpleDirectory("mozilla-unified",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl",".metal"},"Firefox")
    os.system("rm -rf mozilla-unified")

def doDotnetRuntime():
    simpleGithub("dotnet","runtime",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".cs", ".csproj"},"main","DotNET-Runtime")

def doBoost():
    os.system("curl -L https://boostorg.jfrog.io/artifactory/main/release/1.79.0/source/boost_1_79_0.zip -o archive.zip && unzip archive.zip > /dev/null && rm archive.zip")
    simpleDirectory("boost_1_79_0",{".cpp",".hpp",".c",".h",".cmake"},"boost")
    os.system("rm -rf boost_1_79_0")

def doOpenJDK():
    simpleGithub("openjdk","jdk",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".java", ".m", ".mm"},nameOverride="OpenJDK")

def doQt6():
    os.system("git clone git://code.qt.io/qt/qt5.git --depth=1 && cd qt5 && git checkout dev && perl init-repository")  
    simpleDirectory("qt5",{".cpp",".hpp",".cxx", ".cc", ".c",".h",".cmake", ".java", ".cs", ".qml", ".js", ".in", ".m", ".mm", ".S", ".s", ".asm", ".f90", ".metal", ".vert", ".vs", ".frag", ".fs", ".hlsl", ".glsl"},"Qt 6")
    os.system("rm -rf qt5")

def doCPython():
    simpleGithub("python","cpython",{".c",".h",".cpp",".hpp",".py"},"main")

def doKotlin():
    simpleGithub("JetBrains","kotlin",{".c",".h",".cpp",".hpp",".kt",".java"})

def doZig():
    simpleGithub("ziglang","zig",{".c",".h",".cpp",".hpp",".zig",".S",".s",".m",".mm"})

def doFsharp():
    simpleGithub("dotnet","fsharp",{".c",".h",".cpp",".hpp",".cs",".fsi",".fs",".m",".mm"},"main")

def doRuby():
    simpleGithub("ruby","ruby",{".c",".h",".cpp",".hpp",".rb",".y"})

def doGolang():
    simpleGithub("golang","go",{".c",".h",".go",".S",".s",".pl"},nameOverride="golang")

def doSerenityOS():
    simpleGithub("SerenityOS","serenity",{".c",".h",".cpp",".hpp",".ini","CMakeLists.txt",".cmake",".gml",},nameOverride="SerenityOS")

def doXNU():
    simpleGithub("apple","darwin-xnu",{".c",".h",".cpp",".hpp",".m",".mm",".s",".S",".py",".2"},"main","XNU")

def doFreeBSD():
    simpleGithub("freebsd","freebsd-src",{".c",".h",".cpp",".hpp",".m",".mm",".s",".S",".py",".2"},"main","FreeBSD")

def doMaui():
    simpleGithub("dotnet","maui",{".c",".h",".cpp",".hpp",".m",".mm",".cs",".ps1",".java",".css"},"main","Maui")

def dowxWidgets():
    simpleGithub("wxWidgets","wxWidgets",{".c",".h",".cpp",".hpp",".m",".mm",".cs",".ps1",".java",".css","CMakeLists.txt",".cmake"})

def doGTK():
    os.system("git clone https://gitlab.gnome.org/GNOME/gtk --depth=1")
    simpleDirectory("gtk",{".c",".h",".cpp",".hpp",".m",".mm",".cs"},"gtk")
    os.system("rm -rf gtk")

def doPHP():
    simpleGithub("php","php-src",{".c",".h",".cpp",".hpp",".php",".m4",".js",".json",".xml"},nameOverride="PHP")

def doPerl():
    simpleGithub("Perl","perl5",{".c",".h",".cpp",".hpp",".pl",".pm",".t",".pod",".xml",".xs",".sh"},"blead","Perl")

def doDart():
    simpleGithub("dart-lang","sdk",{".c",".h",".cpp",".hpp",".dart",".py",".gn",".java",".yaml"},"main","Dart", dirOverride="sdk-master")

def doMongo():
    simpleGithub("mongodb","mongo",{".c",".h",".cpp",".hpp",".js",".py",".gn",".xml",".wxs",".yml"},nameOverride="MongoDB")

def doFoundationDB():
    simpleGithub("apple","foundationdb",{".c",".h",".cpp",".hpp",".js",".py",".go",".java",".toml",".rst",".sh","CMakeLists.txt",".cmake"},"main","FoundationDB")

def doMySQL():
    simpleGithub("mysql","mysql-server",{".c",".h",".cpp",".hpp",".js",".py",".java",".sql",".php",".sh","CMakeLists.txt",".cmake"},"8.0","MySQL")

def doPostgres():
    simpleGithub("postgres","postgres",{".c",".h",".cpp",".hpp",".js",".pl",".sql",".py",".po"},nameOverride="PostgreSQL")

def doV8():
    os.system("git clone https://chromium.googlesource.com/v8/v8.git --depth=1 --recurse-submodules")
    simpleDirectory("v8",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl",".metal"},"Chromium-V8")
    os.system("rm -rf v8")

def doElectron():
    downloadGithub("electron/electron")
    os.chdir("electron-main")
    os.system("yarn")
    os.chdir("..")
    simpleDirectory("electron-main",{".js",".json",".c",".cpp",".hpp",".h",".map",".ts",".lock",".opts",".mm",".py"},"Electron")

def doJUCE():
    simpleGithub("juce-framework","JUCE",{".cpp",".hpp",".cxx", ".cc", ".c",".h",".cmake", ".java", ".cs", ".qml", ".js", ".in", ".m", ".mm", ".S", ".s", ".asm", ".f90", ".metal", ".vert", ".vs", ".frag", ".fs", ".hlsl", ".glsl"})

def doSqlite():
    simpleGithub("sqlite","sqlite",{".h",".c",".tcl",".cpp",".hpp",".js"})

def doLumberyard():
    simpleGithub("aws","lumberyard",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".py",".html",".xml",".mm",".m"},nameOverride="Lumberyard")

def doCocos2Dx():
    downloadGithub("cocos2d/cocos2d-x")
    os.chdir("cocos2d-x-v4")
    os.system("python3 download-deps.py")
    os.chdir("..")
    simpleDirectory("cocos2d-x-v4", {".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".py",".html",".xml",".mm",".m",".lua",".vert",".frag",".comp"},nameOverride="Cocos2D-x")

def doBabylon():
    downloadGithub("BabylonJS/Babylon.js")
    os.chdir("Babylon.js-master")
    os.system("npm install")
    os.chdir("..")
    simpleDirectory("Babylon.js", {".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".py",".html",".xml",".mm",".m",".lua",".vert",".frag",".comp",".js",".ts",".html",".java",".fx",".tsx",".scss"})

def doBabylonNative():
    os.system("git clone https://github.com/BabylonJS/BabylonNative.git --depth=1 --recurse-submodules")
    os.chdir("BabylonNative/Apps")
    os.system("npm install")
    os.chdir("../..")
    simpleDirectory("BabylonNative", {".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".py",".html",".xml",".mm",".m",".lua",".vert",".frag",".comp",".js",".ts",".html",".java",".fx",".tsx",".scss"})

def doReact():
    downloadGithub("facebook/react")
    os.chdir("react-main")
    os.system("yarn")
    os.chdir("..")
    simpleDirectory("react-main", {".js",".json",".c",".cpp",".hpp",".h",".map",".ts",".lock",".opts",".css",".rs",".html"},"React")

def doNodeJS():
    downloadGithub("nodejs/node")
    os.chdir("node-main")
    os.system("yarn")
    os.chdir("..")
    simpleDirectory("node-main",{".js",".json",".c",".cpp",".hpp",".h",".map",".ts",".lock",".opts",".py",".html",".pod",".S"},"NodeJS")

def doVSCode():
    downloadGithub("microsoft/vscode")
    os.chdir("vscode-main")
    os.system("yarn")
    os.chdir("..")
    simpleDirectory("vscode-main", {".js",".json",".c",".cpp",".hpp",".h",".map",".ts",".lock",".opts",".css",".rs",".html",".yml"},"Visual Studio Code")

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
    "Unreal" : doUE5,
    "Linux" : doLinux,
    "LLVM" : doLLVM,
    "Blender" : doBlender,
    "gcc" : doGCC,
    "swift" : doSwift,
    "chromeprojs" : doChromeProjs,
    "firefox" : doFirefox,
    "dotnet-runtime": doDotnetRuntime,
    "boost" : doBoost,
    "openjdk" : doOpenJDK,
    "qt6" : doQt6,
    "kotlin" : doKotlin,
    "cpython" : doCPython,
    "zig" : doZig, 
    "fsharp" : doFsharp,
    "ruby" : doRuby,
    "golang" : doGolang,
    "serenityos" : doSerenityOS,
    "xnu" : doXNU,
    "freebsd" : doFreeBSD,
    "dotnet-maui" : doMaui,
    "wxWidgets" : dowxWidgets,
    "gtk" : doGTK,
    "php" : doPHP,
    "perl" : doPerl,
    "dart" : doDart,
    "mongodb" : doMongo,
    "foundationdb" : doFoundationDB,
    "mysql" : doMySQL,
    "postgres" : doPostgres,
    "Electron" : doElectron,
    "juce" : doJUCE,
    "v8" : doV8,
    "sqlite" : doSqlite,
    "React" : doReact,
    "NodeJS" : doNodeJS,
    "VSCode" : doVSCode,
    "Lumberyard" : doLumberyard,
    "Cocos2d-X" : doCocos2Dx,
    "Babylon.js" : doBabylon,
    "BabylonNative": doBabylonNative,
}
fn = ""
try:
    if (len(sys.argv) < 2):
        raise KeyError();
    fn = fns[sys.argv[1]]
except KeyError:
    print(f"Not a known codebase. Known codebases:")
    for name in fns:
        print(name)
    exit(1)

fn()
