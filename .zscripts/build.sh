#!/bin/bash

# 将 stderr 重定向到 stdout，避免 execute_command 因为 stderr 输出而报错
exec 2>&1

set -e

# 使用脚本所在目录（.zscripts 目录）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 项目路径（Astro 静态文档站点）
PROJECT_DIR="/home/z/my-project"

# 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 错误：项目目录不存在: $PROJECT_DIR"
    exit 1
fi

echo "🚀 开始构建 Astro 静态站点和 mini-services..."
echo "📁 项目路径: $PROJECT_DIR"

# 切换到项目目录
cd "$PROJECT_DIR" || exit 1

BUILD_DIR="/tmp/build_fullstack_$BUILD_ID"
echo "📁 清理并创建构建目录: $BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 安装依赖
echo "📦 安装依赖..."
bun install

# 构建 Astro 静态站点（产物输出到 dist/）
echo "🔨 构建 Astro 静态站点..."
bun run build

# 校验静态产物是否生成（部署成功率守卫）。
if [ ! -f "dist/index.html" ]; then
    echo "❌ 构建失败：未生成 dist/index.html。"
    exit 1
fi
echo "✅ 静态站点构建完成：dist/index.html 已生成。"

# 构建 mini-services（目录为空时自动跳过）
if [ -d "$PROJECT_DIR/mini-services" ]; then
    echo "🔨 构建 mini-services..."
    sh "$SCRIPT_DIR/mini-services-install.sh"
    sh "$SCRIPT_DIR/mini-services-build.sh"

    echo "  - 复制 mini-services-start.sh 到 $BUILD_DIR"
    cp "$SCRIPT_DIR/mini-services-start.sh" "$BUILD_DIR/mini-services-start.sh"
    chmod +x "$BUILD_DIR/mini-services-start.sh"
else
    echo "ℹ️  mini-services 目录不存在，跳过"
fi

# 收集构建产物：静态站点 + 零依赖静态文件服务器
echo "📦 收集构建产物到 $BUILD_DIR..."

echo "  - 复制 dist/ 到 next-service-dist/"
cp -r dist "$BUILD_DIR/next-service-dist/"

echo "  - 写入 server.js（零依赖静态文件服务器）"
cat > "$BUILD_DIR/next-service-dist/server.js" <<'SERVER_EOF'
// Zero-dependency static file server for the built Astro site (Citadel Developer Wiki).
// Serves ./ on PORT (default 3000). Deployable with plain node or bun.
const http = require('http');
const fs = require('fs');
const path = require('path');

const DIST = __dirname;
const PORT = Number(process.env.PORT || 3000);
const HOST = process.env.HOSTNAME || '0.0.0.0';

const MIME = {
	'.html': 'text/html; charset=utf-8',
	'.css': 'text/css; charset=utf-8',
	'.js': 'text/javascript; charset=utf-8',
	'.mjs': 'text/javascript; charset=utf-8',
	'.json': 'application/json; charset=utf-8',
	'.svg': 'image/svg+xml',
	'.png': 'image/png',
	'.jpg': 'image/jpeg',
	'.jpeg': 'image/jpeg',
	'.gif': 'image/gif',
	'.webp': 'image/webp',
	'.avif': 'image/avif',
	'.ico': 'image/x-icon',
	'.txt': 'text/plain; charset=utf-8',
	'.webmanifest': 'application/manifest+json',
	'.woff': 'font/woff',
	'.woff2': 'font/woff2',
	'.ttf': 'font/ttf',
	'.otf': 'font/otf',
	'.wasm': 'application/wasm',
	'.xml': 'application/xml',
};

function send(res, status, body, type) {
	res.writeHead(status, {
		'Content-Type': type || 'text/plain; charset=utf-8',
		'Cache-Control': 'no-cache',
	});
	res.end(body);
}

function sendFile(res, filePath, status) {
	fs.readFile(filePath, (err, data) => {
		if (err) return send(res, 404, 'Not found');
		const type = MIME[path.extname(filePath).toLowerCase()] || 'application/octet-stream';
		res.writeHead(status || 200, { 'Content-Type': type, 'Cache-Control': 'no-cache' });
		res.end(data);
	});
}

const server = http.createServer((req, res) => {
	let urlPath;
	try {
		urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
	} catch {
		return send(res, 400, 'Bad request');
	}
	if (urlPath.includes('\0')) return send(res, 400, 'Bad request');

	// 1. exact file (assets: /favicon.svg, /pagefind/...)
	let filePath = path.join(DIST, urlPath);
	if (!filePath.startsWith(DIST)) return send(res, 403, 'Forbidden');
	if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
		return sendFile(res, filePath);
	}
	// 2. directory index (/systems/storage/ -> index.html)
	const indexCandidate = path.join(filePath, 'index.html');
	if (fs.existsSync(indexCandidate)) {
		return sendFile(res, indexCandidate, urlPath.endsWith('/') ? 200 : 301);
	}
	// 3. bare path -> .html (legacy /some-page -> /some-page.html)
	const htmlCandidate = filePath + '.html';
	if (fs.existsSync(htmlCandidate)) {
		return sendFile(res, htmlCandidate);
	}
	// 4. fall back to the 404 page
	return sendFile(res, path.join(DIST, '404.html'), 404);
});

server.listen(PORT, HOST, () => {
	console.log(`Citadel Developer Wiki static server listening on http://${HOST}:${PORT}`);
});
SERVER_EOF

# 复制 Caddyfile（如果存在）
if [ -f "Caddyfile" ]; then
    echo "  - 复制 Caddyfile"
    cp Caddyfile "$BUILD_DIR/"
else
    echo "ℹ️  Caddyfile 不存在，跳过"
fi

# 复制 start.sh 脚本
echo "  - 复制 start.sh 到 $BUILD_DIR"
cp "$SCRIPT_DIR/start.sh" "$BUILD_DIR/start.sh"
chmod +x "$BUILD_DIR/start.sh"

# 打包到 $BUILD_DIR.tar.gz
PACKAGE_FILE="${BUILD_DIR}.tar.gz"
echo ""
echo "📦 打包构建产物到 $PACKAGE_FILE..."
cd "$BUILD_DIR" || exit 1
tar -czf "$PACKAGE_FILE" .
cd - > /dev/null || exit 1

echo ""
echo "✅ 构建完成！所有产物已打包到 $PACKAGE_FILE"
echo "📊 打包文件大小:"
ls -lh "$PACKAGE_FILE"
