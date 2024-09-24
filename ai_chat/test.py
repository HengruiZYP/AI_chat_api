import requests
import json

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
        'stream': False,
        'conversation_id': conversation_id
        })
    headers = {
        'Authorization': "Bearer bce-v3/ALTAK-40xNAwxgBkFXqeU3b67TV/80bb537686f21a1756e0db2d9bdd5fa868e56566",
        'Content-Type': 'application/json'
    }
    while True:
            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = response.json()
            answer = response_data.get("answer")
            if answer:
                print(answer)
            else:
                print("No answer returned.")
            
            user_content = input("请输入: ")
            payload = json.dumps({
                'app_id': "e6a11028-4a4c-4c4f-a7c6-64bdee6191d3",
                'query': user_content,
                'stream': False,
                'conversation_id': conversation_id
            })

    
if __name__ == '__main__':
    main()
