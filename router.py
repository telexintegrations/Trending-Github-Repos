from fastapi import APIRouter, Request, status, HTTPException, BackgroundTasks
import httpx
import asyncio  
import os


router = APIRouter()
Telex_webhook_url = os.getenv("TELEX_WEBHOOK_URL")


@router.get("/integration.json", status_code=status.HTTP_200_OK)
def get_integrationjson(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-21",
                "updated_at": "2025-02-21",
            },
            "descriptions": {
                "app_name": "Trending GitHub Repos Tracker",
                "app_description": "Fetches trending GitHub repositories and shares them on Telex.",
                "app_logo": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                "app_url": f"{base_url}",
                "background_color": "#24292e"
            },
            "is_active": True,
            "integration_type": "interval",
            "key_features": [
                "Fetches trending GitHub repositories.",
                "Supports different programming languages.",
                "Posts updates to a Telex channel at set intervals."
            ],
            "integration_category": "Communication & Collaboration",
            "author": "Ayomide Ibitola",
            "settings": [
                {
                    "label": "Language",
                    "type": "text",
                    "required": True,
                    "default": "python"
                },
                {
                    "label": "Interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * *"
                }
            ],
            "target_url": "",
            "tick_url": f"{base_url}/tick",
        }
    }
    

@router.get("/test")
async def get_github_trending_repos(language: str = "python"):
    url = f"https://github-trending-api.de.a9sapp.eu/repositories?language={language}&since=daily"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                repos = response.json()[:5]
                
                
                print("GitHub API Response:", repos)

                return {
                    "trending_repositories": [
                        {
                            "💻name": repo.get("name", "Unknown Repo"),
                            "👨author": repo.get("author", "Unknown Author"),
                            "📦description": repo.get("description", "No description available"),
                            "⭐stars": repo.get("stars", 0),
                            "🍴forks": repo.get("forks", 0),
                            "🔗url": repo.get("url", "#")
                        }
                        for repo in repos
                    ]
                }
            raise HTTPException(status_code=response.status_code, detail="Error: Unable to fetch trending repos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

async def send_trending_repos(payload):
    language = payload.get("settings", {}).get("Language", "python")
    repos = await get_github_trending_repos(language)
    
    
    trending_repos = repos.get("trending_repositories", [])

    
    if not trending_repos:
        message = "🚨 No trending repositories found for the selected language."
    else:
        message = "🤖 Trending GitHub Repositories 🤖\n\n" + "\n\n".join(
          [
            f"💻 {repo['💻name']}\n"
            f"👨 Author: {repo['👨author']}\n"
            f"📦 {repo['📦description']}\n"
            f"⭐ {repo['⭐stars']} | 🍴 {repo['🍴forks']}\n"
            f"🔗 {repo['🔗url']} "  
            for repo in repos["trending_repositories"]
        ]
        )

    data = {
        "event_name": "github_trending_repos",
        "status": "success",
        "message": message,
        "username": "Github Trends Bot"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(Telex_webhook_url, json=data)
        print("Telex API Response:", response.status_code, response.text)


def send_trending_repos_wrapper(payload):
       asyncio.run(send_trending_repos(payload))

@router.post("/tick", status_code=status.HTTP_202_ACCEPTED)
def trigger_trending_repos(payload: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_trending_repos_wrapper, payload)
    return {"status": "Accepted"}
