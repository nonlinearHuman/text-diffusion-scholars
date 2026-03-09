#!/usr/bin/env python3
"""
从PDF中提取图片
"""
import fitz  # PyMuPDF
import os

pdf_dir = '/Users/gesong/.openclaw/workspace/paper_figures'
output_dir = pdf_dir

for pdf_name in ['r2dreamer.pdf', 'icprl.pdf', 'guiding.pdf']:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    if not os.path.exists(pdf_path):
        continue
    
    print(f"处理: {pdf_name}")
    doc = fitz.open(pdf_path)
    
    for page_num in range(min(5, len(doc))):  # 只处理前5页
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            output_name = f"{pdf_name.replace('.pdf', '')}_page{page_num+1}_img{img_index+1}.{image_ext}"
            output_path = os.path.join(output_dir, output_name)
            
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            print(f"  提取: {output_name} ({len(image_bytes)} bytes)")
    
    doc.close()

print("\n完成!")
print("\n当前所有图片:")
os.system(f"ls -lh {output_dir}/*.png {output_dir}/*.jpg 2>/dev/null | head -20")
