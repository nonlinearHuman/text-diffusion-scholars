# CVPR 2026/2025 多模态论文详细信息汇总

## 1. MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping (CVPR 2026)

### 基本信息
- **arXiv**: 2511.15690
- **机构**: 香港科技大学、北京航空航天大学、北京大学
- **代码**: https://github.com/ModelTC/MoDES

### 核心作者信息

#### **Yushi Huang (黄钰诗)** - 第一作者
- **照片**: 未找到 (搜索结果无个人主页照片链接)
- **教育背景**: 未找到详细信息
- **研究方向**: 多模态大语言模型、MoE加速
- **获奖经历**: 未找到
- **近两年代表论文**:
  1. MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping (CVPR 2026)
  2. TFMQ-DM: Temporal Feature Maintenance Quantization for Diffusion Models (其他会议)

#### **Xianglong Liu (刘祥龙)** - 通讯作者
- **照片**: 可能存在于个人主页 https://xlliu-beihang.github.io/
- **职位**: 北京航空航天大学教授
- **教育背景**: 
  - 北京航空航天大学学士和博士
  - 博士导师: Prof. Wei Li
  - 曾在哥伦比亚大学DVMM实验室联合培养,导师: Prof. Shih-Fu Chang
- **研究方向**: 快速视觉计算、鲁棒深度学习(网络量化、对抗攻击防御、少样本学习)
- **获奖经历**:
  - NSFC优秀青年基金
  - 2019北京新星计划
  - MSRA StarTrack计划
  - 2015 CCF青年人才发展计划
- **近两年代表论文**:
  1. MoDES (CVPR 2026)
  2. BiBench: Benchmarking and Analyzing Network Binarization (ICML 2023)
  3. DB-LLM: Accurate Dual-Binarization for Efficient LLMs (ACL 2024)
  4. Outlier Suppression: Pushing the Limit of Low-bit Transformer Language Models (NeurIPS 2022)
  5. BiFSMN: Binary Neural Network for Keyword Spotting (IJCAI 2022)

#### **Jun Zhang (张军)** - 通讯作者
- **照片**: 未找到
- **职位**: 香港科技大学教授
- **教育背景**: 未找到详细信息
- **研究方向**: 机器学习、优化算法
- **获奖经历**: 未找到
- **近两年代表论文**: 未找到详细列表

### 创新点总结
MoDES是首个针对MoE多模态大语言模型的免训练动态专家跳过框架。核心创新包括:(1)全局调制局部门控机制(GMLG),将层级全局重要性融入路由概率;(2)双模态阈值方法(DMT),分别处理文本和视觉token;(3)前沿搜索算法,将参数搜索时间从22天缩短至22小时。在跳过88%专家时仍能保持97.33%的准确率。

### 配图URL
- 论文主图: https://arxiv.org/html/2511.15690 (Figure 1, 2, 3, 4)
- GitHub项目页: https://github.com/ModelTC/MoDES

---

## 2. MultiModalPFN: Extending Prior-Data Fitted Networks for Multimodal Tabular Learning (CVPR 2026)

### 基本信息
- **arXiv**: 2602.20223
- **代码**: https://github.com/too-z/MultiModalPFN

### 核心作者信息

#### **Wall Kim** - 第一作者
- **照片**: 未找到
- **教育背景**: 未找到详细信息
- **研究方向**: 表格数据学习、多模态学习
- **获奖经历**: 未找到
- **近两年代表论文**:
  1. MultiModalPFN: Extending Prior-Data Fitted Networks for Multimodal Tabular Learning (CVPR 2026)

### 创新点总结
MultiModalPFN扩展了TabPFN基础模型以处理表格和非表格模态(如图像、文本)。核心创新包括:(1)多模态编码器和模态投影器;(2)多头门控MLP和交叉注意力池化器,缓解注意力不平衡问题;(3)在医疗和通用多模态数据集上超越SOTA方法。为异构数据学习提供了可扩展的有效框架。

### 配图URL
- 论文主页: https://arxiv.org/html/2602.20223
- GitHub: https://github.com/too-z/MultiModalPFN

---

## 3. Insight-V: Exploring Long-Chain Visual Reasoning with Multimodal Large Language Models (CVPR 2025 Highlight)

