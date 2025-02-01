# import asyncio
# import aiohttp
# import logging
# import json
# from typing import List, Dict, Tuple, Optional
# from dataclasses import dataclass
# from datetime import datetime
# from pathlib import Path
# from sentence_transformers import SentenceTransformer, util
# from openai import AsyncOpenAI
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from pydantic_settings import BaseSettings, SettingsConfigDict
# import uvicorn
# from enum import Enum
# import sys
# if sys.platform.startswith('win'):
#     import asyncio
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# from fastapi.middleware.cors import CORSMiddleware


# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# class Settings(BaseSettings):
#     news_api_key: str
#     openai_api_key: str
#     model_weights: Dict[str, float] = {
#         "bert": 0.4,
#         "openai": 0.6
#     }
    
#     model_config = SettingsConfigDict(env_file=".env")

# class CredibilityLevel(str, Enum):
#     VERIFIED = "VERIFIED"
#     LIKELY_TRUE = "LIKELY_TRUE"
#     UNCERTAIN = "UNCERTAIN"
#     LIKELY_FALSE = "LIKELY_FALSE"
#     MISINFORMATION = "MISINFORMATION"

# class TweetRequest(BaseModel):
#     text: str
#     url: Optional[str] = None

# class CredibilityResponse(BaseModel):
#     text: str
#     credibility_level: CredibilityLevel
#     confidence: float
#     evidence: List[str]
#     sources: List[str]
#     bert_score: float
#     openai_score: float
#     analysis_timestamp: datetime

#     class Config:
#         from_attributes = True

# app = FastAPI(title="Tweet Misinformation Detector")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:3000"],  # React app's URL
# #     allow_credentials=True,
# #     allow_methods=["*"],  # Allows all methods
# #     allow_headers=["*"],  # Allows all headers
# #     expose_headers=["*"],
# # )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow requests from any origin (use ["http://localhost:3000"] for stricter security)
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow necessary methods
#     allow_headers=["*"],  # Allow all headers
# )

# settings = Settings()
# detector = None

# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#       # Startup
#     global detector
#     detector = MisinformationDetector(settings)
#     yield
#     # Shutdown
#     if detector:
#         await detector.cleanup()

# class MisinformationDetector:
#     def __init__(self, settings: Settings):
#         self.settings = settings
#         self.bert_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
#         self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
#         self.session = None

#     async def init_session(self):
#         """Initialize aiohttp session"""
#         if self.session is None:
#             self.session = aiohttp.ClientSession()

#     async def fetch_news_articles(self, text: str) -> List[Dict]:
#         """Fetch relevant news articles for fact checking"""
#         if self.session is None:
#             await self.init_session()

#         params = {
#             "q": text,
#             "apiKey": self.settings.news_api_key,
#             "language": "en",
#             "sortBy": "relevancy",
#             "pageSize": 10
#         }
        
#         try:
#             async with self.session.get("https://newsapi.org/v2/everything", params=params) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     return data.get("articles", [])
#                 else:
#                     logger.warning(f"News API request failed: {response.status}")
#                     return []
#         except Exception as e:
#             logger.error(f"Error fetching news: {e}")
#             return []

#     async def get_openai_analysis(self, text: str, articles: List[Dict]) -> Tuple[float, List[str]]:
#         """Get OpenAI's analysis of the tweet's credibility"""
#         context = "\n".join([
#             f"Title: {article['title']}\nDescription: {article.get('description', '')}"
#             for article in articles[:3]
#         ])
        
#         prompt = f"""Analyze the following tweet for misinformation. Compare it with the provided news context.
        
# Tweet: "{text}"

# Recent news context:
# {context}

# Provide your analysis in the following JSON format:
# {{
#     "credibility_score": float between 0 and 1,
#     "reasoning": [list of reasons for your score],
#     "is_consistent_with_news": boolean,
#     "potential_misinformation_flags": [list of concerning elements, if any]
# }}"""

#         try:
#             response = await self.openai_client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are a fact-checking assistant focused on detecting misinformation in tweets."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.1
#             )
            
#             analysis = json.loads(response.choices[0].message.content)
#             return (
#                 analysis["credibility_score"],
#                 analysis["reasoning"]
#             )
#         except Exception as e:
#             logger.error(f"OpenAI API error: {e}")
#             return 0.5, ["Error in OpenAI analysis"]

#     async def check_credibility(self, text: str) -> CredibilityResponse:
#         """Main method to check tweet credibility"""
#         await self.init_session()
        
#         # Fetch relevant news articles
#         articles = await self.fetch_news_articles(text)
        
