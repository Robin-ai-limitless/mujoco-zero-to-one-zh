# 从零开始使用 MuJoCo：Windows 中文教程

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

## 3. 指定非 C 盘目录（每次新开终端都先执行）

打开“此电脑”，确认有没有 D 盘。没有 D 盘时，只把下面第一行的 D: 改成 E: 或你的实际非 C 盘盘符。使用示例中的英文目录名，不要添加空格。建议预留至少 5 GB 空间。

这一节只是“指定存放位置、创建必要文件夹”，还没有安装 Python 或 MuJoCo。意思是先告诉电脑：安装程序、Conda、环境、下载缓存与临时文件，都放到 MuJoCoLab 文件夹里。

| 名称或命令 | 作用 |
|---|---|
| $Root | 总文件夹地址 |
| if 开头的几行 | 检查盘符与路径，填错就停下 |
| New-Item | 创建必要文件夹 |
| $Conda | 后续调用的 Conda 程序位置 |
| $EnvDir、$Py | 本教程的环境目录和其中的 Python 程序位置 |
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

成功标志：显示总目录和 Miniconda 的安装目标目录，均在非 C 盘。这些变量只对当前终端及其启动程序有效，重开终端后重新执行本节。Conda 可能在用户目录保存少量登记或配置文件；这里重定向的是环境、安装文件及主要缓存，不承诺系统盘零写入。

如果你之前照旧版教程安装过 uv，不用删除它。本版在独立的 mujoco-basics 文件夹创建 Conda 环境，不复用旧版的环境。已经按本版安装成功的人，下次只执行本节和第十节，不重复安装。

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

Conda 负责创建和管理环境；Miniconda 是带有 Conda 的精简安装包。安装包自带的 base Python 版本可以不同，第六节会单独创建 Python 3.10.20 的本教程的环境。

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
5. 点击 Install，等待完成，再点击 Finish，回到原来的 PowerShell。

如果提示目录已有文件，先停止安装。已有本教程的 conda.exe 时直接执行下面的检查；不要覆盖已有 Conda 安装或手动删除旧环境。

~~~powershell
if (-not (Test-Path $Conda)) { throw 'Conda not found. Check the installation folder.' }
& $Conda --version
if ($LASTEXITCODE -ne 0) { throw 'Conda check failed.' }
& $Conda config --show envs_dirs pkgs_dirs
if ($LASTEXITCODE -ne 0) { throw 'Conda path check failed.' }
~~~

成功标志：显示 Conda 版本；envs_dirs 和 pkgs_dirs 指向第三节指定的非 C 盘目录。不要另开窗口继续。

## 6. 创建固定版本的基础环境

### 6.1 安装 Python 3.10.20

~~~powershell
& $Conda create --prefix $EnvDir --override-channels --channel https://repo.anaconda.com/pkgs/main python=3.10.20 pip
if ($LASTEXITCODE -ne 0) { throw 'Environment creation failed. Stop here.' }
~~~

看到 Proceed ([y]/n)? 时，输入 y 并回车。这表示确认安装列出的软件包。

首次使用 Anaconda 软件源时可能要求阅读并接受其服务条款。请根据终端提示阅读并自行决定；如果出现 TosNonInteractiveError，先按错误提示完成对应软件源的条款流程，再重试本节。不要跳过错误继续安装。如果提示找不到这个精确的 Python 版本，保留完整报错并通过仓库 Issues 反馈，不要自行换成其他版本。

### 6.2 安装固定版本 MuJoCo 与 NumPy

~~~powershell
& $Conda run --no-capture-output -p $EnvDir python -m pip install "mujoco==3.13.0" "numpy==2.2.6"
if ($LASTEXITCODE -ne 0) { throw 'Package installation failed. Stop here.' }
~~~

