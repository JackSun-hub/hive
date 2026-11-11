#!/usr/bin/env sh
# CreatorHub 启动入口（macOS / Linux）
# 依次寻找 Python 3.10+ 解释器后运行 creatorhub.py。
set -eu
cd "$(dirname "$0")"

check_python() {
    # 传入解释器名；版本 >= 3.10 时返回其路径
    _py="$1"
    command -v "$_py" >/dev/null 2>&1 || return 1
    "$_py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null || return 1
    command -v "$_py"
    return 0
}

# 1) 项目自带虚拟环境（已 install 过则直接复用）
if [ -x ".venv/bin/python" ]; then
    exec .venv/bin/python creatorhub.py "$@"
fi

# 2) 逐个尝试常见的新版本解释器，最后才回退到 python3
for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if py_path=$(check_python "$candidate"); then
        exec "$py_path" creatorhub.py "$@"
    fi
done

echo "[CreatorHub] 需要先安装 Python 3.10+。" >&2
echo "[CreatorHub] macOS 可用：brew install python@3.11" >&2
exit 1
