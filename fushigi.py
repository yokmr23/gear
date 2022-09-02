import copy
import itertools

import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
from matplotlib.widgets import Slider
from matplotlib.path import Path

import gear_profile as gear

# 平歯車と平歯車
m = .14
z1 = 16
x1 = 0.408
z2 = 28
x2 = 0.32


# 内歯車
z3 = 71
x3 = 1.682
z4 = 74
x4 = 0.0

# ang_v = 4 * np.pi / 200   # アニメーション進行速度
ang_v = np.pi / 360.
v_max = 10.
alpha = 20.0/180.0*np.pi    # 圧力角
x_max = 6.5
x_min = -x_max
y_max = x_max
y_min = -y_max
# sun gear and plamet gear
b = gear.make_param(m, z1, x1, 'hira', z2, x2, 'hira')
sun_carrier_distance = b[0]
sun_gear = gear.Gear(**b[1])
planet_gear = gear.Gear(**b[2])
# planet gear and inner gear
c = gear.make_param(m, z2, x2, 'hira', z3, x3, 'a')
in_gear = gear.Gear(**c[2])     # 固定
# planet gear and inner2 gear
d = gear.make_param(m, z2, x2, 'hira', z4, x4, 'a')
in_gear2 = gear.Gear(**d[2])    # 出力
print(
    f'sun-planet distance:{b[0]}, \
    planet-inner distance:{c[0]}, \
    planet-inner2 distance:{d[0]}')


def inner_fig(hazoko_r):
    circle = np.linspace(2*np.pi-0.03, 0.03, 100, endpoint=True)
    circle_max2 = hazoko_r*1.15
    circle_cos2 = [np.nan]
    circle_sin2 = [np.nan]
    circle_cos2 = np.concatenate((circle_cos2, [circle_max2*0.95]))
    circle_sin2 = np.concatenate((circle_sin2, [0.0]))
    circle_cos2 = np.concatenate((circle_cos2, circle_max2*np.cos(circle)))
    circle_sin2 = np.concatenate((circle_sin2, circle_max2*np.sin(circle)))
    circle_cos2 = np.concatenate((circle_cos2, [circle_max2*0.95]))
    circle_sin2 = np.concatenate((circle_sin2, [0.0]))
    circle_x = np.append(circle_cos2, np.nan)
    circle_y = np.append(circle_sin2, np.nan)
    return circle_x, circle_y


# print(sun_carrier_distance)
# 歯車創成
# 太陽ギア 補正なし
x0, y0 = sun_gear.x, sun_gear.y
# 遊星ギア
x30, y30 = planet_gear.x, planet_gear.y
if planet_gear.hasuu0 % 2:
    ho_flag = False
else:
    hosei_ang = 2*np.pi/planet_gear.hasuu0/2
    x30, y30 = gear.rotate_gear(x30, y30, hosei_ang)
    ho_flag = True
# 内歯車　固定
x1, y1 = in_gear.x, in_gear.y
if ho_flag:
    hosei_ang = 2*np.pi/in_gear.hasuu0/2
    x1, y1 = gear.rotate_gear(x1, y1, hosei_ang)
xx, yy = inner_fig(in_gear2.hazoko/2.)
x1 = np.concatenate((x1, xx))
y1 = np.concatenate((y1, yy))
# 内歯車　出力
x2, y2 = in_gear2.x, in_gear2.y
if ho_flag:
    hosei_ang = 2*np.pi/in_gear2.hasuu0/2
    x2, y2 = gear.rotate_gear(x2, y2, hosei_ang)
xx, yy = inner_fig(in_gear2.hazoko/2.)
x2 = np.concatenate((x2, xx))
y2 = np.concatenate((y2, yy))

# fig, ax = plt.subplots(figsize=(6.4, 6.4), facecolor=(.18, .31, .31))
# 初期表示
fig = plt.figure(figsize=(6.4, 6.4), facecolor=(.50, .50, .50))
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
ax.set_title('Magical Planetary Gears (不思議歯車機構)', color='0.8')
ax.set_facecolor('#8addd5')
ax.set_ylim(y_min, y_max)
ax.set_xlim(x_min, x_max)
a0 = 1+in_gear.hasuu0/sun_gear.hasuu0
a1 = 1-in_gear.hasuu0/in_gear2.hasuu0
gear_ratio = f'{a0/a1:.2f}'
print(gear_ratio)
str1 = "Sun gear(tomato): Input\n" +\
    "Inner gear(green): Output\n" +\
    "Inner gear(orange): fixed\n" +\
    "gear ratio = 1/"+gear_ratio
ax.text(x_min+0.2, y_max-1.5, str1)
# y軸
ax.plot([0.0, 0.0], [y_max, -y_max], color='purple',
        linestyle='-.', linewidth=0.4, alpha=0.5)