本教程使用官方 mujoco 包，不使用旧的 mujoco-py。运行库随 Python 包一起安装，无需另下引擎。[官方说明](https://mujoco.readthedocs.io/en/stable/python.html#installation)

后续命令中的 Conda run 是“在指定环境里执行程序”。这样会准备环境需要的路径，不必手动激活环境，也不用修改 PowerShell 启动脚本。使用完整命令，不要删掉前半段。

### 6.3 检查版本及位置

~~~powershell
& $Conda run --no-capture-output -p $EnvDir python -c "import sys,mujoco,numpy; print('Python:',sys.version.split()[0]); print('Python path:',sys.executable); print('MuJoCo:',mujoco.__version__); print('NumPy:',numpy.__version__); print('Package:',mujoco.__file__); assert sys.version_info[:3]==(3,10,20), 'Python version mismatch'; assert mujoco.__version__=='3.13.0', 'MuJoCo version mismatch'; assert numpy.__version__=='2.2.6', 'NumPy version mismatch'; print('VERSION CHECK PASSED')"
if ($LASTEXITCODE -ne 0) { throw 'Version check failed. Stop here.' }
~~~

必须同时满足：

- Python 显示 3.10.20。
- MuJoCo 显示 3.13.0。
- NumPy 显示 2.2.6。
- Python path 和 Package 均在所选非 C 盘的 envs\mujoco-basics 下。
- 最后显示 VERSION CHECK PASSED。

完成本节后即可运行后面的两个示例。机器人模型和强化学习训练依赖需要按相应项目的说明另行配置。

### 6.4 保存本机依赖记录

~~~powershell
& $Conda run --no-capture-output -p $EnvDir python -m pip freeze | Set-Content -Encoding UTF8 "$Project\requirements-local.txt"
if ($LASTEXITCODE -ne 0) { throw 'Package export failed.' }
Get-Content "$Project\requirements-local.txt"
~~~

这是本机安装记录，便于排错；教程固定 Python、MuJoCo、NumPy 的版本，其他间接依赖仍可能随安装日期不同而变化。

## 7. 第一个模型：小球落地

先进行不打开窗口的计算，判断引擎是否正常：

```powershell
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model ball --headless --seconds 3
```

成功标志：出现 `Finished`，并在 `tutorial\output` 下生成 `ball.csv`。不打开窗口时跑得很快，这是正常的。

再打开窗口：

```powershell
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model ball --seconds 15
```

你应该看到橙色小球从空中掉落，最后停在地面。默认 15 秒仿真后关闭，也可以点击窗口右上角关闭。球下落很快，想再看一次就重新运行该命令。

鼠标左键拖动可旋转视角，滚轮可缩放。不要连续启动许多窗口；关闭上一次窗口再运行下一个命令。终端在窗口运行期间没有新提示符，是程序仍在工作。

打开模型看看：

```powershell
notepad "$Project\models\ball.xml"
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

```powershell
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model pendulum --seconds 20
```

你应该看到蓝色摆杆绕固定点摆动。初始角度为 0.5 弧度（约 28.6 度），电机施加正弦变化的力矩。

比较没有电机输出和有电机输出：

```powershell
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model pendulum --amplitude 0 --seconds 20
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model pendulum --amplitude 4 --seconds 20
```

两条命令顺序运行。第一段在重力作用下自由摆动并逐渐衰减；第二段有周期性的电机驱动。幅值允许 0～5，单位在本模型中为 N·m，因为电机传动比为 1。

打开脚本：

```powershell
notepad "$Project\run_demo.py"
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

```powershell
Get-Content "$Project\output\pendulum.csv" -TotalCount 10
```

每一行依次是仿真时间（秒）、角度（弧度）、电机控制输入；小球文件第二列则是球心高度（米）。可以用记事本打开 CSV，也可以用 Excel 打开。

小球静止时高度约 0.1 米，因为记录的是球心，球有半径。接触求解可能出现微小偏差。

脚本尝试让有窗口的仿真接近真实时间，但电脑较慢时 15 秒仿真可能超过 15 秒钟；无窗口模式不刻意等待。

## 10. 下次开机怎么继续

**不要重新安装。** 打开 PowerShell，重新复制执行第三节全部命令，然后运行：

```powershell
& $Conda run --no-capture-output -p $EnvDir python "$Project\run_demo.py" --model pendulum --seconds 20
```

日常只需要“第三节设置路径 + 一条运行命令”。想查看模型，也可以使用官方查看器：

```powershell
& $Conda run --no-capture-output -p $EnvDir python -m mujoco.viewer --mjcf "$Project\models\pendulum.xml"
```

官方查看器中可以用空格暂停/继续；它不会自动执行本教程 Python 脚本里的正弦控制，所以效果与脚本不同。[查看器文档](https://mujoco.readthedocs.io/en/stable/python.html#interactive-viewer)

## 11. 常见问题

| 现象 | 处理方法 |
|---|---|
| 盘符不存在 | 重新执行第三节，将第一行换成实际存在的非 C 盘路径 |
| `&` 后表达式无效、变量为空 | 新开终端后忘了第三节；完整重做第三节 |
| 找不到 `run_demo.py` | 第四节检查必须全部为 True；通常多套了一层解压目录 |
| `No module named mujoco` | 使用本教程完整的 Conda run 命令，不要直接用电脑上其他 Python；重做第六节安装包部分 |
| 下载超时、连接失败 | 确认网络能访问报错中的域名，网络恢复后重试失败步骤；不要关闭证书验证 |
| GitHub 下载失败 | 可使用已获取的教程 ZIP，按第四节放置文件；Miniconda/Python 下载仍需要可用网络 |
| GLFW、OpenGL、窗口黑屏 | 先跑 `--headless`。如果计算成功，优先检查显卡驱动、本地桌面与远程桌面的图形支持；从电脑或显卡厂商官方渠道更新驱动 |
| DLL load failed | 保留完整报错，检查是否为 x64 Windows，并确认所用 Python 路径；不要从不明网站下载 DLL |
| XML parse error | 检查刚改的引号、标签；从仓库重新复制对应 XML 恢复 |
| 球一开始就落地了 | 正常，下落很快；关闭后重新运行，或提高初始高度 |
| 终端一直不让输入 | 仿真还在运行；关闭窗口，或在终端按 Ctrl+C 停止 |
| PowerShell 出现 `>>` | 通常是只粘贴了半段代码或缺少引号；Ctrl+C 取消后重新复制完整代码框 |

仍有问题时，可在本仓库的 Issues 中反馈，并附上**执行的命令、完整报错文字和下面检查结果**。发布前隐去个人信息，无需提供密码或账号令牌。

```powershell
Write-Host "Root=$Root"
Write-Host "Project=$Project"
Write-Host "Python=$Py"
Test-Path $Py
Test-Path "$Project\run_demo.py"
if (Test-Path $Py) { & $Conda run --no-capture-output -p $EnvDir python -c "import sys,platform; print(sys.executable); print(platform.platform()); print(platform.machine())" }
```

## 12. 完成标准与下一步

- 环境路径检查全部指向非 C 盘。
- 无窗口计算成功，生成 CSV。
- 能看到小球落地，并能修改初始高度。
- 能看到摆杆运动，并比较两个电机幅值的效果。
- 关闭终端后，能按第十节重新运行。

完成这些再学习多关节机器人、传感器、PD 控制、Gymnasium 接口和强化学习。不要第一节就加入机器人模型、训练框架与 CUDA，排查问题会困难很多。

## 官方参考与验证说明

- [MuJoCo Python 官方文档](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo XML 参考](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [Conda Windows 安装说明](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html)
- [Conda 环境和缓存目录配置](https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html)

本教程使用 Miniconda 的自定义安装目录、CONDA_ENVS_PATH、CONDA_PKGS_DIRS、pip 缓存及当前进程临时目录设置，将环境和主要缓存放到非 C 盘。更新日期：2026-11-06。

已在 Windows Conda 环境中核对 Python 3.10.20、MuJoCo 3.13.0、NumPy 2.2.6，并运行两个示例各 3 秒的无窗口仿真，均正常完成并生成 CSV。尚未在全新电脑上完整重走 Miniconda 安装流程，也未验证图形窗口。基础版本相同不代表显卡驱动、Conda 管理工具版本及全部间接依赖完全相同。
