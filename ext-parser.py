import sys
import struct
import math

f = open(sys.argv[1], "rb")
f.seek(1024)
superblock = f.read(1024)
print('\n')

block_size = struct.unpack_from("<I", superblock, 0x18)[0]
print("block size = %dbyte\n"%pow(2,block_size+10))

inode_size = struct.unpack_from("<I", superblock, 0x58)[0]
print("inode size = %dbyte\n"%inode_size)

gdt_size = struct.unpack_from("<H", superblock, 0xFE)[0]
if gdt_size <= 32:
	gdt_size = 32
print("gdt size = %d\n"%gdt_size)

block_size = pow(2, block_size+10)

if block_size == 4096:
        f.seek(block_size)
else:
        f.seek(2048)

gdt = f.read(gdt_size)
print('----------------------gdt information--------------------\n')
print(gdt)

inode_start = struct.unpack_from("<H", gdt, 0x8)[0]
inode_start = block_size * inode_start
print('------------------inode table start address--------------\n')
print(inode_start)

root_start = (inode_start+inode_size)
f.seek(root_start)
root = f.read(inode_size)
print('----------------------root information-------------------\n')
print(root)

