import copy
import itertools

import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from matplotlib.widgets import RadioButtons

import gear_profile as gear

# 平歯車と平歯車
m = 1
z1 = 15
x1 = 0.0
z2 = 18
x2 = 0.0


# 内歯車
z3 = 51
x3 = 0
# ang_v = 4 * np.pi / 200   # アニメーション進行速度
ang_v = 2 * np.pi / 1000
alpha = 20.0 / 180.0 * np.pi  # 圧力角
x_max = 30
x_min = -x_max
y_max = x_max
y_min = -y_max
str0 = [
    "Solar type\nSun gear fixed\n" + f"inner/carrier={1+z1/z3:.3f}",
    "Star type\nCarrier fixed\n" + f"inner/sun={-z1/z3:.3f}",
    "Planetary type\nInner gear fixed\n" + f"carrier/sun={z1/(z1+z3):.3f}",
]

d, g1, g2 = gear.make_param(m, z1, x1, "hira", z2, x2, "hira")
sun_carrier_distance = d
# sun_gear = gear.Gear(z1, m, x1, b[1], b[2])         # 固定
sun_gear = gear.Gear(**g1)
planet_gear = gear.Gear(**g2)
c, g1, g2 = gear.make_param(m, z2, x2, "hira", z3, x3, "a")
in_gear2 = gear.Gear(**g2)  # 出力
print(
    f"distance between sun and planet  :{d}"
    "\n"
    f"distance between planet and inner:{c}"
)
# inner gear 外側


def inner_fig(hazoko_r):
    circle = np.linspace(2 * np.pi - 0.03, 0.03, 100, endpoint=True)
    circle_max2 = hazoko_r * 1.15
    circle_cos2 = [np.nan]
    circle_sin2 = [np.nan]
    circle_cos2 = np.concatenate((circle_cos2, [circle_max2 * 0.95]))
    circle_sin2 = np.concatenate((circle_sin2, [0.0]))
    circle_cos2 = np.concatenate((circle_cos2, circle_max2 * np.cos(circle)))
    circle_sin2 = np.concatenate((circle_sin2, circle_max2 * np.sin(circle)))
    circle_cos2 = np.concatenate((circle_cos2, [circle_max2 * 0.95]))
    circle_sin2 = np.concatenate((circle_sin2, [0.0]))
    circle_x = np.append(circle_cos2, np.nan)
    circle_y = np.append(circle_sin2, np.nan)
    return circle_x, circle_y


# 歯車創成
# 太陽ギア 位相補正なし
x0, y0 = sun_gear.x, sun_gear.y
# 遊星ギア
x30, y30 = planet_gear.x, planet_gear.y
# 歯車噛み合い位相合わせ
if planet_gear.hasuu0 % 2:
    ho_flag = False
else:
    hosei_ang = 2 * np.pi / planet_gear.hasuu0 / 2
    x30, y30 = gear.rotate_gear(x30, y30, hosei_ang)
    ho_flag = True
# 内歯車　出力
# x2, y2 = in_gear2.generate_haguruma()
x2, y2 = in_gear2.x, in_gear2.y
# 歯車噛み合い位相合わせ
if ho_flag:
    hosei_ang = 2 * np.pi / in_gear2.hasuu0 / 2
    x2, y2 = gear.rotate_gear(x2, y2, hosei_ang)
xx, yy = inner_fig(in_gear2.hazoko / 2.0)
x2 = np.concatenate((x2, xx))
y2 = np.concatenate((y2, yy))

# 初期表示
fig = plt.figure(figsize=(6.4, 6.4), facecolor=(0.5, 0.5, 0.6))
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# 各ギアのオブジェクト設定

