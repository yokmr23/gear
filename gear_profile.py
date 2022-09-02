import numpy as np

# 圧力角設定
alpha = 20.0 / 180.0 * np.pi
# N1: 一つのインボリュート曲線部の点の数、N2:歯の頂点の点の数
N1, N2 = 100, 10


def make_param(m, z1, x1, fig1, z2, x2, fig2):
    """
    モジュール、歯車1の歯数、歯車1の転移係数、歯車1の平、内、
    歯車2の歯数、歯車2の転移係数、歯車2の平、内、
    m:float
    z1:integer
    x1:float
    fig1:string
    z2:integer
    x2:float
    fig2:string

    return:
    [軸間距離、歯底径、歯先径、歯底径、歯先径、]
    """
    if fig1 == 'hira' and fig2 == 'hira':
        inv_n = 2*np.tan(alpha)*((x1+x2)/(z1+z2))+inv(alpha)
        alpha_w = get_alpha(inv_n)
        y = (z1+z2)/2*(np.cos(alpha)/np.cos(alpha_w)-1)
        distance = ((z1+z2)/2+y)*m
        ha1 = (1+y-x2)*m
        ha2 = (1+y-x1)*m
        h = (2.25+y-(x1+x2))*m
        da1 = z1*m+2*ha1
        df1 = da1-2*h
        da2 = z2*m+2*ha2
        df2 = da2 - 2*h

    else:
        if not (fig1 == 'hira'):
            inv_n = 2*np.tan(alpha)*((x1-x2)/(z1-z2))+inv(alpha)
            alpha_w = get_alpha(inv_n)
            y = (z1-z2)/2*(np.cos(alpha)/np.cos(alpha_w)-1)
            distance = ((z1-z2)/2+y)*m
            ha1 = (1+x2)*m
            ha2 = (1-x1)*m
            h = 2.25*m
            da1 = z1*m+2*ha1
            df1 = da1-2*h
            da2 = z2*m+2*ha2
            df2 = da2 + 2*h
        else:
            inv_n = 2*np.tan(alpha)*((x2-x1)/(z2-z1))+inv(alpha)
            alpha_w = get_alpha(inv_n)
            y = (z2-z1)/2*(np.cos(alpha)/np.cos(alpha_w)-1)
            distance = ((z2-z1)/2+y)*m
            ha1 = (1+x1)*m
            ha2 = (1-x2)*m
            h = 2.25*m
            da1 = z1*m+2*ha1
            da2 = z2*m-2*ha2
            df1 = da1-2*h
            df2 = da2 + 2*h
    gear1 = {'hasuu': z1,
             'mo': m,
             'shift': x1,
             'hasaki': da1,
             'hazoko': df1,
             'fig': fig1}
    gear2 = {'hasuu': z2,
             'mo': m,
             'shift': x2,
             'hasaki': da2,
             'hazoko': df2,
             'fig': fig2}
    # return [distance, da1, df1, da2, df2]
    return [distance, gear1, gear2]


def differential(x):
    return 1./np.cos(x)/np.cos(x) - 1


def function(x, c):
    return np.tan(x) - x - c


# inv関数
def inv(a):
    """
    インボリュート関数
    パラメータ　a:float
    戻り値　tan(a)-a
    """
    return np.tan(a) - a


# θ=tan(a)-a θからaを求める
#
#
def get_alpha(y):
    """
    インボリュート逆関数
    パラメータ　角度 y : float
    戻り値　a : y=tan(a)-a"""
    y0 = y
    sa = 1.0
    x0 = .6
    while sa > 0.00001:
        x1 = x0 - 1/differential(x0)*function(x0, y0)
        sa = x0 - x1
        x0 = x1

    return x1


def get_distance1(z1, z2, m1, s1, s2):
    """
    # 平歯車と平歯車の中心間距離を求める
    Palameters
    ----------
    z1:
       平歯車1の歯数
    s1:
       平歯車1の転移係数
    z2:int
       平歯車2の歯数
    s2:
       平歯車2の転移係数
    # Returns
    戻り値中心距離
    """
    inv_aw = 2*np.tan(alpha*(s1+s2)/(z1+z2))+inv(alpha)
    aw = get_alpha(inv_aw)
    y = (z1+z2)/2*(np.cos(alpha)/np.cos(aw)-1)
    return ((z1+z2)/2+y)*m1


