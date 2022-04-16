import cv2 as cv
import pygame
import threading

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ASCII CAMERA")
font = pygame.font.SysFont("Calibri", 16)
clock = pygame.time.Clock()

capture = cv.VideoCapture(0)

ASCII_VALUES = '  Ñ@#W$9876543210?!abc;:+=-,._    '
ascii_renders = [font.render(value, False, (255, 255, 255)) for value in ASCII_VALUES]
depth_const = 256 / len(ASCII_VALUES)

class Pixel:
    def __init__(self, value):
        self.value = value

    def change_value(self, value):
        self.value = value

    def draw(self, screen, position):
        screen.blit(ascii_renders[self.value], position)

CAM_DIMENSIONS = (48, 48)
pixel_array = [[Pixel(len(ASCII_VALUES) - 1) for pixel in range(CAM_DIMENSIONS[1])] 
for row in range(CAM_DIMENSIONS[0])]

def _asciify(pixel):
    value = max(min(int(pixel / depth_const), len(ASCII_VALUES)), 0)
    return value

def convert_to_ascii(frame_content):
    global pixel_array
    for r_index, row in enumerate(frame_content):
        for p_index, pixel in enumerate(row):
            pixel_array[p_index][r_index].change_value(_asciify(pixel))

def camera_thread():
    while running:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (CAM_DIMENSIONS[0], CAM_DIMENSIONS[1]))
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        convert_to_ascii(frame)

running = True
threading.Thread(target=camera_thread, daemon=True).start()
while running:

    clock.tick(60)
    pygame.display.set_caption("ASCII CAMERA - " + str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    for r_index, row in enumerate(pixel_array):
        for p_index, pixel in enumerate(row):
            pixel.draw(screen, (100 + r_index * 12, p_index * 12))

    pygame.display.update()

capture.release()
cv.destroyAllWindows()
pygame.quit()