函数契约

项	内容
函数名	save_run_result
action	str，要执行的 job 名
status	str，只能是 success / failed / timeout
attempts	int，当前恒为 1（预留重试）
exit_code	int | None，超时为 None
timed_out	bool
返回	None，副作用是写文件



状态规则表

timed_out	exit_code	status
True	None	timeout
False	0	success
False	非 0（含 2）	failed


JSON 字段

字段	类型	说明
action	string	输入的动作名
status	string	上表的结论
attempts	integer	恒为 1
exit_code	integer | null	超时写 null
timed_out	boolean	
失败行为：status 非法 → ValueError；目录不可写 → 让异常抛出。

退出码规则：main.py 成功 0，失败/超时 1。