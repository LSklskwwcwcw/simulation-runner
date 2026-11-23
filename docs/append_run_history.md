如果传入的字典包含set这种无法转成json的类型，抛出typeerror

如果磁盘满了、没有权限、或者路径是个文件夹，抛出 OSError（及其子类，如 PermissionError）。