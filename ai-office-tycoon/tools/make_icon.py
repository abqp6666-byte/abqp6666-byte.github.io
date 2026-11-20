#!/usr/bin/env python3
"""오늘도 바쁜 AI 사무실 — 런처 아이콘 생성 (픽셀아트, NEAREST 업스케일)"""
import os
from PIL import Image

NAVY   = (27, 36, 55, 255)
NAVY2  = (36, 48, 74, 255)
AMBER  = (255, 179, 71, 255)
AMBER2 = (214, 137, 44, 255)
DARK   = (12, 17, 30, 255)
CYAN   = (158, 241, 255, 255)
GREEN  = (123, 224, 142, 255)
BLUE   = (44, 60, 96, 255)
WHITE  = (255, 253, 245, 255)
GOLD   = (255, 212, 121, 255)

N = 32
img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
px = img.load()


def rect(x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w):
            if 0 <= i < N and 0 <= j < N:
                px[i, j] = c


# 배경 (모서리 픽셀 컷)
rect(0, 0, N, N, NAVY)
for c in range(2):
    for d in range(2 - c):
        for k in range(2 - c):
            px[c * 31 + (0 if c == 0 else 0), 0] = (0, 0, 0, 0)
# 간단한 라운드 컷
cut = [(0, 0), (1, 0), (0, 1), (N - 1, 0), (N - 2, 0), (N - 1, 1),
       (0, N - 1), (1, N - 1), (0, N - 2), (N - 1, N - 1), (N - 2, N - 1), (N - 1, N - 2)]
for (i, j) in cut:
    px[i, j] = (0, 0, 0, 0)

# 바닥 그림자
rect(7, 29, 18, 2, NAVY2)

# 안테나
rect(15, 3, 2, 4, DARK)
rect(14, 1, 4, 3, DARK)
rect(15, 2, 2, 1, GREEN)

# 머리
rect(6, 7, 20, 15, DARK)
rect(7, 8, 18, 13, AMBER)
rect(7, 8, 18, 2, (255, 200, 120, 255))
rect(7, 18, 18, 3, AMBER2)

# 바이저
rect(9, 11, 14, 7, DARK)
rect(10, 12, 12, 5, (20, 30, 48, 255))
rect(11, 13, 3, 2, CYAN)
rect(18, 13, 3, 2, CYAN)
rect(11, 16, 3, 1, (80, 150, 180, 255))
rect(18, 16, 3, 1, (80, 150, 180, 255))

# 옆 볼트
rect(5, 12, 1, 5, DARK)
rect(26, 12, 1, 5, DARK)

# 몸통
rect(8, 21, 16, 6, DARK)
rect(9, 22, 14, 4, BLUE)
rect(14, 22, 4, 4, CYAN)
rect(15, 23, 2, 2, WHITE)

# 팔
rect(6, 22, 2, 4, DARK)
rect(24, 22, 2, 4, DARK)
rect(6, 25, 2, 1, GOLD)
rect(24, 25, 2, 1, GOLD)

# 발
rect(10, 27, 4, 3, DARK)
rect(18, 27, 4, 3, DARK)

OUT = os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "res")
dens = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for name, size in dens.items():
    d = os.path.join(OUT, "mipmap-" + name)
    os.makedirs(d, exist_ok=True)
    big = img.resize((size, size), Image.NEAREST)
    big.save(os.path.join(d, "ic_launcher.png"))

# 미리보기 + README/스토어용 큰 이미지
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "art"), exist_ok=True)
img.resize((512, 512), Image.NEAREST).save(
    os.path.join(os.path.dirname(__file__), "..", "art", "icon-512.png"))
print("icons written")