# sun gearをpatch
xy0 = np.column_stack((x0, y0))
# patch0 = Polygon(xy0, facecolor='tomato', edgecolor='b', alpha=0.8)
patch0 = mpatches.PathPatch(
    Path(xy0, sun_gear.code), facecolor="tomato", edgecolor="b", lw=0.4, alpha=0.8
)
ax.add_patch(patch0)
# carrier gearsをpatch
xy30 = np.column_stack((x30, y30))
# patch30 = Polygon(xy30, facecolor='aqua', edgecolor='b', alpha=0.8)
patch30 = mpatches.PathPatch(
    Path(xy30, planet_gear.code), facecolor="aqua", edgecolor="b", lw=0.4, alpha=0.8
)
ax.add_patch(patch30)
patch31 = copy.copy(patch30)
ax.add_patch(patch31)
patch32 = copy.copy(patch30)
ax.add_patch(patch32)
carrier = [patch30, patch31, patch32]
# inner gears をpatch
xy2 = np.column_stack((x2, y2))
# patch2 = Polygon(xy2, facecolor='green', edgecolor='m', alpha=0.8)
patch2 = mpatches.PathPatch(
    Path(xy2), facecolor="green", edgecolor="b", lw=0.4, alpha=0.8
)
ax.add_patch(patch2)
# ax.cla()
ax.set_title("Planetary Gears (遊星歯車機構)", color="0.8")
ax.set_facecolor("#8addd5")
ax.set_ylim(y_min, y_max)
ax.set_xlim(x_min, x_max)
tx = ax.text(0.02, 0.92, str0[0], transform=ax.transAxes)
# y軸
ax.plot(
    [0.0, 0.0],
    [y_max, -y_max],
    color="purple",
    linestyle="-.",
    linewidth=0.4,
    alpha=0.5,
)
# x軸
ax.plot(
    [-x_max, x_max],
    [0.0, 0.0],
    color="purple",
    linestyle="-.",
    linewidth=0.4,
    alpha=0.5,
)

sp_sun = 0.0
sp_car = 1.0
flag = True


def gearfunc(label):
    """
    RaidoButtonが変更された時
    """
    global sp_sun, sp_car, flag
    if label == "Sun":
        sp_sun = 0
        sp_car = 1.0
        flag = True
        tx.set(text=str0[0])
    elif label == "Carrier":
        sp_car = 0.0
        sp_sun = 1.0
        flag = True
        tx.set(text=str0[1])
    else:
        flag = False
        sp_car = 1.0
        tx.set(text=str0[2])


rax = plt.axes([0.05, 0.05, 0.15, 0.15])
radio = RadioButtons(rax, ("Sun", "Carrier", "Inner"))
radio.on_clicked(gearfunc)


def data_gen():
    for cnt in itertools.count():
        if cnt > 2000:
            break
        else:
            if cnt == 0:
                ang_sun = 0.0
                ang_carrier = 0.0
                ang_inner = 0.0
                ang_planet = 0.0
            if flag:
                ang_sun -= ang_v * sp_sun
                ang_carrier += ang_v * sp_car
                ang_planet += (
                    ang_v * abs(sp_car - sp_sun) * sun_gear.hasuu0 / planet_gear.hasuu0
                )
                ang_inner += (
                    ang_v * sp_car * (sun_gear.hasuu0 / in_gear2.hasuu0 + 1)
                    + ang_v * sp_sun * sun_gear.hasuu0 / in_gear2.hasuu0
                )
            else:
                ang_carrier += ang_v * sp_car
                ang_planet -= ang_v * sp_car * in_gear2.hasuu0 / planet_gear.hasuu0
                ang_sun += (
                    ang_v
                    * sp_car
                    * (in_gear2.hasuu0 + sun_gear.hasuu0)
                    / sun_gear.hasuu0
                )

        yield ang_sun, ang_carrier, ang_planet, ang_inner


def init():
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)
    ax.set_aspect("equal")
    return (
        patch0,
        patch30,
        patch31,
        patch32,
        patch2,
    )


def run(data):
    # v_sun 太陽ギア積算角度
    # v_car キャリア積算角度
    # v_planet キャリアギアの積算角度
    # 内歯車固定
    # 内歯車積算角度
    v_sun, v_car, v_planet, v_out = data
    # 太陽ギア固定
    # ang1 = v_planet - a0 + h
    # 太陽ギアをUpdate
    tr0 = Affine2D().rotate(v_sun) + ax.transData
    patch0.set(transform=tr0)
    # carrier gear の中心位置を太陽ギアの中心からsun_carrier_distamceだけ移動
    # して、ang1自転する
    # ang1 = v_planet  # 太陽ギア自転角速度
    # v_car1 = v_car  # キャリアー公転角速度
    for i in range(3):
        ang1 = v_planet + 2 * np.pi / 3 * i
        v_car1 = v_car + 2 * np.pi / 3 * i
        tr = (
            Affine2D().rotate(ang1).translate(sun_carrier_distance, 0).rotate(v_car1)
            + ax.transData
        )
        carrier[i].set(transform=tr)
    # 内歯車2を回転
    tr2 = Affine2D().rotate(v_out) + ax.transData
    # 内歯車2をupdate
    patch2.set(transform=tr2)

    return patch0, patch30, patch31, patch32, patch2


ani = animation.FuncAnimation(
    fig,
    run,
    data_gen,
    interval=10,
    init_func=init,
    blit=False,
    repeat=False,
    save_count=50,
)
# ani.save("pranetary1.gif", writer="gif")
plt.show()
