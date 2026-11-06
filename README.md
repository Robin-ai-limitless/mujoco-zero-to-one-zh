# 从零开始使用 MuJoCo：Windows 中文教程

**简体中文** | [English](README_EN.md)

面向零基础使用者的开源入门教程。按顺序完成：准备文件夹 → 安装 Python → 安装 MuJoCo → 小球落地 → 电机摆杆 → 保存数据 → 下次重新运行。

**Python、虚拟环境、下载缓存、安装临时目录、模型和实验结果全部放在非 C 盘。** 默认 D 盘；没有 D 盘就用 E 盘。不要为了教程格式化或重新分区。

本教程适用于 Windows 10/11、Intel/AMD 64 位电脑。Mac、Linux 和 Windows ARM 电脑不要直接照抄。本教程使用 Miniconda 提供 Conda，不需要完整 Anaconda 套装、CUDA、独立显卡、Git 或 VS Code。需要能访问 GitHub、Anaconda 官方下载与软件源、PyPI 的网络。

本教程使用以下基础配置：**Conda + Python 3.10.20 + MuJoCo 3.13.0 + NumPy 2.2.6**。固定的是这三个运行时版本；Conda 管理工具本身和其他间接依赖不承诺完全相同。机器人模型、PyTorch、CUDA 和训练配置不属于本教程的基础环境。

说明：我们控制的是开发环境及其缓存位置，不能保证 Windows、浏览器和驱动完全不向系统盘写入日志。本教程不改变整台电脑的系统临时目录。

## 1. 先理解四个词

| 名称 | 作用 |
|---|---|
| PowerShell（终端） | 输入命令，让电脑执行操作的窗口 |
| Python | 运行实验脚本的程序 |
| 虚拟环境 | 本教程专用的 Python 软件包文件夹，不与其他项目混用 |
| MuJoCo | 计算重力、碰撞和关节运动的物理仿真程序 |

XML 文件描述“世界长什么样”，Python 文件决定“世界怎么运行”。看到球落地，是物理仿真；本教程还没有进行强化学习训练。

## 2. 打开正确的终端

1. 按键盘 Windows 键，输入 `PowerShell`。
2. 打开 **Windows PowerShell**，不用选择管理员身份。
3. 正常提示符类似 `PS C:\Users\你的名字>`。这里显示 C 盘不代表环境将装在 C 盘。
4. 复制下面灰色代码框内的内容，粘贴到终端，按回车。不要复制代码框外的说明或 `PS ...>`。
5. 多行粘贴出现提示时，确认内容来自本教程后选择粘贴。出现红色报错就先停下，不要继续下一步。

如果提示符是 `>>>`，说明进入了 Python，输入 `exit()` 后回车，回到 PowerShell。

## 3. 准备非 C 盘目录（首次安装前执行）

打开“此电脑”，确认有没有 D 盘。没有 D 盘时，只把下面第一行的 D: 改成 E: 或你的实际非 C 盘盘符。使用示例中的英文目录名，不要添加空格。建议预留至少 5 GB 空间。

这一节只是“指定存放位置、创建必要文件夹”，还没有安装 Python 或 MuJoCo。意思是先告诉电脑：安装程序、Conda、环境、下载缓存与临时文件，都放到 MuJoCoLab 文件夹里。

| 名称或命令 | 作用 |
|---|---|
| $Root | 总文件夹地址 |
| if 开头的几行 | 检查盘符与路径，填错就停下 |
| New-Item | 创建必要文件夹 |
| $Conda | 后续调用的 Conda 程序位置 |
| $EnvDir、$Py | 预留的环境目录和 Python 程序位置；安装完成后按名字管理环境 |
| $env:CONDA_ENVS_PATH | Conda 环境默认存放位置 |
| $env:CONDA_PKGS_DIRS | Conda 下载及解压的软件包缓存位置 |
| $env:PIP_CACHE_DIR | pip 下载缓存位置 |
| $env:TEMP、$env:TMP | 当前终端及其启动程序的临时目录 |
| Set-Location | 切换终端工作位置 |