# x軸
ax.plot([-x_max, x_max], [0.0, 0.0], color='purple',
        linestyle='-.', linewidth=0.4, alpha=0.5)
# キャリア中心円
circle = np.linspace(2*np.pi, 0, 100, endpoint=True)
ax.plot(sun_carrier_distance*np.cos(circle),
        sun_carrier_distance*np.sin(circle),
        color='purple', linestyle='-.', linewidth=0.4, alpha=0.5)


# sun gear
xy0 = np.column_stack((x0, y0))
patch0 = patches.PathPatch(
    Path(xy0, sun_gear.code), facecolor='tomato',
    edgecolor='b', alpha=0.7, lw=0.5,
    transform=ax.transData)
ax.add_patch(patch0)
# carrier gears
xy30 = np.column_stack((x30, y30))
patch30 = patches.PathPatch(
    Path(xy30, planet_gear.code), facecolor='aqua', edgecolor='b',
    lw=0.5, alpha=0.7, transform=ax.transData,)
ax.add_patch(patch30)
patch31 = copy.copy(patch30)
ax.add_patch(patch31)
patch32 = copy.copy(patch30)
ax.add_patch(patch32)
carrier = [patch30, patch31, patch32]

# inner gears　固定
xy1 = np.column_stack((x1, y1))
patch1 = patches.Polygon(
    xy1, facecolor='orange', edgecolor='r',
    alpha=0.8, transform=ax.transData)
ax.add_patch(patch1)

# inner gears 2 出力
xy2 = np.column_stack((x2, y2))
patch2 = patches.Polygon(
    xy2, facecolor='green', edgecolor='m',
    alpha=0.8, transform=ax.transData)
ax.add_patch(patch2)

axsp = plt.axes([0.25, 0.06, 0.6, 0.03])
sp_slider = Slider(
    ax=axsp,
    label='Sun gear 角速度比',
    valmin=1.,
    valmax=v_max,
    valinit=1.,
)
ang_v1 = ang_v


def update(val):
    global ang_v1
    ang_v1 = ang_v*val


sp_slider.on_changed(update)


def data_gen():
    for cnt in itertools.count():
        if cnt > 1000:
            break
        else:
            if cnt < 1:
                ang_sun = 0.
                ang_planet = 0.
                ang_carrier = 0.
            ang_inner = 0
            ang_sun += ang_v1
            ang_planet -= ang_v1*sun_gear.hasuu0/planet_gear.hasuu0 / \
                (1 + sun_gear.hasuu0/in_gear.hasuu0)
            ang_carrier += ang_v1*sun_gear.hasuu0/in_gear.hasuu0 / \
                (1 + sun_gear.hasuu0/in_gear.hasuu0)
            ang_inner_out = ang_sun / \
                ((1+in_gear.hasuu0/sun_gear.hasuu0) /
                 (1-in_gear.hasuu0/in_gear2.hasuu0))
        yield ang_sun, ang_carrier, ang_planet, ang_inner, ang_inner_out


def init():
    # print('Init')
    # ax.set_aspect('equal')
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    # return line0, line1, line30, line31, line32, line2,
    # return patch, line1, line30, line31, line32, line2,
    return patch0, patch1, patch30, patch31, patch32, patch2,


def run(data):
    # v_sun 太陽ギア積算角度
    # v_car キャリア積算角度
    # v_planet キャリアギアの積算角度
    # 内歯車固定
    # 内歯車積算角度
    v_sun, v_car, v_planet, v_in, v_out = data
    # 太陽ギア固定
    # ang1 = v_planet - a0 + h
    # 太陽ギアをUpdate
    tr0 = Affine2D().rotate(v_sun) + ax.transData
    patch0.set(transform=tr0)
    # carrier gear の中心位置を太陽ギアの中心からsun_carrier_distamceだけ移動
    # して、ang1自転する
    # ang1   # 太陽ギア自転角速度
    # v_car1   # キャリアー公転角速度
    for i in range(3):
        ang1 = v_planet + 2*np.pi/3*i
        v_car1 = v_car + 2*np.pi/3*i
        tr = Affine2D().rotate(ang1).translate(
            sun_carrier_distance, 0).rotate(v_car1) + ax.transData
        carrier[i].set(transform=tr)
    # 内歯車2を回転
    tr2 = Affine2D().rotate(v_out) + ax.transData
    # 内歯車2をupdate
    patch2.set(transform=tr2)

    return patch0, patch1, patch30, patch31, patch32, patch2


ani = animation.FuncAnimation(
    fig, run, data_gen,
    interval=100,
    init_func=init,
    repeat=False,
    blit=False,
    save_count=200)
# ani.save("fusigi.gif", writer="gif")
plt.show()
