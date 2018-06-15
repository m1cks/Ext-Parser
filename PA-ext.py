import struct
import math
import os
from time import sleep

#tools logo
def ToolMain():
    os.system('cls')
    ToolMain="""

     _____             ______      _   
    |  __ \ /\        |  ____|    | |  
    | |__) /  \ ______| |__  __  _| |_ 
    |  ___/ /\ \______|  __| \ \/ / __|
    | |  / ____ \     | |____ >  <| |_ 
    |_| /_/    \_\    |______/_/\_\\__|
            Parse&Analysis-Ext       
    """
    print(ToolMain)
    sleep(2.5)
    os.system('cls')

ToolMain()

n = 0
Period = "."
NSF_lis = []
NSF_dic = {}
dirlist = os.listdir('.')
for i in dirlist:
    if Period in i:
        File = i.split('.')
        Extension = File[1]
        if Extension == 'dd': #you can select other Extension
            n +=1
            NSF_lis.append(i)
            
n = 0
for i in NSF_lis:
    n += 1      
    NSF_dic[n] = i
    print("{0}. {1}".format(n, NSF_dic[n])) 

try:
    Option = input("Select File Number : ") 
    Option = int(round(float(Option)))
except:
    os.system('cls')
    print("You need to select by number")
else:
    if Option <= n and Option > 0:
        os.system('cls')
        print("you select {}".format(NSF_dic[Option])) 
        sleep(1.5) 
    elif type(Option) != int or float:
        os.system('cls')
    else:
        os.system('cls')
        print("Out of range")

 #up is for option list, down is for ext analysis

f = open(NSF_dic[Option], "rb") 
f.seek(1024) 
superblock = f.read(1024)
print('\n')

block_size = struct.unpack_from("<I", superblock, 0x18)[0]

inode_size = struct.unpack_from("<I", superblock, 0x58)[0]

f.seek(1024+136)
LM_path_b = f.read(64)
LM_path = LM_path_b.decode('utf-8')

gdt_size = struct.unpack_from("<H", superblock, 0xFE)[0]
if gdt_size <= 32:
	gdt_size = 32
block_size = pow(2, block_size+10)

if block_size >= 4096:
        f.seek(block_size)
else:
        f.seek(2048)

gdt = f.read(gdt_size)

block_bitmap = struct.unpack_from("<H", gdt, 0x0)[0]
block_bitmap = block_size * block_bitmap 

inode_bitmap = struct.unpack_from("<H", gdt, 0x4)[0]
inode_bitmap = block_size * inode_bitmap 

inode_table = struct.unpack_from("<H", gdt, 0x8)[0]
inode_table = block_size * inode_table 

root_start = (inode_table+inode_size)
f.seek(root_start)
root = f.read(inode_size)

result1 = """
Block Size = {0} bytes          Inode Size = {1} bytes         GDT Size = {2} bytes

Last Mounted Path = {3}

Block Bit map address = {4}    Inode Bitmap address = {5}    Inode Table address = {6}
""".format(block_size, inode_size, gdt_size, LM_path, block_bitmap, inode_bitmap, inode_table)

os.system('cls')
print(result1) #Result of Part 1, part 2 is for inode