# MuJoCo from Scratch: A Windows Beginner Tutorial

[简体中文](README.md) | **English**

An open-source guide for complete beginners: prepare folders → install Python → install MuJoCo → simulate a falling ball → drive a pendulum → save data → run again later.

**Keep Python, environments, download caches, installation temporary files, models, and results off the C: drive.** This guide uses D: by default. Use E: or another existing non-C: drive if needed. Do not format or repartition a disk for this tutorial.

For Windows 10/11 on Intel/AMD x64 computers. These instructions are not intended for macOS, Linux, or Windows ARM. We use Miniconda to provide Conda; the full Anaconda distribution, CUDA, a dedicated GPU, Git, and VS Code are not required. You need access to GitHub, Anaconda's official downloads/package repositories, and PyPI.

Versions: **Conda + Python 3.10.20 + MuJoCo 3.13.0 + NumPy 2.2.6**. The three runtime versions are fixed. The Conda management tool and other indirect dependencies may differ. Robot assets, PyTorch, CUDA, and reinforcement-learning training configurations are outside this basic setup.

We control where the development environment and its main caches are stored. Windows, browsers, and drivers may still write logs to the system drive. We do not change the computer-wide temporary directory.

## 1. Four terms to know

| Term | Meaning |
|---|---|
| PowerShell / terminal | A window where you enter commands |
| Python | The program that runs the example scripts |
| Environment | A separate set of Python packages for this tutorial |
| MuJoCo | A physics engine that computes gravity, collisions, and joint motion |

XML describes the simulated world. Python controls how it runs. A falling ball is a physics simulation; this tutorial does not train a reinforcement-learning policy.

## 2. Open the terminal for initial setup

1. Press the Windows key and search for PowerShell.
2. Open **Windows PowerShell** without administrator privileges.
3. A prompt such as PS C:\Users\YourName> is normal. Its current location does not determine where the environment will be installed.
4. Copy only the contents of a code block, paste them into the terminal, and press Enter. Do not copy the prompt or surrounding explanation.
5. If a multiline-paste warning appears, check the commands before pasting. Stop if a command reports an error.

If the prompt is >>>, you are inside Python. Enter exit() to return to the terminal.

## 3. Prepare a non-C: directory before installing

Open This PC and check which drives exist. If you do not have D:, change only the drive letter in step 3.1 to E: or another existing non-C: drive. Keep the English folder names and avoid spaces. Allow at least 5 GB of free space.

This section only sets locations and creates folders. It does not install Python or MuJoCo.

| Name or command | Purpose |
|---|---|
| $Root | Main working directory |
| if statements | Check the drive and path |
| New-Item | Create folders |
| $Conda | Reserved location of the Conda executable |
| $EnvDir, $Py | Reserved environment and Python locations; after installation, use the environment name |
| $env:CONDA_ENVS_PATH | Default location for environments |
| $env:CONDA_PKGS_DIRS | Conda package download/extraction cache |
| $env:PIP_CACHE_DIR | pip download cache |
| $env:TEMP, $env:TMP | Temporary directory for this terminal and its child processes |
| Set-Location | Change the terminal's working directory |

**Run the following six steps in order in the same PowerShell window. Copy one block at a time and press Enter.** Stop on errors. If you close the window during this preparation stage, start again at 3.1.

Use the copy button in the upper-right corner of each GitHub code block. Do not add backslashes at the ends of command lines. Keep the backslashes already present inside paths.

### 3.1 Choose the main directory

Change the drive letter in the first line if needed. The second line makes PowerShell stop the current operation on an error.

~~~powershell
$Root = 'D:\MuJoCoLab'
$ErrorActionPreference = 'Stop'
Write-Host "Selected folder: $Root"
~~~

You should see Selected folder: D:\MuJoCoLab, or your chosen drive.

### 3.2 Check the path

These commands check for a non-C: drive, an ASCII path without spaces, and an existing drive. Leave the two backslashes after the colon in the first regular expression unchanged.

~~~powershell
if ($Root -notmatch '^[D-Zd-z]:\\') { throw 'Choose an absolute path outside C:.' }
if ($Root -match '\s|[^\x00-\x7F]') { throw 'Use an English path without spaces.' }
if (-not (Test-Path ([IO.Path]::GetPathRoot($Root)))) { throw 'Drive does not exist. Change step 3.1.' }
Write-Host 'Path check passed.'
~~~

You should see Path check passed. If an error appears, check the path in 3.1.

### 3.3 Create and enter the main directory

