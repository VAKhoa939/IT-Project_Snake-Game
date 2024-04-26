import pygame

def is_clicked(object, event, mouse):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouse[0] > object.position[0] and mouse[0] < object.position[0] + object.width:
            if mouse[1] > object.position[1] and mouse[1] < object.position[1] + object.height:
                return True
    return False
    