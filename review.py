import requests
import os
import re

# ✅ 获取环境变量
API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not API_KEY:
    raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")


def review_code(diff_text):
    prompt = f"""
你是一名Java资深架构师，请对以下代码变更进行评审：

【评审重点】
1. Bug风险（空指针、并发问题）
2. 性能问题
3. 安全问题
4. 可维护性问题

【输出格式（必须严格遵守）】
评分：X/5（X为1-5整数）

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

    # ✅ 提取评分（必须在 main 内）
    score_match = re.search(r"评分.*?(\d)\s*/?\s*5", result)

    if score_match:
        score = int(score_match.group(1))
        print(f"AI评分：{score}")

        if score < 4:
            print("❌ AI评分低于4分，禁止提交！")
            exit(1)
        else:
            print("✅ AI评分通过，允许提交")
    else:
        print("❌ 未识别到评分，禁止提交（更安全）")
        exit(1)

    print("hook final test")

    with open("review_result.txt", "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    main()