~~~powershell
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Root = (Resolve-Path $Root).Path
if ($Root -match '^[Cc]:') { throw 'C: is not allowed.' }
Set-Location $Root
Get-Location
~~~

The final output should show your MuJoCoLab directory. Existing folders are reused.

### 3.4 Remember program and environment locations

This only sets variables. The programs may not exist yet. No output is expected, and installation has not started.

~~~powershell
$CondaHome = "$Root\miniconda3"
$Conda = "$CondaHome\Scripts\conda.exe"
$EnvDir = "$Root\envs\mujoco-basics"
$Py = "$EnvDir\python.exe"
$Project = "$Root\tutorial"
~~~

### 3.5 Set cache and temporary locations

This directs subsequent installation processes to the non-C: drive. No output is expected.

~~~powershell
$env:CONDA_ENVS_PATH = "$Root\envs"
$env:CONDA_PKGS_DIRS = "$Root\cache\conda"
$env:PIP_CACHE_DIR = "$Root\cache\pip"
$env:TEMP = "$Root\temp"
$env:TMP = "$Root\temp"
~~~

### 3.6 Create the subfolders and confirm

~~~powershell
New-Item -ItemType Directory -Force -Path $env:CONDA_ENVS_PATH,$env:CONDA_PKGS_DIRS | Out-Null
New-Item -ItemType Directory -Force -Path $env:PIP_CACHE_DIR,$env:TEMP,"$Root\downloads" | Out-Null
Write-Host "Environment root: $Root"
Write-Host "Install Miniconda into: $CondaHome"
~~~

Both displayed locations should be on your chosen non-C: drive. These variables apply to this installation session. After installation, configure the named environment in section 6 and use section 10 for future sessions.

Conda may store small configuration or environment-registration files in your user directory. The environment, installer, and main caches are redirected; zero writes to C: are not guaranteed.

If you followed an earlier uv edition of this tutorial, you do not need to remove uv. This edition uses a separate Conda environment. Once section 6 is complete, go directly to section 10 next time.

## 4. Download the tutorial files

1. On this GitHub repository, click the green **Code** button → **Download ZIP**.
2. Save the ZIP to D:\MuJoCoLab, or your selected non-C: directory. If the browser downloads to C: automatically, enable “Ask where to save each file” in its download settings first.
3. Right-click the ZIP → **Extract All**, and extract it onto the same non-C: drive.
4. Open the extracted folder and locate the items below.
5. Create a folder named tutorial inside MuJoCoLab. Copy the listed files and the models folder into it. You may also copy README_EN.md for offline reading.

| Name | Type | Purpose |
|---|---|---|
| README.md | File | Chinese tutorial |
| run_demo.py | File | Simulation script |
| models | Folder | Contains ball.xml and pendulum.xml |

If extensions are hidden, enable File name extensions: on Windows 11, use View → Show → File name extensions; on Windows 10, use the View tab. Do not manually add duplicate extensions.

Your folder structure must look like this, without an extra repository-name folder in between:

~~~text
D:\MuJoCoLab\
  tutorial\
    README.md
    run_demo.py
    models\
      ball.xml
      pendulum.xml
~~~

Check in the same PowerShell window:

~~~powershell
Test-Path "$Project\run_demo.py"
Test-Path "$Project\models\ball.xml"
Test-Path "$Project\models\pendulum.xml"
~~~

All three results must be True. If any is False, fix the file locations before continuing.

## 5. Install Miniconda once

Conda manages environments. Miniconda is a small installer that includes Conda. Its base Python version may differ; section 6 creates a separate environment named mujoco-basics with Python 3.10.20.

Download the official Windows x64 installer to the non-C: directory:

~~~powershell
$Installer = "$Root\downloads\Miniconda3-latest-Windows-x86_64.exe"
Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile $Installer -UseBasicParsing
Write-Host "Installer: $Installer"
Write-Host "Choose this installation folder: $CondaHome"
~~~

When the download completes, open its installer:

~~~powershell
Start-Process -FilePath $Installer -Wait
~~~

In the installation window:

1. Click Next, read the license terms, and continue if you agree.
2. Select Just Me.
3. **Replace the default Destination Folder** with the location printed in the terminal, normally D:\MuJoCoLab\miniconda3. If you chose E: earlier, use E: here too.
4. Leave Add to PATH and Register as default Python unchecked. The Anaconda Prompt provides the Conda commands used below.
5. Click Install, wait, and then Finish. Continue with 5.1.

If the destination already contains files, stop rather than overwriting an existing Conda installation.

### 5.1 After installation, open Anaconda Prompt

**All terminal commands from this point onward run in Anaconda Prompt.**

