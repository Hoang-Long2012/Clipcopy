import sys
import argparse
import ctypes
import ctypes.wintypes
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002
User32 = ctypes.WinDLL("user32", use_last_error=True)
Kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
User32.OpenClipboard.argtypes = [ctypes.c_void_p]
User32.OpenClipboard.restype = ctypes.c_bool
User32.EmptyClipboard.restype = ctypes.c_bool
User32.SetClipboardData.argtypes = (ctypes.wintypes.UINT, ctypes.wintypes.HANDLE)
User32.SetClipboardData.restype = ctypes.wintypes.HANDLE
User32.CloseClipboard.restype = ctypes.c_bool
Kernel32.GlobalAlloc.argtypes = (ctypes.wintypes.UINT, ctypes.c_size_t,)
Kernel32.GlobalAlloc.restype = ctypes.wintypes.HGLOBAL
Kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
Kernel32.GlobalLock.restype = ctypes.c_void_p
Kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
Kernel32.GlobalUnlock.restype = ctypes.c_bool
Kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
Kernel32.GlobalFree.restype = ctypes.c_void_p
def setClipboard(Text):
	if not User32.OpenClipboard(None):
		raise RuntimeError(f"[WinError: {ctypes.get_last_error()}] Unable to open clipboard.")
	try:
		if not User32.EmptyClipboard():
			raise ctypes.WinError(ctypes.get_last_error())
		Size = (len(Text) + 1) * ctypes.sizeof(ctypes.c_wchar)
		Handle = Kernel32.GlobalAlloc(GMEM_MOVEABLE, Size)
		if not Handle:
			raise ctypes.WinError(ctypes.get_last_error())
		Pointer = Kernel32.GlobalLock(Handle)
		if not Pointer:
			ErrorCode = ctypes.get_last_error()
			Kernel32.GlobalFree(Handle)
			Handle = None
			raise ctypes.WinError(ErrorCode)
		try:
			ctypes.memmove(Pointer, ctypes.create_unicode_buffer(Text), Size)
		finally:
			Kernel32.GlobalUnlock(Handle)
		if not User32.SetClipboardData(CF_UNICODETEXT, Handle):
			ErrorCode = ctypes.get_last_error()
			Kernel32.GlobalFree(Handle)
			raise RuntimeError(f"[WinError: {ErrorCode}] Cannot set clipboard.")
		Handle = None
	finally:
		User32.CloseClipboard()
def clipCopy(Text=None, Show=False):
	Source = Text if isinstance(Text, str) else sys.stdin.read()
	try:
		setClipboard(Source)
		if Show:
			sys.stdout.write(Source)
		return 0
	except (RuntimeError, OSError) as Error:
		sys.stderr.write(f"{Error}\n")
		return 2
def normalizeWindowsArgs(argv):
	Normalized = []
	for Arg in argv:
		if Arg == "/?":
			Normalized.append("--help")
		if Arg.startswith("/") and len(Arg) > 1:
			if len(Arg) == 2:
				Normalized.append("-" + Arg[1:2])
			else:
				Normalized.append("--" + Arg[1:])
		else:
			Normalized.append(Arg)
	return Normalized
def parseArgs():
	Examples = """
Examples:
dir | %(prog)s   Places a copy of the current directory listing into the Windows clipboard.

%(prog)s < readme.txt   Places a copy of the text from readme.txt on to the Windows clipboard.

%(prog)s "Hello"   Copy Hello string to clipboard.

%(prog)s   Copy what you entered to the Windows clipboard."""
	ArgsList = normalizeWindowsArgs(sys.argv[1:])
	Parser = argparse.ArgumentParser(prog="Clipcopy", description="Copy your standard input or text to clipboard.", epilog=Examples, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
	Parser.add_argument("text", type=str, help="Text to copy to clipboard.")
	Parser.add_argument("-v", "--version", action="version", version="%(prog)s version 1.1")
	Parser.add_argument("-s", "--show", action="store_true", help="Show copy content to standard output.")
	return Parser.parse_args(ArgsList)
def main():
	Args = parseArgs()
	sys.exit(clipCopy(Args.text, Args.show))
if __name__ == "__main__":
	main()