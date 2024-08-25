from cx_Freeze import setup, Executable
import textract
import subprocess


buildOptions = {
    "packages": ["os", "textract", "subprocess"],
    "includes": [],
    "include_files": [],
}


setup(name='Instotech Mj Biopharma Raw Data and Index',
      version='0.1',
      description='Generate Index and raw Data for Mj Biopharma',
      options=dict(build_exe=buildOptions),
      executables=[Executable("Mj bio pharma.py")])