1. Close the PowerShell window used for preparation.
2. Search the Start menu for Anaconda Prompt and choose the entry belonging to the Miniconda installation you just completed. Some versions label it Miniconda Prompt.
3. The prompt normally begins with (base), Conda's management environment.
4. If you are on the Anaconda Navigator graphical home screen, use the triangle next to the base environment → Open Terminal.
5. Run:

~~~bat
conda --version
~~~

You should see a Conda version. If conda is not recognized, check that you opened the correct Prompt.

The environment name throughout this guide is **mujoco-basics**. You will activate it by name. Prompt labels such as (base) and (mujoco-basics) describe the state of the terminal; do not copy them as commands.

## 6. Create and activate the environment, then install packages

### 6.1 Configure non-C: environment and cache locations once

The new Anaconda Prompt does not inherit the variables from the earlier PowerShell window. Set the same main directory again. Change D: to your chosen non-C: drive if necessary.

~~~bat
set "MJROOT=D:\MuJoCoLab"
echo %MJROOT%
~~~

You should see your selected MuJoCoLab path. Run these blocks one at a time:

~~~bat
if not exist "%MJROOT%\envs" mkdir "%MJROOT%\envs"
if not exist "%MJROOT%\cache\conda" mkdir "%MJROOT%\cache\conda"
if not exist "%MJROOT%\cache\pip" mkdir "%MJROOT%\cache\pip"
~~~

~~~bat
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
set "PIP_CACHE_DIR=%MJROOT%\cache\pip"
~~~

Save the environment/cache directories in Conda's configuration so the environment can be found by name in future sessions:

~~~bat
set "CONDA_ENVS_PATH=%MJROOT%\envs"
set "CONDA_PKGS_DIRS=%MJROOT%\cache\conda"
conda config --prepend envs_dirs "%MJROOT%\envs"
conda config --prepend pkgs_dirs "%MJROOT%\cache\conda"
~~~

Check:

~~~bat
conda config --show envs_dirs pkgs_dirs
~~~

The selected envs and cache\conda directories must be listed first. Other old directories may also appear. Stop and inspect the configuration if your selected directories are not first.

Conda may save small configuration and registration files in your user directory. The environment, package cache, and main tutorial files stay off C:.

### 6.2 Create the named environment once

~~~bat
conda create -n mujoco-basics --override-channels -c https://repo.anaconda.com/pkgs/main python=3.10.20 pip
~~~

| Part | Meaning |
|---|---|
| conda create | Create an environment |
| -n mujoco-basics | Name it mujoco-basics |
| python=3.10.20 | Install this Python version |
| pip | Include Python's package installer |

When Proceed ([y]/n)? appears, enter y and wait for completion. Anaconda repositories may require you to review and accept their terms on first use. Follow the prompts before continuing. For TosNonInteractiveError, follow the reported repository's terms workflow, then retry.

If the name already exists, inspect conda env list first. Do not confirm overwriting or deleting an environment. An environment created by the previous edition under the configured envs\mujoco-basics directory can be activated by name in the next step.

If the exact Python version is unavailable or downloading fails, keep the full error. Do not silently switch versions.

### 6.3 Activate by name

~~~bat
conda activate mujoco-basics
~~~

The prompt should change from (base) to **(mujoco-basics)**. This is where you install packages and run the examples. Activate it whenever you open a new Anaconda Prompt; you do not need to recreate it.

Check the location:

~~~bat
python -c "import sys; print(sys.executable)"
conda env list
~~~

Python must be under envs\mujoco-basics on your chosen non-C: drive. The active environment has an asterisk in the list. If Python still points to base or C:, stop before installing packages.

### 6.4 Save this environment's cache and temporary settings once

With (mujoco-basics) active, use the same Prompt window where you created the environment:

~~~bat
conda env config vars set "MJROOT=%MJROOT%" "PIP_CACHE_DIR=%MJROOT%\cache\pip" "TEMP=%MJROOT%\temp" "TMP=%MJROOT%\temp"
~~~

Reactivate to apply the saved variables:

~~~bat
conda deactivate
conda activate mujoco-basics
echo %MJROOT%
echo %PIP_CACHE_DIR%
echo %TEMP%
~~~

All three paths should use your non-C: drive. Future activations restore these values automatically.

### 6.5 Install MuJoCo and NumPy in the active environment

Confirm that the prompt begins with (mujoco-basics), then run:

~~~bat
python -m pip install "mujoco==3.13.0" "numpy==2.2.6"
~~~

Using python -m pip installs packages through the active environment's Python. These packages go into mujoco-basics rather than base.

