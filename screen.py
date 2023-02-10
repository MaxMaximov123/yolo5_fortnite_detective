import dxcam
import win32api, win32con
import pygame
import torch
import keyboard
import cv2
from yolov5.main import get_img
import numpy as np


f = True
FPS = 15


print(torch.cuda.is_available())

model = torch.hub.load('ultralytics/yolov5', 'custom', path='pt/best.pt')
model.cuda()
face_cascade_db = cv2.CascadeClassifier("cascades/haarcascade_wallclock.xml")


def click(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


camera = dxcam.create()
camera.start(target_fps=FPS, video_mode=True)


def ex():
	global f
	f = False

k = 1
w, h = int(960 * k), int(540 * k)

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((w, h))
	pygame.display.flip()
	clock = pygame.time.Clock()
	keyboard.add_hotkey('ctrl+X', lambda: ex())
	while f:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				f = False

		image = camera.get_latest_frame()
		image = cv2.resize(image, dsize=(w, h), interpolation=cv2.INTER_CUBIC)
		# print(type(image))
		image = get_img(image, model)
		size = len(image), len(image[0])
		image = np.rot90(image, k=-1)
		image = np.fliplr(image)
		surf = pygame.pixelcopy.make_surface(image)
		surf = pygame.transform.scale(surf, (w, h))
		step = 2
		screen.blit(surf, (0, 0))
		my_font = pygame.font.SysFont(False, 50)
		text_surface = my_font.render(str(round(clock.get_fps(), 4)), False, (255, 0, 0))
		screen.blit(text_surface, (50, 50))
		pygame.display.flip()
		clock.tick(FPS)
	pygame.quit()
