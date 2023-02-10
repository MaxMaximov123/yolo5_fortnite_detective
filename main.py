import cv2
import os
# Model
import shutil
# Image


def get_img(img, model):
	# Inference
	results = model(img, size=640)  # includes NMS
	# results.save()
	# shutil.rmtree('runs/detect')
	results.render()
	return results.ims[0]