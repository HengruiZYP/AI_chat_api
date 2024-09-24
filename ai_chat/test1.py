import requests
import json
import re

def get_conversation_id():
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
    
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)

        # 打印原始响应内容以进行调试
        print("Raw response content:", response.text)

        if response.text:
            try:
                # 使用正则表达式提取 JSON 数据
                json_pattern = re.compile(r'data:\s*(\{.*?\})(?=\s*data:|\s*$)', re.DOTALL)
                matches = json_pattern.findall(response.text)
                
                for match in matches:
                    try:
                        response_data = json.loads(match)
                        answer = response_data.get("answer")
                        if answer:
                            print(answer)
                        else:
                            print("No answer returned.")
                    except json.JSONDecodeError:
                        print("Failed to parse JSON segment: ", match)
            except Exception as e:
                print("An error occurred: ", str(e))
        else:
            print("Empty response received.")
        
        user_content = input("请输入: ")
        payload = json.dumps({
            'app_id': "e6a11028-4a4c-4c4f-a7c6-64bdee6191d3",
            'query': user_content,
            'stream': True,
            'conversation_id': conversation_id
        })

if __name__ == '__main__':
    main()