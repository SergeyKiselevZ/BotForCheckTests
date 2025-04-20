import cv2
import numpy as np
import math


def find_contours(photo):
    thresh = 120
    ret,thresh_img = cv2.threshold(photo, thresh, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros(photo.shape)
    cv2.drawContours(img_contours, contours, -1, (255,255,255), 1)
    return  contours

def four_point_transform(image, rect):
	(tl, tr, br, bl) = [i for i in rect]

	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	return warped

def get_dist(point1, point2):
    d1 = point1[0] - point2[0]
    d2 = point1[1] - point2[1]
    return math.sqrt(d1 * d1 + d2 * d2)

def get_rect(countur_item):
    if get_dist(countur_item[0][0], countur_item[2][0])>get_dist(countur_item[1][0], countur_item[3][0]):
        x1 = countur_item[0][0][0]
        y1 = countur_item[0][0][1]
        x2 = countur_item[2][0][0]
        y2 = countur_item[2][0][1]

        return (x1,y1), (x2,y2)
    else:
        x1 = countur_item[1][0][0]
        y1 = countur_item[1][0][1]
        x2 = countur_item[3][0][0]
        y2 = countur_item[3][0][1]

        return (x1, y1), (x2, y2)


def get_average_area(contours):
    sum = 0
    count = 0

    for contour in contours:
        sum += cv2.contourArea(contour)
        count += 1

    average_area = sum/count
    return average_area
new_images = []

def do_approx(contours):

    approxes = []
    all_approxes = []
    for contour in contours:
        arclen = cv2.arcLength(contour, True)
        eps = 0.05
        epsilon = arclen * eps
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) != 4:
            continue
        all_approxes.append(approx)
    average_area = get_average_area(all_approxes)
    for i in all_approxes:
        if cv2.contourArea(i) < average_area:
            continue
        if len(i) != 4:
            continue
        approxes.append(i)
    return approxes

def cut(photo, approx):
    p1, p2 = get_rect(approx)
    return photo[min(p1[1], p2[1]):max(p1[1], p2[1]), min(p1[0], p2[0]):max(p1[0], p2[0])]


def convert_photo(photo):
    new_photo = cv2.medianBlur(photo, 7)
    new_photo = cv2.GaussianBlur(new_photo, (7, 7), 0)
    photo_grey = cv2.cvtColor(new_photo, cv2.COLOR_BGR2GRAY)
    return photo_grey

def core(path: str, name: str, id):
    new_names = []
    src_photo = cv2.imread(path+name)
    photo = convert_photo(src_photo)
    contours = find_contours(photo)
    approxes = do_approx(contours)
    for i,approx in enumerate(approxes):
        cv2.imwrite(f'tests/{id}/{name.replace('.jpg', '')}{i}.jpg', cut(src_photo, approx))
        new_names.append(f'{name.replace('.jpg', '')}{i}.jpg')
    return new_names

def core_t(name):
    new_names = []
    src_photo = cv2.imread(name)
    photo = convert_photo(src_photo)
    contours = find_contours(photo)
    #cv2.drawContours(src_photo, contours, -1, (255, 255, 255), 1)
    approxes = do_approx(contours)
    for i,approx in enumerate(approxes):
        print(approx)
        #cv2.imwrite(f'{name.replace('.jpg', '')}{i}.jpg', cut(src_photo, approx))
        cv2.drawContours(src_photo, [approx], -1, (255, 255, 255), 1)
        #new_names.append(f'{name.replace('.jpg', '')}{i}.jpg')
    #return new_names
    cv2.imshow('fd', src_photo)
    cv2.waitKey()
    cv2.destroyAllWindows()

#('tmp/1508526598/AgACAgIAAxkBAAIL1Gf-ali7V00uLYj2ZUqPeTAlIai4AAKI6TEbgQnxSzY8gbpAz9nUAQADAgADeQADNgQ.jpg')