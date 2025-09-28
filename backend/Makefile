# Makefile

SRC = .

.PHONY: lint

lint:
#TODO 补充lint命令
# 自动修复代码中的错误
	ruff check $(SRC) --fix
# 格式化代码
	ruff format $(SRC)
# 再次检查代码，确保格式和风格问题被修复
	ruff check $(SRC)

# 退出时打印退出状态
exit_code:
	@echo $?