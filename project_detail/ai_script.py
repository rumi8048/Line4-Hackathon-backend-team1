import openai
import re
from project.settings import OPENAI_API_KEY



# OpenAI API 클라이언트 설정
client = openai.OpenAI(
    api_key=OPENAI_API_KEY
)

input_data = []
# 특수기호 및 접두사를 필터링하는 함수
def clean_text(text):
    # 불필요한 접두사 및 특수기호 제거
    text = re.sub(r"^(해결책:|요약:|제목:)\s*", "", text)  # 접두사 제거
    text = re.sub(r"[*\n]", "", text)  # 모든 별표 및 줄바꿈 문자 제거
    return text.strip()

# GPT 요청 함수
def generate_report(input_data):
    reports = []

    for item in input_data:
        for discussion in item.get('discussion', []):
            feedback_desc = item.get('feedback_description', '')
            discussion_desc = discussion.get('description', '')

            # 피드백과 토론 내용을 결합
            combined_text = f"Feedback: {feedback_desc}. Discussion: {discussion_desc}"

            try:
                # GPT API 요청을 통해 요약 및 해결책 생성
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a professional summarizer and problem solver. Summarize the feedback and discussion, then provide a solution. Use a polite tone in Korean. Do not include prefixes like '제목:' or '요약:'."},
                        {"role": "user", "content": f"Summarize the following and provide a solution:\n\n{combined_text}\n\nOutput a title, summary, and solution without any prefixes or unnecessary text."}
                    ]
                )

                # API 응답의 구조를 출력하여 디버깅
                print("API Response:", response)

                # 응답에서 title, summary, solution 추출
                result = response.choices[0].message.content.strip()

                if result:
                    # 결과를 파싱하여 title, summary, solution 분리
                    sections = result.split("\n\n")
                    title = clean_text(sections[0].strip())
                    
                    # summary가 비어 있으면 자동으로 생성
                    summary = clean_text(sections[1].strip()) if len(sections) > 1 else f"{discussion_desc}에 대해 '{feedback_desc}'라는 피드백이 제공되었습니다."
                    
                    # solution이 비어 있으면 자동으로 생성
                    solution = clean_text(sections[2].strip()) if len(sections) > 2 else ""

                    # 보고서에 필요한 필드만 추가
                    report = {
                        "title": title,
                        "summary": summary,
                        "solution": solution
                    }

                    reports.append(report)
            except Exception as e:
                print("Error processing response:", e)

    return reports

# 입력 JSON 데이터
# input_data = 
# [
#     {
#         "id": 1,
#         "feedback_writer": "밍키",
#         "upload_date": "2024-11-13",
#         "images": [],
#         "discussion": [{
#                 "id": 5,
#                 "discussion_writer": {
#                     "nickname": "밍키",
#                     "role": "슈퍼유저!!",
#                     "university": "대학교1"
#                 },
#                 "title": "테스트1-1",
#                 "description": "백엔드의 CSRF 토큰 오류가 납니다.",
#                 "images": []
#             }],
#         "can_update_and_delete": True,
#         "is_collaborator": True,
#         "is_adopted": False,
#         "feedback_description": "흠... 그 부분은 로그인할 때 JWT 토큰 방식을 사용하시는 것을 추천드립니다. 그러면 CSRF 오류가 나지 않습니다."
#     },
#     {
#         "id": 2,
#         "feedback_writer": "밍키",
#         "upload_date": "2024-11-13",
#         "images": [],
#         "discussion": [
#             {
#                 "id": 4,
#                 "discussion_writer": {
#                     "nickname": "밍키",
#                     "role": "슈퍼유저!!",
#                     "university": "대학교1"
#                 },
#                 "title": "테스트1-1",
#                 "description": "프론트,백 통신할 때 오류가 나요ㅜㅜ",
#                 "images": []
#             }
#         ],
#         "can_update_and_delete": True,
#         "is_collaborator": True,
#         "is_adopted": False,
#         "feedback_description": "음 저건 http 를 사용해서 생기는 오류네요. https 로 수정해주세요."
#     }
# ]

# 보고서 생성 실행 및 JSON 형식으로 출력
output_report = generate_report(input_data)
# print(json.dumps(output_report, ensure_ascii=False, indent=4))