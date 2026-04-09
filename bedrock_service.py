import boto3
import time
import random
from botocore.exceptions import ClientError

# ✅ CONFIG (your actual values)
KNOWLEDGE_BASE_ID = "ZHFVLKY5HQ"
REGION = "us-east-1"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# ✅ Create client
bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

# ✅ Build correct model ARN
MODEL_ARN = f"arn:aws:bedrock:{REGION}::foundation-model/{MODEL_ID}"


def query_knowledge_base(query, retries=5):
    """
    Queries Bedrock Knowledge Base using RetrieveAndGenerate
    Includes retry with exponential backoff for throttling
    """
    for attempt in range(retries):
        try:
            time.sleep(1.5)
            response = bedrock_agent_runtime.retrieve_and_generate(
                input={"text": query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                        "modelArn": MODEL_ARN
                    }
                }
            )

            answer = response["output"]["text"]
            citations = response.get("citations", [])

            return answer, citations

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ThrottlingException":
                wait_time = min(10, (2 ** attempt)) + random.uniform(0, 1)
                print(f"⚠️ Throttled. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)

            elif error_code == "AccessDeniedException":
                raise Exception("❌ Access denied. Check IAM permissions.")

            elif error_code == "ResourceNotFoundException":
                raise Exception("❌ Resource not found. Check KB ID or Model ARN.")

            else:
                raise e

    raise Exception("❌ Max retries exceeded due to throttling.")