#         # Get BERT similarity score
#         if articles:
#             article_texts = [f"{a['title']} {a.get('description', '')}" for a in articles]
#             tweet_embedding = self.bert_model.encode(text, convert_to_tensor=True)
#             article_embeddings = self.bert_model.encode(article_texts, convert_to_tensor=True)
#             bert_score = float(article_embeddings.max().item())
#         else:
#             bert_score = 0.5
        
#         # Get OpenAI analysis
#         openai_score, reasoning = await self.get_openai_analysis(text, articles)
        
#         # Calculate weighted final score
#         final_score = (
#             bert_score * self.settings.model_weights["bert"] +
#             openai_score * self.settings.model_weights["openai"]
#         )
        
#         # Determine credibility level
#         if final_score > 0.8:
#             level = CredibilityLevel.VERIFIED
#         elif final_score > 0.6:
#             level = CredibilityLevel.LIKELY_TRUE
#         elif final_score > 0.4:
#             level = CredibilityLevel.UNCERTAIN
#         elif final_score > 0.2:
#             level = CredibilityLevel.LIKELY_FALSE
#         else:
#             level = CredibilityLevel.MISINFORMATION
        
#         sources = [article["url"] for article in articles if "url" in article]
        
#         return CredibilityResponse(
#             text=text,
#             credibility_level=level,
#             confidence=final_score,
#             evidence=reasoning,
#             sources=sources,
#             bert_score=bert_score,
#             openai_score=openai_score,
#             analysis_timestamp=datetime.utcnow()
#         )

#     async def cleanup(self):
#         """Clean up resources"""
#         if self.session:
#             await self.session.close()
#             self.session = None

# # FastAPI application



# @app.post("/analyze", response_model=CredibilityResponse)
# async def analyze_tweet(tweet: TweetRequest):
# # """Analyze a tweet for misinformation"""
#     try:
#         global detector
#         if detector is None:
#             detector = MisinformationDetector(settings)
#         result = await detector.check_credibility(tweet.text)
#         return result
#     except Exception as e:
#         logger.error(f"Error analyzing tweet: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     # """Analyze a tweet for misinformation"""
#     # try:
#     #     result = await detector.check_credibility(tweet.text)
#     #     return result
#     # except Exception as e:
#     #     logger.error(f"Error analyzing tweet: {e}")
#     #     raise HTTPException(status_code=500, detail=str(e))

# # @app.on_event("shutdown")
# # async def shutdown_event():
# #     await detector.cleanup()



# app = FastAPI(title="Tweet Misinformation Detector", lifespan=lifespan)






# # CLI interface
# async def main():
#     """CLI interface for testing"""
#     detector = None
#     try:
#         detector = MisinformationDetector(Settings())
#         tweet_text = input("Enter the tweet text to analyze: ")
#         result = await detector.check_credibility(tweet_text)
#         print("\nAnalysis Results:")
#         print(f"Credibility Level: {result.credibility_level}")
#         print(f"Confidence Score: {result.confidence:.2f}")
#         print("\nEvidence:")
#         for item in result.evidence:
#             print(f"- {item}")
#         print("\nSources:")
#         for source in result.sources:
#             print(f"- {source}")
#         print(f"\nBERT Score: {result.bert_score:.2f}")
#         print(f"OpenAI Score: {result.openai_score:.2f}")
#     finally:
#         if detector:
#             await detector.cleanup()

# # if __name__ == "__main__":
# #     import sys
# #     if len(sys.argv) > 1 and sys.argv[1] == "serve":
# #         uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# #     else:
# #         asyncio.run(main())
# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1 and sys.argv[1] == "serve":
#         uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
#     else:
#         asyncio.run(main())

import asyncio
import aiohttp
import logging
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from openai import AsyncOpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import uvicorn
from enum import Enum
import sys
if sys.platform.startswith('win'):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tweet Misinformation Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    news_api_key: str
    openai_api_key: str
    model_weights: Dict[str, float] = {
        "bert": 0.25,
        "openai": 0.75
    }
    
    model_config = SettingsConfigDict(env_file=".env")

class CredibilityLevel(str, Enum):
    VERIFIED = "VERIFIED"
    LIKELY_TRUE = "LIKELY_TRUE"
    UNCERTAIN = "UNCERTAIN"
    LIKELY_FALSE = "LIKELY_FALSE"
    MISINFORMATION = "MISINFORMATION"

class TweetRequest(BaseModel):
    text: str
    url: Optional[str] = None