下面分成 6 个小步骤。**按顺序在同一个 PowerShell 窗口执行，一次只复制一个代码框，按回车后再继续。** 如果出现红色报错，先停止，不要执行下一步。中途关闭窗口后，需要从 3.1 重新开始。

使用 GitHub 代码框右上角的复制按钮。行末不要额外添加反斜杠，路径中原有的反斜杠需要保留。

### 3.1 选择总目录

只按实际情况修改第一行盘符。例如没有 D 盘而有 E 盘，就改成 E:\MuJoCoLab。第二行表示遇到错误时停止当前操作。

~~~powershell
$Root = 'D:\MuJoCoLab'
$ErrorActionPreference = 'Stop'
Write-Host "Selected folder: $Root"
~~~

应显示 Selected folder: D:\MuJoCoLab（或所选盘符），表示已记住路径。

### 3.2 检查路径

这几行检查是否使用非 C 盘、英文无空格路径，以及盘符是否存在。第一行正则表达式中的冒号后有两个反斜杠，请保持原样。

~~~powershell
if ($Root -notmatch '^[D-Zd-z]:\\') { throw 'Choose an absolute path outside C:.' }
if ($Root -match '\s|[^\x00-\x7F]') { throw 'Use an English path without spaces.' }
if (-not (Test-Path ([IO.Path]::GetPathRoot($Root)))) { throw 'Drive does not exist. Change step 3.1.' }
Write-Host 'Path check passed.'
~~~

应显示 Path check passed.。出现红色报错时，回到 3.1 检查盘符及目录写法。

### 3.3 创建并进入总目录

~~~powershell
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Root = (Resolve-Path $Root).Path
if ($Root -match '^[Cc]:') { throw 'C: is not allowed.' }
Set-Location $Root
Get-Location
~~~

最后应显示选定的 MuJoCoLab 目录。文件夹已经存在时会继续使用。

### 3.4 记住程序和环境的位置

这里仅设置路径变量，此时这些程序可能还没安装。正常情况下不会显示新文字，也不代表安装完成。

~~~powershell
$CondaHome = "$Root\miniconda3"
$Conda = "$CondaHome\Scripts\conda.exe"
$EnvDir = "$Root\envs\mujoco-basics"
$Py = "$EnvDir\python.exe"
$Project = "$Root\tutorial"
~~~

### 3.5 指定缓存与临时目录

这一步让后续安装程序使用非 C 盘的环境、缓存和临时目录。正常情况下不会显示新文字。

~~~powershell
$env:CONDA_ENVS_PATH = "$Root\envs"
$env:CONDA_PKGS_DIRS = "$Root\cache\conda"
$env:PIP_CACHE_DIR = "$Root\cache\pip"
$env:TEMP = "$Root\temp"
$env:TMP = "$Root\temp"
~~~

### 3.6 创建所需子目录并确认结果

~~~powershell
New-Item -ItemType Directory -Force -Path $env:CONDA_ENVS_PATH,$env:CONDA_PKGS_DIRS | Out-Null
New-Item -ItemType Directory -Force -Path $env:PIP_CACHE_DIR,$env:TEMP,"$Root\downloads" | Out-Null
Write-Host "Environment root: $Root"
Write-Host "Install Miniconda into: $CondaHome"
~~~

成功标志：显示总目录和 Miniconda 的安装目标目录，均在非 C 盘。这些变量用于本次安装准备；安装完成后按第六节配置命名环境，以后使用第十节的启动步骤。Conda 可能在用户目录保存少量登记或配置文件；这里重定向的是环境、安装文件及主要缓存，不承诺系统盘零写入。

如果你之前照旧版教程安装过 uv，不用删除它。本版在独立的 mujoco-basics 文件夹创建 Conda 环境，不复用旧版的环境。已经完成本版第六节配置后，下次直接执行第十节，不重复安装。

## 4. 下载本教程文件

