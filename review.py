import requests
import os

if not API_KEY:
    raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")
API_KEY = os.getenv("DASHSCOPE_API_KEY")

def review_code(diff_text):
    prompt = f"""
你是一名Java资深架构师，请对以下代码变更进行评审：

【评审重点】
1. Bug风险（空指针、并发问题）
2. 性能问题
3. 安全问题
4. 可维护性问题

【输出格式】
🔴 Critical:
🟡 Warning:
🔵 Info:

【代码变更如下】
{diff_text}
"""

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "input": {
            "prompt": prompt
        }
    }

    response = requests.post(
    url,
    headers=headers,
    json=data,
    proxies={"http": None, "https": None}
)

    result = response.json()

    try:
        return result["output"]["text"]
    except:
        return str(result)


def main():
    with open("diff.txt", "r") as f:
        diff = f.read()

    result = review_code(diff)

    print("=== AI评审结果 ===")
    print(result)
	print("hook test")
    with open("review_result.txt", "w", encoding="utf-8") as f:
    	f.write(result)

if __name__ == "__main__":
    main()