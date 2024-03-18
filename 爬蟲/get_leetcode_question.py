import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import os
def get_all_titles():
    # 透過 api 取得所有題目的標題
    url = "https://leetcode.com/api/problems/all/"
    slugs = []
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        r_json = response.json()
        for slug in r_json["stat_status_pairs"]:
            slugs.append(slug["stat"]["question__title_slug"])
    return slugs
def get_quest_info(title):
    query = """
    query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n
    """
    body = {"operationName":"questionData",
            "variables":{"titleSlug":title},
            "query":query}

    url = "https://leetcode.com/graphql"
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        r_json = response.json()
        return r_json["data"]["question"]

def parseContent(content):
    if content==None:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

def parseTags(tags):
    tagString=""
    if(len(tags)==0):
        return tagString

    for i in range(len(tags)-1):
        tagString=tagString+tags[i]['name']+","
    tagString = tagString + tags[len(tags)-1]['name']
    return tagString

if __name__ == "__main__":
    # 取得標題
    slugs = get_all_titles()
    columns = ['Id', 'title', 'titleSlug', 'content', 'isPaidOnly', 'difficulty', 'likes', 'dislikes', 'tag']
    df = pd.DataFrame(columns=columns)

    for i in range(len(slugs)):
        slug = slugs[i]
        # 取得題目資訊的 json 檔
        quest_json = get_quest_info(slug)
        id = quest_json['questionFrontendId']
        title = quest_json['title']
        titleSlug = quest_json['titleSlug']
        content=parseContent(quest_json['content'])
        isPaidOnly = quest_json['isPaidOnly']
        difficulty = quest_json['difficulty']
        likes = quest_json['likes']
        dislikes = quest_json['dislikes']
        tag = parseTags(quest_json['topicTags'])

        df.loc[len(df)] = [id, title, titleSlug, content, isPaidOnly, difficulty, likes, dislikes, tag]

        print("(%d/%d)"%(i,len(slugs)))
        print("id:",id)
        print("title:",title)
        print("titleSlug:",titleSlug)
        print("content:",content)
        print("isPaidOnly:",isPaidOnly)
        print("difficulty:",difficulty)
        print("likes:",likes)
        print("dislikes:",dislikes)
        print("tag:",tag)
        print("==========")
    print(df)
    # try:
    # 刪除檔案
        # os.remove('leetcode_problem.csv')
        # df.to_csv('leetcode_problem.csv', index=False, encoding='utf-8-sig')
    # except FileNotFoundError:
    # 檔案不存在
        # df.to_csv('leetcode_problem.csv', index=False, encoding='utf-8-sig')