1. 在本 GitHub 仓库页面点击绿色 **Code** → **Download ZIP**。
2. 浏览器询问保存位置时，选择 `D:\MuJoCoLab`（或你的非 C 盘目录）。如果浏览器默认下载到 C 盘，先在浏览器“设置 → 下载”中启用每次询问保存位置。
3. 右键下载的 ZIP → **全部解压缩**，解压到同一个非 C 盘目录。
4. 打开解压出来的文件夹，确认能看到下表列出的两个文件和一个文件夹。
5. 在 `MuJoCoLab` 下新建一个文件夹，命名为 `tutorial`。将上述文件及 `models` 文件夹复制进去。

| 应找到的名称 | 类型 | 用途 |
|---|---|---|
| README.md | 文件 | 这份教程 |
| run_demo.py | 文件 | 启动仿真的 Python 程序 |
| models | 文件夹 | 装有 ball.xml 和 pendulum.xml 两个模型 |

如果只看到 README 或 run_demo，可能是 Windows 隐藏了扩展名。Windows 11 在文件资源管理器中选择“查看 → 显示 → 文件扩展名”；Windows 10 在“查看”选项卡勾选“文件扩展名”。不要手动给文件重复添加后缀。

最终必须是下面这种结构，不能再多套一层仓库名文件夹：

```text
D:\MuJoCoLab\
  tutorial\
    README.md
    run_demo.py
    models\
      ball.xml
      pendulum.xml
```

在刚才的 PowerShell 中检查：

```powershell
Test-Path "$Project\run_demo.py"
Test-Path "$Project\models\ball.xml"
Test-Path "$Project\models\pendulum.xml"
```

三次都显示 `True` 才继续。显示 `False` 代表文件放错地方，先在文件资源管理器中调整。

## 5. 安装 Miniconda（只需一次）

Conda 负责创建和管理环境；Miniconda 是带有 Conda 的精简安装包。安装包自带的 base Python 版本可以不同，第六节会单独创建一个名为 mujoco-basics、使用 Python 3.10.20 的环境。

先下载官方 Windows x64 安装包，保存到刚才指定的非 C 盘目录：

~~~powershell
$Installer = "$Root\downloads\Miniconda3-latest-Windows-x86_64.exe"
Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile $Installer -UseBasicParsing
Write-Host "Installer: $Installer"
Write-Host "Choose this installation folder: $CondaHome"
~~~

下载完成后启动安装界面：

~~~powershell
Start-Process -FilePath $Installer -Wait
~~~

这是需要你操作的安装窗口，请按下面步骤点击：

1. 点击 Next（下一步），阅读许可条款，同意后再继续。
2. 安装范围选择 Just Me（仅当前用户）。
3. **安装目录不要用默认位置。** 将 Destination Folder 改成终端显示的路径，默认是 D:\MuJoCoLab\miniconda3。如果第三节改成 E 盘，这里也必须是 E 盘。
4. 不勾选 Add to PATH，也不勾选 Register as default Python。我们会用完整路径调用，不依赖这些设置。
5. 点击 Install，等待完成，再点击 Finish。随后按 5.1 打开 Anaconda Prompt。

如果提示目录已有文件，先停止安装，不要覆盖已有 Conda 安装。

### 5.1 安装完成后，打开 Anaconda Prompt

从这里开始，后续所有终端命令都在 **Anaconda Prompt** 中执行。

1. 关闭刚才用于准备和安装的 PowerShell 窗口。
2. 按 Windows 键，搜索 Anaconda Prompt，打开与刚安装的 Miniconda 对应的入口。部分安装版本显示为 Miniconda Prompt。
3. 正常情况下，行首显示 (base)。这是 Conda 自带的管理环境。
4. 如果看到 Anaconda Navigator 图形首页，可选择 base 环境旁的三角按钮 → Open Terminal。
5. 复制下面的命令，按回车。

~~~bat
conda --version
~~~

应显示 Conda 版本号。如果提示 conda 不是内部或外部命令，请确认打开的是上述 Prompt。不要继续在原来的 PowerShell 窗口粘贴后面的命令。

本教程将新环境命名为 **mujoco-basics**。以后用这个名字激活，不用记环境完整路径。以下代码中的命令提示符示例，如 (base) 和 (mujoco-basics)，用于说明状态，不要一起复制。

