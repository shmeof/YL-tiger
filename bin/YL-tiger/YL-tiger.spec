# -*- mode: python -*-
a = Analysis(['YL-tiger.py'],
             pathex=['D:\\Work_Android\\Env_Android\\Android_Environment\\build\\python\\PythonToExe\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'YL-tiger.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='YL-tiger.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'YL-tiger.exe.app'))
