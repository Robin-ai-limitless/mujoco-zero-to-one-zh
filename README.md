# 从零开始使用 MuJoCo：Windows 中文教程

面向没有编程基础、只会复制粘贴的朋友。按顺序完成：准备文件夹 → 安装 Python → 安装 MuJoCo → 小球落地 → 电机摆杆 → 保存数据 → 下次重新运行。

**Python、虚拟环境、下载缓存、安装临时目录、模型和实验结果全部放在非 C 盘。** 默认 D 盘；没有 D 盘就用 E 盘。不要为了教程格式化或重新分区。

本教程适用于 Windows 10/11、Intel/AMD 64 位电脑。Mac、Linux 和 Windows ARM 电脑不要直接照抄。简单示例不需要 CUDA、独立显卡、Anaconda、Git 或 VS Code。需要能访问 GitHub、Astral 和 PyPI 的网络。

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

打开“此电脑”，确认有没有 D 盘。**没有 D 盘时，只把下面第一行的 `D:` 改成 `E:` 或你的实际非 C 盘盘符。** 后续命令使用变量，不需要逐行改盘符。

建议可用空间至少 3 GB。这是预留空间，不是安装包大小。

```powershell
$Root = 'D:\MuJoCoLab'
$ErrorActionPreference = 'Stop'
if ($Root -notmatch '^[D-Zd-z]:\\') { throw 'Please choose an absolute path outside C:.' }
if (-not (Test-Path ([IO.Path]::GetPathRoot($Root)))) { throw 'Drive does not exist. Change the first line.' }
New-Item -ItemType Directory -Force -Path $Root | Out-Null
$Root = (Resolve-Path $Root).Path
if ($Root -match '^[Cc]:') { throw 'C: is not allowed.' }
$env:UV_UNMANAGED_INSTALL = "$Root\tools\uv"
$env:UV_CACHE_DIR = "$Root\cache\uv"
$env:UV_PYTHON_INSTALL_DIR = "$Root\python"
$env:UV_PYTHON_BIN_DIR = "$Root\tools\python-bin"
$env:UV_TOOL_DIR = "$Root\tools\uv-tools"
$env:UV_TOOL_BIN_DIR = "$Root\tools\uv-tools-bin"
$env:PIP_CACHE_DIR = "$Root\cache\pip"
$env:TEMP = "$Root\temp"
$env:TMP = "$Root\temp"
New-Item -ItemType Directory -Force -Path $env:TEMP,$env:UV_CACHE_DIR,$env:PIP_CACHE_DIR | Out-Null
$Project = "$Root\tutorial"
$Uv = "$Root\tools\uv\uv.exe"
$Py = "$Root\envs\mujoco\Scripts\python.exe"
Set-Location $Root
Write-Host "Environment root: $Root"
```

成功标志：最后显示 `Environment root: D:\MuJoCoLab`（或你选择的盘符）。这些设置只对当前终端及其启动的程序有效。关掉终端后，重新执行本节即可恢复。

## 4. 下载本教程文件

1. 在本 GitHub 仓库页面点击绿色 **Code** → **Download ZIP**。
2. 浏览器询问保存位置时，选择 `D:\MuJoCoLab`（或你的非 C 盘目录）。如果浏览器默认下载到 C 盘，先在浏览器“设置 → 下载”中启用每次询问保存位置。
3. 右键下载的 ZIP → **全部解压缩**，解压到同一个非 C 盘目录。
4. 打开解压出来的文件夹，找到 `README.md`、`run_demo.py` 和 `models`。
5. 在 `MuJoCoLab` 下新建一个文件夹，命名为 `tutorial`。将上述文件及 `models` 文件夹复制进去。

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

## 5. 安装环境管理工具 uv

uv 负责下载 Python 和安装软件包。以下命令下载官方安装脚本到刚指定的非 C 盘临时目录，再执行安装。执行策略只对这个安装进程放行，不修改整台电脑的策略。

```powershell
Invoke-WebRequest -Uri 'https://astral.sh/uv/install.ps1' -OutFile "$env:TEMP\uv-install.ps1" -UseBasicParsing
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\uv-install.ps1"
if ($LASTEXITCODE -ne 0) { throw 'uv installation failed. Stop here.' }
if (-not (Test-Path $Uv)) { throw 'uv.exe not found. Stop here.' }
& $Uv --version
```

成功标志：打印 `uv` 和版本号。不要另开终端继续；新窗口会丢失第三节的变量。

## 6. 安装 Python 和 MuJoCo

以下使用 Python 3.11。电脑原来有没有 Python 都不影响，我们始终明确指定本教程的程序路径。

```powershell
& $Uv python install 3.11
if ($LASTEXITCODE -ne 0) { throw 'Python download failed.' }
& $Uv venv --python 3.11 --managed-python "$Root\envs\mujoco"
if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
& $Uv pip install --python $Py 'mujoco>=3.3,<4'
if ($LASTEXITCODE -ne 0) { throw 'MuJoCo installation failed.' }
& $Py -c "import sys,mujoco; print('Python:',sys.executable); print('Base:',sys.base_prefix); print('MuJoCo:',mujoco.__version__); print('Package:',mujoco.__file__)"
if ($LASTEXITCODE -ne 0) { throw 'Import check failed.' }
```

