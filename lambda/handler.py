import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import torch

tokenizer = AutoTokenizer.from_pretrained('./tokenizer/', cache_dir="./")

# MODEL_PATH = "./model/distilbert_classification.pth"  # Ensure this is the path where you've saved your model in the Docker container
# model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

tokenizer = AutoTokenizer.from_pretrained('./tokenizer/', cache_dir = './')
model = AutoModelForSequenceClassification.from_pretrained('./model/',  cache_dir = './')


model.eval()  # Set the model to evaluation mode

def handler(event, context):
    """
    AWS Lambda function handler for predicting sentiment.
    """
    try:
    # Extract text from the incoming event
        body = json.loads(event['body'])
        
        # Tokenize the text and convert to tensor
        inputs = tokenizer(body['text'], return_tensors='pt')

        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)[0].item()

        logits = list( logits.detach().numpy()[0] )
        logits = [str(x) for x in logits]

        # Return the response
        return {
                "statusCode": 200,
                "headers": {
                    'Content-Type': 'application/json',
                },
                "body": json.dumps({'predictions': predictions, 'logits': logits})
            }
    except Exception as e:
        
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
            },
            "body": json.dumps({"error": repr(e)})
        }