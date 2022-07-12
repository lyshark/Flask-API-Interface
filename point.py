def isPointinPolygon(point, rangelist):  # [[0,0],[1,1],[0,1],[0,0]] [1,0.8]
    # 判断是否在外包矩形内，如果不在，直接返回false
    lnglist = []
    latlist = []
    for i in range(len(rangelist) - 1):
        lnglist.append(rangelist[i][0])
        latlist.append(rangelist[i][1])
    print(lnglist, latlist)
    maxlng = max(lnglist)
    minlng = min(lnglist)
    maxlat = max(latlist)
    minlat = min(latlist)
    print(maxlng, minlng, maxlat, minlat)
    if (point[0] > maxlng or point[0] < minlng or
            point[1] > maxlat or point[1] < minlat):
        return False
    count = 0
    point1 = rangelist[0]
    for i in range(1, len(rangelist)):
        point2 = rangelist[i]
        # import pdb
        # pdb.set_trace()
        # 点与多边形顶点重合
        if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
            print("在顶点上")
            return False

        # 判断线段两端点是否在射线两侧 不在肯定不相交 射线（-∞，lat）（lng,lat）
        if (point1[1] < point[1] and point2[1] >= point[1]) or (point1[1] >= point[1] and point2[1] < point[1]):
            # 求线段与射线交点 再和lat比较
            point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1])
            print(point12lng)
            # 点在多边形边上

            if (point12lng == point[0]):

                print("点在多边形边上")
                return False

            if (point12lng > point[0]):
                # print(count)
                count += 1

        point1 = point2

    print(count)
    if count % 2 == 0:
        return False
    else:
        return True


if __name__ == '__main__':

    print(isPointinPolygon([116.483145, 39.902757], [[116.356287, 39.906115],
                                                    [116.38341, 39.915266],
                                                    [116.451988, 39.920006],
                                                    [116.424093, 39.915266],
                                                    [116.453447, 39.898609],
                                                    [116.424093, 39.897753],
                                                    [116.397228, 39.885636],
                                                    [116.38341, 39.897753],
                                                     ]))