### 基本信息
- **arXiv**: 2411.14432
- **机构**: 南洋理工大学、腾讯
- **代码**: https://github.com/dongyh20/Insight-V

### 核心作者信息

#### **Yuhao Dong (董宇豪)** - 第一作者
- **照片**: 未找到独立主页
- **教育背景**: 未找到详细信息(可能为NTU学生)
- **研究方向**: 视觉推理、多模态大语言模型
- **获奖经历**: CVPR 2025 Highlight论文
- **近两年代表论文**:
  1. Insight-V: Exploring Long-Chain Visual Reasoning (CVPR 2025)
  2. 3DTopia-XL: Scaling High-quality 3D Asset Generation (CVPR 2025)

#### **Ziwei Liu (刘子玮)** - 通讯作者
- **照片**: 个人主页 https://liuziwei7.github.io/
- **职位**: 南洋理工大学副教授
- **教育背景**: 未找到详细信息(曾在Microsoft Research和Google Research实习)
- **研究方向**: 计算机视觉、机器学习、计算机图形学
- **获奖经历**:
  - Singapore President's Young Scientist Award (2025)
  - PAMI Mark Everingham Prize
  - MIT TR Innovators under 35 Asia Pacific
  - ICBS Frontiers of Science Award
  - Asian Young Scientist Fellowship
  - CVPR Best Paper Award Candidate
- **近两年代表论文**:
  1. Insight-V (CVPR 2025)
  2. 3DTopia-XL (CVPR 2025)
  3. Video-MMMU (被OpenAI GPT-5引用)
  4. CelebA (获CCF-CV Test of Time Award)
  5. VChain (ICCV 2025 Outstanding Paper Award)

#### **Yongming Rao (饶永铭)** - 作者
- **照片**: 个人主页 https://raoyongming.github.io/
- **职位**: 腾讯高级研究员
- **教育背景**: 
  - 清华大学电子工程系学士(2018)
  - 清华大学博士(2023),导师: Prof. Jiwen Lu
- **研究方向**: 大型多模态模型、AI基础模型、计算机视觉
- **获奖经历**:
  - 清华大学优秀博士论文
  - 2022中国国家奖学金
  - ICCV 2021 MVP点云补全挑战赛冠军
  - 百度AI华人新星百强榜
  - CVPR 2021/ECCV 2020 Outstanding Reviewer
- **近两年代表论文**:
  1. Insight-V (CVPR 2025)
  2. VPD: Unleashing Text-to-Image Diffusion Models for Visual Perception (ICCV 2023)
  3. HorNet: Efficient High-Order Spatial Interactions (NeurIPS 2022)
  4. DenseCLIP: Language-Guided Dense Prediction (CVPR 2022)
  5. Point-BERT: Pre-Training 3D Point Cloud Transformers (CVPR 2022)

### 创新点总结
Insight-V探索多模态大语言模型的长链视觉推理能力。核心创新包括:(1)提出长链推理框架,分解复杂视觉推理任务;(2)构建高质量推理链数据集;(3)训练策略优化长程推理。在多个视觉推理基准上取得显著提升,是CVPR 2025 Highlight论文。

### 配图URL
- 论文PDF: https://openaccess.thecvf.com/content/CVPR2025/papers/Dong_Insight-V_Exploring_Long-Chain_Visual_Reasoning_with_Multimodal_Large_Language_Models_CVPR_2025_paper.pdf
- GitHub: https://github.com/dongyh20/Insight-V

---

## 4. DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment (CVPR 2025)

### 基本信息
- **arXiv**: 2412.16334
- **机构**: Meta FAIR, 巴黎萨克雷大学, POSTECH等

### 核心作者信息

#### **Cijo Jose** - 第一作者
- **照片**: 未找到
- **职位**: Meta FAIR研究员
- **教育背景**: 未找到详细信息
- **研究方向**: 自监督视觉学习、视觉语言对齐
- **获奖经历**: 未找到
- **近两年代表论文**:
  1. DINOv2 Meets Text (CVPR 2025)
  2. DINOv3 (Meta AI Research)

#### **Théo Moutakanni** - 作者
- **照片**: 未找到
- **机构**: Meta FAIR, 巴黎萨克雷大学CentraleSupélec
- **教育背景**: 未找到详细信息
- **研究方向**: 计算机视觉、自监督学习

