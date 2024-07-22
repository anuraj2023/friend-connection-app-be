from fastapi import APIRouter, HTTPException, Query, Path
from db import prisma
from typing import List, Optional

from api.auth import get_password_hash
from db import prisma
from custom_types.index import User, UserCreation, UserProfile, UserResponse, FriendListDetails, StatusUpdateResponse

router = APIRouter()

@router.post("/user/signup", response_model=UserResponse)
async def create_user(user_input: UserCreation):
    user = await prisma.user.find_unique(where={"username": user_input.username})
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user_input.password)
    created_user = await prisma.user.create(
        data={"username": user_input.username, "hashed_password": hashed_password, 
              "email": user_input.email, "first_name": user_input.first_name, "last_name": user_input.last_name}
    )
    return created_user

@router.get("/users/strangers", response_model=List[User])
async def get_all_stranger_users(current_user_id: int):
    try:
        all_users = await prisma.user.find_many()
        
        friends = await prisma.friends.find_many(where={
            'OR': [
                {'userId1': current_user_id},
                {'userId2': current_user_id},
            ]
        })
        friend_ids = {friend.userId1 for friend in friends}.union({friend.userId2 for friend in friends})
        friend_ids.discard(current_user_id)
        
        pending_requests = await prisma.friend_request.find_many(where={
            'OR': [
                {'fromUserId': current_user_id},
                {'toUserId': current_user_id},
            ]
        })
        pending_ids = {request.fromUserId for request in pending_requests}.union({request.toUserId for request in pending_requests})
        pending_ids.discard(current_user_id)
        
        strangers = [user for user in all_users if user.id not in friend_ids and user.id not in pending_ids and user.id != current_user_id]
        
        return strangers
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(user_id: int = Path(..., title="User ID")):
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    status_updates = await prisma.statusupdate.find_many(
        where={"user_id": user_id}
    )
    
    status_updates_response = [
        StatusUpdateResponse(
            id=status.id,
            status=status.status,
            created_at=status.created_at.isoformat()
        ) for status in status_updates
    ]
    
    return UserProfile(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        status_updates=status_updates_response
    )

@router.get("/users/search/", response_model=List[UserResponse])
async def search_users(
    user_id: int = Query(..., title="ID of the user making the search"),
    query: Optional[str] = Query(..., title="Search Query", min_length=1)
):
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    friends = await prisma.friend.find_many(
        where={
            "OR": [
                {"user1_id": user_id},
                {"user2_id": user_id}
            ]
        }
    )

    friend_ids = set()
    for friend in friends:
        friend_ids.add(friend.user1_id if friend.user1_id != user_id else friend.user2_id)

    users = await prisma.user.find_many(
        where={
            "AND": [
                {
                    "OR": [
                        {"first_name": {"contains": query}},
                        {"last_name": {"contains": query}}
                    ]
                },
                {"id": {"not": user_id}},
                {"id": {"notIn": list(friend_ids)}}
            ]
        }
    )
    return users

@router.get("/friends/{user_id}/details", response_model=List[FriendListDetails])
async def get_friends_details(user_id: int):
    try:
        friends = await prisma.friend.find_many(
            where={"OR": [{"user1_id": user_id}, {"user2_id": user_id}]},
            include={"user1": True, "user2": True}
        )

        friend_details = []
        for friend in friends:
            friend_id = friend.user1_id if friend.user2_id == user_id else friend.user2_id
            friend_user = friend.user1 if friend.user2_id == user_id else friend.user2

            latest_status = await prisma.statusupdate.find_first(
                where={"user_id": friend_id},
                order={"created_at": "desc"}
            )

            friend_details.append({
                "id": friend_user.id,
                "first_name": friend_user.first_name,
                "last_name": friend_user.last_name,
                "username": friend_user.username,
                "email": friend_user.email,
                "latest_status": latest_status.status if latest_status else "NA",
                "status_created_at": latest_status.created_at.isoformat() if latest_status else "NA"
            })

        return friend_details

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

