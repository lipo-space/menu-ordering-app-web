from fastapi import APIRouter, HTTPException, Query
from datetime import date
from typing import Optional
from ..models.menu import MenuCreate, MenuUpdate
from ..db.supabase_client import supabase

router = APIRouter()


def reshape_menu_response(menu_data):
    """Reshape Supabase response to match existing API format"""
    if not menu_data:
        return None

    dishes = [item['dishes'] for item in menu_data.get('menu_dishes', [])]
    return {
        'id': menu_data['id'],
        'date': menu_data['date'],
        'dishes': dishes,
        'created_at': menu_data['created_at']
    }


@router.get("", response_model=dict)
async def list_menus(
    start_date: Optional[date] = Query(None, description="Filter menus from this date"),
    end_date: Optional[date] = Query(None, description="Filter menus until this date"),
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List menus with optional date filtering"""
    query = supabase.table('menus').select('*, menu_dishes(dishes(*))')

    if start_date:
        query = query.gte('date', start_date.isoformat())
    if end_date:
        query = query.lte('date', end_date.isoformat())

    # Get total count
    count_query = supabase.table('menus').select('id', count='exact')
    if start_date:
        count_query = count_query.gte('date', start_date.isoformat())
    if end_date:
        count_query = count_query.lte('date', end_date.isoformat())
    count_response = count_query.execute()
    total = count_response.count if hasattr(count_response, 'count') else len(count_response.data)

    # Get paginated results
    response = query.order('date', desc=True).range(offset, offset + limit - 1).execute()

    menus = [reshape_menu_response(menu) for menu in response.data]

    return {
        "data": menus,
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    }


@router.post("", response_model=dict, status_code=201)
async def create_menu(menu: MenuCreate):
    """Create a new menu"""
    # Check if menu for this date already exists
    existing = supabase.table('menus').select('id').eq('date', menu.date.isoformat()).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Menu already exists for this date")

    # Validate dish IDs
    for dish_id in menu.dish_ids:
        dish = supabase.table('dishes').select('id').eq('id', str(dish_id)).single().execute()
        if not dish.data:
            raise HTTPException(status_code=400, detail=f"Dish {dish_id} not found")

    # Create menu
    menu_response = supabase.table('menus').insert({
        'date': menu.date.isoformat()
    }).execute()

    menu_id = menu_response.data[0]['id']

    # Insert menu_dishes relationships
    dish_data = [{'menu_id': menu_id, 'dish_id': str(dish_id)} for dish_id in menu.dish_ids]
    supabase.table('menu_dishes').insert(dish_data).execute()

    # Increment times_enjoyed for each dish
    for dish_id in menu.dish_ids:
        current = supabase.table('dishes').select('times_enjoyed').eq('id', str(dish_id)).single().execute()
        supabase.table('dishes').update({
            'times_enjoyed': current.data['times_enjoyed'] + 1
        }).eq('id', str(dish_id)).execute()

    # Fetch created menu with dishes
    return await get_menu_by_date(menu.date)


@router.get("/today", response_model=dict)
async def get_today_menu():
    """Get today's menu"""
    today = date.today().isoformat()
    return await get_menu_by_date(date.fromisoformat(today))


@router.get("/{menu_date}", response_model=dict)
async def get_menu_by_date(menu_date: date):
    """Get menu by date"""
    response = supabase.table('menus').select(
        '*, menu_dishes(dishes(*))'
    ).eq('date', menu_date.isoformat()).maybe_single().execute()

    if not response or not hasattr(response, 'data') or not response.data:
        raise HTTPException(status_code=404, detail="Menu not found for this date")

    return reshape_menu_response(response.data)


@router.put("/{menu_date}", response_model=dict)
async def update_menu(menu_date: date, menu_update: MenuUpdate):
    """Update menu for a specific date"""
    # Check if menu exists
    existing = supabase.table('menus').select('id').eq('date', menu_date.isoformat()).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Menu not found for this date")

    menu_id = existing.data['id']

    # Get old dish_ids
    old_dishes_response = supabase.table('menu_dishes').select('dish_id').eq('menu_id', menu_id).execute()
    old_dish_ids = set(str(d['dish_id']) for d in old_dishes_response.data)

    # Validate new dish IDs
    for dish_id in menu_update.dish_ids:
        dish = supabase.table('dishes').select('id').eq('id', str(dish_id)).single().execute()
        if not dish.data:
            raise HTTPException(status_code=400, detail=f"Dish {dish_id} not found")

    # Delete old menu_dishes
    supabase.table('menu_dishes').delete().eq('menu_id', menu_id).execute()

    # Insert new menu_dishes
    dish_data = [{'menu_id': menu_id, 'dish_id': str(dish_id)} for dish_id in menu_update.dish_ids]
    supabase.table('menu_dishes').insert(dish_data).execute()

    # Calculate dish changes
    new_dish_ids = set(str(dish_id) for dish_id in menu_update.dish_ids)
    added_dish_ids = new_dish_ids - old_dish_ids
    removed_dish_ids = old_dish_ids - new_dish_ids

    # Increment times_enjoyed for added dishes
    for dish_id in added_dish_ids:
        current = supabase.table('dishes').select('times_enjoyed').eq('id', dish_id).single().execute()
        supabase.table('dishes').update({
            'times_enjoyed': current.data['times_enjoyed'] + 1
        }).eq('id', dish_id).execute()

    # Decrement times_enjoyed for removed dishes
    for dish_id in removed_dish_ids:
        current = supabase.table('dishes').select('times_enjoyed').eq('id', dish_id).single().execute()
        supabase.table('dishes').update({
            'times_enjoyed': max(0, current.data['times_enjoyed'] - 1)
        }).eq('id', dish_id).execute()

    # Fetch updated menu
    return await get_menu_by_date(menu_date)


@router.delete("/{menu_date}", status_code=204)
async def delete_menu(menu_date: date):
    """Delete menu for a specific date"""
    # Get menu and dish_ids before deletion
    existing = supabase.table('menus').select('id').eq('date', menu_date.isoformat()).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Menu not found for this date")

    menu_id = existing.data['id']
    dishes_response = supabase.table('menu_dishes').select('dish_id').eq('menu_id', menu_id).execute()
    dish_ids = [str(d['dish_id']) for d in dishes_response.data]

    # Delete menu (cascade handles menu_dishes)
    supabase.table('menus').delete().eq('id', menu_id).execute()

    # Decrement times_enjoyed for each dish
    for dish_id in dish_ids:
        current = supabase.table('dishes').select('times_enjoyed').eq('id', dish_id).single().execute()
        if current.data:
            supabase.table('dishes').update({
                'times_enjoyed': max(0, current.data['times_enjoyed'] - 1)
            }).eq('id', dish_id).execute()

    return None
