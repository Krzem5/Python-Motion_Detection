from PIL import Image, ImageDraw
import cv2
import numpy
import os
import threading



class MotionDetection:
	def __init__(self,**opts):
		self.opts={"cam_id":0,"image_scale_factor":1,"max_color_diff":[10,10,10]}
		self.opts.update(opts)
		self.cap=cv2.VideoCapture(self.opts["cam_id"])
		self.last_img=None
		self.d_img=[]
		self.motion=False



	def start(self):
		thr=threading.Thread(target=self.loop,args=(),kwargs={})
		thr.deamon=True
		thr.start()



	def loop(self):
		while True:
			_,img=self.cap.read()
			if (type(img)!=numpy.ndarray):
				return
			self.d_img,self.motion=self.detect_motion(img)



	def detect_motion(self,img):
		h,w,_=img.shape
		img=cv2.resize(img,(w//self.opts["image_scale_factor"],h//self.opts["image_scale_factor"]))
		img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		img=Image.fromarray(img)
		data=list(img.getdata())
		if (self.last_img==None):
			self.last_img=img
			img=img.resize((img.width*self.opts["image_scale_factor"],img.height*self.opts["image_scale_factor"]))
			return cv2.cvtColor(numpy.array(img),cv2.COLOR_RGB2BGR),False
		l_data=list(self.last_img.getdata())
		self.last_img=img
		for i in range(0,len(data)):
			c1=data[i]
			c2=l_data[i]
			if (abs(c1[0]-c2[0])>self.opts["max_color_diff"][0] or abs(c1[1]-c2[1])>self.opts["max_color_diff"][1] or abs(c1[2]-c2[2])>self.opts["max_color_diff"][2]):
				img=img.resize((img.width*self.opts["image_scale_factor"],img.height*self.opts["image_scale_factor"]))
				return cv2.cvtColor(numpy.array(img),cv2.COLOR_RGB2BGR),True
		img=img.resize((img.width*self.opts["image_scale_factor"],img.height*self.opts["image_scale_factor"]))
		return cv2.cvtColor(numpy.array(img),cv2.COLOR_RGB2BGR),False



DETECTION=MotionDetection(cam_id=1,image_scale_factor=10,max_color_diff=[40,40,40])
DETECTION.start()



while True:
	_,img=DETECTION.cap.read()
	cv2.imshow("Cam",img)
	os.system("CLS")
	if (DETECTION.motion==True):
		cv2.imshow("Detection",DETECTION.d_img)
		print("Yes")
	else:
		print("No")
	if (cv2.waitKey(30)&0xff==27):
		break
DETECTION.cap.release()
cv2.destroyAllWindows()