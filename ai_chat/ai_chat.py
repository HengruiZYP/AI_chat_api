import requests
import json
import re


def get_conversation_id():
    """
    获取对话ID。
    
    Args:
        无参数。
    
    Returns:
        str: 对话ID。

    """
    url = "https://qianfan.baidubce.com/v2/app/conversation"

    # 替换app_id和Authorization为自己的ID和秘钥
    payload = json.dumps({
        'app_id': "e6a11028-4a4c-4c4f-a7c6-64bdee6191d3"
    })
    headers = {
        'Authorization': "Bearer bce-v3/ALTAK-40xNAwxgBkFXqeU3b67TV/80bb537686f21a1756e0db2d9bdd5fa868e56566",
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("conversation_id")



def process_stream_response(response):
    """
    从stream response中解析并打印JSON格式数据中的"answer"字段
    
    Args:
        response: requests.models.Response对象，需要处理的stream response
    
    Returns:
        None
    
    """
    buffer = ""
    json_pattern = re.compile(r'data:\s*(\{.*?\})(?=\s*data:|\s*$)', re.DOTALL)
    
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        buffer += chunk
        
        matches = json_pattern.findall(buffer)
        
        for match in matches:
            try:
                response_data = json.loads(match)
                answer = response_data.get("answer")
                if answer:
                    print(answer, end='', flush=True)  # 动态输出不换行
                buffer = buffer.replace(f"data: {match}\n", "")
            except json.JSONDecodeError:
                continue
    print()  # 在所有输出完成后换行



def main():
    conversation_id = get_conversation_id()
    url = "https://qianfan.baidubce.com/v2/app/conversation/runs"
    # 替换app_id和Authorization为自己的ID和秘钥
    payload = json.dumps({
        'app_id': "e6a11028-4a4c-4c4f-a7c6-64bdee6191d3",
        'query': "你好",
        'stream': True,
        'conversation_id': conversation_id
    })
    headers = {
        'Authorization': "Bearer bce-v3/ALTAK-40xNAwxgBkFXqeU3b67TV/80bb537686f21a1756e0db2d9bdd5fa868e56566",
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    process_stream_response(response)

    while True:
        user_content = input("\n请输入: ")
        payload = json.dumps({
            'app_id': "e6a11028-4a4c-4c4f-a7c6-64bdee6191d3",
            'query': user_content,
            'stream': True,
            'conversation_id': conversation_id
        })
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        process_stream_response(response)


if __name__ == '__main__':
    main()