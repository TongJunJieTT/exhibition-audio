import qrcode
import os
import json
from urllib.parse import quote

def generate_qrcodes_github():
    """为GitHub Pages生成展品二维码"""
    
    # 配置信息 - 请修改为您的实际信息
    GITHUB_USERNAME = "TongJunJieTT"  # 替换为您的GitHub用户名
    REPO_NAME = "exhibition-audio"     # 替换为您的仓库名
    
    # GitHub Pages基础URL
    BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
    
    # 展品数据 - 根据您的实际展品修改
    exhibits = {
        'exhibit_001': {
            'name': '声展',
            'title': '声展',
            'subtitle': '声展'
        }
        # 可以继续添加更多展品...
    }
    
    # 创建输出目录
    os.makedirs('qrcodes', exist_ok=True)
    os.makedirs('qrcodes_small', exist_ok=True)  # 小尺寸版本
    
    print("=" * 60)
    print("🎯 GitHub Pages 展品二维码生成器")
    print("=" * 60)
    print(f"📝 配置信息:")
    print(f"   GitHub用户名: {GITHUB_USERNAME}")
    print(f"   仓库名称: {REPO_NAME}")
    print(f"   访问地址: {BASE_URL}")
    print("=" * 60)
    
    # 生成配置文件（用于网页）
    config_data = {
        'base_url': BASE_URL,
        'exhibits': exhibits
    }
    
    with open('exhibition_config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print("📋 开始生成二维码...")
    
    success_count = 0
    
    for exhibit_id, exhibit_info in exhibits.items():
        try:
            # 生成展品访问URL
            exhibit_url = f"{BASE_URL}/index.html?exhibit={exhibit_id}"
            
            print(f"\n🔗 处理展品: {exhibit_info['name']}")
            print(f"   URL: {exhibit_url}")
            
            # 生成大尺寸二维码（用于打印）
            qr_large = qrcode.QRCode(
                version=6,  # 较大的版本，容纳更多数据
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=15,  # 较大的像素块
                border=4,
            )
            qr_large.add_data(exhibit_url)
            qr_large.make(fit=True)
            
            img_large = qr_large.make_image(fill_color="black", back_color="white")
            large_filename = f"qrcodes/{exhibit_id}_{exhibit_info['name']}.png"
            img_large.save(large_filename)
            
            # 生成小尺寸二维码（用于预览）
            qr_small = qrcode.QRCode(
                version=4,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=2,
            )
            qr_small.add_data(exhibit_url)
            qr_small.make(fit=True)
            
            img_small = qr_small.make_image(fill_color="black", back_color="white")
            small_filename = f"qrcodes_small/{exhibit_id}_{exhibit_info['name']}_small.png"
            img_small.save(small_filename)
            
            success_count += 1
            print(f"   ✅ 生成成功: {large_filename}")
            print(f"   📱 小尺寸: {small_filename}")
            
        except Exception as e:
            print(f"   ❌ 生成失败: {str(e)}")
    
    # 生成展品列表HTML（便于管理）
    generate_exhibit_list_html(exhibits, BASE_URL)
    
    # 生成使用说明
    generate_readme_file(exhibits, GITHUB_USERNAME, REPO_NAME)
    
    print("\n" + "=" * 60)
    print(f"🎉 二维码生成完成！")
    print(f"📊 统计信息:")
    print(f"   成功生成: {success_count} 个展品二维码")
    print(f"   大尺寸文件: qrcodes/ 目录（适合打印）")
    print(f"   小尺寸文件: qrcodes_small/ 目录（适合预览）")
    print(f"   配置文件: exhibition_config.json")
    print(f"   展品列表: exhibit_list.html")
    print("\n📋 下一步操作:")
    print(f"1. 将整个项目上传到GitHub仓库: {REPO_NAME}")
    print(f"2. 开启GitHub Pages功能")
    print(f"3. 访问: {BASE_URL} 测试")
    print(f"4. 打印 qrcodes/ 目录中的二维码")
    print("=" * 60)

def generate_exhibit_list_html(exhibits, base_url):
    """生成展品列表HTML文件，便于管理"""
    html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>展品二维码管理</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .exhibit-card { 
            border: 1px solid #ddd; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .exhibit-info { flex: 1; }
        .qrcode-preview img { width: 100px; height: 100px; }
        .exhibit-url { 
            background: #f5f5f5; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-size: 12px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <h1>展品二维码管理</h1>
    <p>基础URL: <code>{base_url}</code></p>
    
    <div id="exhibit-list">
'''.format(base_url=base_url)

    for exhibit_id, exhibit_info in exhibits.items():
        exhibit_url = f"{base_url}/index.html?exhibit={exhibit_id}"
        qr_small_path = f"qrcodes_small/{exhibit_id}_{exhibit_info['name']}_small.png"
        qr_large_path = f"qrcodes/{exhibit_id}_{exhibit_info['name']}.png"
        
        html_content += f'''
        <div class="exhibit-card">
            <div class="exhibit-info">
                <h3>{exhibit_info['name']}</h3>
                <p><strong>ID:</strong> {exhibit_id}</p>
                <p><strong>副标题:</strong> {exhibit_info['subtitle']}</p>
                <div class="exhibit-url">{exhibit_url}</div>
            </div>
            <div class="qrcode-preview">
                <img src="{qr_small_path}" alt="{exhibit_info['name']}">
                <p style="text-align: center; font-size: 12px;">
                    <a href="{qr_large_path}" download>下载大图</a>
                </p>
            </div>
        </div>
        '''

    html_content += '''
    </div>
</body>
</html>
'''
    
    with open('exhibit_list.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📄 生成展品列表: exhibit_list.html")

def generate_readme_file(exhibits, username, repo_name):
    """生成README文件"""
    readme_content = f'''
# 展品音频二维码导览系统

基于GitHub Pages的展品音频导览解决方案。

## 访问地址
https://{username}.github.io/{repo_name}/

## 展品列表

| 展品ID | 展品名称 | 副标题 | 访问链接 |
|--------|----------|--------|----------|
'''
    
    for exhibit_id, exhibit_info in exhibits.items():
        exhibit_url = f"https://{username}.github.io/{repo_name}/?exhibit={exhibit_id}"
        readme_content += f"| {exhibit_id} | {exhibit_info['name']} | {exhibit_info['subtitle']} | [访问]({exhibit_url}) |\n"
    
    readme_content += '''

## 文件结构