成功标志：Python、Base 和 Package 三个路径都在你选择的非 C 盘，MuJoCo 打印版本号。这里不需要手动激活虚拟环境；`& $Py` 已经指向正确环境。

安装的官方 `mujoco` 软件包包含运行库，无需再单独安装引擎。此教程使用官方 Python API，不使用旧的 `mujoco-py`。[官方安装说明](https://mujoco.readthedocs.io/en/stable/python.html#installation)

记录本次安装版本，便于老师与朋友复现：

```powershell
& $Uv pip freeze --python $Py | Set-Content -Encoding UTF8 "$Project\requirements-local.txt"
Get-Content "$Project\requirements-local.txt"
```

本教程安装 3.x 范围内当时可用的版本，并非固定的完整依赖锁定。大家要用完全相同的软件包版本，可以分享生成的 `requirements-local.txt`，让对方在完成前面的 Python 和虚拟环境步骤后执行：

```powershell
& $Uv pip install --python $Py -r "$Project\requirements-local.txt"
```

## 7. 第一个模型：小球落地

先进行不打开窗口的计算，判断引擎是否正常：

```powershell
& $Py "$Project\run_demo.py" --model ball --headless --seconds 3
```

成功标志：出现 `Finished`，并在 `tutorial\output` 下生成 `ball.csv`。不打开窗口时跑得很快，这是正常的。

再打开窗口：

```powershell
& $Py "$Project\run_demo.py" --model ball --seconds 15
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
& $Py "$Project\run_demo.py" --model pendulum --seconds 20
```

你应该看到蓝色摆杆绕固定点摆动。初始角度为 0.5 弧度（约 28.6 度），电机施加正弦变化的力矩。

比较没有电机输出和有电机输出：

```powershell
& $Py "$Project\run_demo.py" --model pendulum --amplitude 0 --seconds 20
& $Py "$Project\run_demo.py" --model pendulum --amplitude 4 --seconds 20
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
& $Py "$Project\run_demo.py" --model pendulum --seconds 20
```

日常只需要“第三节设置路径 + 一条运行命令”。想查看模型，也可以使用官方查看器：

```powershell
& $Py -m mujoco.viewer --mjcf "$Project\models\pendulum.xml"
```

官方查看器中可以用空格暂停/继续；它不会自动执行本教程 Python 脚本里的正弦控制，所以效果与脚本不同。[查看器文档](https://mujoco.readthedocs.io/en/stable/python.html#interactive-viewer)

## 11. 常见问题

| 现象 | 处理方法 |
|---|---|
| 盘符不存在 | 重新执行第三节，将第一行换成实际存在的非 C 盘路径 |
| `&` 后表达式无效、变量为空 | 新开终端后忘了第三节；完整重做第三节 |
| 找不到 `run_demo.py` | 第四节检查必须全部为 True；通常多套了一层解压目录 |
| `No module named mujoco` | 使用 `& $Py`，不要直接用电脑上其他 `python`；重做第六节安装包部分 |
| 下载超时、连接失败 | 确认网络能访问报错中的域名，网络恢复后重试失败步骤；不要关闭证书验证 |
| GitHub 下载失败 | 请老师直接分享教程 ZIP，并按第四节放置文件；uv/Python 下载仍需要可用网络 |
| GLFW、OpenGL、窗口黑屏 | 先跑 `--headless`。如果计算成功，优先检查显卡驱动、本地桌面与远程桌面的图形支持；从电脑或显卡厂商官方渠道更新驱动 |
| DLL load failed | 保留完整报错，检查是否为 x64 Windows，并确认所用 Python 路径；不要从不明网站下载 DLL |
| XML parse error | 检查刚改的引号、标签；从仓库重新复制对应 XML 恢复 |
| 球一开始就落地了 | 正常，下落很快；关闭后重新运行，或提高初始高度 |
| 终端一直不让输入 | 仿真还在运行；关闭窗口，或在终端按 Ctrl+C 停止 |
| PowerShell 出现 `>>` | 通常是只粘贴了半段代码或缺少引号；Ctrl+C 取消后重新复制完整代码框 |

仍有问题时，把**执行的命令、完整报错文字和下面检查结果**交给老师。无需提供密码或账号令牌。

```powershell
Write-Host "Root=$Root"
Write-Host "Project=$Project"
Write-Host "Python=$Py"
Test-Path $Py
Test-Path "$Project\run_demo.py"
if (Test-Path $Py) { & $Py -c "import sys,platform; print(sys.executable); print(platform.platform()); print(platform.machine())" }
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
- [uv 安装目录设置](https://docs.astral.sh/uv/reference/installer/)
- [uv 存储目录说明](https://docs.astral.sh/uv/reference/storage/)

安装流程使用 uv 官方的目录重定向机制；只改工具安装位置不足以移动 Python 和缓存，因此第三节分别配置它们。教程编写日期：2026-11-06。

已在 Windows 的现有 MuJoCo 3.12.0 环境中运行两个示例各 3 秒的无窗口仿真：小球最终球心高度约 0.09963 米，摆杆角度变化且保持有限，CSV 正常生成。已检查 Python 语法和 XML 结构。尚未在全新电脑上完整重走安装流程，也未验证图形窗口；不同电脑的驱动、网络和权限仍需现场验证。
