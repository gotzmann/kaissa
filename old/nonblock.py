import msvcrt
import os

from ctypes import windll, byref, wintypes, GetLastError, WinError
###from ctypes.wintypes import HANDLE, DWORD, POINTER, BOOL
from ctypes.wintypes import HANDLE, DWORD, LPDWORD, BOOL

###LPDWORD = POINTER(DWORD)

PIPE_NOWAIT = wintypes.DWORD(0x00000001)

ERROR_NO_DATA = 232

def pipe_no_wait(pipefd):
  """ pipefd is a integer as returned by os.pipe """

  SetNamedPipeHandleState = windll.kernel32.SetNamedPipeHandleState
  SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
  SetNamedPipeHandleState.restype = BOOL

  h = msvcrt.get_osfhandle(pipefd)

  res = windll.kernel32.SetNamedPipeHandleState(h, byref(PIPE_NOWAIT), None, None)
  if res == 0:
      print(WinError())
      return False
  return True


#if __name__  == '__main__':
  # CreatePipe
#  r, w = os.pipe()

#  pipe_no_wait(r)

#  print(os.write(w, 'xxx'))
#  print(os.read(r, 1024))
#  try:
#    print(os.write(w, 'yyy'))
##    print(os.read(r, 1024))
#    print(os.read(r, 1024))
#  except OSError as e:
#    print(dir(e), e.errno, GetLastError())
#    print(WinError())
#    if GetLastError() != ERROR_NO_DATA:
#        raise

#  print(os.write(w, 'zzz'))
#  print(os.read(r, 1024))
