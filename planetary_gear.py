import gear_profile
import matplotlib.pyplot as plt
# import numpy as np
import matplotlib.animation as animation
import numpy as np
import itertools
import matplotlib.patches as patches

module = 1.0
# ang_v = 4 * np.pi / 200   # アニメーション進行速度
ang_v = 2 * np.pi / 200
alpha = 20.0/180.0*np.pi    # 圧力角
x_max = 28
x_min = -x_max
y_max = x_max
y_min = -y_max
#
# in_gear = gear_profile.Gear(42, module, 0.99502242, fig='a')      # 固定
sun_gear = gear_profile.Gear(15, module, -0.307006)             # 平歯車
planet_gear = gear_profile.Gear(15, module, -0.307006)             # 平歯車
in_gear2 = gear_profile.Gear(45, module, -0.921018, fig='a')    # 出力
# 平歯車と平歯車の中心距離
# 平歯車1の歯数、転位係数　z1 s1
# 平歯車2の歯数、転位係数　z2 s2
# モジュール　m
sun_carrier_distance = gear_profile.get_distance1(
    sun_gear.hasuu0,
    planet_gear.hasuu0,
    sun_gear.mo0,
    sun_gear.shift,
    planet_gear.shift
)

# ギアオブジェクトを回転させる
# X, Y ギアオブジェクト
# ang 回転角　左回転 +　、右回転　-


def init_gear_pos(x, y, ang):
    X = x*np.cos(ang)-y*np.sin(ang)
    Y = y*np.cos(ang)+x*np.sin(ang)
    return X, Y


circle = np.linspace(2*np.pi-0.03, 0.03, 100, endpoint=True)
circle_max2 = in_gear2.get_hasaki_diameter() + 3.
circle_cos2 = [np.nan]
circle_sin2 = [np.nan]
circle_cos2 = np.append(circle_cos2, [circle_max2-2.0])
circle_sin2 = np.append(circle_sin2, [0.0])
circle_cos2 = np.append(circle_cos2, circle_max2*np.cos(circle))
circle_sin2 = np.append(circle_sin2, circle_max2*np.sin(circle))
circle_cos2 = np.append(circle_cos2, [circle_max2-2.0])
circle_sin2 = np.append(circle_sin2, [0.0])

# circle_max = in_gear.get_hasaki_diameter() + 4.0
# circle_cos = [np.nan]
# circle_sin = [np.nan]
# circle_cos = np.append(circle_cos, [circle_max-2.0])
# circle_sin = np.append(circle_sin, [0.0])
# circle_cos = np.append(circle_cos, circle_max*np.cos(circle))
# circle_sin = np.append(circle_sin, circle_max*np.sin(circle))
# circle_cos = np.append(circle_cos, [circle_max-2.0])
# circle_sin = np.append(circle_sin, [0.0])

circle = np.linspace(2*np.pi, 0, 100, endpoint=True)
circle_cos1 = [np.nan]
circle_sin1 = [np.nan]
circle_cos1 = np.append(circle_cos1, 0.4*np.cos(circle))
circle_sin1 = np.append(circle_sin1, 0.4*np.sin(circle))
# print(sun_carrier_distance)
# 歯車創成
# 太陽ギア
x0, y0 = sun_gear.generate_haguruma()
hosei_ang = -sun_gear.a0 - sun_gear.a1/2
x0, y0 = init_gear_pos(x0, y0, hosei_ang)
x0 = np.append(x0, circle_cos1)
y0 = np.append(y0, circle_sin1)
# 遊星ギア
x30, y30 = planet_gear.generate_haguruma()
if planet_gear.hasuu0 % 2:
    hosei_ang = -planet_gear.a0 - planet_gear.a1/2
else:
    hosei_ang = -planet_gear.a0 - planet_gear.a1/2 \
        + 2*np.pi/planet_gear.hasuu0/2
x30, y30 = init_gear_pos(x30, y30, hosei_ang)
x30 = np.append(x30, circle_cos1)
y30 = np.append(y30, circle_sin1)
# 内歯車　固定
# x1, y1 = in_gear.generate_haguruma()
# if planet_gear.hasuu0 % 2:
#    hosei_ang = -in_gear.a0 - in_gear.a1/2
# else:
#    hosei_ang = -in_gear.a0 - in_gear.a1/2 \
#        + 2*np.pi/in_gear.hasuu0/2
# x1, y1 = init_gear_pos(x1, y1, hosei_ang)
# x1 = np.append(x1, circle_cos)
# y1 = np.append(y1, circle_sin)
# 内歯車　出力
x2, y2 = in_gear2.generate_haguruma()
if planet_gear.hasuu0 % 2:
    hosei_ang = -in_gear2.a0 - in_gear2.a1/2
