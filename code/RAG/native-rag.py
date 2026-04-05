"""
项目功能：实现基于 DeepSeek API 的 RAG (Retrieval-Augmented Generation) 系统

使用说明：
1. 在 .env 文件中设置 DEEPSEEK_API_KEY=您的API Key
2. 安装依赖：pip install openai python-dotenv nltk numpy
3. 运行代码：python native-rag.py

功能包括：
- 文档切分（Chunking）
- 向量化（Embedding）
- 向量库检索
- 拼上下文 → LLM 生成
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string

# 加载 .env 文件中的环境变量（从 code 目录加载）
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

# 从环境变量中获取 API Key
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')

# 初始化 OpenAI 客户端（使用 DeepSeek API）
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com")

# 加载 nltk 数据
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class RAGSystem:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        """初始化 RAG 系统"""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.document_chunks = []
    
    def chunk_document(self, text):
        """文档切分"""
        # 首先将文本按句子分割
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # 如果当前块加上新句子超过大小限制，就保存当前块
            if current_length + sentence_length > self.chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # 重叠部分：保留最后几个句子
                    current_chunk = current_chunk[-2:]
                    current_length = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # 处理最后一个块
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        self.document_chunks = chunks
        print(f"文档切分完成，共 {len(chunks)} 个 chunks")
        return chunks
    
    def preprocess_text(self, text):
        """文本预处理"""
        # 转小写
        text = text.lower()
        # 移除标点
        text = text.translate(str.maketrans('', '', string.punctuation))
        # 分词
        words = text.split()
        # 移除停用词
        stop_words = set(stopwords.words('chinese'))
        words = [word for word in words if word not in stop_words]
        return set(words)
    
    def calculate_similarity(self, text1, text2):
        """计算文本相似度"""
        set1 = self.preprocess_text(text1)
        set2 = self.preprocess_text(text2)
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union
    
    def retrieve_relevant_chunks(self, query, top_k=3):
        """检索相关的 chunks"""
        if not self.document_chunks:
            raise ValueError("请先切分文档")
        
        # 计算相似度
        similarities = []
        for i, chunk in enumerate(self.document_chunks):
            similarity = self.calculate_similarity(query, chunk)
            similarities.append((i, similarity))
        
        # 按相似度排序，取前 top_k 个
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:top_k]]
        
        # 返回相关的 chunks
        relevant_chunks = [(self.document_chunks[idx], similarities[idx][1]) for idx in top_indices]
        print(f"检索到 {len(relevant_chunks)} 个相关 chunks")
        return relevant_chunks
    
    def generate_answer(self, query, top_k=3):
        """生成回答"""
        # 检索相关 chunks
        relevant_chunks = self.retrieve_relevant_chunks(query, top_k)
        
        # 构建上下文
        context = "\n".join([f"[相关内容 {i+1}]: {chunk}" for i, (chunk, _) in enumerate(relevant_chunks)])
        
        # 构建 prompt
        prompt = f"""你是一个智能助手，根据以下提供的上下文信息回答用户的问题。

上下文信息：
{context}

用户问题：
{query}

请根据上下文信息，用中文简洁明了地回答用户的问题。如果上下文信息中没有相关内容，请明确说明。"""
        
        # 调用 LLM 生成回答
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的问答助手，基于提供的上下文信息回答问题。"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        
        answer = response.choices[0].message.content
        return answer

def main():
    """主函数"""
    # 示例文档（可以替换为你的实际文档）
    sample_document = """
    人工智能（Artificial Intelligence，简称AI）是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。
    
    人工智能的发展历史可以追溯到1956年的达特茅斯会议，当时约翰·麦卡锡等人正式提出了“人工智能”这一术语。
    
    人工智能的主要研究领域包括：机器学习、深度学习、自然语言处理、计算机视觉、机器人学、专家系统等。
    
    机器学习是人工智能的核心技术之一，它使计算机能够从数据中学习而无需显式编程。深度学习是机器学习的一个分支，它使用多层神经网络来模拟人脑的学习过程。
    
    自然语言处理（NLP）是人工智能的一个重要领域，它研究如何使计算机能够理解和生成人类语言。主要应用包括机器翻译、文本分类、情感分析、问答系统等。
    
    计算机视觉是人工智能的另一个重要领域，它研究如何使计算机能够理解和处理图像和视频。主要应用包括图像识别、目标检测、人脸识别、自动驾驶等。
    
    人工智能的发展面临着一些挑战，包括数据隐私、算法偏见、就业影响、安全风险等。同时，人工智能也带来了许多机遇，如提高生产效率、改善医疗保健、促进科学研究等。
    
    未来，人工智能将继续发展，可能会在更多领域得到应用，如教育、金融、交通、能源等。随着技术的进步，人工智能系统将变得更加智能、更加可靠，为人类社会带来更多福祉。
    """
    
    # 初始化 RAG 系统
    rag_system = RAGSystem(chunk_size=500, chunk_overlap=100)
    
    # 切分文档
    rag_system.chunk_document(sample_document)
    
    # 示例查询
    queries = [
        "人工智能的定义是什么？",
        "人工智能的主要研究领域有哪些？",
        "机器学习和深度学习的关系是什么？",
        "自然语言处理的应用有哪些？",
        "人工智能发展面临的挑战有哪些？"
    ]
    
    # 处理每个查询
    for query in queries:
        print(f"\n{'='*60}")
        print(f"用户查询：{query}")
        answer = rag_system.generate_answer(query)
        print(f"回答：{answer}")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
