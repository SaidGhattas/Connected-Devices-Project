import machine
import time
import ssd1306

from machine import Pin, SoftI2C
import ssd1306
import framebuf
i2c = SoftI2C(sda=Pin(23), scl=Pin(22))

x=2
y=2
global px,py 

px=0
py=14
global px2,py2

px2=110
py2=14
global bpx,bpy
bpx=0
bpy=0
global bpx2,bpy2
bpx2=0
bpy2=0
display = ssd1306.SSD1306_I2C(128, 32, i2c) 
bullet=[[1,1,1,0],[1,1,1,1],[1,1,1,1],[1,1,1,0]]
bullet2=[[0,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,1]]

monster=[
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,0,1,0,0,1,0,1]]    
monster2=[
        [0,1,0,0,0,0,1,0],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,0,0,1,1,0],
        [0,1,0,0,0,0,1,0]] 
btn = Pin(15, Pin.IN, Pin.PULL_UP) 

def game_over(player):
    x=2
    y=2
    px=0
    py=14
    global px2,py2
    px2=110
    py2=14
    global bpx,bpy
    bpx=128
    bpy=0
    global bpx2,bpy2
    bpx2=0
    bpy2=0
    while True:
        display.fill(0)
        display.text('Game Over', 0, 0, 1)
        display.text('Player '+player+" won", 0, 10, 1)
        display.show()
        time.sleep(0.5)
        if btn.value()==0:
            draw_m(x,y,px,py,px2,py2)
            break
def draw_m(x,y,px,py,px2,py2):
    display.fill(0)
    display.show()

    
    display.line(0, 8*y+14, 127, 8*y+14, 1)
    #monster diplay
    fbuf = framebuf.FrameBuffer(bytearray((8*x)*(8*y)), 8*x, 8*y, framebuf.MONO_HLSB)
    for i in range(8*x):
        for j in range(8*y):
            fbuf.pixel(j,i,monster[i//x][j//y])
    display.blit(fbuf, px, py, 0)   
            
    #monster2 diplay
    fbuf = framebuf.FrameBuffer(bytearray((8*x)*(8*y)), 8*x, 8*y, framebuf.MONO_HLSB)
    for i in range(8*x):
        for j in range(8*y):
            fbuf.pixel(j,i,monster2[i//x][j//y])
            
    display.blit(fbuf, px2, py2, 0)  
    
  
    display.show()

def back_mx():
    global px
    if px>=0:
        px-=2

    draw_m(x,y,px,py,px2,py2)

def forward_mx():
    global px
    if px<=50:
        px +=2
    draw_m(x,y,px,py,px2,py2)
def jump():
    global py
    
    if py==14:
        while py>0:
            py-=2
            draw_m(x,y,px,py,px2,py2)
        time.sleep(0.2)
        while py<14:
            py+=2
            draw_m(x,y,px,py,px2,py2)
    draw_m(x,y,px,py,px2,py2)
def shoot():
    print("shoot")
    global bpx,bpy
    bpx=px+8
    bpy=py+8
    fbuf = framebuf.FrameBuffer(bytearray((4)*(4)), 4,4, framebuf.MONO_HLSB)
    for i in range(4):
        for j in range(4):
            fbuf.pixel(j,i,bullet[i][j])
    display.blit(fbuf, bpx,bpy, 0)   
      
    display.show()
    while bpx<128:
        bpx+=4
        display.blit(fbuf, bpx,bpy, 0)  
        if bpx>=px2-4 and bpx<=px2+8 and bpy>=py2-4 and bpy<=py2+8:
                print("hit")
                game_over("1")  
        else:
            display.show()
            draw_m(x,y,px,py,px2,py2)


def back_mx2():
    global px2
    
    if px2>60:
        px2-=1
    draw_m(x,y,px,py,px2,py2)
    
def forward_mx2():
    global px2
    if px2<110:
        px2 +=1

    draw_m(x,y,px,py,px2,py2)

def jump2():
    global py2
    
    if py2==14:
        while py2>0:
            py2-=1
            draw_m(x,y,px,py,px2,py2)

        time.sleep(0.2)
        while py2<14:
            py2+=1
            draw_m(x,y,px,py,px2,py2)
    draw_m(x,y,px,py,px2,py2)

def shoot2():
    global bpx2,bpy2
    bpx2=px2+8
    bpy2=py2+8
    fbuf = framebuf.FrameBuffer(bytearray((4)*(4)), 4,4, framebuf.MONO_HLSB)
    for i in range(4):
        for j in range(4):
            fbuf.pixel(j,i,bullet2[i][j])
    
    display.blit(fbuf, bpx2,bpy2, 0)      
    
    display.show()
    while bpx2>0:
        bpx2-=4
        display.blit(fbuf, bpx2,bpy2, 0)      
        if bpx2>=px-4 and bpx2<=px+8 and bpy2>=py-4 and bpy2<=py+8:
                print("hit")
                game_over("2")
        display.show()
        draw_m(x,y,px,py,px2,py2)




