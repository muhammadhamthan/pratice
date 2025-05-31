from pathlib import Path
from ultralytics import YOLO

#PRE-DEFINITED YOLOV9
model =  YOLO('yolov9s.pt')

image_path = Path(r'C:\Users\muham\OneDrive\Pictures\Desktop\python\ham\bus.jpg')                  

results = model(image_path)
print(results)

#specify the output folder
output_dir = Path(r'C:\Users\muham\OneDrive\Pictures\Desktop\python\ham\output_image')

output_dir.mkdir(parents=True, exist_ok=True)# ensure the output folder exists and it is used to create the folder automatically


#save the resulting image with detected objects to the output folder
output_image_path = output_dir / 'image1.jpg'

results[0].save(output_image_path) # IT IS USED TO SAVE THE FIRST IMAGE (BY MENTIONING "RESULTS[0]")