def rotate_gear(x, y, ang):
    """
    ギアオブジェクトを回転させる

    Parameters
    x,y:float
     左回転　+ 右回転　-
    ang:float
     回転角

    Returns
    -------
    回転後の値
    """
    X0 = x*np.cos(ang)-y*np.sin(ang)
    Y0 = y*np.cos(ang)+x*np.sin(ang)
    return X0, Y0


class Gear:
    def __init__(
            self, hasuu, mo, shift, hasaki, hazoko, fig='hira'):
        """
        hasuu: int
        mo: float
        shift: float
        hasakikei: float
        hazokokei: float
        fig: string
        """
        self.hasuu0 = hasuu
        self.mo0 = mo
        self.shift = shift
        if fig == 'hira':
            self.hasaki = hasaki
            self.hazoko = hazoko
        else:
            self.hasaki = hazoko
            self.hazoko = hasaki
        self.da = hasuu * mo        # 基準円直径
        self.d0 = self.da * np.cos(alpha)   # 基礎円直径
        self.fig = fig
        self.x = np.array([])
        self.y = np.array([])
        self.code = np.array([])
        self.generate_haguruma()

    def get_width_teeth_arc(self):
        """
        歯幅の基準円の円弧の長さ
        """
        return self.mo0*np.pi + 4*self.mo0*self.shift

    def get_width_teeth_ang(self):
        """
        歯幅の基準円の円弧角度
        """
        return self.get_width_teeth_arc()/self.hasuu0/self.mo0*2

    def get_width_kijunen_kisoen(self):
        """
        基準円とインボリュート曲線の交点と基礎円とインボリュート曲線との交点
        二つの交点と中心からのなす角度
        """
        return np.tan(np.arccos(self.d0/self.da))-np.arccos(self.d0/self.da)

    def get_width_hasaki_ang(self):
        ang = np.tan(np.arccos(self.d0/self.hasaki)) -\
            np.arccos(self.d0/self.hasaki) -\
            self.get_width_kijunen_kisoen()
        return self.get_width_teeth_ang()/4-ang

    def get_width_hazoko_ang(self):
        """
        歯底幅角度
        """
        ang0 = self.get_width_kijunen_kisoen()
        if self.hazoko > self.d0:
            # 歯底径>基礎円径
            ang = np.arccos(self.d0/self.hazoko)
            ang = np.tan(ang)-ang
            ang0 -= ang
        return self.get_width_hazoko()/2. - ang0

    def hazoko_center_kijun(self):
        """
        歯底中央点と基準線とインボリュートの交点のなす角度
        """
        return np.pi/self.hasuu0/2 - 2*self.shift/self.hasuu0*np.tan(alpha)

    def hasaki_cente_kijun(self):
        """
        歯先中央点と基準線とインボリュートの交点のなす角度
        """
        return np.pi/self.hasuu0/2 + 2*self.shift/self.hasuu0*np.tan(alpha)

    def hasaki_edge_kijun(self):
        """
        歯先エッジと基準線とインボリュートの交点のなす角度
        """
        a = np.tan(np.arccos(self.d0/self.hasaki)) - \
            np.arccos(self.d0/self.hasaki)
        return a-self.get_width_kijunen_kisoen()

    def hasaki_edge_center(self):
        """
        歯先始まり位置角度、歯先終わり位置の角度、なす角度
        """
        a = np.tan(np.arccos(self.d0/self.hasaki)) - \
            np.arccos(self.d0/self.hasaki)-self.get_width_kijunen_kisoen()
        a = self.hasaki_cente_kijun()-a
        end_a = np.pi/self.hasuu0 - self.hazoko_edge_center()[2]    # 歯底中央位置角度
        start_a = end_a-a
        return [start_a, end_a, end_a-start_a]

    def kijun_hazoko_edge(self):
        """
        インボリュート曲線と基準円との交点と中心を結ぶ直線と
        インボリュート直線と歯底との交点と中心を結ぶ直線がなす角度を求める
        """
        a0 = self.get_width_kijunen_kisoen()
        if self.d0 < self.hazoko:
            a0 -= np.tan(np.arccos(self.d0/self.hazoko)) - \
                np.arccos(self.d0/self.hazoko)
        return a0

    def hazoko_edge_center(self):
        """
        歯底エッジと歯底中央
        戻り値　歯底始まり角度、歯底終わり角度、歯底中央とエッジ部角度
        角度は左回転が正値
        """
        a = self.hazoko_center_kijun()-self.kijun_hazoko_edge()
        return [-a, 0, a]

    def get_func1(self, a):
        ang = np.arccos(a)
        return np.tan(ang)-ang

    def gear_hazoko_part(self):
        """
        歯底部作成
        極座標で表現(radius,theata)
        """
        hazoko_ang = self.hazoko_edge_center()
        if self.d0 > self.hazoko:
            radius = np.array([self.hazoko/2., self.hazoko/2.])
            theta = np.array([hazoko_ang[0], hazoko_ang[1]])
            code = np.array([1, 3])
        else:
            radius = np.full(4, self.hazoko/2.)
            theta = np.linspace(
                hazoko_ang[0], hazoko_ang[1], 4, endpoint=False)
            code = np.array([1, 2, 2, 2])
        return [radius, theta, code]

    def involute_curve(self):
        """
        片側インボリュート作成
        """
        if self.hazoko > self.d0:
            theta_sa = self.get_func1(self.d0/self.hazoko)
            start_radius = self.hazoko/2.

        else:
            theta_sa = 0.
            start_radius = self.d0/2.
        end_radius = self.hasaki/2.
        radius = np.linspace(start_radius, end_radius, N1)     # 長さ
        theta = self.get_func1(self.d0/2./radius)-theta_sa
        code = np.full(N1, 2)
        return [radius, theta, code]

    def gear_hasaki_part(self):
        """
        片側歯先部作成
        """
        # code = np.array([])
        theta = self.hasaki_edge_center()
        radius = np.full(N2, self.hasaki/2.)
        theta = np.linspace(theta[0], theta[1], N2)
        code = np.full(N2, 2)
        return [radius[1:], theta[1:], code[1:]]

    def gear_half(self):
        """
        一枚の歯車を作成
        戻り値:x座標、y座標、コード
        """
        radius = np.array([])
        theta = np.array([])
        code = np.array([])
        b = [self.gear_hazoko_part(),
             self.involute_curve(),
             self.gear_hasaki_part()]
        for i in b:
            radius = np.concatenate((radius, i[0]))
            theta = np.concatenate((theta, i[1]))
            code = np.concatenate((code, i[2]))

        return [radius, theta, code]

    def add_pointA(self):
        radius, theta, code = self.gear_half()
        # 葉の山の中心がx軸上に配置されるように回転する
        theta -= (np.pi/self.hasuu0-self.hazoko_edge_center()[2])
        theta_symmetry = np.flip(theta)
        theta_symmetry = theta_symmetry * -1
        radius_symmetry = np.flip(radius)
        code_symmetry = np.flip(code)
        # x軸に対して上下対象にする->歯車の一歯を創成
        theta = np.concatenate((theta, theta_symmetry[1:-1]))
        radius = np.concatenate((radius, radius_symmetry[1:-1]))
        code = np.concatenate((code, code_symmetry[1:-1]))
        return radius, theta, code

    def generate_haguruma(self):
        radius, theta, code = self.add_pointA()
        self.x = np.array([])
        self.y = np.array([])
        self.code = np.array([])
        # x座標、y座標変換
        for i in np.arange(0, 2*np.pi, 2*np.pi/self.hasuu0):
            self.x = np.concatenate((self.x, radius*np.cos(theta+i)))
            self.y = np.concatenate((self.y, radius*np.sin(theta+i)))
            self.code = np.concatenate((self.code, code))

        self.x = np.append(self.x, self.x[0])
        self.y = np.append(self.y, self.y[0])
        self.code = np.append(self.code, 2)
        # self.code1[-1] = 79


def test():
    for i in range(10):
        y = (i+1)*0.01
        x = get_alpha(y)

        print(y, x)


if __name__ == '__main__':
    test()
