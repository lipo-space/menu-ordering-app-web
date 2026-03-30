from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..models.dish import DishCreate, DishUpdate, Dish
from ..db.supabase_client import supabase

router = APIRouter()


@router.get("", response_model=dict)
async def list_dishes(
    search: Optional[str] = Query(None, description="Search dishes by name"),
    limit: int = Query(50, ge=1, le=100, description="Number of dishes to return"),
    offset: int = Query(0, ge=0, description="Number of dishes to skip"),
):
    """List all dishes with optional search"""
    query = supabase.table('dishes').select('*')

    if search:
        query = query.ilike('name', f'%{search}%')

    # Get total count
    count_query = supabase.table('dishes').select('id', count='exact')
    if search:
        count_query = count_query.ilike('name', f'%{search}%')
    count_response = count_query.execute()
    total = count_response.count if hasattr(count_response, 'count') else len(count_response.data)

    # Get paginated results
    response = query.order('created_at', desc=True).range(offset, offset + limit - 1).execute()

    return {
        "data": response.data,
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    }


@router.post("", response_model=Dish, status_code=201)
async def create_dish(dish: DishCreate):
    """Create a new dish"""
    # Check for duplicate name
    existing = supabase.table('dishes').select('id').eq('name', dish.name).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Dish with this name already exists")

    # Create dish
    response = supabase.table('dishes').insert({
        'name': dish.name,
        'description': dish.description
    }).execute()

    return response.data[0]


@router.get("/{dish_id}", response_model=Dish)
async def get_dish(dish_id: str):
    """Get dish by ID"""
    response = supabase.table('dishes').select('*').eq('id', dish_id).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Dish not found")

    return response.data


@router.put("/{dish_id}", response_model=Dish)
async def update_dish(dish_id: str, dish_update: DishUpdate):
    """Update dish"""
    # Check if dish exists
    existing = supabase.table('dishes').select('id').eq('id', dish_id).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Check for duplicate name if name is being updated
    if dish_update.name is not None:
        duplicate = supabase.table('dishes').select('id').eq('name', dish_update.name).neq('id', dish_id).execute()
        if duplicate.data:
            raise HTTPException(status_code=409, detail="Dish with this name already exists")

    # Update dish
    update_data = {}
    if dish_update.name is not None:
        update_data['name'] = dish_update.name
    if dish_update.description is not None:
        update_data['description'] = dish_update.description

    response = supabase.table('dishes').update(update_data).eq('id', dish_id).execute()

    return response.data[0]


@router.delete("/{dish_id}", status_code=204)
async def delete_dish(dish_id: str):
    """Delete a dish"""
    # Check if dish exists
    existing = supabase.table('dishes').select('id').eq('id', dish_id).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Delete dish (cascade will handle menu_dishes and combination_dishes)
    supabase.table('dishes').delete().eq('id', dish_id).execute()

    return None
