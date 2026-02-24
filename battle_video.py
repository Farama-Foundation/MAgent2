"""MAgent2 Battle 可视化 - 纯 numpy 渲染 + ffmpeg 合成视频

不依赖 pygame，直接从环境底层数据画网格图。
红队 = 红色，蓝队 = 蓝色，空地 = 白色。
先保存 BMP 帧文件，再用 ffmpeg 合成 mp4。
"""

import os
import struct
import subprocess
import numpy as np


def write_bmp(filepath, img):
    """写一个 24-bit BMP 文件 (不需要 PIL)"""
    h, w, _ = img.shape
    # BMP 行需要 4 字节对齐
    row_size = (w * 3 + 3) & ~3
    padding = row_size - w * 3
    pixel_size = row_size * h

    # BMP header (14 bytes) + DIB header (40 bytes)
    header = struct.pack('<2sIHHI', b'BM', 54 + pixel_size, 0, 0, 54)
    dib = struct.pack('<IiiHHIIiiII', 40, w, h, 1, 24, 0, pixel_size, 2835, 2835, 0, 0)

    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(dib)
        # BMP 存储是从下到上，BGR 顺序
        pad_bytes = b'\x00' * padding
        for y in range(h - 1, -1, -1):
            row = img[y]
            # RGB -> BGR
            f.write(row[:, ::-1].tobytes())
            if padding:
                f.write(pad_bytes)


def render_frame(env, handles, map_size, cell_size=10):
    """从环境底层数据手动渲染一帧 RGB 图像"""
    h = w = map_size * cell_size
    img = np.full((h, w, 3), 240, dtype=np.uint8)  # 浅灰背景

    # 画网格线
    for i in range(0, h, cell_size):
        img[i, :] = [220, 220, 220]
        img[:, i] = [220, 220, 220]

    # 画墙壁 (深灰)
    walls = env._get_walls_info()
    for wx, wy in walls:
        y0, y1 = wy * cell_size, (wy + 1) * cell_size
        x0, x1 = wx * cell_size, (wx + 1) * cell_size
        if 0 <= y0 < h and 0 <= x0 < w:
            img[y0:y1, x0:x1] = [100, 100, 100]

    # 红队和蓝队
    colors = [(220, 50, 50), (50, 50, 220)]
    for i, handle in enumerate(handles):
        positions = env.get_pos(handle)
        alive = env.get_alive(handle)
        color = colors[i % 2]
        for j in range(len(positions)):
            if alive[j]:
                px, py = positions[j]
                y0 = py * cell_size + 1
                x0 = px * cell_size + 1
                y1 = y0 + cell_size - 2
                x1 = x0 + cell_size - 2
                if 0 <= y0 < h and 0 <= x0 < w:
                    img[max(0,y0):min(h,y1), max(0,x0):min(w,x1)] = color

    return img


def run_battle_video(output_path="battle_video.mp4", map_size=45, max_cycles=200):
    from magent2.environments.battle.battle import parallel_env as battle_parallel_env

    env = battle_parallel_env(map_size=map_size, max_cycles=max_cycles)
    observations, infos = env.reset()

    inner_env = env.env
    handles = env.handles

    # 创建临时帧目录
    frame_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_frames")
    os.makedirs(frame_dir, exist_ok=True)

    print(f"=== Battle Video Generation ===")
    print(f"Map: {map_size}x{map_size}, max_cycles: {max_cycles}")

    # 第一帧
    frame = render_frame(inner_env, handles, map_size)
    write_bmp(os.path.join(frame_dir, "frame_0000.bmp"), frame)
    cycle = 0

    while env.agents:
        actions = {agent: env.action_space(agent).sample() for agent in env.agents}
        observations, rewards, terminations, truncations, infos = env.step(actions)
        cycle += 1

        frame = render_frame(inner_env, handles, map_size)
        write_bmp(os.path.join(frame_dir, f"frame_{cycle:04d}.bmp"), frame)

        if cycle % 25 == 0:
            red = sum(1 for a in env.agents if a.startswith("red"))
            blue = sum(1 for a in env.agents if a.startswith("blue"))
            print(f"  cycle {cycle:>4d}: red={red:>3d}, blue={blue:>3d}")

    env.close()
    print(f"\nSimulation done! {cycle + 1} frames saved.")

    # ffmpeg 从图片序列合成视频
    fps = 10
    input_pattern = os.path.join(frame_dir, "frame_%04d.bmp")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        output_path,
    ]

    print(f"Encoding video with ffmpeg ...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_kb = os.path.getsize(output_path) / 1024
        duration = (cycle + 1) / fps
        print(f"Done! {output_path} ({size_kb:.0f} KB, {duration:.1f}s)")
    else:
        print(f"ffmpeg error:\n{result.stderr}")

    # 清理帧文件
    import glob
    for f in glob.glob(os.path.join(frame_dir, "*.bmp")):
        os.remove(f)
    os.rmdir(frame_dir)
    print("Temp frames cleaned up.")


if __name__ == "__main__":
    run_battle_video()
