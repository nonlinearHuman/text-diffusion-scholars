#!/usr/bin/env python3
"""
生成 CVPR 2026 论文推荐页面的专业图片
包括：作者头像和技术架构图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = "/Users/gesong/.openclaw/workspace/cvpr2026-images"
os.makedirs(output_dir, exist_ok=True)

def create_gradient_avatar(name, initials, size=300):
    """创建渐变色头像"""
    # 创建渐变背景
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # 渐变色（从左上到右下）
    colors = {
        "Li Hu": ("#3B82F6", "#8B5CF6"),  # 蓝到紫
        "Ziwei Liu": ("#10B981", "#3B82F6"),  # 绿到蓝
        "PKU Team": ("#8B5CF6", "#EC4899"),  # 紫到粉
        "SJTU Team": ("#F59E0B", "#EF4444"),  # 橙到红
        "NVIDIA": ("#76B900", "#059669"),  # NVIDIA 绿
    }
    
    color1, color2 = colors.get(name, ("#3B82F6", "#8B5CF6"))
    
    # 绘制渐变
    for y in range(size):
        ratio = y / size
        r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
        g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
        b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # 绘制圆形边框
    draw.ellipse([10, 10, size-10, size-10], outline='white', width=3)
    
    # 绘制文字
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    # 绘制白色文字阴影
    draw.text((x+2, y+2), initials, font=font, fill='rgba(0,0,0,0.3)')
    draw.text((x, y), initials, font=font, fill='white')
    
    return img

def create_tech_diagram_1():
    """UCM 架构图"""
    img = Image.new('RGB', (800, 300), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # 绘制三个模块
    modules = [
        ("时间感知\n位置编码", "#DBEAFE", "#2563EB"),
        ("双流DiT\n高保真生成", "#EDE9FE", "#7C3AED"),
        ("相机控制\n+长期记忆", "#FEF3C7", "#F59E0B"),
    ]
    
    x_start = 80
    for i, (text, bg_color, border_color) in enumerate(modules):
        x = x_start + i * 240
        y = 60
        
        # 绘制圆角矩形
        draw.rounded_rectangle([x, y, x+200, y+180], radius=15, 
                              fill=bg_color, outline=border_color, width=3)
        
        # 绘制文字
        lines = text.split('\n')
        for j, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_text)
            text_w = bbox[2] - bbox[0]
            text_x = x + (200 - text_w) // 2
            text_y = y + 70 + j * 25
            draw.text((text_x, text_y), line, font=font_text, fill=border_color)
        
        # 绘制箭头
        if i < 2:
            arrow_x = x + 210
            arrow_y = y + 90
            draw.polygon([(arrow_x, arrow_y), (arrow_x+25, arrow_y-10), 
                         (arrow_x+25, arrow_y+10)], fill='#64748B')
    
    # 标题
    draw.text((280, 10), "UCM架构：统一相机控制与记忆机制", 
             font=font_title, fill='#1E293B')
    
    return img

def create_tech_diagram_2():
    """PhysX-Anything 架构图"""
    img = Image.new('RGB', (800, 300), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
    except:
        font_title = ImageText.load_default()
        font_text = ImageText.load_default()
        font_small = ImageText.load_default()
    
    # 绘制三个模块
    draw.rounded_rectangle([40, 80, 160, 220], radius=10, 
                          fill="#DBEAFE", outline="#2563EB", width=2)
    draw.text((65, 140), "单图输入", font=font_text, fill="#1E40AF")
    
    draw.rounded_rectangle([220, 60, 520, 240], radius=10, 
                          fill="#EDE9FE", outline="#7C3AED", width=2)
    draw.text((320, 100), "VLM物理生成", font=font_text, fill="#5B21B6")
    draw.text((280, 135), "几何+物理属性", font=font_small, fill="#6B7280")
    draw.text((300, 160), "Token ↓193×", font=font_small, fill="#6B7280")
    
    draw.rounded_rectangle([580, 80, 720, 220], radius=10, 
                          fill="#D1FAE5", outline="#10B981", width=2)
    draw.text((615, 125), "仿真就绪\n3D资产", font=font_text, fill="#065F46")
    
    # 箭头
    draw.polygon([(175, 150), (210, 140), (210, 160)], fill='#64748B')
    draw.polygon([(535, 150), (570, 140), (570, 160)], fill='#64748B')
    
    draw.text((220, 15), "PhysX-Anything: 单图到仿真就绪3D资产", 
             font=font_title, fill='#1E293B')
    
    return img

def create_tech_diagram_3():
    """EVA 架构图"""
    img = Image.new('RGB', (800, 300), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    draw.rounded_rectangle([60, 80, 180, 220], radius=10, 
                          fill="#DBEAFE", outline="#2563EB", width=2)
    draw.text((85, 130), "历史帧\n+动作", font=font_text, fill="#1E40AF")
    
    draw.rounded_rectangle([240, 60, 500, 240], radius=10, 
                          fill="#EDE9FE", outline="#7C3AED", width=2)
    draw.text((345, 100), "EVA", font=font_title, fill="#5B21B6")
    draw.text((290, 140), "反射+自回归", font=font_small, fill="#6B7280")
    draw.text((290, 165), "多阶段训练", font=font_small, fill="#6B7280")
    
    draw.rounded_rectangle([560, 80, 720, 220], radius=10, 
                          fill="#D1FAE5", outline="#10B981", width=2)
    draw.text((600, 130), "未来帧\n预测", font=font_text, fill="#065F46")
    
    draw.polygon([(195, 150), (230, 140), (230, 160)], fill='#64748B')
    draw.polygon([(515, 150), (550, 140), (550, 160)], fill='#64748B')
    
    draw.text((200, 15), "EVA: 反射机制增强的具身视频预测", 
             font=font_title, fill='#1E293B')
    
    return img

def create_tech_diagram_4():
    """UniDriveDreamer 架构图"""
    img = Image.new('RGB', (800, 300), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    draw.rounded_rectangle([40, 100, 140, 200], radius=8, 
                          fill="#DBEAFE", outline="#2563EB", width=2)
    draw.text((60, 140), "历史帧\n+动作", font=font_text, fill="#1E40AF")
    
    draw.rounded_rectangle([200, 60, 520, 240], radius=10, 
                          fill="#EDE9FE", outline="#7C3AED", width=2)
    draw.text((300, 95), "UniDriveDreamer", font=font_title, fill="#5B21B6")
    draw.text((290, 140), "单阶段多模态生成", font=font_small, fill="#6B7280")
    draw.text((295, 165), "理解+规划+生成", font=font_small, fill="#6B7280")
    
    draw.rounded_rectangle([580, 80, 720, 150], radius=6, 
                          fill="#D1FAE5", outline="#10B981", width=2)
    draw.text((610, 105), "多相机视频", font=font_text, fill="#065F46")
    
    draw.rounded_rectangle([580, 160, 720, 230], radius=6, 
                          fill="#FEF3C7", outline="#F59E0B", width=2)
    draw.text((620, 185), "LiDAR序列", font=font_text, fill="#92400E")
    
    draw.polygon([(155, 150), (190, 140), (190, 160)], fill='#64748B')
    draw.line([(535, 120), (570, 115)], fill='#64748B', width=2)
    draw.line([(535, 180), (570, 195)], fill='#64748B', width=2)
    
    draw.text((190, 15), "UniDriveDreamer: 单阶段多模态生成框架", 
             font=font_title, fill='#1E293B')
    
    return img

def create_tech_diagram_5():
    """Cosmos-Drive-Dreams 架构图"""
    img = Image.new('RGB', (800, 300), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    draw.rounded_rectangle([40, 80, 180, 220], radius=10, 
                          fill="#76B900", outline="#4A7C00", width=2)
    draw.text((65, 115), "Cosmos", font=font_title, fill="white")
    draw.text((55, 150), "世界基础模型", font=font_small, fill="white")
    
    draw.rounded_rectangle([240, 60, 500, 240], radius=10, 
                          fill="#EDE9FE", outline="#7C3AED", width=2)
    draw.text((300, 100), "Drive-Dreams", font=font_title, fill="#5B21B6")
    draw.text((300, 140), "物理一致性", font=font_small, fill="#6B7280")
    draw.text((295, 165), "多传感器仿真", font=font_small, fill="#6B7280")
    
    draw.rounded_rectangle([560, 60, 760, 240], radius=10, 
                          fill="#D1FAE5", outline="#10B981", width=2)
    draw.text((620, 100), "合成数据", font=font_text, fill="#065F46")
    draw.text((615, 130), "用于训练", font=font_text, fill="#065F46")
    draw.text((615, 160), "降低成本", font=font_text, fill="#065F46")
    
    draw.polygon([(195, 150), (230, 140), (230, 160)], fill='#64748B')
    draw.polygon([(515, 150), (550, 140), (550, 160)], fill='#64748B')
    
    draw.text((190, 15), "Cosmos-Drive-Dreams: 可扩展驾驶数据生成", 
             font=font_title, fill='#1E293B')
    
    return img

# 生成所有图片
if __name__ == "__main__":
    print("正在生成头像...")
    avatars = [
        ("li-hu", "Li Hu", "李"),
        ("ziwei-liu", "Ziwei Liu", "刘"),
        ("pku-team", "PKU Team", "北"),
        ("sjtu-team", "SJTU Team", "上"),
        ("nvidia", "NVIDIA", "NV"),
    ]
    
    for filename, name, initials in avatars:
        img = create_gradient_avatar(name, initials)
        img.save(os.path.join(output_dir, f"{filename}.png"))
        print(f"  ✓ {filename}.png")
    
    print("\n正在生成技术架构图...")
    diagrams = [
        ("diagram-ucm", create_tech_diagram_1),
        ("diagram-physx", create_tech_diagram_2),
        ("diagram-eva", create_tech_diagram_3),
        ("diagram-unidrive", create_tech_diagram_4),
        ("diagram-cosmos", create_tech_diagram_5),
    ]
    
    for filename, func in diagrams:
        img = func()
        img.save(os.path.join(output_dir, f"{filename}.png"))
        print(f"  ✓ {filename}.png")
    
    print(f"\n✅ 所有图片已生成到: {output_dir}")