## 6. 创建、激活环境并安装库

### 6.1 指定非 C 盘的环境和缓存目录（只配置一次）

新开的 Anaconda Prompt 不会继承前面 PowerShell 中设置的变量。先在这里重新指定总目录；没有 D 盘时，将第一行改成实际的非 C 盘盘符。继续使用之前的 MuJoCoLab 文件夹。

~~~bat
set "MJROOT=D:\MuJoCoLab"
echo %MJROOT%
~~~

应显示 D:\MuJoCoLab（或所选盘符）。接着逐块执行：

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

设置 Conda 的环境与缓存位置，同时将目录保存到 Conda 配置，方便下次按名字找到环境：

~~~bat
set "CONDA_ENVS_PATH=%MJROOT%\envs"
set "CONDA_PKGS_DIRS=%MJROOT%\cache\conda"
conda config --prepend envs_dirs "%MJROOT%\envs"
conda config --prepend pkgs_dirs "%MJROOT%\cache\conda"
~~~

检查：

~~~bat
conda config --show envs_dirs pkgs_dirs
~~~

应看到所选非 C 盘的 envs 和 cache\conda 目录。配置中可能还列出其他旧目录；本教程所选目录必须排在前面。若不是，先停止并检查配置。

Conda 可能在用户目录保存少量配置与环境登记文件；环境、软件包缓存和本教程的主要文件放在非 C 盘。

### 6.2 创建一个名叫 mujoco-basics 的环境（只创建一次）

~~~bat
conda create -n mujoco-basics --override-channels -c https://repo.anaconda.com/pkgs/main python=3.10.20 pip
~~~

这条命令中：

| 部分 | 含义 |
|---|---|
| conda create | 新建环境 |
| -n mujoco-basics | 给环境命名为 mujoco-basics |
| python=3.10.20 | 安装指定版本的 Python |
| pip | 安装 Python 软件包管理工具 |

**首次运行时，如果出现是否接受 Anaconda 软件源条款的询问，同意条款就输入 `a`（accept），按回车继续。**

之后看到 Proceed ([y]/n)?（是否安装软件包）时，输入 `y` 并回车，等待完成。出现 TosNonInteractiveError 时，按报错提示完成对应软件源的条款流程后重试。

如果提示同名环境已存在，先运行 conda env list 检查位置，不要确认覆盖或删除。旧版教程创建的环境如已位于已配置的 envs\mujoco-basics 下，可以直接在下一步按名字激活。

如果找不到指定 Python 版本或下载失败，请保留完整报错，不要自行改版本后继续。

### 6.3 按名字激活环境

~~~bat
conda activate mujoco-basics
~~~

成功后行首应从 (base) 变成 **(mujoco-basics)**。这是后续安装库和运行程序的环境。每次重新打开 Anaconda Prompt 都要重新激活，但不需要重新创建。

检查实际环境位置：

~~~bat
python -c "import sys; print(sys.executable)"
conda env list
~~~

Python 路径必须位于所选非 C 盘的 envs\mujoco-basics 下；环境列表中当前环境旁有星号。如果仍然指向 base 或 C 盘，先停止，不要安装软件包。

### 6.4 保存路径并设置临时目录（首次配置）

在创建环境的同一个 Anaconda Prompt 中，只保存以下两个变量：

~~~bat
conda env config vars set -n mujoco-basics "MJROOT=%MJROOT%" "PIP_CACHE_DIR=%MJROOT%\cache\pip"
~~~

**执行成功后，直接关闭这个 Anaconda Prompt，重新打开一个新的窗口。不要在这个旧窗口中先执行 conda deactivate。** 新窗口中执行：

~~~bat
conda activate mujoco-basics
echo %MJROOT%
echo %PIP_CACHE_DIR%
~~~

两个路径都应在所选非 C 盘。然后为当前窗口设置临时目录：

~~~bat
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
~~~

MJROOT 和 pip 缓存会在下次激活时自动恢复。TEMP、TMP 只在当前窗口设置，不保存到 Conda 环境配置；每次新开窗口后按第十节执行。