The official mujoco package includes the runtime library; no separate engine download is needed. [Official installation instructions](https://mujoco.readthedocs.io/en/stable/python.html#installation).

Check the versions:

~~~bat
python -c "import sys; print('Python:',sys.version.split()[0]); print('Path:',sys.executable)"
python -c "import mujoco,numpy; print('MuJoCo:',mujoco.__version__); print('NumPy:',numpy.__version__)"
~~~

Expected: Python 3.10.20, MuJoCo 3.13.0, NumPy 2.2.6, and a Python path on the non-C: drive.

### 6.6 Install another package later

Activate the environment first. For example, install the Pillow image-processing library:

~~~bat
conda activate mujoco-basics
python -m pip install pillow
~~~

Verify it:

~~~bat
python -c "from PIL import Image; print('Pillow installed successfully')"
~~~

Expected output: Pillow installed successfully. Its installation name is pillow, while its import name is PIL. This extra example is not required for the MuJoCo demos.

The general form is python -m pip install PACKAGE_NAME. To select a version, append ==VERSION. Replace those placeholders with real names and versions.

If another package proposes changing a fixed dependency such as NumPy, check compatibility before proceeding. Repeat the version checks in 6.5 after installation.

List installed packages:

~~~bat
python -m pip list
~~~

Leave the environment:

~~~bat
conda deactivate
~~~

The prompt returns to (base). To continue, run conda activate mujoco-basics again.

## 7. First model: a falling ball

Activate the environment and enter the tutorial folder in Anaconda Prompt:

~~~bat
conda activate mujoco-basics
cd /d "%MJROOT%\tutorial"
dir run_demo.py
dir models
~~~

You should find run_demo.py and models. The /d option changes both drive and directory. MJROOT uses the location saved earlier, including your chosen drive.

First test the physics without opening a window:

~~~bat
python run_demo.py --model ball --headless --seconds 3
~~~

Expected: Finished appears, and tutorial\output\ball.csv is created. Headless execution is fast because it does not deliberately wait for real time.

Now open the simulation window:

~~~bat
python run_demo.py --model ball --seconds 15
~~~

An orange ball should fall and settle on the floor. The example ends after about 15 seconds of simulation, or you can close the window early. The fall is quick; rerun the command to watch again.

Drag with the left mouse button to rotate the view; use the scroll wheel to zoom. Close one example before starting another. While a window is running, the terminal may not show a new prompt.

Open the model:

~~~bat
notepad "%MJROOT%\tutorial\models\ball.xml"
~~~

| XML setting | Meaning |
|---|---|
| gravity="0 0 -9.81" | Downward gravity in m/s² |
| timestep="0.002" | Each physics step advances 0.002 seconds |
| type="plane" | Floor |
| pos="0 0 1.5" | Initial ball-center height of 1.5 meters |
| freejoint | Allows free translation and rotation |
| type="sphere" size="0.1" | A sphere of radius 0.1 meters |
| mass="1" | Mass of 1 kilogram |
| rgba | Red, green, blue, opacity; each ranges from 0 to 1 |

Exercise: change the ball's pos="0 0 1.5" to pos="0 0 2.5". Press Ctrl+S, close Notepad, and rerun the ball command. The fall distance should increase. Preserve the quotes and XML tags.

## 8. Second model: a motor-driven pendulum

~~~bat
python run_demo.py --model pendulum --seconds 20
~~~

A blue rod should swing around a fixed pivot. Its initial angle is 0.5 radians, approximately 28.6 degrees. A motor applies a sinusoidal torque.

Compare zero motor input with a larger input:

~~~bat
python run_demo.py --model pendulum --amplitude 0 --seconds 20
python run_demo.py --model pendulum --amplitude 4 --seconds 20
~~~

The commands run sequentially. The first rod swings under gravity and gradually loses motion through damping; the second receives periodic motor input. Allowed amplitudes are 0–5. In this model, with transmission gear 1, the unit is N·m.

Open the script:

~~~bat
notepad "%MJROOT%\tutorial\run_demo.py"
~~~

| Code | Purpose |
|---|---|
| MjModel.from_xml_path(...) | Load the model structure |
| MjData(model) | Create dynamic state, including positions and velocities |
| data.qpos | Position state; the pendulum's only element is its joint angle |
| data.qvel | Velocity state; angular velocity for this pendulum |
| data.ctrl[0] = control | Set the first actuator's input |
| mj_step(model, data) | Advance physics by one step |
| viewer.sync() | Synchronize the viewer and simulation |

The freely moving ball has 7 position components (3 coordinates plus 4 quaternion components) and 6 velocity components. Do not assume qpos[0] is a joint angle in every model. The printed nq, nv, and nu values are the position, velocity, and control dimensions.

The motor signal is amplitude * sin(2 * pi * 0.5 * time): 0.5 Hz, repeating every 2 seconds. This is a predefined control signal, not a learned policy.

## 9. Save and inspect data

Each run writes a CSV automatically. A new run of the same model overwrites that model's previous CSV. Copy and rename earlier files first if you want to keep them.

~~~bat
notepad "%MJROOT%\tutorial\output\pendulum.csv"
~~~

Columns are simulation time in seconds, angle in radians, and motor input. In ball.csv, the second column is ball-center height in meters. You can open CSV files in Notepad or Excel.

The settled ball-center height is approximately 0.1 meters because the ball has a radius. Small contact-solver deviations are normal.

The graphical example attempts real-time pacing. A slow computer may take longer than 15 wall-clock seconds to simulate 15 seconds. Headless mode does not deliberately wait.

## 10. Run again next time

Open Anaconda Prompt and execute these three commands:

~~~bat
conda activate mujoco-basics
cd /d "%MJROOT%\tutorial"
python run_demo.py --model pendulum --seconds 20
~~~

Check for (mujoco-basics) before running the script. Once setup is complete, do not recreate the environment or reinstall packages each time.

To open the official model viewer:

~~~bat
python -m mujoco.viewer --mjcf models\pendulum.xml
~~~

Press Space to pause or resume. The standalone viewer does not execute the script's sinusoidal controller, so the motion differs. [Viewer documentation](https://mujoco.readthedocs.io/en/stable/python.html#interactive-viewer).

## 11. Troubleshooting

| Symptom | What to check |
|---|---|
| Drive does not exist | Check the selected drive; correct sections 3 and 6.1 during initial setup |
| Environment mujoco-basics not found | Open the same Anaconda Prompt installation, run conda env list, and check envs_dirs from 6.1 |
| run_demo.py not found | Run the cd command in section 10; check for an extra nested extraction folder |
| No module named mujoco | Activate mujoco-basics, inspect the Python path, then install as in 6.5 |
| Download timeout or connection failure | Check access to the domain in the error; retry when connectivity returns; do not disable certificate verification |
| GitHub download fails | Use an already obtained tutorial ZIP as in section 4; Miniconda/Python downloads still need working connectivity |
| GLFW/OpenGL error or black window | Try --headless; if physics works, check graphics drivers and local/remote desktop graphics support; obtain drivers from official vendors |
| DLL load failed | Keep the full error; check x64 Windows and the selected Python path; do not download random DLL files |
| XML parse error | Check edited quotes/tags or restore that XML file from the repository |
| Ball has already landed | The fall is quick; rerun or increase the initial height |
| Terminal is busy | The simulation is still running; close its window or press Ctrl+C |
| Prompt still shows (base) | Activation failed; read the error and inspect conda env list |

For further help, open an Issue with the command, full error text, and the diagnostic output below. Remove personal information before posting. Do not include passwords or tokens.

~~~bat
conda env list
echo %CONDA_PREFIX%
echo %MJROOT%
where python
python -c "import sys,platform; print(sys.executable); print(platform.platform()); print(platform.machine())"
~~~

## 12. Completion checklist and next steps

- Environment paths point to a non-C: drive.
- Headless simulation finishes and creates CSV files.
- You can watch the ball fall and change its initial height.
- You can run the pendulum and compare motor amplitudes.
- After closing the terminal, you can run again using section 10.

Then explore multi-joint robots, sensors, PD control, Gymnasium interfaces, and reinforcement learning. Adding robot assets, training frameworks, and CUDA at the beginning makes troubleshooting harder.

## Official references and validation

- [MuJoCo Python documentation](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [Conda installation on Windows](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html)
- [Conda environment and cache settings](https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html)

This guide installs Miniconda off C:, configures envs_dirs and pkgs_dirs in Anaconda Prompt, and creates a separate named environment. pip cache and temporary settings are saved with that environment. Updated: 2026-11-06.

Validation used an existing Windows Conda environment with Python 3.10.20, MuJoCo 3.13.0, and NumPy 2.2.6. Both examples completed 3 seconds of headless simulation and generated CSV files. Named activation and both examples were also tested through cmd.exe using the existing Conda installation. The complete Miniconda installation and creation of a new named environment have not been tested on a clean computer; graphical windows have not been verified. Matching runtime versions does not guarantee identical drivers, Conda tool versions, or every indirect dependency.
