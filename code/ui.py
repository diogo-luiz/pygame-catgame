import pygame

class UI:
    def __init__(self, surface):
        
        self.display_surface = surface
        self.teste = False
        # coins
        self.coin = pygame.image.load('graphics/ui/coin.png')
        self.coin_rect = self.coin.get_rect(topleft= (50,61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF',30)
    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)

    def show_interact(self):
        texto = self.font.render('Pressione E para pegar', False, '#33323d')
        texto_rect = texto.get_rect(midleft = (600,360))
        self.display_surface.blit(texto,texto_rect)