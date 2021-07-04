import numpy as np
# import matplotlib.pyplot as plt

alpha = 20.0 / 180.0 * np.pi


def differential(x):
    return 1./np.cos(x)/np.cos(x) - 1


def function(x, c):
    return np.tan(x) - x - c


def inv(a):
    return np.tan(a) - a

# θ=tan(a)-a θからaを求める


def get_alpha(y):
    # y0 = 0.02
    y0 = y
    sa = 1.0
    x0 = .6
    while sa > 0.00001:
        x1 = x0 - 1/differential(x0)*function(x0, y0)
        # print(differential(x0), function(x0, y0))
        sa = x0 - x1
        # print(sa, x1)
        x0 = x1

    return x1
# 平歯車と平歯車の中心距離
# 平歯車1の歯数、転位係数　z1 s1
# 平歯車2の歯数、転位係数　z2 s2
# モジュール　m


def get_distance1(z1, z2, m1, s1, s2):
    inv_aw = 2*np.tan(alpha*(s1+s2)/(z1+z2))+inv(alpha)
    aw = get_alpha(inv_aw)
    y = (z1+z2)/2*(np.cos(alpha)/np.cos(aw)-1)
    return ((z1+z2)/2+y)*m1


class Gear:
    # resolution = 0.001
    def __init__(self, hasuu, mo, shift=0, fig='hira', resolution=0.001):
        self.hasuu0 = hasuu
        self.mo0 = mo
        self.resolution = resolution
        self.shift = shift
        self.x = np.array([])
        self.y = np.array([])
        self.fig = fig
        self.a0 = 0
        self.a1 = 0
    # 基準円直径を求める

    def get_std_diameter(self):
        return self.hasuu0 * self.mo0

    # 基礎円直径を求める
    def get_base_diameter(self):
        a = self.get_std_diameter()
        return a * np.cos(np.pi*20./180.)

    # 歯先半径
    def get_hasaki_diameter(self):
        if self.fig == 'hira':
            return self.hasuu0 * self.mo0 / 2 + self.mo0 * (1 + self.shift)
        else:
            return self.hasuu0 * self.mo0 / 2 \
                - (1-self.shift)*self.mo0 \
                + 2.25*self.mo0

    # 歯底半径
    def get_hazoko_diameter(self):
        # return self.hasuu0 * self.mo0 / 2
        # - 1.25 * self.mo0 * (1 - self.shift)
        if self.fig == 'hira':
            return self.hasuu0 * self.mo0 / 2 \
                + self.mo0 * (1 + self.shift)-2.25*self.mo0
        else:
            return self.hasuu0 * self.mo0 / 2 \
                - (1-self.shift)*self.mo0
    # 転位係数を求める

    def get_shift_v(self):
        return self.shift

    # 基礎円と基準円がそれぞれ交差するインボリュート曲線の交点と中心点
    # 結ぶ直線間の角度の2倍と歯と歯の角度の1/2の和
    def get_shift(self, ang):
        cos_a = self.get_base_diameter() / self.get_std_diameter()
        a = np.arccos(cos_a)
        
        return (np.tan(a) - a)-ang
    #
    #

    def get_theta(self):
        cos_a = self.get_base_diameter() / self.get_std_diameter()
        a = np.arccos(cos_a)
        return np.tan(a) - a

    # 一枚の歯を創成

    def add_pointA(self, rotate=0):
        r_base = self.get_base_diameter()/2   # 基礎円半径
        r_top = self.get_hasaki_diameter()      # 歯先円半径
        r_bottom = self.get_hazoko_diameter()   # 歯底円半径
        
        # 歯先円までのtheta
        ang_top = np.arccos(float(r_base)/float(r_top))
        theta_top = np.tan(ang_top) - ang_top
        
        # 歯底円までの角度
        if r_base > r_bottom:
            # ang_bottom = 0
            theta_bottom = 0.0
            # 追加、内歯車の場合歯先部分を接触しないよう逃がす
            if not self.fig == 'hira': 
                self.x = np.append(self.x, r_bottom)
                self.y = np.append(self.y, -np.tan(alpha)*(r_base-r_bottom))
            # 平歯車の場合は逃がさない
            else:
                self.x = np.append(self.x, r_bottom)
                self.y = np.append(self.y, 0.0)
        else:
            ang_bottom = np.arccos(r_base/r_bottom)
            theta_bottom = np.tan(ang_bottom) - ang_bottom
        # 歯の片側を作成
        for i in np.linspace(theta_bottom, theta_top, 100, endpoint=True):
            l0 = r_base/np.cos(get_alpha(i))
            self.x = np.append(self.x, l0*np.cos(i-theta_bottom))
            self.y = np.append(self.y, l0*np.sin(i-theta_bottom))
        # 初期位置保存
        # 周期角度
        self.a0 = self.get_shift(theta_bottom)
        # 歯厚み補正係数
        self.a1 = 4.0*self.get_shift_v() * \
            np.tan(alpha)/self.hasuu0 + np.pi/self.hasuu0
        # 回転角度
        rotate = self.a0 * 2 + self.a1
        n = range(self.x.size)
        # 歯の反対側を作成
        for i in reversed(n):
            x0 = self.x[i]
            y0 = -self.y[i]
            # rotate = self.get_shift()
            x = x0*np.cos(rotate)-y0*np.sin(rotate)
            y = y0*np.cos(rotate)+x0*np.sin(rotate)
            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y)
        pass

    def generate_haguruma(self):
        x = np.array([])
        y = np.array([])
        self.add_pointA(0)
        # rotate = self.get_shift()
        # x, yに一枚の歯の形状を保存
        x = np.append(x, self.x)
        y = np.append(y, self.y)
        # 残りの歯を作成
        for i in range(1, self.hasuu0):
            rotate = 2.*np.pi/self.hasuu0*i
            x = np.append(x, self.x*np.cos(rotate) -
                          self.y*np.sin(rotate))
            y = np.append(y, self.y*np.cos(rotate) +
                          self.x*np.sin(rotate))
        # 最初の位置に戻る
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        return x, y


