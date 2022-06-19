import sys
import random

import glm  # pip install PyGLM
import plotly.graph_objects as go

from Point import Point
from Line import Line
from Cone import Cone
from Collision import Collision, CollisionLine


def points_to_scatter(point_array, form_triangle: bool):
    x_array = [point.x for point in point_array]
    y_array = [point.y for point in point_array]
    z_array = [point.z for point in point_array]
    if form_triangle:
        x_array.append(point_array[0].x)
        y_array.append(point_array[0].y)
        z_array.append(point_array[0].z)
    return [x_array, y_array, z_array]


def print_points(points):
    print("Want to recreate the same inputs? Copy line below:")
    print("points = [", end='')
    for point in points:
        print("Point(glm.vec3(" + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + ")), ", end='')
    print("]")



def main(n, t, m):
    drawAllCollisions = False
    NO_POINTS = n
    THETA = t
    MEW = m
    MIN_X = 0
    MIN_Y = 0
    MIN_Z = 0
    MAX_X = 1000
    MAX_Y = 1000
    MAX_Z = 0

    points = [Point(glm.vec3(random.random() * MAX_X, random.random() * MAX_Y,
                             random.random() * MAX_Z), i) for i in range(NO_POINTS)]

    # Buggy inputs:
    #   Error when rounding: n = 5
    # points = [Point(glm.vec3(885.869140625, 538.2119140625, 0.0)), Point(glm.vec3(313.7813415527344, 756.8295288085938, 0.0)), Point(glm.vec3(924.343017578125, 636.501953125, 0.0)), Point(glm.vec3(400.0970153808594, 756.957763671875, 0.0)), Point(glm.vec3(65.90353393554688, 869.4907836914062, 0.0)), ]
    #   Error with NaN in normal dir? n = 250
    # points = [Point(glm.vec3(125.17713928222656, 838.6481323242188, 0.0)), Point(glm.vec3(751.6796875, 170.53602600097656, 0.0)), Point(glm.vec3(327.36236572265625, 416.0408020019531, 0.0)), Point(glm.vec3(662.0630493164062, 126.8289566040039, 0.0)), Point(glm.vec3(110.539794921875, 111.97134399414062, 0.0)), Point(glm.vec3(589.041015625, 122.83514404296875, 0.0)), Point(glm.vec3(76.03773498535156, 567.4397583007812, 0.0)), Point(glm.vec3(798.53271484375, 867.0066528320312, 0.0)), Point(glm.vec3(393.5541076660156, 895.37890625, 0.0)), Point(glm.vec3(628.5780029296875, 469.3189697265625, 0.0)), Point(glm.vec3(747.4935302734375, 244.43312072753906, 0.0)), Point(glm.vec3(876.904541015625, 15.898128509521484, 0.0)), Point(glm.vec3(548.5388793945312, 295.2676696777344, 0.0)), Point(glm.vec3(330.62109375, 553.9141235351562, 0.0)), Point(glm.vec3(485.0704650878906, 391.302001953125, 0.0)), Point(glm.vec3(530.9567260742188, 787.70263671875, 0.0)), Point(glm.vec3(397.8472595214844, 38.728797912597656, 0.0)), Point(glm.vec3(618.2874145507812, 761.6834716796875, 0.0)), Point(glm.vec3(308.3902587890625, 320.5961608886719, 0.0)), Point(glm.vec3(562.95751953125, 320.7244873046875, 0.0)), Point(glm.vec3(862.9016723632812, 540.2740478515625, 0.0)), Point(glm.vec3(275.3444519042969, 174.82061767578125, 0.0)), Point(glm.vec3(939.3003540039062, 5.873211860656738, 0.0)), Point(glm.vec3(491.08544921875, 388.8739013671875, 0.0)), Point(glm.vec3(663.365478515625, 589.3890991210938, 0.0)), Point(glm.vec3(84.00117492675781, 437.3174133300781, 0.0)), Point(glm.vec3(369.9527587890625, 850.9749145507812, 0.0)), Point(glm.vec3(283.05322265625, 369.3768615722656, 0.0)), Point(glm.vec3(971.75048828125, 524.92138671875, 0.0)), Point(glm.vec3(602.951171875, 392.3110046386719, 0.0)), Point(glm.vec3(975.362548828125, 791.1912841796875, 0.0)), Point(glm.vec3(785.4332885742188, 431.9457702636719, 0.0)), Point(glm.vec3(636.1445922851562, 173.4879608154297, 0.0)), Point(glm.vec3(659.2599487304688, 56.042911529541016, 0.0)), Point(glm.vec3(419.93798828125, 478.2568359375, 0.0)), Point(glm.vec3(214.84329223632812, 800.491455078125, 0.0)), Point(glm.vec3(850.4352416992188, 322.18267822265625, 0.0)), Point(glm.vec3(986.2579345703125, 636.779052734375, 0.0)), Point(glm.vec3(510.1514587402344, 172.81253051757812, 0.0)), Point(glm.vec3(451.29248046875, 731.97607421875, 0.0)), Point(glm.vec3(154.27529907226562, 918.7409057617188, 0.0)), Point(glm.vec3(311.1960144042969, 451.2516784667969, 0.0)), Point(glm.vec3(343.364013671875, 808.8546142578125, 0.0)), Point(glm.vec3(980.5426635742188, 439.685546875, 0.0)), Point(glm.vec3(755.27880859375, 108.42537689208984, 0.0)), Point(glm.vec3(842.728759765625, 835.9515380859375, 0.0)), Point(glm.vec3(763.6404418945312, 721.6607666015625, 0.0)), Point(glm.vec3(587.4329223632812, 117.73633575439453, 0.0)), Point(glm.vec3(992.234619140625, 141.24755859375, 0.0)), Point(glm.vec3(756.7864990234375, 790.767333984375, 0.0)), Point(glm.vec3(269.5863037109375, 150.0015106201172, 0.0)), Point(glm.vec3(198.187744140625, 301.41522216796875, 0.0)), Point(glm.vec3(940.8580322265625, 898.078857421875, 0.0)), Point(glm.vec3(745.3720703125, 110.96556091308594, 0.0)), Point(glm.vec3(631.2745361328125, 720.5927734375, 0.0)), Point(glm.vec3(46.713558197021484, 481.4901123046875, 0.0)), Point(glm.vec3(114.70624542236328, 25.85926628112793, 0.0)), Point(glm.vec3(880.3948974609375, 716.30859375, 0.0)), Point(glm.vec3(378.29229736328125, 656.4744262695312, 0.0)), Point(glm.vec3(612.8433227539062, 620.9407958984375, 0.0)), Point(glm.vec3(593.8286743164062, 960.8055419921875, 0.0)), Point(glm.vec3(162.39056396484375, 298.3587951660156, 0.0)), Point(glm.vec3(233.56593322753906, 741.3648681640625, 0.0)), Point(glm.vec3(678.4176025390625, 297.880126953125, 0.0)), Point(glm.vec3(595.8073120117188, 918.729248046875, 0.0)), Point(glm.vec3(425.4487609863281, 762.7750244140625, 0.0)), Point(glm.vec3(732.9705200195312, 585.74755859375, 0.0)), Point(glm.vec3(826.5882568359375, 226.60284423828125, 0.0)), Point(glm.vec3(278.72259521484375, 465.3988952636719, 0.0)), Point(glm.vec3(425.2297058105469, 190.02281188964844, 0.0)), Point(glm.vec3(516.8456420898438, 587.654052734375, 0.0)), Point(glm.vec3(424.9285583496094, 171.275634765625, 0.0)), Point(glm.vec3(217.77769470214844, 834.5972290039062, 0.0)), Point(glm.vec3(999.21044921875, 656.59423828125, 0.0)), Point(glm.vec3(427.7001953125, 824.5879516601562, 0.0)), Point(glm.vec3(698.1670532226562, 363.53631591796875, 0.0)), Point(glm.vec3(287.76470947265625, 238.98477172851562, 0.0)), Point(glm.vec3(387.9540100097656, 96.34467315673828, 0.0)), Point(glm.vec3(928.27587890625, 656.5725708007812, 0.0)), Point(glm.vec3(821.4404907226562, 220.53042602539062, 0.0)), Point(glm.vec3(312.1059265136719, 744.2323608398438, 0.0)), Point(glm.vec3(206.0889129638672, 190.50494384765625, 0.0)), Point(glm.vec3(795.7761840820312, 152.00804138183594, 0.0)), Point(glm.vec3(659.3345947265625, 818.3126220703125, 0.0)), Point(glm.vec3(267.034912109375, 201.50411987304688, 0.0)), Point(glm.vec3(29.14385223388672, 864.80078125, 0.0)), Point(glm.vec3(382.6377258300781, 225.6544189453125, 0.0)), Point(glm.vec3(857.6838989257812, 482.29913330078125, 0.0)), Point(glm.vec3(933.5540771484375, 740.1531372070312, 0.0)), Point(glm.vec3(451.6324768066406, 856.0337524414062, 0.0)), Point(glm.vec3(419.9515075683594, 589.3967895507812, 0.0)), Point(glm.vec3(862.7601318359375, 61.20317840576172, 0.0)), Point(glm.vec3(114.98979949951172, 132.95277404785156, 0.0)), Point(glm.vec3(166.32298278808594, 326.0904846191406, 0.0)), Point(glm.vec3(561.79150390625, 457.38934326171875, 0.0)), Point(glm.vec3(565.4035034179688, 161.2906951904297, 0.0)), Point(glm.vec3(720.021484375, 910.2745971679688, 0.0)), Point(glm.vec3(597.4682006835938, 258.7468566894531, 0.0)), Point(glm.vec3(51.20353317260742, 439.8556213378906, 0.0)), Point(glm.vec3(9.047525405883789, 213.4448699951172, 0.0)), Point(glm.vec3(889.0830078125, 88.4409408569336, 0.0)), Point(glm.vec3(310.4600830078125, 277.3382873535156, 0.0)), Point(glm.vec3(315.0370788574219, 778.965087890625, 0.0)), Point(glm.vec3(120.03466796875, 346.896484375, 0.0)), Point(glm.vec3(909.912109375, 917.0689697265625, 0.0)), Point(glm.vec3(686.632080078125, 276.05364990234375, 0.0)), Point(glm.vec3(465.7032470703125, 259.47332763671875, 0.0)), Point(glm.vec3(880.1488647460938, 444.1290588378906, 0.0)), Point(glm.vec3(772.472412109375, 806.142822265625, 0.0)), Point(glm.vec3(533.3875732421875, 353.87738037109375, 0.0)), Point(glm.vec3(828.7398681640625, 753.2467041015625, 0.0)), Point(glm.vec3(35.34895706176758, 232.39297485351562, 0.0)), Point(glm.vec3(466.0735778808594, 50.802059173583984, 0.0)), Point(glm.vec3(489.30926513671875, 4.842413425445557, 0.0)), Point(glm.vec3(988.8976440429688, 968.1593627929688, 0.0)), Point(glm.vec3(674.3786010742188, 61.062843322753906, 0.0)), Point(glm.vec3(267.3049621582031, 601.7655639648438, 0.0)), Point(glm.vec3(842.46533203125, 627.8425903320312, 0.0)), Point(glm.vec3(98.33977508544922, 792.7072143554688, 0.0)), Point(glm.vec3(452.94671630859375, 882.1981201171875, 0.0)), Point(glm.vec3(516.2533569335938, 633.3634643554688, 0.0)), Point(glm.vec3(545.9307250976562, 641.3960571289062, 0.0)), Point(glm.vec3(920.8411865234375, 112.41223907470703, 0.0)), Point(glm.vec3(671.3509521484375, 730.2647094726562, 0.0)), Point(glm.vec3(324.8806457519531, 3.057003974914551, 0.0)), Point(glm.vec3(716.3748779296875, 777.114013671875, 0.0)), Point(glm.vec3(360.13134765625, 6.974967002868652, 0.0)), Point(glm.vec3(217.8095245361328, 608.540771484375, 0.0)), Point(glm.vec3(213.4007110595703, 33.10831832885742, 0.0)), Point(glm.vec3(93.33491516113281, 427.6329040527344, 0.0)), Point(glm.vec3(801.8197631835938, 318.8878479003906, 0.0)), Point(glm.vec3(483.5690002441406, 50.324012756347656, 0.0)), Point(glm.vec3(213.9612274169922, 183.5867919921875, 0.0)), Point(glm.vec3(137.4250030517578, 287.00396728515625, 0.0)), Point(glm.vec3(464.4901428222656, 337.018310546875, 0.0)), Point(glm.vec3(613.7736206054688, 507.0749206542969, 0.0)), Point(glm.vec3(633.9862670898438, 691.9628295898438, 0.0)), Point(glm.vec3(296.3188171386719, 609.6568603515625, 0.0)), Point(glm.vec3(9.90749740600586, 28.94700050354004, 0.0)), Point(glm.vec3(382.1888427734375, 62.692176818847656, 0.0)), Point(glm.vec3(267.4572448730469, 543.5350341796875, 0.0)), Point(glm.vec3(790.865966796875, 53.72731399536133, 0.0)), Point(glm.vec3(565.7926635742188, 125.58332824707031, 0.0)), Point(glm.vec3(69.97575378417969, 550.7916870117188, 0.0)), Point(glm.vec3(255.91151428222656, 713.89697265625, 0.0)), Point(glm.vec3(838.9676513671875, 60.84620666503906, 0.0)), Point(glm.vec3(294.831298828125, 214.51385498046875, 0.0)), Point(glm.vec3(525.58642578125, 258.90667724609375, 0.0)), Point(glm.vec3(436.7019958496094, 796.3497314453125, 0.0)), Point(glm.vec3(633.9094848632812, 911.78515625, 0.0)), Point(glm.vec3(967.6902465820312, 399.9129638671875, 0.0)), Point(glm.vec3(971.9349975585938, 13.843534469604492, 0.0)), Point(glm.vec3(859.5698852539062, 381.6270446777344, 0.0)), Point(glm.vec3(259.10107421875, 185.94410705566406, 0.0)), Point(glm.vec3(332.0260925292969, 859.748046875, 0.0)), Point(glm.vec3(173.02749633789062, 553.7377319335938, 0.0)), Point(glm.vec3(459.1239929199219, 622.231201171875, 0.0)), Point(glm.vec3(81.52092742919922, 341.6582946777344, 0.0)), Point(glm.vec3(152.8263397216797, 546.9017333984375, 0.0)), Point(glm.vec3(211.2753448486328, 543.5086059570312, 0.0)), Point(glm.vec3(464.6287841796875, 535.3984375, 0.0)), Point(glm.vec3(540.8884887695312, 621.3721923828125, 0.0)), Point(glm.vec3(851.3781127929688, 151.938232421875, 0.0)), Point(glm.vec3(154.52989196777344, 443.812744140625, 0.0)), Point(glm.vec3(312.2110595703125, 407.1512145996094, 0.0)), Point(glm.vec3(881.0437622070312, 360.07049560546875, 0.0)), Point(glm.vec3(24.002607345581055, 527.7470092773438, 0.0)), Point(glm.vec3(444.97662353515625, 74.51988220214844, 0.0)), Point(glm.vec3(579.7239379882812, 884.4529418945312, 0.0)), Point(glm.vec3(229.2714385986328, 701.0546264648438, 0.0)), Point(glm.vec3(571.731201171875, 964.7749633789062, 0.0)), Point(glm.vec3(109.76153564453125, 160.1816864013672, 0.0)), Point(glm.vec3(569.1005249023438, 196.6462860107422, 0.0)), Point(glm.vec3(902.19091796875, 171.66378784179688, 0.0)), Point(glm.vec3(501.6150207519531, 111.7235107421875, 0.0)), Point(glm.vec3(274.2543029785156, 281.77288818359375, 0.0)), Point(glm.vec3(20.375185012817383, 203.31028747558594, 0.0)), Point(glm.vec3(10.82472038269043, 86.85987854003906, 0.0)), Point(glm.vec3(977.7600708007812, 833.2132568359375, 0.0)), Point(glm.vec3(959.0568237304688, 191.41522216796875, 0.0)), Point(glm.vec3(664.8436279296875, 388.8227844238281, 0.0)), Point(glm.vec3(416.46527099609375, 886.9631958007812, 0.0)), Point(glm.vec3(846.0744018554688, 792.5794677734375, 0.0)), Point(glm.vec3(559.8082885742188, 214.53005981445312, 0.0)), Point(glm.vec3(391.2542724609375, 105.61578369140625, 0.0)), Point(glm.vec3(991.1195678710938, 696.3988037109375, 0.0)), Point(glm.vec3(326.8067626953125, 467.6157531738281, 0.0)), Point(glm.vec3(84.0280532836914, 647.88623046875, 0.0)), Point(glm.vec3(688.1602783203125, 793.0617065429688, 0.0)), Point(glm.vec3(690.0017700195312, 692.0372314453125, 0.0)), Point(glm.vec3(989.7771606445312, 502.92620849609375, 0.0)), Point(glm.vec3(474.44342041015625, 992.6065673828125, 0.0)), Point(glm.vec3(291.5843505859375, 210.89210510253906, 0.0)), Point(glm.vec3(277.4609069824219, 699.9564208984375, 0.0)), Point(glm.vec3(772.2660522460938, 558.15087890625, 0.0)), Point(glm.vec3(369.8965759277344, 602.122802734375, 0.0)), Point(glm.vec3(368.7974548339844, 262.26080322265625, 0.0)), Point(glm.vec3(704.1763916015625, 738.57275390625, 0.0)), Point(glm.vec3(317.93603515625, 522.7310180664062, 0.0)), Point(glm.vec3(680.9057006835938, 928.2547607421875, 0.0)), Point(glm.vec3(584.5027465820312, 933.3385620117188, 0.0)), Point(glm.vec3(528.2421264648438, 231.44281005859375, 0.0)), Point(glm.vec3(781.3278198242188, 74.57020568847656, 0.0)), Point(glm.vec3(374.76141357421875, 701.9618530273438, 0.0)), Point(glm.vec3(532.0762939453125, 632.70263671875, 0.0)), Point(glm.vec3(349.9007263183594, 915.3753051757812, 0.0)), Point(glm.vec3(481.4733581542969, 391.3621520996094, 0.0)), Point(glm.vec3(229.10671997070312, 403.59490966796875, 0.0)), Point(glm.vec3(549.22509765625, 241.1029815673828, 0.0)), Point(glm.vec3(650.2515258789062, 565.8099365234375, 0.0)), Point(glm.vec3(947.1454467773438, 849.3511352539062, 0.0)), Point(glm.vec3(19.896577835083008, 138.8218231201172, 0.0)), Point(glm.vec3(224.97219848632812, 2.467531442642212, 0.0)), Point(glm.vec3(180.05401611328125, 176.35665893554688, 0.0)), Point(glm.vec3(347.5259094238281, 47.77940368652344, 0.0)), Point(glm.vec3(823.7935791015625, 972.3230590820312, 0.0)), Point(glm.vec3(823.3939819335938, 120.989501953125, 0.0)), Point(glm.vec3(818.453125, 600.3275146484375, 0.0)), Point(glm.vec3(810.6159057617188, 787.7965087890625, 0.0)), Point(glm.vec3(83.75547790527344, 205.4712677001953, 0.0)), Point(glm.vec3(926.0728759765625, 427.2684326171875, 0.0)), Point(glm.vec3(538.3755493164062, 984.6616821289062, 0.0)), Point(glm.vec3(895.4511108398438, 23.454084396362305, 0.0)), Point(glm.vec3(726.0612182617188, 346.61248779296875, 0.0)), Point(glm.vec3(769.5709228515625, 981.1991577148438, 0.0)), Point(glm.vec3(405.1874694824219, 730.2109375, 0.0)), Point(glm.vec3(386.3848571777344, 249.78160095214844, 0.0)), Point(glm.vec3(915.77392578125, 71.83794403076172, 0.0)), Point(glm.vec3(260.498779296875, 756.7972412109375, 0.0)), Point(glm.vec3(470.7697448730469, 432.037841796875, 0.0)), Point(glm.vec3(898.6670532226562, 945.787353515625, 0.0)), Point(glm.vec3(238.2416534423828, 696.4132690429688, 0.0)), Point(glm.vec3(966.6986694335938, 582.6705932617188, 0.0)), Point(glm.vec3(10.310844421386719, 672.1082763671875, 0.0)), Point(glm.vec3(968.8162231445312, 105.14885711669922, 0.0)), Point(glm.vec3(103.6960678100586, 451.5562438964844, 0.0)), Point(glm.vec3(282.7325744628906, 294.8834533691406, 0.0)), Point(glm.vec3(87.67345428466797, 672.1713256835938, 0.0)), Point(glm.vec3(269.1955871582031, 90.5503158569336, 0.0)), Point(glm.vec3(213.90602111816406, 14.753612518310547, 0.0)), Point(glm.vec3(110.54118347167969, 72.94966888427734, 0.0)), Point(glm.vec3(348.6347961425781, 752.8617553710938, 0.0)), Point(glm.vec3(24.4144344329834, 47.516029357910156, 0.0)), Point(glm.vec3(546.5674438476562, 429.50958251953125, 0.0)), Point(glm.vec3(71.77794647216797, 143.521484375, 0.0)), Point(glm.vec3(494.46575927734375, 390.1024475097656, 0.0)), Point(glm.vec3(125.6423110961914, 687.0242309570312, 0.0)), Point(glm.vec3(497.90753173828125, 461.72509765625, 0.0)), Point(glm.vec3(340.9859619140625, 867.939208984375, 0.0)), Point(glm.vec3(594.4802856445312, 645.0469970703125, 0.0)), ]


    print_points(points)

    cones = [Cone(points[i], THETA, MEW, i) for i in range(len(points))]

    all_collisions = []
    for i in range(NO_POINTS):
        for j in range(i + 1, NO_POINTS):
            print("Generating Collisions: " + str(i*NO_POINTS+j) + " of " + str(NO_POINTS*NO_POINTS))
            all_collisions.append(Collision(cones[i], cones[j]))

    all_collisions.sort(key=lambda d: d.scale)

    triangles = []
    col_points = []
    col_lines = []
    col_line_id = 0
    final_lines = []

    def setCollisionLineEnd(id: int, intersectionPoint: Point):
        print("Connection Progress: "+str(len(final_lines))+" of ~"+str(n*6))
        for col_linee in col_lines:
            if col_linee.id == id:
                col_linee.setEnd(intersectionPoint)
                final_lines.append(col_linee)
                return


    count = 0
    for collision in all_collisions:
        print("Checking Collisions: " + str(count) + " of " + str(len(all_collisions)))
        count+=1
        ignore = False
        for cone in cones:
            # If the collision happens inside a cone, it won't be valid so we ignore it
            if cone.center != collision.topCone.center and cone.center != collision.bottomCone.center \
                    and cone.point_inside_cone(collision.collision_point, collision.scale):
                ignore = True
                break
        if not ignore:
            # Add collision
            col_points.append(collision.collision_point)
            collision.calculate_directions()
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_1),
                                           collision.coneIDs, col_line_id))
            col_line_id += 1
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_2),
                                           collision.coneIDs, col_line_id))
            col_line_id += 1

            # Create triangles for debugging
            triangles.append(collision.topCone.get_triangle_vertices(collision.scale, collision.vector_between))
            triangles.append(collision.bottomCone.get_triangle_vertices(collision.scale, collision.vector_between))

    # Connect the collision lines, depending on their cones
    for col_line in col_lines:
        breakFlag = False
        if not col_line.foundEnd:
            coneIDs = col_line.coneIDs
            for other_col_line in col_lines:
                # check if they're not from the same collision
                if not other_col_line.foundEnd:
                    if other_col_line.id != col_line.id:
                        # check if they share the first coneID
                        otherConeIDs = other_col_line.coneIDs
                        if coneIDs[0] == otherConeIDs[0]:
                            # we search for a third collision which has the missing 2 IDs
                            missingIDs = [coneIDs[1], otherConeIDs[1]]
                            missingIDs.sort()
                            for third_col_line in col_lines:
                                if not third_col_line.foundEnd:
                                    if missingIDs == third_col_line.coneIDs:
                                        # there are always 2 of those, so we need to check which intersects
                                        intersections = col_line.findClosestIntersections(
                                            [other_col_line, third_col_line])
                                        if intersections[1]:
                                            # The three lines intersect (yay)
                                            intersectionPoint = col_line.line.findIntersection2D(other_col_line.line)
                                            # We found 3 lines that form an intersection in the diagram
                                            setCollisionLineEnd(col_line.id, intersectionPoint)
                                            setCollisionLineEnd(other_col_line.id, intersectionPoint)
                                            setCollisionLineEnd(third_col_line.id, intersectionPoint)
                                            breakFlag = True
                                            break
                            if breakFlag:
                                break

    quadBoundaryLines = [
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(1, 0, 0)), [0,0], col_line_id),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), [0,0], col_line_id+1),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), [0,0], col_line_id+2),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(1, 0, 0)), [0,0], col_line_id+3),

        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(-1, 0, 0)), [0,0], col_line_id+4),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), [0,0], col_line_id + 5),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), [0,0], col_line_id + 6),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(-1, 0, 0)), [0,0], col_line_id + 7),

    ]

    buggy_lines = []
    # Handle all collisions with wall
    # TODO: Avoid the wrong lines by crossing them with final lines?
    for col_line in col_lines:
        if not col_line.foundEnd:
            wallHit = col_line.findClosestIntersections(quadBoundaryLines)
            if wallHit[0]:
                intersectionPoint = col_line.line.findIntersection2D(wallHit[0].line)
                setCollisionLineEnd(col_line.id, intersectionPoint)
            else:
                buggy_lines.append(col_line)


    """
    def findNextIntersection(inputLine, closestLines=None):
        if closestLines is None:
            closestLines = inputLine.findClosestIntersections(col_lines)

        closestLine = closestLines[0]
        secondClosestLine = closestLines[1]

        if not closestLine:
            # Inputline has no hit lines, i.e. it goes out of bounds
            wallHit = inputLine.findClosestIntersections(quadBoundaryLines)
            intersectionPoint = inputLine.line.findIntersection2D(wallHit[0].line)
            setCollisionLineEnd(inputLine.id, intersectionPoint)
            return False

        if secondClosestLine:
            intersectionPoint = inputLine.line.findIntersection2D(closestLine.line)
            intersectionPoint2 = inputLine.line.findIntersection2D(secondClosestLine.line)
            if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                # We found 3 lines that form an intersection in the diagram
                setCollisionLineEnd(inputLine.id, intersectionPoint)
                setCollisionLineEnd(closestLine.id, intersectionPoint)
                setCollisionLineEnd(secondClosestLine.id, intersectionPoint)
                return False

        # The 3 lines do not form an intersectionPoint
        # We need to find out if the input line is also closest from the hit line's origin
        closestLineClosestLines = closestLine.findClosestIntersections(col_lines)

        if closestLineClosestLines[0].id == inputLine.id:
            intersectionPoint = closestLineClosestLines[0].line.findIntersection2D(closestLine.line)
            setCollisionLineEnd(closestLine.id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[0].id, intersectionPoint)
            if closestLineClosestLines[1]:
                intersectionPoint2 = closestLineClosestLines[1].line.findIntersection2D(closestLine.line)
                if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                    setCollisionLineEnd(closestLineClosestLines[1].id, intersectionPoint)
            return False

        elif closestLineClosestLines[1] and closestLineClosestLines[1].id == inputLine.id:
            intersectionPoint = closestLineClosestLines[1].line.findIntersection2D(closestLine.line)
            setCollisionLineEnd(closestLine.id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[1].id, intersectionPoint)
            intersectionPoint2 = closestLineClosestLines[0].line.findIntersection2D(closestLine.line)
            if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                setCollisionLineEnd(closestLineClosestLines[0].id, intersectionPoint)
            return False

        else:
            # The hit line has a closer neighbor, we start the function again with those two lines as input
            return[closestLine, closestLineClosestLines]

    i = 0
    if drawAllCollisions:
    i = len(col_lines)
    final_lines = col_lines
    while i < len(col_lines):
        print(str(i) + "/" + str(len(col_lines)))
        line = col_lines[i]
        if not line.foundEnd:
            newInputLines = findNextIntersection(line)
            while newInputLines:
                print(str(i) + "/" + str(len(col_lines)))
                print(newInputLines[0].id, newInputLines[1][0].id, newInputLines[1][1].id)
                newInputLines = findNextIntersection(newInputLines[0], newInputLines[1])
        else:
            i += 1

        # Ideas for Cone:
        # Remove all further collisions inside the area those 3 lines form
        # (maybe research point inside non-convex hull polynomials)
    """

    """Render Stuff"""
    print("Preparing Render...")
    lines = []

    for col_line in final_lines:
        line = col_line.line
        if line.end is not None:
            lines.append([line.p.coords, line.end.coords])
        else:
            lines.append([line.p.coords, line.p.coords + line.norm_dir * 100])

    scatter_points = points_to_scatter(points, False)
    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))
    scatter_lines = []
    for line in lines:
        scatter_lines.append(points_to_scatter(line, False))
    scatter_buggy = []
    #for line in buggy_lines:
    #    scatter_buggy.append(points_to_scatter(line, False))
    scatter_collisions = points_to_scatter(col_points, False)


    data = []
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue', 'size': 5}))
    for scatter_line in scatter_lines:
        data.append(go.Scatter3d(x=scatter_line[0], y=scatter_line[1], z=scatter_line[2], mode='lines',
                                 line={'color': 'black'}))

    #for scatter_line in scatter_buggy:
    #    data.append(go.Scatter3d(x=scatter_line[0], y=scatter_line[1], z=scatter_line[2], mode='lines',
    #                             line={'color': 'red'}))

    for scatter_triangle in scatter_triangles:
        data.append(go.Scatter3d(x=scatter_triangle[0], y=scatter_triangle[1], z=scatter_triangle[2], mode='lines',
                                 line={'color': "lightblue"}))
    #data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
    #                                     mode='markers', marker={'color': 'violet', 'size': 5}))


    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[MIN_X, MAX_X], linewidth=1),
            yaxis=dict(tickmode="linear", range=[MIN_Y, MAX_Y], linewidth=1),
            zaxis=dict(tickmode="linear", range=[MIN_Z, MAX_Z], linewidth=1),
        ))
    fig.show()
    print_points(points)


if __name__ == '__main__':
    if len(sys.argv) > 3 and 0 <= float(sys.argv[3]) <= 1 and 0 <= float(sys.argv[2]) <= 90:
        main(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Usage: main.py <Number of points (ℕ)> <Theta (degrees, 0.0-90.0)> <Mew (scalar, 0.0-1.0)>")