else:
    hosei_ang = -in_gear2.a0 - in_gear2.a1/2 \
        + 2*np.pi/in_gear2.hasuu0/2
x2, y2 = init_gear_pos(x2, y2, hosei_ang)
x2 = np.append(x2, circle_cos2)
y2 = np.append(y2, circle_sin2)

# fig, ax = plt.subplots(figsize=(6.4, 6.4), facecolor=(.18, .31, .31))
# 初期表示
fig = plt.figure(figsize=(6.4, 6.4), facecolor=(.18, .30, .30))
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
ax.set_title('Magical Planetary Gears (不思議歯車機構)', color='0.8')
ax.set_facecolor('#8addd5')
ax.set_ylim(y_min, y_max)
ax.set_xlim(x_min, x_max)
ax.text(x_min+0.2, y_max-1.5, "Sun gear(tomato):Input")
ax.text(x_min+0.2, y_max-3.0, "Inner gear(green):Output")
ax.text(x_min+0.2, y_max-4.5, "Inner gear(orange):fixed")
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
ax.plot(in_gear2.hasuu0/2.0*in_gear2.mo0*np.cos(circle),
        in_gear2.hasuu0/2.0*in_gear2.mo0*np.sin(circle),
        color='purple', linestyle='-.', linewidth=0.4, alpha=0.5)
ax.plot(in_gear2.hasuu0/2.0*in_gear2.mo0*np.cos(alpha)*np.cos(circle),
        in_gear2.hasuu0/2.0*in_gear2.mo0*np.cos(alpha)*np.sin(circle),
        color='purple', linestyle='-.', linewidth=0.4, alpha=0.5)

# line0, = ax.plot([], [], 'r')
# line1, = ax.plot([], [], 'y')
# line30, = ax.plot([], [], 'g')
# line31, = ax.plot([], [], 'g')
# line32, = ax.plot([], [], 'g')
# line2, = ax.plot([], [], 'b')
# ax.grid()
# 各ギアのオブジェクト設定
x0data = np.array([])  # '太陽ギア歯形x軸'
y0data = np.array([])  # '太陽ギア歯形y軸'
# x1data = np.array([])  # '内歯ギア歯形x軸'
# y1data = np.array([])  # '内歯ギア歯形y軸'
x30data = np.array([])  # '遊星ギア歯形x軸'
y30data = np.array([])  # '遊星ギア歯形y軸'
x31data = np.array([])  # '遊星ギア歯形x軸'
y31data = np.array([])  # '遊星ギア歯形y軸'
x32data = np.array([])  # '遊星ギア歯形x軸'
y32data = np.array([])  # '遊星ギア歯形y軸'
x2data = np.array([])   # 内歯ギア
y2data = np.array([])
# sun gear
xy0 = np.column_stack((x0data, y0data))
patch0 = patches.Polygon(xy0, facecolor='tomato', edgecolor='b', alpha=0.8)
ax.add_patch(patch0)
# carrier gears
xy30 = np.column_stack((x30data, y30data))
patch30 = patches.Polygon(xy30, facecolor='aqua', edgecolor='b', alpha=0.8)
ax.add_patch(patch30)

xy31 = np.column_stack((x31data, y31data))
patch31 = patches.Polygon(xy31, facecolor='aqua', edgecolor='b', alpha=0.8)
ax.add_patch(patch31)

xy32 = np.column_stack((x32data, y32data))
patch32 = patches.Polygon(xy32, facecolor='aqua',
                          edgecolor='b', alpha=0.8)
ax.add_patch(patch32)

# inner gears　固定
# xy1 = np.column_stack((x1data, y1data))
# patch1 = patches.Polygon(xy1, facecolor='orange',
#                         edgecolor='r', alpha=0.7)
# ax.add_patch(patch1)

# inner gears 2 出力
xy2 = np.column_stack((x2data, y2data))
patch2 = patches.Polygon(xy2, facecolor='green', edgecolor='m', alpha=0.7)
ax.add_patch(patch2)

#


