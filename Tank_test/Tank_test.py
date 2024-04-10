import turtle
import random
import math

#Screen Settings
screen = turtle.Screen()          # for screen (window)
screen.setup(500, 500)
screen.tracer(0)
screen.bgcolor('blue')

import turtle
 
# Defines a new class, Grid with a specified size.
class Grid:
    def __init__(self, size):
        self.size = size
        self.obstacles = {}  # Creates an empty dictionary which can store obstacles.
    
    # Defines a method to toggle whether or not there is an obstacle at the specified row and column coordinates.
    def toggle_obstacle(self, row, col):
        # The conditional statement checks whether the row and column coordinates are within the grid boundaries
        # between 0 and self.size and if there's an obstacle present at those coordinates.
        if (0 <= row < self.size) and (0 <= col < self.size):
            if (row, col) in self.obstacles:
                del self.obstacles[(row, col)]  # Removes any obstacle if they are already present.
            else:
                self.obstacles[(row, col)] = True  # Adds obstacle if it is empty.
 
    #Defines a method to check whether or not there is an obstacle at the specified coordinate. Returns True/False.
    def is_obstacle(self, row, col):
        return (0 <= row < self.size) and (0 <= col < self.size) and ((row, col) in self.obstacles)
 
# Function to convert the existing screen coordinates into grid coordinates
def screen_to_grid(x, y, cell_size):
    row = int(y // cell_size)
    col = int(x // cell_size)
    return row, col
 
# Function to handle the mouse clicks.
def handle_click(x, y):
    row, col = screen_to_grid(x, y, cell_size)
    grid.toggle_obstacle(row, col)
    draw_grid()
 
# Function to draw the grid and obstacles
def draw_grid():
    turtle.clear()
    turtle.penup()
    turtle.speed(0)
    for row in range(grid.size):
        for col in range(grid.size):
            x = col * cell_size
            y = row * cell_size
            if grid.is_obstacle(row, col):
                draw_obstacle(x, y, cell_size)
            else:
                draw_empty_square(x, y, cell_size)
    turtle.update()
 
# Function to draw an obstacle at a given coordinate
def draw_obstacle(x, y, size):
    turtle.goto(x + size // 2, y + size // 2)
    turtle.pendown()
    turtle.fillcolor('black')
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()
 
# Function to draw an empty square at a given coordinate.
def draw_empty_square(x, y, size):
    turtle.goto(x, y)
    turtle.pendown()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.penup()
 
# Initializes the grid.
grid_size = 30
grid = Grid(grid_size)
cell_size = 20
 
# Setting up the turtle screen.
turtle.setup(grid_size * cell_size, grid_size * cell_size)
turtle.Screen().bgcolor('white')
turtle.Screen().onclick(handle_click)
turtle.hideturtle()
 


#Tank draw settings
tank = turtle.Turtle()
tank.speed(0)                 # draw as fast as possible
tank.width(4)                    # line thickness
                                

#enemy tank initialization
enemy_tank1 = turtle.Turtle()
enemy_tank1.speed(0)  # Draw as fast as possible
enemy_tank1.width(4)  # Line thickness

enemy_tank2 = turtle.Turtle()
enemy_tank2.speed(0)  # Draw as fast as possible
enemy_tank2.width(4)  # Line thickness

#initial positions for enemy tanks
enemy_tank1.goto(-100, 0)
enemy_tank2.goto(100, 0)

turret_angle = 0

bullets = []

def create_bullet(): #initial bullet creation
    bullet = turtle.Turtle()
    bullet.color("yellow") #bullet color and shape
    bullet.shape("circle")
    bullet.penup()
    bullet.speed(0)
    bullet.shapesize(0.5, 0.5) #bullet cosmetic stats ^
    bullet.hideturtle()
    bullets.append({
        "bullet": bullet,
        "state": "ready"
    })

# Create bullets
for _ in range(3):  # Number of bullets
    create_bullet()

def fire_bullet(): #fire bullet code
    for bullet_dict in bullets:
        bullet = bullet_dict["bullet"]
        state = bullet_dict["state"]
        if state == "ready": #declares ready state of bullet
            bullet_dict["state"] = "firing"
            bullet.setheading(turret_angle)
            bullet.goto(tank.position())
            bullet.showturtle()
            break  # Only fire one bullet at a time

def draw_tank(tank):
    tank.clear()
    # Draw the line inside the circle
    tank.dot(50,"blue")
    tank.forward(30)            #turret draw
    tank.backward(30)
    screen.update()
    tank.setheading(turret_angle)
    tank.pendown()
    tank.forward(30)
    tank.penup()
    tank.goto(x, y)
    screen.update()

x = 0
y = 0
angle = 0
velocity = 5

def draw_enemy_tank(enemy_tank, color):
    enemy_tank.clear()
    enemy_tank.dot(50, "red")
    enemy_tank.forward(30)     # enemy turret draw
    enemy_tank.backward(30)
    screen.update()
     

def movement(angle, velocity):

    angle = math.radians(angle)

    dx = velocity * math.cos(angle)
    dy = velocity * math.sin(angle)

    return dx, dy

def move():
     global x, y,angle
     dx, dy = movement(angle, velocity)
     new_x, new_y = x + dx, y + dy
     
      
    
    # Check for collisions
     if not collision(new_x, new_y):
        x, y = new_x, new_y
     else:
        angle +=90
        dx, dy = movement(angle, velocity)
        x, y = x + dx, y + dy
     tank.goto(x, y)
     draw_tank(tank)
     move_bullet() 
     
     






def move_bullet():
    
    # Loops through each bullet in the list, retrieves the bullet object and its state
    for bullet_dict in bullets:
        bullet = bullet_dict["bullet"]
        state = bullet_dict["state"]
        
        #Based on the state of the bullet, if the bullet is in firing state, it moves forward.
        if state == "firing":
            bullet.forward(15)
            
         


def up():
    global angle
    angle = turret_angle                                
    move()

def down():
    global angle
    angle = turret_angle + 180
    move()

def left():
    global turret_angle
    turret_angle += 10
    draw_tank(tank)

def right():
    global turret_angle
    turret_angle -= 10
    draw_tank(tank)

def update_enemy_movement():
    for enemy_tank in [enemy_tank1, enemy_tank2]:
        # angle calculations
        dx = x - enemy_tank.xcor()
        dy = y - enemy_tank.ycor()
        angle_to_player = math.atan2(dy, dx)
        angle_to_player_degrees = math.degrees(angle_to_player)

        # draws enemy tank at new position
        draw_enemy_tank(enemy_tank, "red")

        # sets orientation
        enemy_tank.setheading(angle_to_player_degrees)

        # move the enemy tank towards the player (speed)
        enemy_tank.forward(2)  

    # delay to update movement of enemy tanks
    screen.ontimer(update_enemy_movement, 250)

def collision(new_x,new_y): 
        #screen collision detection
       if abs(new_x) >= screen.window_width() / 2 or abs(new_y) >= screen.window_height() / 2:
        return True
            #(xb - xa)^2 + (yb - ya)^2 <= (ra + rb)^2
       distance_between_1 = math.sqrt((new_x - enemy_tank1.xcor())**2 + (new_y - enemy_tank1.ycor())** 2)               #Static Circle-Circle collison detection. sqrt(Change of x)^2 + sqrt(change of y)^2
       distance_between_2 = math.sqrt((new_x - enemy_tank2.xcor())**  2 + (new_y - enemy_tank2.ycor()) ** 2)
       collide_dis = 60

       if distance_between_1 < collide_dis or distance_between_2 < collide_dis:             #compare distance and radii of circles to determine collision
            return True
       
    # Bullets collision with walls and enemy tanks
       for bullet_dict in bullets:
        bullet = bullet_dict["bullet"]
        # Bullet collision with walls
        if abs(bullet.xcor()) > (screen.window_width()/2) - 10 or abs(bullet.ycor()) > (screen.window_height()/2) - 10:
            bullet.hideturtle()
            bullet_dict["state"] = "ready"
            bullet.goto(1000, 1000)  # Moves the bullet off-screen to be gone
            continue

        # Bullet collision with enemy tanks
        if bullet.distance(enemy_tank1) < collide_dis / 2:  # Adjust collision size
            # Could add health or destroy mechanic here
            bullet.hideturtle()
            bullet_dict["state"] = "ready"
            bullet.goto(1000, 1000)

        if bullet.distance(enemy_tank2) < collide_dis / 2:  # Adjust collision size
            #could also add health or destroy mechanic here
            bullet.hideturtle()
            bullet_dict["state"] = "ready"
            bullet.goto(1000, 1000)

   

       return False


       
                
def show_dist():
  
    distance1 = int(enemy_tank1.distance(x, y))              #initial distance to tank 1.
    distance2 = int(enemy_tank2.distance(x, y))              #initial distance to tank 2. 
    
    # Printing out the initial distance to the enemy tanks
    print("Distance to Enemy Tank 1: ", distance1, "m")
    print("Distance to Enemy Tank 2: ", distance2, "m")
    
    # Pairs each tank index with its distance respectively.
    # Enemy Tank 1, represented by index 1 and its distance from our tank is stored in tank1_distance
    # Enemy Tank 2, represented by index 2 and its distance from our tank is stored in tank2_distance
    tank1_distance = (1, distance1)
    tank2_distance = (2, distance2)
    sorted_distances = [tank1_distance, tank2_distance]

    #Arranges the enemy tank distances in ascending order implementing  selection sort
    for i in range(len(sorted_distances)): 
      small = i
      for j in range(i+1, len(sorted_distances)): #Iterates through the list of distances to find the smallest distance.
        if sorted_distances[j][1] < sorted_distances[small][1]:
            small = j
      sorted_distances[i], sorted_distances[small] = sorted_distances[small], sorted_distances[i]
      #It eventually swaps the current distance with the smallest distance which ensures that the distances are sorted from closer to farther.

# Prints sorted list of tanks with distances (ascending order) and corresponding indices.
    print("Tanks sorted by distance:")
    tank_index = 1  # Starts with initial tank index 1
    for distance in sorted_distances:
        print("Enemy Tank", tank_index, "is:", distance, "units away from player")
        tank_index += 1  # Increments the tank index by 1 for the next change. 

    screen.ontimer(show_dist, 1500) #this will constantly update the screen with a recursive call, 1500 ms delay
    
    




    
turtle.listen()
turtle.onkeypress(fire_bullet, "space") #added keybind press for bullet
turtle.onkeypress(down, "Down")
turtle.onkeyrelease(down, "Down")
turtle.onkeypress(up, "Up")
turtle.onkeyrelease(up, "Up")
turtle.onkeypress(left, "Left")
turtle.onkeyrelease(left,"Left")
turtle.onkeypress(right, "Right")
turtle.onkeyrelease(right,"Right")


 
draw_grid()
draw_tank(tank)

update_enemy_movement()

show_dist()
screen.update()

turtle.mainloop()