#### **Dahyun Kang** - 作者
- **照片**: 未找到
- **机构**: Meta FAIR, POSTECH
- **教育背景**: POSTECH
- **研究方向**: 视觉语言模型

### 创新点总结
dino.txt框架将DINOv2自监督视觉编码器与文本对齐,实现图像级和像素级视觉语言任务。核心创新:(1)利用LiT训练范式,以DINOv2作为视觉编码器;(2)通过图像块平均训练对齐;(3)使用文本和图像模态筛选数据;(4)仅用CLIP一小部分的计算成本达到SOTA零样本分类和开放词汇分割性能。

### 配图URL
- 论文PDF: https://openaccess.thecvf.com/content/CVPR2025/papers/Jose_DINOv2_Meets_Text_A_Unified_Framework_for_Image-_and_Pixel-Level_CVPR_2025_paper.pdf
- GitHub: https://github.com/facebookresearch/dinov2

---

## 5. Magma: A Foundation Model for Multimodal AI Agents (CVPR 2025)

### 基本信息
- **arXiv**: 2502.13130
- **机构**: Microsoft Research
- **代码**: https://github.com/microsoft/Magma
- **项目主页**: https://microsoft.github.io/Magma/

### 核心作者信息

#### **Jianwei Yang (杨建伟)** - 第一作者 & 项目负责人
- **照片**: 个人主页 https://jwyang.github.io/
- **职位**: 
  - 现任: xAI技术团队成员
  - 曾任: Meta SuperIntelligence Lab研究科学家、Microsoft Research首席研究员
- **教育背景**: 未找到详细信息
- **研究方向**: 多模态基础模型、通用多模态智能体
- **获奖经历**: 
  - CVPR 2022 Best Paper Final list (GLIP论文)
  - NeurIPS 2021 Spotlight (Focal Attention论文)
- **近两年代表论文**:
  1. Magma: A Foundation Model for Multimodal AI Agents (CVPR 2025)
  2. Phi-3-Vision (2024)
  3. Semantic-SAM: Segment and Recognize Anything at Any Granularity (ECCV 2024)
  4. SEEM: Segment Everything Everywhere all at once (NeurIPS 2023)
  5. X-Decoder: Generalized Decoding for Pixel, Image, and Language (CVPR 2023)
  6. GLIP: Grounded Language-Image Pre-training (CVPR 2022 Best Paper Final)

#### **Reuben Tan** - 联合作者
- **照片**: 未找到
- **机构**: Microsoft Research
- **研究方向**: 多模态AI代理

#### **Qianhui Wu** - 联合作者
- **照片**: 未找到
- **机构**: Microsoft Research
- **研究方向**: 多模态学习

### 创新点总结
Magma是首个能够理解和执行多模态输入的基础模型,同时具备数字环境UI导航和物理环境机器人操作能力。核心创新:(1)保留视觉语言理解能力;(2)添加动作执行能力;(3)在数字和物理世界中无缝切换。项目在Hacker News排名第一(2025年2月20日),代表了Microsoft Research在多模态AI代理方向的旗舰工作。

### 配图URL
- 项目主页: https://microsoft.github.io/Magma/
- GitHub: https://github.com/microsoft/Magma
- 论文PDF: https://openaccess.thecvf.com/content/CVPR2025/papers/Yang_Magma_A_Foundation_Model_for_Multimodal_AI_Agents_CVPR_2025_paper.pdf

---

## 总结

### 研究趋势分析
1. **MoE加速** - MoDES针对多模态MoE模型的高效推理
2. **表格多模态学习** - MultiModalPFN扩展基础模型应用场景
3. **视觉推理** - Insight-V探索长链推理能力
4. **视觉语言对齐** - DINOv2 Meets Text统一图像和像素级任务
5. **多模态AI代理** - Magma实现理解与行动统一

### 知名研究团队
- **北京航空航天大学** (Xianglong Liu团队) - 网络量化、模型压缩
- **南洋理工大学** (Ziwei Liu团队) - 视觉生成、多模态学习
- **腾讯** (Yongming Rao等) - 大型多模态模型
- **Meta FAIR** - 自监督视觉学习
- **Microsoft Research** (Jianwei Yang等) - 多模态基础模型

---

**注**: 部分作者照片、详细教育背景和完整论文列表未能在公开资料中找到。建议通过Google Scholar、个人主页或ResearchGate获取更完整信息。
