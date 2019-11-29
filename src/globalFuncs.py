import pygame
def toggleFull(win): #global functions
    win = pygame.display.get_surface()
    tmp = win.convert()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = win.get_width(),win.get_height()
    flags = win.get_flags()
    bits = win.get_bitsize()
    
    win = pygame.display.set_mode((w,h),flags^pygame.FULLSCREEN,bits)
    win.blit(tmp,(0,0))

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return win
