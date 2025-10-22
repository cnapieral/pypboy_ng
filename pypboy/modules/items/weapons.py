import pypboy
import pygame
import game
import config

class Module(pypboy.SubModule):
    label = " Weapons "
    
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
        
        # Create weapon instances
        self.weapons = [
            # Weapon("Chinese Army Knife", "images/weapons/knife.png", 5, 1, 20, 100, "Standard issue"),
            # Weapon("Combat Knife", "images/weapons/knife.png", 10, 2, 35, 100, "Sharp edge"),
            # Weapon("Sword", "images/weapons/sword.png", 15, 5, 50, 100, "Rusty but effective"),
            # Weapon("Pistol", "images/weapons/pistol.png", 20, 3, 80, 100, "Small but deadly"),
            # Weapon("Shotgun", "images/weapons/shotgun.png", 35, 8, 120, 100, "High damage"),
            Weapon("Flammenwerfer", "images/weapons/flamer.png", 45, 10, 200, 100, "Brenn es nieder")
        ]
        
        # Set up the weapon display
        self.selected_weapon = self.weapons[0]  # Default to first weapon
        
        # Create menu items for weapons
        menu_items = []
        for weapon in self.weapons:
            menu_items.append(weapon.name)
        
        # Create menu (this would need to be properly implemented based on your framework)
        # self.menu = pypboy.Menu(menu_items, self.change_items)
        
        # Display the selected weapon with stats
        self.display_weapon_stats(self.selected_weapon)
    
    def display_weapon_stats(self, weapon):
        # Add weapon to display
        self.add(weapon)
        
        # Draw stats on weapon image
        if weapon.image:
            # Draw value stat
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 2, 200), 
                           (weapon.image.get_width() - 2, 220), 2)
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 85, 200), 
                           (weapon.image.get_width(), 200), 2)
            text = config.FONTS[14].render(str(weapon.value), True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 85 - (text.get_width() + 5), 204))
            text = config.FONTS[14].render("VAL", True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 85 + 2, 204))
            
            # Draw weight stat
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 95, 200), 
                           (weapon.image.get_width() - 95, 220), 2)
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 95 - 85, 200), 
                           (weapon.image.get_width() - 95, 200), 2)
            text = config.FONTS[14].render(str(weapon.weight), True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 95 - (text.get_width() + 5), 204))
            text = config.FONTS[14].render("WG", True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 95 - 85 + 2, 204))
            
            # Draw damage stat
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 190, weapon.image.get_height() - 80), 
                           (weapon.image.get_width() - 190, weapon.image.get_height() - 60), 2)
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 190 - 85, 200), 
                           (weapon.image.get_width() - 190, 200), 2)
            text = config.FONTS[14].render(str(weapon.damage), True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 190 - (text.get_width() + 5), 204))
            text = config.FONTS[14].render("DAM", True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 190 - 85 + 2, 204))
            
            # Row 2
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 2, 230), 
                           (weapon.image.get_width() - 2, 250), 2)
            text = config.FONTS[14].render("-- --", True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 95 - 85 + 2, 234))
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 95 - 85, 230), 
                           (weapon.image.get_width(), 230), 2)
            
            # Draw condition
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 190, 230), 
                           (weapon.image.get_width() - 190, 250), 2)
            pygame.draw.line(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 190 - 85, 230), 
                           (weapon.image.get_width() - 190, 230), 2)
            pygame.draw.rect(weapon.image, (95, 255, 177), 
                           (weapon.image.get_width() - 190 - 55, 237, 40, 12))
            pygame.draw.rect(weapon.image, (0, 70, 0), 
                           (weapon.image.get_width() - 190 - 55 + 40, 237, 10, 12))
            text = config.FONTS[14].render("CND", True, (95, 255, 177), (0, 0, 0))
            weapon.image.blit(text, (weapon.image.get_width() - 190 - 85 + 2, 234))

    def change_items(self):
        print("Changing")

class Weapon(game.Entity):
    def __init__(self, name, imageloc, damage, weight, value, condition, notes):
        super(Weapon, self).__init__((config.WIDTH, config.HEIGHT))
        self.name = name
        self.imageloc = imageloc
        self.image = pygame.image.load(self.imageloc)
        self.damage = damage
        self.weight = weight
        self.value = value
        self.condition = condition
        self.notes = notes