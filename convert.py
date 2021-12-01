import re
from nbtlib.tag import *
from nbtlib import schema

import gzip
from nbtlib.nbt import File

def fileobj_to_dic(fileobj, *, byteorder="big"):
    magic_number = fileobj.read(2)
    fileobj.seek(0)

    if magic_number == b"\x1f\x8b":
        fileobj = gzip.GzipFile(fileobj=fileobj)
        
    return File.from_fileobj(fileobj, byteorder)

def get_properties(s):
    result = ""

    l = s.split('[')[1].strip(']')
    l = re.split('[=|,]',l)

    for i in range(0, len(l), 2):
        if i != 0:
            # カンマ
            result += ','
        result += l[i] + ':' + f'\"{l[i+1]}\"'

    return result

def get_block_list(d):
    block_list = ["" for _ in range(len(d))]
    for block, no in d.items():
        block_list[no] = block
    return block_list

def get_one_block_commands(commands):
    front = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[\
{id:armor_stand,Health:0,Passengers:[\
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[\
{id:command_block_minecart,Command:'gamerule commandBlockOutput false\'},\
{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}\'},"

    back = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:\"fill ~ ~ ~ ~ ~-2 ~ air\"}\'},\
{id:command_block_minecart,Command:\'kill @e[type=command_block_minecart,distance=..1]\'}]}]}]}"
    result = []
    for i in range(0,len(commands),150):
        tmp = ""
        for c in commands[i:min(i+150,len(commands))]:
            tmp += "{id:command_block_minecart,Command:" + f"\'{c.strip('/')}\'" + '},'
        result.append(front + tmp + back)

    return result

# エンティティタグを追加
Entity = schema('Entity', {})


def convert(f, add_tag, mode):
    nbt_file = fileobj_to_dic(f)
    schematic = nbt_file['Schematic']

    block_data = schematic['BlockData']
    print(block_data)

    i = 0

    block_list = get_block_list(schematic['Palette']) # schematic内でのブロックリスト

    commands = []

    # タグをつける
    tag = ''
    if add_tag:
        tag = f',Tags:[\"{add_tag}\"]'

    for y in range(schematic['Height']):
        for z in range(schematic['Length']):
            for x in range(schematic['Width']):
                properties = "" # bock state
                block_no = schematic['BlockData'][i]
                block = block_list[block_no]
                i += 1

                if '[' in block:
                    # 向きの情報などがある時
                    properties = f',Properties:{{{get_properties(block)}}}'
                    block = block.split('[')[0]

                if block == 'minecraft:air' or block == 'minecraft:void_air' or block == 'minecraft:cave_air':
                    # 空気の時無視
                    continue

                command = f'/summon falling_block ^{x} ^{y} ^{z} {{BlockState:{{Name:\"{block}\"{properties}}},NoGravity:1b,Time:-2147483648{tag}}}'
                commands.append(command)
                
    # モードによって送信
    if mode == 'command_block':
        return get_one_block_commands(commands)
    elif mode == 'data_pack':
        return ['\n'.join(commands).replace('/','')]

if __name__ == '__main__':
    with open('ribals.schem', 'rb') as f:        
        convert(f)


