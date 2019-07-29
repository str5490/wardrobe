import cv2
import enum
import numpy as np

class Colors_Name(enum.Enum):
	# 하양 베이지 라임 아이보리 개나리 노랑 살구 옥 은 귤
    white = 0
    beige = enum.auto()
    lime = enum.auto()
    ivory = enum.auto()
    #forsythia = enum.auto()
    yellow = enum.auto()
    apricot = enum.auto()
    Turquoise = enum.auto()
    silver = enum.auto()
    tangerine = enum.auto()
	# 연두 산호 하늘 주황 밝은파랑 시안 황토 자홍 분홍 담청 
    chartreuse = enum.auto()
    coral = enum.auto()
    sky_blue = enum.auto()
    orange = enum.auto()
    light_blue = enum.auto()
    cyan = enum.auto()
    ocher = enum.auto()
    claret = enum.auto()
    pink = enum.auto()
    powder_blue = enum.auto()
	# 초록 바다 회색 밝은보라 빨강 올리브 에메랄드그린 카키 아쿠아마린 암청
    green = enum.auto()
    seagrass = enum.auto()
    gray = enum.auto()
    light_purple = enum.auto()
    red = enum.auto()
    olive = enum.auto()
    emerald_green = enum.auto()
    khaki = enum.auto()
    aqua_marine = enum.auto()
    dark_blue = enum.auto()
	# 심홍 보라 파랑 갈색 청자 청록 군청 코발트블루 장미 자주
    magenta = enum.auto()
    purple = enum.auto()
    blue = enum.auto()
    brown = enum.auto()
    blue_purple = enum.auto()
    blue_green = enum.auto()
    ultramarine = enum.auto()
    cobalt_blue = enum.auto()
    rose = enum.auto()
    amethyst = enum.auto()
	# 고동 남색 검정
    anburn = enum.auto()
    navy = enum.auto()
    black = enum.auto()

color_num = len(Colors_Name)

# https://encycolorpedia.kr/named 참고
colors_rgb = np.zeros([color_num, 3], dtype = int)
colors_rgb[Colors_Name.white.value] = [255, 255, 255]
colors_rgb[Colors_Name.beige.value] = [245, 245, 220]
colors_rgb[Colors_Name.lime.value] = [191, 255, 0]
colors_rgb[Colors_Name.ivory.value] = [236, 230, 204]
#colors_rgb[Colors_Name.forsythia.value] = [236, 230, 0]
colors_rgb[Colors_Name.yellow.value] = [247, 212, 0]
colors_rgb[Colors_Name.apricot.value] = [251, 206, 177]
colors_rgb[Colors_Name.Turquoise.value] = [131, 220, 183]
colors_rgb[Colors_Name.silver.value] = [192, 192, 192]
colors_rgb[Colors_Name.tangerine.value] = [248, 155, 0]
colors_rgb[Colors_Name.chartreuse.value] = [129, 193, 71]
colors_rgb[Colors_Name.coral.value] = [242, 152, 134]
colors_rgb[Colors_Name.sky_blue.value] = [80, 188, 223]
colors_rgb[Colors_Name.orange.value] = [255, 127, 0]
colors_rgb[Colors_Name.light_blue.value] = [74, 168, 216]
colors_rgb[Colors_Name.cyan.value] = [0, 163, 210]
colors_rgb[Colors_Name.ocher.value] = [198, 138, 18]
colors_rgb[Colors_Name.claret.value] = [255, 0, 255]
colors_rgb[Colors_Name.pink.value] = [255, 51, 153]
colors_rgb[Colors_Name.powder_blue.value] = [62, 145, 181]
colors_rgb[Colors_Name.green.value] = [0, 128, 0]
colors_rgb[Colors_Name.seagrass.value] = [0, 128, 255]
colors_rgb[Colors_Name.gray.value] = [128, 128, 128]
colors_rgb[Colors_Name.light_purple.value] = [137, 119, 173]
colors_rgb[Colors_Name.red.value] = [255, 0, 0]
colors_rgb[Colors_Name.olive.value] = [128, 128, 0]
colors_rgb[Colors_Name.emerald_green.value] = [0, 141, 98]
colors_rgb[Colors_Name.khaki.value] = [143, 120, 75]
colors_rgb[Colors_Name.aqua_marine.value] = [94, 126, 155]
colors_rgb[Colors_Name.dark_blue.value] = [0, 128, 128]
colors_rgb[Colors_Name.magenta.value] = [220, 20, 60]
colors_rgb[Colors_Name.purple.value] = [139, 0, 255]
colors_rgb[Colors_Name.blue.value] = [0, 103, 163]
colors_rgb[Colors_Name.brown.value] = [150, 75, 0]
colors_rgb[Colors_Name.blue_purple.value] = [105, 55, 161]
colors_rgb[Colors_Name.blue_green.value] = [0, 86, 102]
colors_rgb[Colors_Name.ultramarine.value] = [70, 73, 100]
colors_rgb[Colors_Name.cobalt_blue.value] = [0, 73, 140]
colors_rgb[Colors_Name.rose.value] = [141, 25, 43]
colors_rgb[Colors_Name.amethyst.value] = [102, 0, 153]
colors_rgb[Colors_Name.anburn.value] = [128, 0, 0]
colors_rgb[Colors_Name.navy.value] = [0, 0, 128]
colors_rgb[Colors_Name.black.value] = [0, 0, 0]


color_diff = np.zeros([color_num], dtype = int)
color_target = np.zeros([3], dtype = int)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color_raw = img[y, x]
        one_pixel = np.uint8([[color_raw]])
        color_target = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2RGB)
        print(color_target[0][0])

        for i in Colors_Name:
            color_diff[i.value] = abs(color_target[0][0][0] - colors_rgb[i.value][0])
            color_diff[i.value] += abs(color_target[0][0][1] - colors_rgb[i.value][1])
            color_diff[i.value] += abs(color_target[0][0][2] - colors_rgb[i.value][2])
        print (color_diff, color_diff.argmin())
        color = color_diff.argmin()

        print(Colors_Name(color).name+'.mp3')
        print(colors_rgb[color])

img = cv2.imread('color_test_img.jpg', cv2.IMREAD_COLOR)
cv2.imshow('ImageDisplay', img)
cv2.setMouseCallback('ImageDisplay', mouse_callback)

cv2.waitKey(0)
cv2.destroyAllWindows()
