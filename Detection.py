import cv2

import numpy as np
def ORB(input_image, stored_image):

	    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)


	    orb_detector = cv2.ORB(1600, 1.3)


	    (keypoints_1, descriptor_1) = orb_detector.detectAndCompute(gray, None)

	    (keypoints_2, descriptor_2) = orb_detector.detectAndCompute(stored_image, None)

	    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	    matches_found =  brute_force.match(descriptor_1,descriptor_2)


	    matches_found = sorted(matches_found, key=lambda val: val.distance)

	    return len(matches_found)
def detGlass(temp):

	capture = cv2.VideoCapture(0)

	stored_image = cv2.imread('cam.jpg', 0)

	glass_count = 0

	n=0
	while n<30:
		n+=1
		ret, capturing = capture.read()

		frame_height, frame_width = capturing.shape[:2]

		x1_top_left = frame_width / 3
		y1_top_left = (frame_height / 2) + (frame_height / 4)
		x2_bottom_right = (frame_width / 3) * 2
		y2_bottom_right = (frame_height / 2) - (frame_height / 4)

		### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)
	    

		cropped_box = capturing[y2_bottom_right:y1_top_left , x1_top_left:x2_bottom_right]
		capturing = cv2.flip(capturing,1)
		matches_found = ORB(cropped_box, stored_image)
		string = "Matches Found = " + str(matches_found)
		

		cv2.putText(capturing, string, (150,400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
		set_threshold = 120
		if matches_found > set_threshold:
			
			glass_count += 1
			#resized_frame = cv2.resize(capturing, (250, 250))
			#gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
			#path = './glass_count/' + str(glass_count) + '.jpg'
			#cv2.imwrite(path, gray)
			#cv2.putText(gray, str(glass_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
			#cv2.imshow('Detection', gray)

			#cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

			#cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

		#cv2.imshow('Glass_Detection', capturing)

		#c = cv2.waitKey(1)
		

	capture.release()
	cv2.destroyAllWindows()	
	if glass_count > 5:
		temp = 1
	return temp
def detMetal(temp):

	capture = cv2.VideoCapture(0)

	stored_image = cv2.imread('cocacola.jpg', 0)

	metal_count = 0

	n=0
	while n<30:
		n+=1
		ret, capturing = capture.read()

		frame_height, frame_width = capturing.shape[:2]

		x1_top_left = frame_width / 3
		y1_top_left = (frame_height / 2) + (frame_height / 4)
		x2_bottom_right = (frame_width / 3) * 2
		y2_bottom_right = (frame_height / 2) - (frame_height / 4)

		### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)
	    

		cropped_box = capturing[y2_bottom_right:y1_top_left , x1_top_left:x2_bottom_right]
		capturing = cv2.flip(capturing,1)
		matches_found = ORB(cropped_box, stored_image)
		string = "Matches Found = " + str(matches_found)
		

		cv2.putText(capturing, string, (150,400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
		set_threshold = 120
		if matches_found > set_threshold:
			
			metal_count += 1
			#resized_frame = cv2.resize(capturing, (250, 250))
			#gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
			#path = './metal_count/' + str(metal_count) + '.jpg'
			#cv2.imwrite(path, gray)
			#cv2.putText(gray, str(metal_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
			#cv2.imshow('Detection', gray)

			#cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

			#cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

		#cv2.imshow('Metal_Detection', capturing)

		#c = cv2.waitKey(1)
		

	capture.release()
	cv2.destroyAllWindows()
	if metal_count > 5:
		temp = 2
	return temp
def detPet(temp):

	capture = cv2.VideoCapture(0)

	stored_image = cv2.imread('Pet.jpg', 0)

	pet_count = 0

	n=0
	while n<30:
		n+=1
		ret, capturing = capture.read()

		frame_height, frame_width = capturing.shape[:2]

		x1_top_left = frame_width / 3
		y1_top_left = (frame_height / 2) + (frame_height / 4)
		x2_bottom_right = (frame_width / 3) * 2
		y2_bottom_right = (frame_height / 2) - (frame_height / 4)

		### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)
	    

		cropped_box = capturing[y2_bottom_right:y1_top_left , x1_top_left:x2_bottom_right]
		capturing = cv2.flip(capturing,1)
		matches_found = ORB(cropped_box, stored_image)
		string = "Matches Found = " + str(matches_found)
		

		cv2.putText(capturing, string, (150,400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
		set_threshold = 120
		if matches_found > set_threshold:
			
			pet_count += 1
			#resized_frame = cv2.resize(capturing, (250, 250))
			#gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
			#path = './pet_count/' + str(pet_count) + '.jpg'
			#cv2.imwrite(path, gray)
			#cv2.putText(gray, str(pet_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
			#cv2.imshow('Detection', gray)

			#cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

			#cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

		#cv2.imshow('Pet_Detection', capturing)

		#c = cv2.waitKey(1)
		
	capture.release()
	cv2.destroyAllWindows()
	if pet_count > 5:
		temp = 3
	return temp
temp = 0
if detGlass(temp) == 1:
	print("Glass")
elif detMetal(temp) == 2:
	print("Metal")
elif detPet(temp) == 3:
	print("Pet")
else:
	print("Other")
