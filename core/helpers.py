import os

# list the files in a directory recursively
# dont set dirs or files
def traverse(directory, __dirs=[], __files=[]):
	cwd = os.path.abspath(directory)
	entries = os.listdir(cwd)

	for f in entries:
		current = os.path.join(cwd, f)
		if os.path.isdir(current):
			__dirs.append(current)
			traverse(current, __dirs, __files)
		else:
			__files.append(current)
	return {'files': __files, 'dirs': __dirs}