#### 可选恢复：仅适用于旧命令执行后激活失败

**仅当你执行过旧版包含 TEMP、TMP 的保存命令，并在随后重新激活时出现“找不到文件”或“找不到环境”的错误，才使用下面的恢复步骤。** 正常安装、正常激活，或仅显示覆盖变量的 WARNING 而没有激活失败时，请跳过整段恢复步骤，直接继续 6.5。

旧命令把 TEMP、TMP 也存入了环境配置。下面清除的是本教程的旧设置，并恢复环境搜索路径，不需要重建环境。这是针对该旧流程的恢复方法，不代表所有“找不到文件/环境”错误都由同一原因造成；请保留完整错误文字。

1. 关闭出现问题的窗口，重新打开 **Anaconda Prompt**，先保持在 base。
2. 设置实际安装目录（如果用 E 盘，只修改第一行盘符），检查环境仍然存在：

~~~bat
set "MJROOT=D:\MuJoCoLab"
dir "%MJROOT%\envs\mujoco-basics\conda-meta\history"
~~~

应该能列出 history 文件。如果提示找不到文件，先用 conda env list 查看实际环境位置；不要直接重建或删除环境。

3. 确认上述文件存在后，逐条执行：

~~~bat
conda env config vars unset TEMP TMP -p "%MJROOT%\envs\mujoco-basics"
conda config --prepend envs_dirs "%MJROOT%\envs"
set "CONDA_ENVS_PATH=%MJROOT%\envs"
~~~

4. 按名字激活，再设置当前窗口的临时目录：

~~~bat
conda activate mujoco-basics
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
~~~


### 6.5 在当前环境安装 MuJoCo 和 NumPy

确认行首是 (mujoco-basics)，再执行：

~~~bat
python -m pip install "mujoco==3.13.0" "numpy==2.2.6"
~~~

这里使用 python -m pip，表示通过当前已激活环境的 Python 安装软件包。它们会装入 mujoco-basics，不会装入 base。

