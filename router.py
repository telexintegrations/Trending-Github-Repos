from fastapi import APIRouter,Request,status,HTTPException,BackgroundTasks
import httpx
router = APIRouter()

@router.get("/integration.json",status_code= status.HTTP_200_OK)
def get_integrationjson( request : Request):
    base_url = str(request.base_url).rstrip("/")
    return{
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
                    "default": "/1* * * *"  
                }
            ],
            "target_url": "",
            "tick_url": f"{base_url}/tick",
        }
    }
@router.get("/test")
async def get_github_trending_repos( language = "python"):
    url = f"https://github-trending-api.de.a9sapp.eu/repositories?language={language}&since=daily"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code==200:
                repos = response.json()[:5]
                return {
                    "trending_repositories": [
                        {   
                            "💻name": repo["name"],
                            "👨author": repo["author"],
                            "📦description": repo["description"],
                            "⭐stars": repo["stars"],
                            "🍴forks": repo["forks"],
                            "🔗url": repo["url"]
                        }
                    for repo in repos
                  ]
                }
            return[ " Error: Unable to fetch trending repos"]
    except Exception as e:
        return[f"Error: {str(e)}"]
    

async def send_trending_repos(payload):
    language = payload.get("settings",{}).get("Language","python")
    repos = await get_github_trending_repos(language)
    message = " 🤖 Trending GitHub Repositories 🤖\n\n" + "\n\n".join(repos)

    data={
        "event_name":"github_trending_repos",
        "status":"success",
        "message":message,
        "username":"Github Trends Bot"
    }

    async with httpx.AsyncClient() as client:
        await client.post(payload["return_url"],json=data)

@router.post("/tick",status_code=status.HTTP_202_ACCEPTED)
def trigger_trending_repos(payload:dict , background_tasks: BackgroundTasks):
    background_tasks.add_task(send_trending_repos, payload)
    return{"status":"Accepted"}
