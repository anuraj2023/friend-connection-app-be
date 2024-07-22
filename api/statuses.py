# from typing import List
# from fastapi import APIRouter, HTTPException
# from datetime import datetime
# from db import prisma
# from custom_types.index import FriendStatus, StatusUpdateCreateUpdateInput, StatusUpdateResponse, UserProfile

# router = APIRouter()

# @router.post("/user/statusupdate")
# async def create_or_update_status(status_update_data: StatusUpdateCreateUpdateInput):
#     try:
#         existing_status = await prisma.statusupdate.find_first(
#             where={"user_id": status_update_data.user_id}
#         )
        
#         if existing_status:
#             updated_status = await prisma.statusupdate.update(
#                 where={"id": existing_status.id},
#                 data={
#                     "status": status_update_data.status,
#                     "created_at": datetime.utcnow()
#                 }
#             )
#             return updated_status
#         else:
#             created_status_update = await prisma.statusupdate.create(
#                 data={
#                     "user_id": status_update_data.user_id,
#                     "status": status_update_data.status,
#                     "created_at": datetime.utcnow()
#                 }
#             )
#             return created_status_update
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/friends/{user_id}/statuses", response_model=List[FriendStatus])
# async def read_friends_statuses(user_id: int):
#     friends = await prisma.friend.find_many(where={"OR": [{"user1Id": user_id}, {"user2Id": user_id}]})
    
#     friend_ids = {friend.user1Id if friend.user2Id == user_id else friend.user2Id for friend in friends}
#     friend_ids.add(user_id)
    
#     statuses = await prisma.statusupdate.find_many(where={"userId": {"in": list(friend_ids)}})
    
#     return statuses

from typing import List
from fastapi import APIRouter, HTTPException
from datetime import datetime
from db import prisma
from custom_types.index import FriendStatus, StatusUpdateCreateUpdateInput, StatusUpdateResponse, UserProfile

router = APIRouter()

@router.post("/user/statusupdate")
async def create_or_update_status(status_update_data: StatusUpdateCreateUpdateInput):
    try:
        existing_status = await prisma.statusupdate.find_first(
            where={"user_id": status_update_data.user_id}
        )
        
        if existing_status:
            updated_status = await prisma.statusupdate.update(
                where={"id": existing_status.id},
                data={
                    "status": status_update_data.status,
                    "created_at": datetime.utcnow()
                }
            )
            return updated_status
        else:
            created_status_update = await prisma.statusupdate.create(
                data={
                    "user_id": status_update_data.user_id,
                    "status": status_update_data.status,
                    "created_at": datetime.utcnow()
                }
            )
            return created_status_update
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/friends/{user_id}/statuses", response_model=List[FriendStatus])
async def read_friends_statuses(user_id: int):
    friends = await prisma.friend.find_many(where={"OR": [{"user1Id": user_id}, {"user2Id": user_id}]})
    
    friend_ids = {friend.user1Id if friend.user2Id == user_id else friend.user2Id for friend in friends}
    friend_ids.add(user_id)
    
    statuses = await prisma.statusupdate.find_many(where={"userId": {"in": list(friend_ids)}})
    
    return statuses

@router.get("/user/{user_id}/status", response_model=StatusUpdateResponse)
async def read_user_status(user_id: int):
    try:
        status = await prisma.statusupdate.find_first(
            where={"user_id": user_id},
            order={"created_at": "desc"} 
        )
        if status:
            status_dict = status.dict()
            status_dict['created_at'] = status_dict['created_at'].isoformat()
            return status_dict
        else:
            raise HTTPException(status_code=404, detail="Status not found for the given user_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