官方 mujoco 软件包包含运行库，无需再单独安装引擎。[官方安装说明](https://mujoco.readthedocs.io/en/stable/python.html#installation)

检查版本：

~~~bat
python -c "import sys; print('Python:',sys.version.split()[0]); print('Path:',sys.executable)"
python -c "import mujoco,numpy; print('MuJoCo:',mujoco.__version__); print('NumPy:',numpy.__version__)"
~~~

应分别显示 Python 3.10.20、MuJoCo 3.13.0、NumPy 2.2.6，且 Python 路径在非 C 盘。

### 6.6 以后怎么给这个环境安装其他库？

每次先激活环境，然后安装所需库。例如，安装常用的图像处理库 Pillow：

~~~bat
conda activate mujoco-basics
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
python -m pip install pillow
~~~

验证安装：

~~~bat
python -c "from PIL import Image; print('Pillow installed successfully')"
~~~

应显示 Pillow installed successfully。注意：安装时的名字是 pillow，代码中的导入名字是 PIL。这个额外示例不是运行 MuJoCo 的必需依赖。

通用格式是 python -m pip install 库名。例如想指定版本，在库名后添加 ==版本号。不要把“库名”“版本号”等中文占位说明原样复制为命令。

安装其他包时，若提示将修改 NumPy 等基础依赖版本，先确认是否仍符合本教程的固定版本要求。安装完成后可以重新执行 6.5 的版本检查。

查看当前环境已安装的库：

~~~bat
python -m pip list
~~~

退出当前环境：

~~~bat
conda deactivate
~~~

行首恢复为 (base)。要继续本教程，重新执行 conda activate mujoco-basics。

## 7. 第一个模型：小球落地

在 Anaconda Prompt 中激活环境并进入教程文件夹：

~~~bat
conda activate mujoco-basics
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
cd /d "%MJROOT%\tutorial"
dir run_demo.py
dir models
~~~

应能找到 run_demo.py 和 models 文件夹。cd /d 表示同时切换盘符和目录；选择其他盘符时，前面保存的 MJROOT 会自动使用对应路径。

运行下面的命令，直接打开 MuJoCo 仿真窗口：

```bat
python run_demo.py --model ball --seconds 15
```

**成功标志：弹出 MuJoCo 图形窗口，能看到橙色小球从空中掉落，最后停在地面。** 只有终端输出或 CSV 文件，不能算完成这一节。默认 15 秒仿真后关闭，也可以点击窗口右上角关闭。球下落很快，想再看一次就重新运行该命令。

鼠标左键拖动可旋转视角，滚轮可缩放。不要连续启动许多窗口；关闭上一次窗口再运行下一个命令。终端在窗口运行期间没有新提示符，是程序仍在工作。

打开模型看看：

```bat
notepad "%MJROOT%\tutorial\models\ball.xml"
```

| XML 内容 | 含义 |
|---|---|
| `gravity="0 0 -9.81"` | 重力向下，单位 m/s² |
| `timestep="0.002"` | 一次物理计算前进 0.002 秒 |
| `type="plane"` | 地面 |
| `pos="0 0 1.5"` | 小球初始中心高度 1.5 米 |
| `<freejoint/>` | 允许球自由平移和旋转 |
| `type="sphere" size="0.1"` | 半径 0.1 米的球 |
| `mass="1"` | 质量 1 千克 |
| `rgba` | 红、绿、蓝、不透明度，各取 0～1 |

练习：将球的 `pos="0 0 1.5"` 改成 `pos="0 0 2.5"`，按 Ctrl+S 保存，关闭记事本，再运行小球命令。下落距离应该增加。只修改数字，保留英文引号和 XML 标签。

## 8. 第二个模型：用电机驱动摆杆

```bat
python run_demo.py --model pendulum --seconds 20
```

你应该看到蓝色摆杆绕固定点摆动。初始角度为 0.5 弧度（约 28.6 度），电机施加正弦变化的力矩。

比较没有电机输出和有电机输出：

```bat
python run_demo.py --model pendulum --amplitude 0 --seconds 20
python run_demo.py --model pendulum --amplitude 4 --seconds 20
```

两条命令顺序运行。第一段在重力作用下自由摆动并逐渐衰减；第二段有周期性的电机驱动。幅值允许 0～5，单位在本模型中为 N·m，因为电机传动比为 1。

打开脚本：

```bat
notepad "%MJROOT%\tutorial\run_demo.py"
```

理解这几个关键动作即可：

| 代码 | 作用 |
|---|---|
| `MjModel.from_xml_path(...)` | 读取模型结构 |
| `MjData(model)` | 创建位置、速度等动态状态 |
| `data.qpos` | 位置；本摆杆唯一的元素是关节角度 |
| `data.qvel` | 速度；本摆杆为角速度 |
| `data.ctrl[0] = control` | 设置第一个电机的输入 |
| `mj_step(model, data)` | 推进一次物理计算 |
| `viewer.sync()` | 同步窗口与仿真状态 |

注意：自由运动的小球有 7 个位置分量（3 个坐标加 4 个四元数分量），6 个速度分量；不能认为所有模型的 `qpos[0]` 都是关节角。脚本打印的 `nq`、`nv`、`nu` 分别是位置、速度和控制输入维数。

电机输入由 `amplitude * sin(2 * pi * 0.5 * time)` 产生，频率为 0.5 Hz，即每 2 秒重复一次。这里是预先规定的控制信号，不是自动学习到的策略。

## 9. 保存和查看实验数据

每次运行自动保存 CSV。相同模型的新运行会覆盖该模型旧 CSV；需要保留时，先复制旧文件并改名。

```bat
notepad "%MJROOT%\tutorial\output\pendulum.csv"
```

每一行依次是仿真时间（秒）、角度（弧度）、电机控制输入；小球文件第二列则是球心高度（米）。可以用记事本打开 CSV，也可以用 Excel 打开。

小球静止时高度约 0.1 米，因为记录的是球心，球有半径。接触求解可能出现微小偏差。

脚本尝试让有窗口的仿真接近真实时间，但电脑较慢时 15 秒仿真可能超过 15 秒钟。

## 10. 下次打开电脑怎么继续？

打开 Anaconda Prompt，按顺序执行下面的命令：

~~~bat
conda activate mujoco-basics
if not exist "%MJROOT%\temp" mkdir "%MJROOT%\temp"
set "TEMP=%MJROOT%\temp"
set "TMP=%MJROOT%\temp"
cd /d "%MJROOT%\tutorial"
python run_demo.py --model pendulum --seconds 20
~~~

先看到 (mujoco-basics)，再运行脚本。首次准备好环境后，不需要重新下载、创建环境或安装库。

想打开官方模型查看器：

~~~bat
python -m mujoco.viewer --mjcf models\pendulum.xml
~~~

空格可暂停/继续。官方查看器不会执行本教程脚本中的正弦控制，效果会与脚本不同。[查看器说明](https://mujoco.readthedocs.io/en/stable/python.html#interactive-viewer)

## 11. 常见问题

| 现象 | 处理方法 |
|---|---|
| 盘符不存在 | 检查所选非 C 盘是否存在；首次配置时更正第三节和 6.1 的盘符 |
| 找不到 mujoco-basics 环境 | 打开与安装时相同的 Anaconda Prompt，执行 conda env list；检查 6.1 的 envs_dirs 配置 |
| 找不到 run_demo.py | 在 Anaconda Prompt 中执行第十节的 cd 命令；检查解压后是否多套了一层目录 |
| `No module named mujoco` | 先执行 conda activate mujoco-basics，检查 python 路径，再按 6.5 安装 |
| 下载超时、连接失败 | 确认网络能访问报错中的域名，网络恢复后重试失败步骤；不要关闭证书验证 |
| GitHub 下载失败 | 可使用已获取的教程 ZIP，按第四节放置文件；Miniconda/Python 下载仍需要可用网络 |
| GLFW、OpenGL、窗口黑屏 | 保留终端完整报错，检查显卡驱动、本地桌面与远程桌面的图形支持；从电脑或显卡厂商官方渠道更新驱动 |
| DLL load failed | 保留完整报错，检查是否为 x64 Windows，并确认所用 Python 路径；不要从不明网站下载 DLL |
| XML parse error | 检查刚改的引号、标签；从仓库重新复制对应 XML 恢复 |
| 球一开始就落地了 | 正常，下落很快；关闭后重新运行，或提高初始高度 |
| 终端一直不让输入 | 仿真还在运行；关闭窗口，或在终端按 Ctrl+C 停止 |
| 激活后仍显示 (base) | 激活失败；查看上一条错误并执行 conda env list 检查环境名 |

仍有问题时，可在本仓库的 Issues 中反馈，并附上**执行的命令、完整报错文字和下面检查结果**。发布前隐去个人信息，无需提供密码或账号令牌。

~~~bat
conda env list
echo %CONDA_PREFIX%
echo %MJROOT%
where python
python -c "import sys,platform; print(sys.executable); print(platform.platform()); print(platform.machine())"
~~~

## 12. 官方参考与验证说明

- [MuJoCo Python 官方文档](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo XML 参考](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [Conda Windows 安装说明](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html)
- [Conda 环境和缓存目录配置](https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html)

本教程先将 Miniconda 安装到非 C 盘，再在 Anaconda Prompt 中配置 envs_dirs、pkgs_dirs，创建名为 mujoco-basics 的独立环境。pip 缓存随环境保存，临时目录在每次打开的终端中单独设置。更新日期：2026-11-06。

已在 Windows Conda 环境中核对 Python 3.10.20、MuJoCo 3.13.0、NumPy 2.2.6，并运行两个示例各 3 秒的无窗口仿真，均正常完成并生成 CSV。另已通过 cmd.exe 调用现有 Conda，按名字激活环境并运行两个无窗口示例。尚未在全新电脑上完整重走 Miniconda 安装和新建命名环境流程，也未验证图形窗口。基础版本相同不代表显卡驱动、Conda 管理工具版本及全部间接依赖完全相同。
