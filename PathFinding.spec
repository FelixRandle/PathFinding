# -*- mode: python -*-

block_cipher = None

assetData = [('./assets/fonts', 'assets/fonts/'),
              ('assets/home', 'assets/home/'),
              ('assets/settings', 'assets/settings/'),
              ('assets/solving', 'assets/solving/'),
              ('assets/speeds', 'assets/speeds/'),
              ('colours.pckl', '.'),
              ('userData.db', '.')]

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=assetData,
             hiddenimports=['application.py'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PathFinding',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='assets\\maze.ico')
