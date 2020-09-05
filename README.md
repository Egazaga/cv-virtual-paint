# cv-virtual-paint
Virtual paint made using yolov4 and OpenCV.  
Video demonstration: https://youtu.be/ZJdUfrZnqzw

## Additional downloads
Yolov4 weights. Copy this to model/ folder.  
https://drive.google.com/file/d/1RH37aFcNyoAesPxnTW4JE8VzGKSaEUTo/view?usp=sharing

## Useful links
### Pre-built OpenCV versions with CUDA support
Copy lib\python3\cv2.cp37-win_amd64.pyd from archive to \venv\Lib\site-packages. With CUDA detection rate is around 17 fps on GTX 1060 6GB, without CUDA it's 1 fps.  
https://jamesbowley.co.uk/downloads/
### Google colab for yolov4 training
Google colab is a free remote linux server with IPython environment and Nvidia Tesla GPU. Link leads to tutorial for training the model.  
https://colab.research.google.com/drive/1mzL6WyY9BRx4xX476eQdhKDnd_eixBlG
### Anotation tool
Awesome web app for converting raw video to annotated detection dataset. A 40 second video got me about 1000 training images, which was enough for this task.  
https://cvat.org
### Dataset augmentation tool
Increace the size of your dataset by croping, rotating and changing brightness.  
https://app.roboflow.com