def test1():
    for i in range(10):
        y = (i+1)*0.01
        x = get_alpha(y)
        print(y, x)


def test():
    # in_gear = Gear(42, 1, 0.7, fig='a')
    # sun_gear = Gear(15, 1, 0.55854693)
    # carrier0 = Gear(15, 1, 0.55854693)
    in_gear2 = Gear(45, 1, 0.0, 'a')
    # gear0.add_pointA()
    # si = gear0.x.size
    # for i in range(si):
    #    x = gear0.x[i]
    #    y = gear0.y[i]
    #    r = np.sqrt(x*x + y*y)
    # print('{} x={} y={} r={}'.format(i, x, y, r))
    # print('歯先半径={} 歯底半径={}'.format(
    #    gear0.get_hasaki_diameter(), gear0.get_hazoko_diameter()))
    print('歯数={}'.format(in_gear2.hasuu0))
    print('転位係数={}'.format(in_gear2.shift))
    #print('歯先円半径={}'.format(in_gear2.hasaki_diameter)
    #print('歯底円半径={}'.format(in_gear2.hazoko_diameter)
    # in_gear2.generate_haguruma()
    # print("a0={}".format(in_gear2.a0))
    # print("a1={}".format(in_gear2.a1))
    # for i in range(in_gear2.x.size):
    #    print(i, in_gear2.x[i], in_gear2.y[i], np.sqrt(
    #        in_gear2.x[i]*in_gear2.x[i]+in_gear2.y[i]*in_gear2.y[i]))
    in_gear2.add_pointA()
    for i in range(in_gear2.x.size):
        x = in_gear2.x[i]
        y = in_gear2.y[i]
        print(x,y,np.sqrt(x*x+y*y))

if __name__ == '__main__':
    test()
