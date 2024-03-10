from __future__ import annotations

import os
import sys
from time import sleep

import leetcode
import leetcode.auth

# Initialize client
configuration = leetcode.Configuration()

# NOTE: cookies var is just a dict with `csrftoken` and `LEETCODE_SESSION`
# fields which contain corresponding cookies from web browser
#這邊填leetcode_session&csrf_token
leetcode_session = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTAxOTAxODQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZjY4ZDczYWI5YTM1MDMwY2Q3M2U2NWNiMDhhZDVmMmY3MjhiZWQ1ZDJkODg1ZjllOGJmM2FjYzM5OTA5OTQ2IiwiaWQiOjEwMTkwMTg0LCJlbWFpbCI6ImNob3Vlbnl1OTQwODA4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiY2hvdWVueXU5NDA4MDgiLCJ1c2VyX3NsdWciOiJjaG91ZW55dTk0MDgwOCIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9hdmF0YXJzL2F2YXRhcl8xNjkwMjAxNzY2LnBuZyIsInJlZnJlc2hlZF9hdCI6MTcwNzg0MTI0MywiaXAiOiIyNDA3OjRkMDA6M2MwMjo4NTk2OjY1Yzk6YzZjYjo4YjVhOmM4YzkiLCJpZGVudGl0eSI6IjlmZWE3MDFhNjI3YTU3ZDBjNDU4ZGIyZTFjYjYwZDYyIiwic2Vzc2lvbl9pZCI6NTU1NDc3NDksIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.7Y782kSiyNuyVaRqRkAdEJzjC8O_o4YCtAEy81iOXIo'
csrf_token = 'UlrQIL5Ka13ZOMRjgkNw5tWO4oAbEHAkv46hBNNK9ayfJppAFaZCvIprkfjCyjgC'

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

graphql_request = leetcode.GraphqlQuery(
    query="""
{
  user {
    username
    isCurrentUserPremium
  }
}
    """,
    variables=leetcode.GraphqlQueryVariables(),
)

# print(api_instance.graphql_post(body=graphql_request))

graphql_request = leetcode.GraphqlQuery(
    query="""
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            boundTopicId
            title
            content
            translatedTitle
            isPaidOnly
            difficulty
            likes
            dislikes
            isLiked
            similarQuestions
            contributors {
              username
              profileUrl
              avatarUrl
              __typename
            }
            langToValidPlayground
            topicTags {
              name
              slug
              translatedName
              __typename
            }
            companyTagStats
            codeSnippets {
              lang
              langSlug
              code
              __typename
            }
            stats
            codeDefinition
            hints
            solution {
              id
              canSeeDetail
              __typename
            }
            status
            sampleTestCase
            enableRunCode
            metaData
            translatedContent
            judgerAvailable
            judgeType
            mysqlSchemas
            enableTestMode
            envInfo
            __typename
          }
        }
    """,
    variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug="two-sum"),
    operation_name="getQuestionDetail",
)

# print(api_instance.graphql_post(body=graphql_request))

# Get stats
api_response = api_instance.api_problems_topic_get(topic="shell")

# print("Stats of this session")
# print(api_response)


# Try to test your solution

code = """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
"""
#程式語言
test_submission = leetcode.TestSubmission(
    data_input="[2,7,11,15]\n9",
    typed_code=code,
    question_id=1,
    test_mode=False,
    lang="python3",
)
#題目
interpretation_id = api_instance.problems_problem_interpret_solution_post(
    problem="two-sum", body=test_submission
)


print("Test has been queued. Result:")
print(interpretation_id)

sleep(5)  # FIXME: should probably be a busy-waiting loop

test_submission_result = api_instance.submissions_detail_id_check_get(
    id=interpretation_id.interpret_id
)

print("Got test result:")
print(test_submission_result)
del test_submission_result['std_output_list']
del test_submission_result['task_name']
del test_submission_result['expected_std_output_list']
del test_submission_result['expected_task_name']
del test_submission_result['compare_result']
leetcode.TestSubmissionResult(**test_submission_result)

# Real submission
submission = leetcode.Submission(
    judge_type="large", typed_code=code, question_id=1, test_mode=False, lang="python3"
)

submission_id = api_instance.problems_problem_submit_post(
    problem="two-sum", body=submission
)

print("Submission has been queued. Result:")
print(submission_id)

sleep(5)  # FIXME: should probably be a busy-waiting loop

submission_result = api_instance.submissions_detail_id_check_get(
    id=submission_id.submission_id
)

print("Got submission result:")
print(f"This is submission_result:{submission_result}")
del submission_result['task_name']
del submission_result['finished']
print(leetcode.SubmissionResult(**submission_result))