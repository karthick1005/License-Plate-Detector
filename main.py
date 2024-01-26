from ultralytics import YOLO
import cv2

import util
from sort import *
from util import get_car, read_license_plate, write_csv, check_image

results = {}

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./models/license_plate_detector.pt')
vehiclexml = cv2.CascadeClassifier('cars.xml')


def check_file():
    frame = cv2.imread('detected_vehicle.png')

    vehicles = [2, 3, 5, 7]

    # Detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])

    # Track vehicles
    # track_ids = mot_tracker.update(np.asarray(detections_))

    # Detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # Assign license plate to car
        # xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)
        #
        # if car_id != -1:
        # Crop license plate
        license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

        # Process license plate
        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
        # Visualize or save the results if needed
        # visualize_plot(license_plate_crop, license_plate_crop_gray, license_plate_crop_thresh)

        # Read license plate number
        # plate_crop= check_image(license_plate_crop_thresh,license_plate_crop_gray)
        # # print(plate_crop)
        license_plate_text = read_license_plate(license_plate_crop_gray)
        print(license_plate_text)

        # Store results if needed
        # results[car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
        #                   'license_plate': {'bbox': [x1, y1, x2, y2],
        #                                     'text': license_plate_text,
        #                                     'bbox_score': score,
        #                                     'text_score': license_plate_text_score}}

    # Print or save the final results if needed
    # print(results)

    # Optionally, write the results to a CSV file
    # write_csv(results, './test.csv')


def live_video():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        controlkey = cv2.waitKey(1)
        if ret:
            vehicle = vehiclexml.detectMultiScale(frame, 1.15, 4)

            if len(vehicle) != 0:
                cv2.imwrite('detected_vehicle.png', frame)
                check_file()
            # for (x, y, w, h) in vehicle:
            #     print("vehicle detected")
            #     cv2.imwrite('detected_vehicle.png', frame)
            #     check_file()
            cv2.imshow('vehicle detected', frame)
        else:
            break
        if controlkey == ord('q'):
            break


def visualize_plot(license_plate_crop, license_plate_crop_gray, license_plate_crop_thresh):
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(1, 3, 2)
    plt.imshow(license_plate_crop_gray, cmap='gray')
    plt.title('Grayscale Image')

    plt.subplot(1, 3, 3)
    plt.imshow(license_plate_crop_thresh, cmap='gray')
    plt.title('Thresholded Image')

    plt.show()


def recordedvideo():
    # load video
    cap = cv2.VideoCapture('./sample2.mp4')

    vehicles = [2, 3, 5, 7]
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    # read frames
    frame_nmr = -1
    frame_nmr = -1
    ret = True
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:
                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255,
                                                                 cv2.THRESH_BINARY_INV)
                    visualize_plot(license_plate_crop, license_plate_crop_gray, license_plate_crop_thresh)
                    # read license plate number
                    # license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                    license_plate_text = read_license_plate(license_plate_crop_thresh)
                    print(license_plate_text)
                    # if license_plate_text is not None:
                    # results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                    #                               'license_plate': {'bbox': [x1, y1, x2, y2],
                    #                                                 'text': license_plate_text,
                    #                                                 'bbox_score': score,
                    #                                                 'text_score': license_plate_text_score}}

    # write results
    # write_csv(results, './test.csv')


val = int(input("Enter whether live video (0) or recorded video(1)"))
if val==0:
    live_video()
else :
    recordedvideo()