class CredibilityResponse(BaseModel):
    text: str
    credibility_level: CredibilityLevel
    confidence: float
    evidence: List[str]
    sources: List[str]
    bert_score: float
    openai_score: float
    analysis_timestamp: datetime

    class Config:
        from_attributes = True

class MisinformationDetector:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bert_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.session = None

    async def init_session(self):
        """Initialize aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def fetch_news_articles(self, text: str) -> List[Dict]:
        """Fetch relevant news articles for fact checking"""
        if self.session is None:
            await self.init_session()

        params = {
            "q": text,
            "apiKey": self.settings.news_api_key,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 10
        }
        
        try:
            async with self.session.get("https://newsapi.org/v2/everything", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("articles", [])
                else:
                    logger.warning(f"News API request failed: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    async def get_openai_analysis(self, text: str, articles: List[Dict]) -> Tuple[float, List[str]]:
        """Get OpenAI's analysis of the tweet's credibility"""
        context = "\n".join([
            f"Title: {article['title']}\nDescription: {article.get('description', '')}"
            for article in articles[:3]
        ])
        
        prompt = f"""Analyze the following tweet for misinformation. Compare it with the provided news context.
        
Tweet: "{text}"

Recent news context:
{context}

Provide your analysis in the following JSON format:
{{
    "credibility_score": float between 0 and 1,
    "reasoning": [list of reasons for your score],
    "is_consistent_with_news": boolean,
    "potential_misinformation_flags": [list of concerning elements, if any]
}}"""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a fact-checking assistant focused on detecting misinformation in tweets."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return (
                analysis["credibility_score"],
                analysis["reasoning"]
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return 0.5, ["Error in OpenAI analysis"]

    async def check_credibility(self, text: str) -> CredibilityResponse:
        """Main method to check tweet credibility"""
        await self.init_session()
        
        # Fetch relevant news articles
        articles = await self.fetch_news_articles(text)
        
        # Get BERT similarity score
        if articles:
            article_texts = [f"{a['title']} {a.get('description', '')}" for a in articles]
            tweet_embedding = self.bert_model.encode(text, convert_to_tensor=True)
            article_embeddings = self.bert_model.encode(article_texts, convert_to_tensor=True)
            bert_score = float(article_embeddings.max().item())
        else:
            bert_score = 0.5
        
        # Get OpenAI analysis
        openai_score, reasoning = await self.get_openai_analysis(text, articles)
        
        # Calculate weighted final score
        final_score = (
            bert_score * self.settings.model_weights["bert"] +
            openai_score * self.settings.model_weights["openai"]
        )
        
        # Determine credibility level
        if final_score > 0.8:
            level = CredibilityLevel.VERIFIED
        elif final_score > 0.6:
            level = CredibilityLevel.LIKELY_TRUE
        elif final_score > 0.4:
            level = CredibilityLevel.UNCERTAIN
        elif final_score > 0.2:
            level = CredibilityLevel.LIKELY_FALSE
        else:
            level = CredibilityLevel.MISINFORMATION
        
        sources = [article["url"] for article in articles if "url" in article]
        
        return CredibilityResponse(
            text=text,
            credibility_level=level,
            confidence=final_score,
            evidence=reasoning,
            sources=sources,
            bert_score=bert_score,
            openai_score=openai_score,
            analysis_timestamp=datetime.utcnow()
        )

    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            self.session = None

# FastAPI application

settings = Settings()
detector = MisinformationDetector(settings)

@app.post("/analyze", response_model=CredibilityResponse)
async def analyze_tweet(tweet: TweetRequest):
    """Analyze a tweet for misinformation"""
    try:
        result = await detector.check_credibility(tweet.text)
        return result
    except Exception as e:
        logger.error(f"Error analyzing tweet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    await detector.cleanup()

# CLI interface
async def main():
    """CLI interface for testing"""
    detector = None
    try:
        detector = MisinformationDetector(Settings())
        tweet_text = input("Enter the tweet text to analyze: ")
        result = await detector.check_credibility(tweet_text)
        print("\nAnalysis Results:")
        print(f"Credibility Level: {result.credibility_level}")
        print(f"Confidence Score: {result.confidence:.2f}")
        print("\nEvidence:")
        for item in result.evidence:
            print(f"- {item}")
        print("\nSources:")
        for source in result.sources:
            print(f"- {source}")
        print(f"\nBERT Score: {result.bert_score:.2f}")
        print(f"OpenAI Score: {result.openai_score:.2f}")
    finally:
        if detector:
            await detector.cleanup()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    else:
        asyncio.run(main())