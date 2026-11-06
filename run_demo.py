"""Run with the tutorial virtual environment; paths are relative to this file."""
import argparse
import csv
import math
import time
from pathlib import Path

import mujoco

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["ball", "pendulum"], default="ball")
    parser.add_argument("--seconds", type=float, default=15)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--amplitude", type=float, default=2)
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be finite and positive")
    if not math.isfinite(args.amplitude) or not 0 <= args.amplitude <= 5:
        parser.error("--amplitude must be between 0 and 5")
    model = mujoco.MjModel.from_xml_path(str(ROOT / "models" / f"{args.model}.xml"))
    data = mujoco.MjData(model)
    if args.model == "pendulum":
        data.qpos[0] = 0.5
    mujoco.mj_forward(model, data)
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    filename = output / f"{args.model}.csv"
    print(f"MuJoCo {mujoco.__version__}; nq={model.nq}, nv={model.nv}, nu={model.nu}")

    with filename.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "height_m" if args.model == "ball" else "angle_rad", "control"])

        def step():
            control = args.amplitude * math.sin(2 * math.pi * 0.5 * data.time)
            if model.nu:
                data.ctrl[0] = control
            mujoco.mj_step(model, data)
            value = data.qpos[2] if args.model == "ball" else data.qpos[0]
            writer.writerow([float(data.time), float(value), control if model.nu else 0])

        if args.headless:
            while data.time < args.seconds:
                step()
        else:
            from mujoco import viewer as mj_viewer
            with mj_viewer.launch_passive(model, data) as viewer:
                with viewer.lock():
                    viewer.cam.lookat[:] = [0, 0, 0.8]
                    viewer.cam.distance = 4
                    viewer.cam.azimuth = 90
                    viewer.cam.elevation = -20
                while viewer.is_running() and data.time < args.seconds:
                    started = time.perf_counter()
                    with viewer.lock():
                        step()
                    viewer.sync()
                    time.sleep(max(0, model.opt.timestep - (time.perf_counter() - started)))
    print(f"Finished: simulation time={data.time:.3f}s; CSV={filename}")


if __name__ == "__main__":
    main()
