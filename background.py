import pygame
import random
from bird import Bird

minimumDistance = 200
maxSpread = 350

cloudSpeed = 120
objectSpeed = 90


def check(objectList):
    res = []
    for i in objectList:
        res.append(i.x)
    res.sort()
    for i in range(len(res) - 1):
        if res[i + 1] - res[i] < minimumDistance:
            return False
    return True


def recreatelist(s, objectList):
    res = []
    for i in objectList:
        res.append(i.x)
    res.sort()
    for i in range(len(res) - 1):
        while res[i + 1] - res[i] < minimumDistance:
            res[i + 1] += 50

    returnee = []

    for i in res:
        returnee.append(s.Object(s.screensize))
        returnee[-1].x = i
    return returnee


class Background:
    class Cloud:
        def __init__(self):
            self.img = pygame.image.load(r"res/cloud.png")
            self.x = 0
            self.y = 0

        def __repr__(self):
            return f"object Cloud. img={self.img}. x,y={(self.x, self.y)}"

    class Object:
        def __init__(self, screensize):
            self.top = pygame.image.load(r"res/column_top.png")
            self.body = pygame.image.load(r"res/column_body.png")
            self.bottom = pygame.image.load(r"res/column_bottom.png")
            self.bottomHeight = 15
            self.bodyHeight = 94
            self.topHeight = 15
            self.dx = 6
            self.width = 85
            self.x = screensize[0] + random.randint(0, maxSpread)
            self.y = 200
            self.height = screensize[0]
            self.columnsBottom = random.randint(0, 3)
            self.columnsTop = random.randint(0, 3 - self.columnsBottom)

        def __repr__(self):
            return f"object Object. x={self.x}, y={self.y}, height={self.height}, bottomCol={self.columnsBottom}, topHole={self.columnsTop}"

    def __init__(self, screen, color=(40, 255, 255), terraincolor=(0, 255, 0)):
        self.screensize = (screen.get_width(), screen.get_height())
        self.color = color
        self.terraincolor = terraincolor
        self.objects = [
            self.Object(self.screensize) for _ in range(3)
        ]
        if not check(self.objects):
            self.objects = recreatelist(self, self.objects)
        self.removed = 0  # number of objects removed. Used for the difficulty
        self.sky = [
            self.Cloud() for _ in range(10)
        ]
        for i, cloud in enumerate(self.sky):
            cloud.x = self.screensize[0] / len(self.sky) * i + random.randint(-50, 50)
            cloud.y = random.randint(0, self.screensize[1] * 4 / 5)

    def showTerrain(self, screen: pygame.display):

        pygame.draw.rect(screen, self.terraincolor, pygame.Rect(
            0, self.screensize[1] * 4 / 5, self.screensize[0], self.screensize[1] / 5)  # fill a third of the screen
                         )

    def moveSky(self, screen, dt):

        for cloud in self.sky:

            screen.blit(cloud.img, (cloud.x, cloud.y))

            cloud.x -= cloudSpeed * dt

            if cloud.x < -136:
                self.sky.remove(cloud)
                a = self.Cloud()
                a.y = random.randint(-50, self.screensize[1])
                a.x = self.screensize[0]
                self.sky.append(a)

    def updateObjects(self, screen: pygame.display, dt: float, bird: Bird):

        for obj in self.objects:

            if obj.x < -obj.width:
                self.objects.remove(obj)
                self.removed += 1
                self.objects.append(self.Object(self.screensize))
                if self.objects[-2].x > self.screensize[0] - minimumDistance:
                    self.objects[-1].x = self.objects[-2].x + minimumDistance + random.randint(0, maxSpread)
                if not self.removed % 15 and len(self.objects) < 7:
                    self.objects.append(self.Object(self.screensize))
                    self.objects[-1].x = self.objects[-2].x + minimumDistance + random.randint(0, maxSpread)

            else:
                rects = [
                    obj.bottom.get_rect(x=obj.x, y=self.screensize[1] - obj.bottomHeight),
                    obj.body.get_rect(x=obj.x + obj.dx, y=self.screensize[1] - obj.bottomHeight - obj.bodyHeight),
                    obj.top.get_rect(x=obj.x, y=0),
                    obj.body.get_rect(x=obj.x + obj.dx, y=obj.topHeight)
                ]
                obj.x -= objectSpeed * dt
                # show the object
                # bottom
                screen.blit(obj.bottom, (obj.x, self.screensize[1] - obj.bottomHeight))
                screen.blit(obj.body, (obj.x + obj.dx, self.screensize[1] - obj.bottomHeight - obj.bodyHeight))
                # top
                screen.blit(obj.top, (obj.x, 0))
                screen.blit(obj.body, (obj.x + obj.dx, obj.topHeight))
                # bottom columns
                for i in range(obj.columnsBottom):
                    screen.blit(
                        obj.body,
                        (obj.x + obj.dx, self.screensize[1] - obj.bottomHeight - obj.bodyHeight * (i + 1))
                    )
                    rects.append(obj.body.get_rect(x=obj.x + obj.dx,
                                                   y=self.screensize[1] - obj.bottomHeight - obj.bodyHeight * (i + 1)))

                # top columns
                for i in range(obj.columnsTop):
                    screen.blit(
                        obj.body,
                        (obj.x + obj.dx, obj.bottomHeight + obj.bodyHeight * (i + 1))
                    )
                    rects.append(obj.body.get_rect(x=obj.x + obj.dx, y=obj.bottomHeight + obj.bodyHeight * (i + 1)))

                # check for collisions
                for rect in rects:
                    if bird.surface.get_rect(
                            x=bird.x, y=bird.y
                    ).colliderect(rect):
                        pygame.quit()
                        exit(0)
