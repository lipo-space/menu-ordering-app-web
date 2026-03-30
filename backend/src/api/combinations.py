from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from ..db.supabase_client import supabase
from ..models.combination import Combination, CombinationCreate, CombinationUpdate

router = APIRouter()


@router.get("", response_model=List[Combination])
async def list_combinations():
    """List all combinations with their dishes"""
    response = supabase.table('combinations').select(
        '*, combination_dishes(dishes(*))'
    ).order('created_at', desc=True).execute()

    combinations = []
    for item in response.data:
        dishes = [d['dishes'] for d in item['combination_dishes']]
        combinations.append({
            'id': item['id'],
            'name': item['name'],
            'dishes': dishes,
            'created_at': item['created_at']
        })

    return combinations


@router.post("/", response_model=Combination, status_code=201)
async def create_combination(data: CombinationCreate):
    """Create a new combination"""
    # Create combination
    comb_response = supabase.table('combinations').insert({
        'name': data.name
    }).execute()

    combination_id = comb_response.data[0]['id']

    # Insert dish relationships
    dish_data = [{'combination_id': combination_id, 'dish_id': str(dish_id)} for dish_id in data.dish_ids]
    supabase.table('combination_dishes').insert(dish_data).execute()

    # Update times_paired for each dish
    for dish_id in data.dish_ids:
        supabase.table('dishes').update({
            'times_paired': supabase.table('dishes').select('times_paired').eq('id', str(dish_id)).single().execute().data['times_paired'] + 1
        }).eq('id', str(dish_id)).execute()

    # Fetch the created combination with dishes
    return await get_combination(combination_id)


@router.get("/{combination_id}", response_model=Combination)
async def get_combination(combination_id: UUID):
    """Get a single combination by ID"""
    response = supabase.table('combinations').select(
        '*, combination_dishes(dishes(*))'
    ).eq('id', str(combination_id)).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Combination not found")

    dishes = [d['dishes'] for d in response.data['combination_dishes']]
    return {
        'id': response.data['id'],
        'name': response.data['name'],
        'dishes': dishes,
        'created_at': response.data['created_at']
    }


@router.put("/{combination_id}", response_model=Combination)
async def update_combination(combination_id: UUID, data: CombinationUpdate):
    """Update a combination"""
    # Check if combination exists
    existing = supabase.table('combinations').select('id').eq('id', str(combination_id)).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Combination not found")

    # Get old dish_ids
    old_dishes_response = supabase.table('combination_dishes').select('dish_id').eq(
        'combination_id', str(combination_id)
    ).execute()
    old_dish_ids = set(str(d['dish_id']) for d in old_dishes_response.data)

    # Delete old combination_dishes
    supabase.table('combination_dishes').delete().eq(
        'combination_id', str(combination_id)
    ).execute()

    # Update combination name if provided
    if data.name is not None:
        supabase.table('combinations').update({'name': data.name}).eq('id', str(combination_id)).execute()

    # Insert new combination_dishes
    if data.dish_ids is not None:
        dish_data = [{'combination_id': str(combination_id), 'dish_id': str(dish_id)} for dish_id in data.dish_ids]
        supabase.table('combination_dishes').insert(dish_data).execute()

        # Calculate dish changes
        new_dish_ids = set(str(dish_id) for dish_id in data.dish_ids) if data.dish_ids else set()
        added_dish_ids = new_dish_ids - old_dish_ids
        removed_dish_ids = old_dish_ids - new_dish_ids

        # Update times_paired for added dishes
        for dish_id in added_dish_ids:
            supabase.table('dishes').update({
                'times_paired': supabase.table('dishes').select('times_paired').eq('id', dish_id).single().execute().data['times_paired'] + 1
            }).eq('id', dish_id).execute()

        # Update times_paired for removed dishes
        for dish_id in removed_dish_ids:
            supabase.table('dishes').update({
                'times_paired': supabase.table('dishes').select('times_paired').eq('id', dish_id).single().execute().data['times_paired'] - 1
            }).eq('id', dish_id).execute()

    # Fetch updated combination
    return await get_combination(combination_id)


@router.delete("/{combination_id}", status_code=204)
async def delete_combination(combination_id: UUID):
    """Delete a combination"""
    # Get dish_ids before deletion
    dishes_response = supabase.table('combination_dishes').select('dish_id').eq(
        'combination_id', str(combination_id)
    ).execute()
    dish_ids = [str(d['dish_id']) for d in dishes_response.data]

    # Delete combination (cascade deletes combination_dishes)
    supabase.table('combinations').delete().eq('id', str(combination_id)).execute()

    # Decrement times_paired for each dish
    for dish_id in dish_ids:
        supabase.table('dishes').update({
            'times_paired': supabase.table('dishes').select('times_paired').eq('id', dish_id).single().execute().data['times_paired'] - 1
        }).eq('id', dish_id).execute()

    return None
