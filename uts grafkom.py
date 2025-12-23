import tkinter as tk
import math

# ================= KONFIGURASI =================
WIDTH, HEIGHT = 700, 450
root = tk.Tk()
root.title("Mini Scene Grafika 2D - Rumah 2 Lantai, Jalan & Pepohonan")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

img = tk.PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image(WIDTH//2, HEIGHT//2, image=img)

# ================= BASIC =================
def clear():
    img.put("white", to=(0,0,WIDTH,HEIGHT))

def plot(x,y,color="black"):
    if 0<=x<WIDTH and 0<=y<HEIGHT:
        img.put(color,(int(x),int(y)))

# ================= DDA =================
def dda(x1,y1,x2,y2,color="black"):
    dx, dy = x2-x1, y2-y1
    steps = int(max(abs(dx),abs(dy)))
    if steps == 0: return
    x_inc, y_inc = dx/steps, dy/steps
    x,y = x1,y1
    for _ in range(steps):
        plot(round(x),round(y),color)
        x+=x_inc
        y+=y_inc

# ================= MIDPOINT CIRCLE =================
def circle(cx,cy,r,color):
    x,y = 0,r
    d = 1-r
    while x<=y:
        for dx,dy in [(x,y),(y,x),(-x,y),(-y,x),
                      (x,-y),(y,-x),(-x,-y),(-y,-x)]:
            plot(cx+dx,cy+dy,color)
        if d<0:
            d+=2*x+3
        else:
            d+=2*(x-y)+5
            y-=1
        x+=1

# ================= CAHAYA MATAHARI =================
def sun_rays(cx, cy, r, length=25, color="orange"):
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        dda(cx + r*math.cos(rad),
            cy + r*math.sin(rad),
            cx + (r+length)*math.cos(rad),
            cy + (r+length)*math.sin(rad),
            color)

# ================= POLYGON =================
def draw_polygon(p,color):
    for i in range(len(p)):
        dda(p[i][0],p[i][1],p[(i+1)%len(p)][0],p[(i+1)%len(p)][1],color)

# ================= TRANSFORMASI =================
def translate(p, tx, ty):
    return [(x+tx,y+ty) for x,y in p]

def scale(p, s):
    return [(x*s,y*s) for x,y in p]

def rotate(p, a):
    rad = math.radians(a)
    return [(x*math.cos(rad)-y*math.sin(rad),
             x*math.sin(rad)+y*math.cos(rad)) for x,y in p]

def reflect_x(p):
    return [(x,-y) for x,y in p]

def reflect_y(p):
    return [(-x,y) for x,y in p]

# ================= OBJEK RUMAH 2 LANTAI =================
floor1 = [(-45,0),(45,0),(45,50),(-45,50)]
floor2 = [(-45,-50),(45,-50),(45,0),(-45,0)]
roof   = [(-55,-50),(0,-90),(55,-50)]

door   = [(-8,50),(8,50),(8,25),(-8,25)]
win1   = [(-35,10),(-20,10),(-20,30),(-35,30)]
win2   = [(20,10),(35,10),(35,30),(20,30)]
win3   = [(-35,-40),(-20,-40),(-20,-20),(-35,-20)]
win4   = [(20,-40),(35,-40),(35,-20),(20,-20)]

tx, ty = 350, 270
angle = 0
size = 1
rx = ry = False

# ================= INPUT =================
def key(e):
    global tx, ty, angle, size, rx, ry
    if e.keysym=="Left": tx-=10
    if e.keysym=="Right": tx+=10
    if e.keysym=="Up": ty-=10
    if e.keysym=="Down": ty+=10
    if e.keysym=="q": angle-=10
    if e.keysym=="e": angle+=10
    if e.keysym=="w": size+=0.1
    if e.keysym=="s": size-=0.1
    if e.keysym=="x": rx = not rx
    if e.keysym=="y": ry = not ry
    if e.keysym=="r":
        tx,ty,angle,size,rx,ry = 350,270,0,1,False,False
    if e.keysym=="Escape":
        root.destroy()

root.bind("<Key>",key)

# ================= JALAN =================
def draw_road():
    draw_polygon([(0,350),(WIDTH,350),(WIDTH,450),(0,450)],"black")
    dda(0,360,WIDTH,360,"black")
    dda(0,440,WIDTH,440,"black")
    for x in range(0, WIDTH, 40):
        dda(x,400,x+20,400,"black")

# ================= POHON =================
def draw_tree(x,y):
    # Batang
    trunk = [(x-5,y),(x+5,y),(x+5,y+40),(x-5,y+40)]
    draw_polygon(trunk,"brown")

    # Daun
    circle(x,y-5,15,"green")
    circle(x-10,y,12,"green")
    circle(x+10,y,12,"green")
    circle(x,y-15,12,"green")

# ================= LOOP =================
def loop():
    clear()

    # Matahari
    circle(600,80,30,"orange")
    sun_rays(600,80,30,25,"orange")

    # Awan
    for x in [120,150,180]:
        circle(x,90,18,"lightblue")

    # Jalan
    draw_road()

    # Pepohonan
    draw_tree(100,280)
    draw_tree(180,280)
    draw_tree(520,280)

    # Rumah
    parts = [floor1,floor2,roof,door,win1,win2,win3,win4]
    for p in parts:
        obj = p
        if rx: obj = reflect_x(obj)
        if ry: obj = reflect_y(obj)
        obj = rotate(scale(obj,size),angle)
        obj = translate(obj,tx,ty)
        draw_polygon(obj,"black")

    canvas.create_text(WIDTH//2,20,
        text="Mini Scene Grafika 2D",
        font=("Arial",12,"bold"), fill="black")

    root.after(40,loop)

loop()
root.mainloop()