def data_gen():
    for cnt in itertools.count():
        if cnt > 200:
            break 
        else:
            ang_sun = 0
            ang_carrier = ang_v*cnt
            # ang_carrier += ang_v
            ang_planet = ang_carrier * sun_gear.hasuu0/planet_gear.hasuu0
            ang_inner = ang_carrier * (sun_gear.hasuu0 / in_gear2.hasuu0 + 1)
        #    ang_inner_out = ang_sun / \
        #        ((1+in_gear.hasuu0/sun_gear.hasuu0) /
        #         (1-in_gear.hasuu0/in_gear2.hasuu0))
        yield ang_sun, ang_carrier, ang_planet, ang_inner
        # yield 0, 0, 0, flag


def init():
    # print('Init')
    # ax.set_aspect('equal')
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    # return line0, line1, line30, line31, line32, line2,
    # return patch, line1, line30, line31, line32, line2,
    return patch0, patch30, patch31, patch32, patch2,


def run(data):
    # v_sun 太陽ギア積算角度
    # v_car キャリア積算角度
    # v_planet キャリアギアの積算角度
    # 内歯車固定
    # 内歯車積算角度
    v_sun, v_car, v_planet, v_out = data
    # テンポラリーな配列設定
    tempx = np.array([])
    tempy = np.array([])
    # 太陽ギア固定
    # ang1 = v_planet - a0 + h
    ang1 = v_planet
    v_car1 = v_car
    # carrier gear の中心位置を太陽ギアの中心からsun_carrier_distamceだけ移動
    # して、ang1自転する
    tempx = x30*np.cos(ang1)-y30*np.sin(ang1) + sun_carrier_distance
    tempy = y30*np.cos(ang1)+x30*np.sin(ang1)
    # v_carだけ公転する
    x30data = tempx*np.cos(v_car1)-tempy*np.sin(v_car1)
    y30data = tempy*np.cos(v_car1)+tempx*np.sin(v_car1)

    # 120°離れた位置に
    ang1 = v_planet + 2*np.pi/3
    v_car1 += 2*np.pi/3
    tempx = x30*np.cos(ang1)-y30*np.sin(ang1) + sun_carrier_distance
    tempy = y30*np.cos(ang1)+x30*np.sin(ang1)
    x31data = tempx*np.cos(v_car1)-tempy*np.sin(v_car1)
    y31data = tempy*np.cos(v_car1)+tempx*np.sin(v_car1)

    # 240°離れた位置に
    ang1 = v_planet + 4*np.pi/3
    v_car1 += 2*np.pi/3
    tempx = x30*np.cos(ang1)-y30*np.sin(ang1) + sun_carrier_distance
    tempy = y30*np.cos(ang1)+x30*np.sin(ang1)
    x32data = tempx*np.cos(v_car1)-tempy*np.sin(v_car1)
    y32data = tempy*np.cos(v_car1)+tempx*np.sin(v_car1)

    # 太陽ギアを回転
    x0data = x0*np.cos(v_sun)-y0*np.sin(v_sun)
    y0data = y0*np.cos(v_sun)+x0*np.sin(v_sun)
    # 内歯車2を回転
    x2data = x2*np.cos(v_out)-y2*np.sin(v_out)
    y2data = y2*np.cos(v_out)+x2*np.sin(v_out)

    # 太陽ギアをパッチ
    xy0 = np.column_stack([x0data, y0data])
    patch0.set_xy(xy0)
    #
    # キャリアギアをパッチ
    xy30 = np.column_stack([x30data, y30data])
    patch30.set_xy(xy30)
    xy31 = np.column_stack([x31data, y31data])
    patch31.set_xy(xy31)
    xy32 = np.column_stack([x32data, y32data])
    patch32.set_xy(xy32)

    # 内歯車2をパッチ
    xy2 = np.column_stack([x2data, y2data])
    patch2.set_xy(xy2)

    # 内歯車をパッチ
    # xy1 = np.column_stack([x1data, y1data])
    # patch1.set_xy(xy1)
    
    # return patch0, line1, patch30, patch31, patch32, line2
    return patch0, patch30, patch31, patch32, patch2


ani = animation.FuncAnimation(
    fig, run, data_gen,
    interval=100,
    init_func=init,
    repeat=False,
    blit=True,
    save_count=200)
# ani.save("fusigi.gif", writer="gif")
plt.show()
