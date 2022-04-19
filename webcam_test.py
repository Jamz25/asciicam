import cv2 as cv
import pygame
import threading
import time

pygame.init()
screen = pygame.display.set_mode((575, 620))
pygame.display.set_caption("ASCII CAMERA")
font = pygame.font.SysFont("Calibri", 9)
clock = pygame.time.Clock()

capture = cv.VideoCapture(0)

ASCII_VALUES = 'Ñ@#W$9876543210?!abc;:+=-,._'
depth_const = 256 / len(ASCII_VALUES)
ascii_renders = [font.render(ASCII_VALUES[value], False, (255-(depth_const*value), 255-(depth_const*value), 
    255-(depth_const*value))) for value in range(len(ASCII_VALUES))]

CAM_DIMENSIONS = (64, 64)
pixel_array = [[len(ASCII_VALUES) - 1 for pixel in range(CAM_DIMENSIONS[1])] 
for row in range(CAM_DIMENSIONS[0])]

def _asciify(pixel):
    value = max(min(len(ASCII_VALUES) - int(pixel / depth_const), len(ASCII_VALUES) - 1), 0)
    return value

def convert_to_ascii(frame_content):
    global pixel_array, send_packet
    for r_index, row in enumerate(frame_content):
        for p_index, pixel in enumerate(row):
            pixel_array[p_index][r_index] = _asciify(pixel)

def camera_thread():
    while running:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (CAM_DIMENSIONS[0], CAM_DIMENSIONS[1]))
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        convert_to_ascii(frame)

camera_surface = pygame.Surface((575, 578))
running = True
threading.Thread(target=camera_thread).start()
while running:

    clock.tick(60)
    pygame.display.set_caption("ASCII CAMERA - " + str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.image.save(camera_surface, str(hash(time.time())) + ".png")

    screen.fill((80, 80, 80))
    camera_surface.fill(0)

    for r_index, row in enumerate(pixel_array):
        for p_index, pixel in enumerate(row):
            camera_surface.blit(ascii_renders[pixel], (r_index * 9, p_index * 9))

    screen.blit(camera_surface, (0, 0))

    pygame.display.update()

capture.release()
cv.destroyAllWindows()
pygame.quit()