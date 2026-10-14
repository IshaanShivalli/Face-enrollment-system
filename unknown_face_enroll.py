from project.utils import Conf
from imutils.video import VideoStream
from tinydb import TinyDB
import face_recognition
import argparse
import imutils
import time
import cv2
import os
from imutils import paths

                                                       
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--id", required=True, 
 help="Unique student ID of the student")
ap.add_argument("-n", "--name", required=True, 
 help="Name of the student")
ap.add_argument("-c", "--conf", default="config/config.json", 
 help="Path to the input configuration file")
args = vars(ap.parse_args())

                             
conf = Conf(args["conf"])

                                                   
db = TinyDB(conf["db_path"])
studentTable = db.table("student")
print(studentTable)
                                            
student = studentTable.search(lambda record: args["id"] in record)

uk_images = list(paths.list_images("unknown"))

                                                                    
                    
if len(student) == 0: 

	for uk_image in uk_images:

		time.sleep(2.0)

                                                                 
                            
		faceCount = 0
		total = 0

                                      
		status = "detecting"

                                                    
		os.makedirs(os.path.join(conf["dataset_path"], conf["class"], 
		 args["id"]), exist_ok=True)

                                              
		while conf["n_face_detection"]>=total:
                                                                 
                                                               
                                                               
                         
			frame = cv2.imread(uk_image)
			frame = imutils.resize(frame, width=400)
			frame = cv2.flip(frame, 1)
			orig = frame.copy()
    
                                                              
                                                            
                                                                 
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			boxes = face_recognition.face_locations(rgb,
			 model=conf["detection_method"])
   
                                  
			for (top, right, bottom, left) in boxes:
                                           
				cv2.rectangle(frame, (left, top), (right, bottom), 
				 (0, 0,255), 2)

                                                           
                                                        
				if faceCount < conf["n_face_detection"]:
                                                    
                               
					faceCount += 1
					status = "detecting"
					continue

                                                             
                            
                                                      
				img_path = uk_image.split('\\')[-1].split(".")[0]
				p = os.path.join(conf["dataset_path"], conf["class"],
				 args["id"],f"{str(total).zfill(5)}_{img_path}.png")
				cv2.imwrite(p, orig[top:bottom, left:right])
				total += 1

                                     
				status = "saving"

                                    
			cv2.putText(frame, "Status: {}".format(status), (10, 20),
			 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                          
			cv2.imshow("Frame", frame)
			cv2.waitKey(5)

                                                                  
              
			if total == conf["face_count"]:
				break

                                                
		studentTable.insert({args["id"]: [args["name"], "enrolled"]})

                                                       
		print("[INFO] {} face images stored".format(total))
		print("[INFO] cleaning up...")
		cv2.destroyAllWindows()
             

                                              
else:
                              
	name = student[0][args["id"]][0]
	print("[INFO] {} has already already been enrolled...".format(
	 name))

                    
db.close()
